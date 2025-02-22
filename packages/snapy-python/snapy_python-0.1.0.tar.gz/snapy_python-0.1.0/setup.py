from setuptools import setup, find_packages

setup(
    name="snapy_python",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Important for including non-Python files
    package_data={"snapy_python": ["assets/*.pdf"]},  # Ensures PDF is included
    install_requires=[],  # Add dependencies if needed
)
