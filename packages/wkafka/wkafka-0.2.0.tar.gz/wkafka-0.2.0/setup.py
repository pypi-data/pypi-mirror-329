try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    # pip install tomli
    import tomli as tomllib  # Python <3.11

from pathlib import Path
from setuptools import setup, find_packages

# Cargar configuración desde pyproject.toml
with open("pyproject.toml", "rb") as archivo:
    config_project = tomllib.load(archivo)

# Leer el README.md para la descripción larga
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Configuración del paquete
setup(
    name=config_project["project"]["name"],  # Nombre del paquete en PyPI
    version=config_project["project"]["version"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
    description=config_project["project"]["description"],
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=config_project["project"]["authors"][0]["name"],
    author_email=config_project["project"]["authors"][0]["email"],
    license="MIT",
    install_requires=[
        "opencv-python",
        "numpy",
        "kafka-python",
        "loguru",
        "rich",
    ],
    python_requires=config_project["project"]["requires-python"],
    url="https://github.com/wisrovi/wkafka/issues",
)
