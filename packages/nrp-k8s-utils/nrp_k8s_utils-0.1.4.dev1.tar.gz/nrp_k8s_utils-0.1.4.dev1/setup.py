from setuptools import setup, find_packages

setup(
    name="nrp_k8s_utils",
    version="0.1.4-dev1",
    author="Trevin Lee",
    author_email="trl008@ucsd.edu",
    description="A Python package designed for NRP cluster users.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.nrp-nautilus.io/Trevin/nrp_k8s_utils",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "PyYAML",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
