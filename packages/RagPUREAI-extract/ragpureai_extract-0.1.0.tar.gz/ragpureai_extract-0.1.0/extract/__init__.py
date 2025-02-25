import os
import ctypes

# Caminho absoluto para o diretório do pacote
pkg_dir = os.path.dirname(__file__)

# Carrega a biblioteca principal e a dependência
lib_path = os.path.join(pkg_dir, 'RagPUREAI_extract.cpython-312-x86_64-linux-gnu.so')
# dep_path = os.path.join(pkg_dir, 'dep.so')

lib = ctypes.CDLL(lib_path)
# dep = ctypes.CDLL(dep_path)