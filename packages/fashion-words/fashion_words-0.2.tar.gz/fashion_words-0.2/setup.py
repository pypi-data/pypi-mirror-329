from setuptools import setup, find_packages

setup(
    name="fashion_words",
    version="0.2",  #  AQUI está a nova versão (altere se necessário)
    packages=find_packages(),
    include_package_data=True,
    description="Um pacote de palavras relacionadas à moda para NLP",
    author="Melissa Albuquerque",
    install_requires=[],
    package_data={
        "fashion_words": ["fashion_words/categories.json"]
    },
    python_requires=">=3.6",
)
