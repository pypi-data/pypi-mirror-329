from setuptools import setup, find_packages

setup(
    name="pygen-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click", "PyInquirer"],
    entry_points={
        'console_scripts': [
            'pygen=pygen_cli.cli:create_project',
        ],
    },
)
