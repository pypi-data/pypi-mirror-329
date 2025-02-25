from setuptools import setup, find_packages

setup(
    name="coef_analysis",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    author="Leonardo Areias",
    author_email="leorareias@gmail.com",
    description="Biblioteca para análise de coeficientes de correlação",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/leo-areias/coef_analysis.git",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
