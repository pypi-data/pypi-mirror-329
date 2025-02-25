from setuptools import setup, find_packages

setup(
    name="fpcli",
    version="0.1.32",
    description="This the simple command line interface using this package  you can easly integrate the command line interface for fastapi which is developed into the typer package ",
    author="Rohit kumar",
    packages=find_packages(include=["fpcli", "fpcli.*"]),
    install_requires=['typer'],  # Add dependencies here
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "fastapi-admin=fpcli:app",  # mycli will be the command name
        ],
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
