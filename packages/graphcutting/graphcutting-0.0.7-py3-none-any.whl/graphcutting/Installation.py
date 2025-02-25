import importlib


def _get_cg():
    CG_nodes = ["n0", "n1", "n2", "n3", "n4"]
    CG_edges = [("n0", "n1"), ("n0", "n2"), ("n1", "n2"), ("n1", "n3"), ("n2", "n3"), ("n2", "n4"),
                ("n3", "n4")]
    CG_edges_weights = {
        ("n0", "n1"): 3.0, ("n0", "n2"): 2.5, ("n1", "n2"): 2.5,
        ("n1", "n3"): 1.2, ("n2", "n3"): 1.2, ("n2", "n4"): 2.8, ("n3", "n4"): 2.8
    }
    CG_nodes_weights = {"n0": 3, "n1": 4, "n2": 5, "n3": 6, "n4": 7}

    cg = (CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights)
    return cg

def _is_class_name_is_part(module_name):
    return "Part" in module_name

def _iterate_parts_from_init():
    strategies=[]
    module = importlib.import_module("graphcutting")
    for part_name in module.__all__:
        if _is_class_name_is_part(part_name):
            part_module = importlib.import_module(f"graphcutting.{part_name}")
            class_ptr = getattr(part_module, part_name)
            strategies.append(class_ptr)
    return strategies

def install_check():
    """check installation.
    because the dependencies or lazy, we need mock graph and try to partition it.
    """
    cg = _get_cg()
    part = 2
    strategies_class_ptr = _iterate_parts_from_init()
    check_result={}
    for strategy_class_ptr in strategies_class_ptr:

        try:
            strategy=strategy_class_ptr() # default hyper parameter
            r=strategy.part(*cg, part)
            res=1

        except Exception as e:
            print(f"Warning {strategy_class_ptr.__name__} : {e}")
            res=0
        check_result[strategy_class_ptr.__name__]=res

    return check_result