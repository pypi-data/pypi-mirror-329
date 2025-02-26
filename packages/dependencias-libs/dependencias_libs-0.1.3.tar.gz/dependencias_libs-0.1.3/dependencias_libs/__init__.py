import os

def get_libtorch_cpu_path():
    """
    Retorna o caminho para o diretório onde o libtorch foi extraído.
    """
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "libtorch", "cpu")

# Exemplo: você pode também carregar uma biblioteca se for o caso:
# import ctypes
# lib_path = os.path.join(get_libtorch_cpu_path(), "nome_da_lib.so")
# lib = ctypes.CDLL(lib_path)
# Exemplo de uso em outro arquivo do seu pacote
# from .libtorch_downloader import get_libtorch_cpu_path

# def minha_funcao():
#     path = get_libtorch_cpu_path()
#     print("libtorch está em:", path)
#     # aqui você pode usar ctypes para carregar a biblioteca .so, etc.
