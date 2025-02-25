from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import shutil

class CustomInstallCommand(install):
    """Comando customizado para baixar e extrair o libtorch durante a instalação."""
    def run(self):
        # Executa a instalação padrão
        install.run(self)
        # Executa a rotina de download do libtorch
        self.download_libtorch()

    def download_libtorch(self):
        # Defina os nomes e URLs
        libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
        libtorch_cpu_url = (
            "https://download.pytorch.org/libtorch/cpu/"
            "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
        )
        # Caminho para o diretório do pacote (aqui consideramos que o pacote se chama "libs")
        pkg_dir = os.path.join(os.path.dirname(__file__), "libs")
        # Diretório onde os arquivos serão colocados: deve ser "libtorch/cpu" dentro de "libs"
        libtorch_dir = os.path.join(pkg_dir, "libtorch")
        cpu_dir = os.path.join(libtorch_dir, "cpu")

        # Remove o arquivo zip e o diretório de destino se já existirem
        if os.path.exists(libtorch_cpu_zip):
            os.remove(libtorch_cpu_zip)
        if os.path.exists(cpu_dir):
            shutil.rmtree(cpu_dir)

        # Cria o diretório de destino (garantindo que libtorch existe)
        os.makedirs(libtorch_dir, exist_ok=True)

        # Baixa o arquivo zip
        print("Baixando libtorch...")
        subprocess.check_call(["wget", libtorch_cpu_url, "-O", libtorch_cpu_zip])

        # Descompacta o arquivo dentro de libtorch_dir
        print("Extraindo libtorch...")
        subprocess.check_call(["unzip", "-o", libtorch_cpu_zip, "-d", libtorch_dir])

        # Após extrair, normalmente os arquivos estarão em libtorch_dir/libtorch
        extracted_dir = os.path.join(libtorch_dir, "libtorch")
        if os.path.exists(extracted_dir):
            # Renomeia o diretório extraído para "cpu"
            os.rename(extracted_dir, cpu_dir)
        else:
            print("Erro: diretório extraído não encontrado!")

        # Remove o arquivo zip baixado
        os.remove(libtorch_cpu_zip)
        print("Libtorch baixado e extraído com sucesso.")

setup(
    name="dependencias_libs",
    version="0.1.0",
    packages=find_packages(),  # Isso encontrará a pasta "libs" (desde que contenha __init__.py)
    include_package_data=True,
    cmdclass={"install": CustomInstallCommand},
    description="Pacote de dependências que baixa e prepara o libtorch",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
)
