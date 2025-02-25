import os
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import subprocess

WITH_ZOLTAN = os.environ.get("WITH_ZOLTAN", "0") == "1"


src_c_lang_path = os.path.join('src', 'c_lang', 'ZoltanGraphPart.c')

cmdclass={}
ext_modules = []
if WITH_ZOLTAN:
    class CustomBuildExt(build_ext):
        def run(self):
            ZOLTAN_LIBRARY = os.environ.get('ZOLTAN_LIBRARY')
            os.environ["CC"] = "mpicc"

            # Ensure paths are handled correctly regardless of where the build is invoked from
            # project_root = os.path.dirname(os.path.abspath(__file__))

            build_path = "build"
            input_files = [src_c_lang_path]
            os.makedirs(build_path, exist_ok=True)
            # output_binary = os.path.join(build_path, "zoltanGraphPart")
            output_binary = "zoltanGraphPart"

            compile_command = (
                f"mpicc {' '.join(input_files)} "
                f"-o {output_binary} "
                f"-L{ZOLTAN_LIBRARY} "
                "-lzoltan -lmpi -lm -lparmetis -lptscotch -lscotch -lmetis"
            )
            print("Compilation: ")
            print(compile_command)

            # Execute the compilation command
            result = subprocess.run(compile_command, shell=True)
            if result.returncode != 0:
                raise RuntimeError("Compilation failed!")

            super().run()

    cmdclass = {"build_ext": CustomBuildExt}
    ext_modules.append(Extension("graphcutting.zoltangraphpart", sources=[src_c_lang_path]))
else:
    print("No Zoltan compilation")

setup(
    name="graphcutting",
    version="0.0.7",
    description="Graph partitioning toolbox",
    author="Pierrick Pochelu",
    author_email="pierrick.pochelu@gmail.com",
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    extras_require={
        'all': ["networkx", "python-igraph", "igraph", "node2vec", "scikit-learn", "python-louvain", "PyMetis"]
    }
)


