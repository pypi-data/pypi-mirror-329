import setuptools

def get_readme():
    with open("README.md", "rt", encoding="utf-8") as fh:
        return fh.read()

#def get_requirements():
#    with open("requirements.txt", "rt", encoding="utf-8") as fh:
#        return [line.strip() for line in fh.readlines()]

def get_version():
    with open("src/scparadise/__init__.py", "rt", encoding="utf-8") as fh:
        for line in fh.readlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1].strip()
    raise RuntimeError("Unable to find version string in __init__.py")

setuptools.setup(
    name="scparadise",
    version=get_version(),
    author="Vadim Chechekhin",
    author_email="vadimchex97@gmail.com",
    description="A tool for automatic cell type annotation, modality prediction and benchmarking",
    long_description=get_readme(),
    #install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.7',
)