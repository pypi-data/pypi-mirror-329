from setuptools import setup, find_packages

setup(
    name='RagPUREAI_libs',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,  # Informa para incluir os dados especificados no MANIFEST.in
    package_data={
        'bind_libs': ['*.so'],  # Inclui todos os arquivos .so dentro do pacote
    },
    author='Seu Nome',
    author_email='seu.email@exemplo.com',
    description='Binding de C++ e Python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
)