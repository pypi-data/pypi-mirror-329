from setuptools import setup, find_packages

setup(
    name="scpfetch",  
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="kanata",
    description="API wrapper for getting SCP data",
    url="https://github.com/Kanata-05/SCP-API",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
