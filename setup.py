import setuptools

package_requirements_file = "requirements.txt"
docs_requirements_file = "docs/requirements.txt"
documentation_requirements = open(docs_requirements_file).read().split("\n")

setuptools.setup(
    version="0.0.0",
    name="energy_flexibility_kpis",  # Name of the package
    author="Hicham Johra",
    author_email="hj@build.aau.dk",
    description="Python package for the computation of energy flexibility KPIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HichamJohra/energy_flexibility_kpis",
    project_urls={
        "Bug Tracker": "https://github.com/HichamJohra/energy_flexibility_kpis/issues",
        "Documentation": "https://github.com/HichamJohra/energy_flexibility_kpis",
        "Source Code": "https://github.com/HichamJohra/energy_flexibility_kpis",
    },
    packages=setuptools.find_packages(),
    data_files=[("requirements", [package_requirements_file, docs_requirements_file])],
    python_requires=">=3.9",
    install_requires=open(package_requirements_file).read().split("\n"),  # Automatically install the requirements
    extras_require={
        "dev": [
            "setuptools>=42",
            "wheel",
            "pytest",
            "pytest-cov",
            "pytest-xdist",
        ]
        + documentation_requirements,
    },
)
