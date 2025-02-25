from setuptools import setup, find_packages

# Read dependencies from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="qubicon",
    version="3.5.2",
    author="Stephan Karas",
    author_email="stephan.karas@qubicon-ag.com",
    description="Python SDK for interacting with the Qubicon platform through the library or CLI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.qub-lab.io/qub-client/qubicon-python-library",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),  # Auto-updated dependencies
    entry_points={
        "console_scripts": [
            "qubicon-client=qubicon.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
