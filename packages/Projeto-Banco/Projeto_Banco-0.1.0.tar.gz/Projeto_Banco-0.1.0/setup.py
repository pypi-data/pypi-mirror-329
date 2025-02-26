from setuptools import setup, find_packages

setup(
    name="Projeto_Banco",
    version="0.1.0",
    author="Ronald",
    author_email="ronaldkurouzo@gmail.com",
    description="pacote python de um projeto POO de Bancos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hidan404/Dio---desafio-1.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Adicione dependências aqui
        
    ],
)
