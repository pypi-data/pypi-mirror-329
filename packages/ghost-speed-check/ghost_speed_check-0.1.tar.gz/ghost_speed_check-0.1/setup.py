from setuptools import setup, find_packages

setup(
    name="ghost_speed_check",  # Name of the package
    version="0.1",
    packages=find_packages(),  # Automatically find all the packages
    install_requires=["speedtest-cli", "rich", "requests"],  # Required dependencies
    author="Deepak Dumka",
    author_email="ddumka102@gmail.com",
    description="A package to check internet speed and display current date and time.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Deepakdumka1/internet_speed_checker.git",  # Link to your project (if public)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
