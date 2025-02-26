# dependencias_libs/libtorch_downloader.py
import os
import subprocess
import shutil

# URL e nome do arquivo que você quer baixar
LIBTORCH_CPU_ZIP_NAME = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
LIBTORCH_CPU_URL = (
    "https://download.pytorch.org/libtorch/cpu/"
    "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
)

def ensure_libtorch_available():
    """
    Verifica se o libtorch está presente no caminho esperado.
    Se não estiver, faz o download e extrai.
    """
    # Caminho raiz onde você quer guardar o libtorch
    base_dir = os.path.dirname(__file__)
    libtorch_dir = os.path.join(base_dir, "libtorch")
    cpu_dir = os.path.join(libtorch_dir, "cpu")

    # Se o diretório "cpu" já existe, supomos que o libtorch já foi baixado e extraído.
    if os.path.exists(cpu_dir):
        print("Libtorch já está disponível em:", cpu_dir)
        return

    # Se não existe, criar a pasta "libtorch"
    os.makedirs(libtorch_dir, exist_ok=True)

    # Baixa o arquivo zip localmente (usando o `wget` ou `requests`, etc.)
    # Aqui como exemplo, uso subprocess/wget, mas poderia usar requests
    print("Baixando libtorch de", LIBTORCH_CPU_URL)
    subprocess.check_call(["wget", LIBTORCH_CPU_URL, "-O", LIBTORCH_CPU_ZIP_NAME])

    # Extrai dentro de libtorch_dir
    print("Extraindo libtorch para", libtorch_dir)
    subprocess.check_call(["unzip", "-o", LIBTORCH_CPU_ZIP_NAME, "-d", libtorch_dir])

    # Renomeia o libtorch extraído de libtorch_dir/libtorch -> libtorch_dir/cpu
    extracted_dir = os.path.join(libtorch_dir, "libtorch")
    if os.path.exists(extracted_dir):
        os.rename(extracted_dir, cpu_dir)
    else:
        print("ERRO: não foi encontrado o diretório libtorch extraído.")

    # Remove o arquivo zip
    os.remove(LIBTORCH_CPU_ZIP_NAME)

    print("Libtorch instalado em:", cpu_dir)

def get_libtorch_cpu_path():
    """
    Retorna o caminho para o diretório onde o libtorch foi extraído.
    (Chama ensure_libtorch_available() para garantir que ele existe.)
    """
    ensure_libtorch_available()
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "libtorch", "cpu")
