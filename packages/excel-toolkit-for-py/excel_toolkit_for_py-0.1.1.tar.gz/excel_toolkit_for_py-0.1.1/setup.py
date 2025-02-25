from setuptools import setup, find_packages

setup(
    name="excel-toolkit-for-py",
    version="0.1.1",
    author="Roberto Lima",
    author_email="robertolima.izphera@gmail.com",
    description="📊 Facilite a leitura, manipulação e exportação de arquivos Excel e CSV com Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/robertolima-dev/excel-toolkit-for-py",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "openpyxl>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    license="MIT", 
)
