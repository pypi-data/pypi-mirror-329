from setuptools import setup, find_packages

setup(
    name="isaac_cli_utils",
    version="0.1.0",
    author="Isaac Harrison Gutekunst",
    author_email="",
    description="A collection of CLI utilities",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "open_ports=cli_utils.netstat:main",
        ],
    },
    install_requires=[
        "rich",
    ],
)
