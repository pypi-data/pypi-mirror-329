from setuptools import setup, find_packages

setup(
    name='RagPUREAI_extract',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,  # Informa para incluir os dados especificados no MANIFEST.in
    package_data={
        'bind_extract': ['*.so'],  # Inclui todos os arquivos .so dentro do pacote
    },
    author='Seu Nome',
    author_email='seu.email@exemplo.com',
    description='Binding de C++ e Python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        # Use o nome exato do pacote que você definiu no setup.py do RagPUREAI_lib
        # Se lá estiver "name='RagPUREAI-libs'", use 'RagPUREAI-libs==0.1.0'
        'RagPUREAI_libs==0.1.1',
    ],
)