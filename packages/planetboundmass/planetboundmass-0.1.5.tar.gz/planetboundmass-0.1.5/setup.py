import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="planetboundmass",
    version="0.0.0",
    author="Jingyao Dou",
    author_email="qb20321@bristol.ac.uk",
    description="Search bound particles from SWIFT simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JingyaoDOU/planetboundmass",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires="<=3.8.18",
    package_data={"planetboundmass": ["data/*.txt"]},
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "h5py",
        "woma",
        "unyt",
        "swiftsimio<=6.1.1",
        "scipy",
        "seaborn",
    ],
)
