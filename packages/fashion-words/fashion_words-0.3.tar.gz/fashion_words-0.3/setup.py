from setuptools import setup, find_packages

setup(
    name="fashion_words",
    version="0.3",  # 🚀 NOVA VERSÃO para garantir que o PyPI aceite
    packages=find_packages(),
    include_package_data=True,  # 🔹 Garante que os arquivos extras sejam incluídos
    description="Um pacote de palavras relacionadas à moda para NLP",
    author="Melissa Albuquerque",
    install_requires=[],
    package_data={
        "fashion_words": ["categories.json"],  # 🔥 FORÇANDO a inclusão do JSON
    },
    python_requires=">=3.6",
)
