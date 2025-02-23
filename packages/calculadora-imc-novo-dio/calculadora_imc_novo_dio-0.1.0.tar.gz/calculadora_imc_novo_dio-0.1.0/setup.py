from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="calculadora_imc_novo_dio",  # Nome do pacote
    version="0.1.0",  # Versão
    author="Thiago Epiphanio",
    author_email="seuemail@example.com",
    description="Uma calculadora simples de IMC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThiagoEpiphanio/calculadora-imc",
    packages=find_packages(),  # Encontra os pacotes automaticamente
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
