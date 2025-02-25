from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="bdscriptes",
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    version="0.3.7",
    description="Esta es la descripción de mi paquete",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The BDS World Team",
    author_email="bdscriptes@gmail.com",
    url="https://github.com/BDScriptES/BDScriptES",
    install_requires=["discord.py"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
