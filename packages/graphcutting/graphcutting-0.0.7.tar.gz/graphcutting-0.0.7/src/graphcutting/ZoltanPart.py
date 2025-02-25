import subprocess as sp
import ctypes
import os
from collections import defaultdict
from graphcutting.util import make_symmetry


tmp_graph_file = "/tmp/graph_data.txt"
zoltan_bin_name = 'zoltanGraphPart'

def get_zoltan_binary():
    # Assumes the binary is located in the build folder relative to the module
    current_dir = os.path.dirname(__file__)


    binary_path = os.path.join(current_dir, '../../', zoltan_bin_name)
    if os.path.exists(binary_path):
        pass
    else:
        binary_path = os.path.join(current_dir, '../', zoltan_bin_name)

    #binary_path=os.path.join(current_dir,"zoltangraphpart.cpython-310-x86_64-linux-gnu.so")

    if not os.path.isfile(binary_path):
        raise FileNotFoundError("Compiled Zoltan binary not found. \n"
                                f"Expected location: {binary_path} \n"
                                "Did you run setup.py?")
    return os.path.abspath(binary_path)


def _run_subprocess(program: str, args: str) -> str:
    cmd_str = program+" "+args
    cmd = cmd_str.split(" ")

    #print("Launch: ", cmd)
    result = sp.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout
    lines = output.split("\n")
    return lines


def _call_c_function(so_file: str, args: str) -> str:
    # Load the C library
    lib = ctypes.CDLL(so_file)

    # Define argument types
    lib.compute.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    input_bytes = args.encode('utf-8')  # Convert to bytes (C uses char*)
    output = ctypes.create_string_buffer(len(input_bytes) + 1)  # Allocating mutable buffer

    # Call the C function
    lib.compute(input_bytes, output)
    out = output.value.decode('utf-8')  # Convert back to Python string
    return out

def _check_zoltan_algo(algo:str):
    if algo not in {"PHG", "PARMETIS", "SCOTCH"}:
        raise ValueError(f"Zoltan algo should be 'PHG' (default), 'PARMETIS', 'SCOTCH'. Got '{algo}'.")

def _partition_zoltan(CG_nodes: list[str],
                     CG_edges: list[tuple[str, str]],
                     CG_edges_weights: dict[str, float],
                     CG_nodes_weights: dict[str, float],
                     parts: int,
                     algo:str="PHG",

                     ) -> list[int]:
    zoltan_program = get_zoltan_binary()

    _check_zoltan_algo(algo)

    ROUND = 6  # limit the numeric representation for saving disk

    num_nodes = len(CG_nodes)

    # node weights
    node_weights = [CG_nodes_weights[n] for n in CG_nodes]

    # Compute num_edges
    num_edges = []
    neigh = defaultdict(lambda: [])
    for edge in CG_edges:
        neigh[edge[0]].append(edge[1])
    for n in CG_nodes:
        num_neigh = len(neigh[n])
        num_edges.append(num_neigh)

    # edges_indices and edges_weights
    from_node_to_nodeID = {}
    for i, n in enumerate(CG_nodes):
        from_node_to_nodeID[n] = i

    edges_weights = []
    edges_indices = []
    for nodeID in range(num_nodes):
        node_name = CG_nodes[nodeID]
        neighs = neigh[node_name]
        for neigh_name in neighs:
            edge_index = from_node_to_nodeID[neigh_name]
            edges_indices.append(edge_index)

            edge = (node_name, neigh_name)
            w = CG_edges_weights[edge]
            edges_weights.append(w)

    # Create the param string
    params = []
    for l in [[num_nodes], num_edges, edges_indices, node_weights, edges_weights]:
        l_str = [str(round(e, ROUND)) for e in l]
        params.extend(l_str)
    params_str = " ".join(params)

    # Write
    with open(tmp_graph_file, "w") as f:
        f.write(params_str)

    cmd = []
    cmd.append(str(parts))
    cmd.append(algo)
    cmd.append(tmp_graph_file)
    cmd_str = " ".join(cmd)

    lines = _run_subprocess(zoltan_program, cmd_str)
    #lines = call_c_function(zoltan_program, cmd_str)

    #os.remove(tmp_graph_file)

    node_colors = []
    try:
        for line in lines:
            if line and line[0]=="*":
                partition_id_str=line[1:]
                partition_id = int(partition_id_str.strip())
                node_colors.append(partition_id)
    except Exception as e:
        print(f"Error parsing partitioning output: {e}")
        return []

    return node_colors

class ZoltanPart:
    def __init__(self, algo:str="PHG", tmp_graph_file:str="/tmp/graph_data.txt"):
        self.algo=algo
        self.tmp_graph_file=tmp_graph_file

    def part(self, CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts):

        CG_edges2, CG_edges_weights2= make_symmetry(CG_edges, CG_edges_weights)

        partitioning=_partition_zoltan(CG_nodes, CG_edges2, CG_edges_weights2, CG_nodes_weights,
                                       parts,
                                       algo=self.algo)
        return partitioning

    def get_name(self):
        return "zoltan_"+self.algo