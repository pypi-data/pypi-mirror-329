from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open ("requirements.txt") as f:
    requeriments = f.read().splitlines()

setup(
    name="pacote_moozer",
    version="0.0.1",
    author="Moozer",
    author_email="moozer_charles@hotmail.com",
    description="Meu primeiro pacote teste",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moozer-cloud/image-processing-package.git",
    packages=find_packages(),
    install_requires=requeriments,
    python_requeres=">=3.8",
)