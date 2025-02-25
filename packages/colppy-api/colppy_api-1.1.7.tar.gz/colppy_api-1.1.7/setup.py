from setuptools import setup, find_packages

setup(
    name="colppy-api",
    version="1.1.7",
    description="Cliente API para Colppy (NO OFICIAL)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Groovinads (Juan Manuel Panozzo)",
    author_email="juanmanuel.panozzo@groovinads.com",
    url="https://bitbucket.org/groovinads/colppi-api",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.24.0",
        "click>=8.1.3",
        "colorama>=0.4.6",
        "pandas>=2.0.0",
        "python-dateutil>=2.8.2"
    ],
    entry_points={
        "console_scripts": [
            "colppy-api=colppy.cli.main:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
) 