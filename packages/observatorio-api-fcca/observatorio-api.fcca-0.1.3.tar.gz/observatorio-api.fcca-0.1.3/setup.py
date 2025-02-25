from setuptools import setup, find_packages

setup(
    name="observatorio-api.fcca",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["requests"],
    author="Rodolfo Lopez",
    author_email="1803672F@umich.mx",
    description="API - Observatorio de gestión pública e inteligencia de mercados",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sites.google.com/umich.mx/observatoriofcca",  # Replace with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
