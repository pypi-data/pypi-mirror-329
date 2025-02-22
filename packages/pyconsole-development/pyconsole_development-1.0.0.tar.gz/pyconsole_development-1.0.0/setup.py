from setuptools import setup, find_packages

setup(
    name="pyconsole-development",
    version="1.0.0",
    author="Sikandar",
    author_email="sikandar.dev@gmail.com",
    description="A simple console utility for printing messages with color using colorama",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sikandardeveloper/pyconsole",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["colorama"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
