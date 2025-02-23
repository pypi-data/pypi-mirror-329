from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_vpp",
    version="0.0.1",
    author="Vinicius Silva",
    author_email="viniciussilvavpp@gmail.com",
    description="Um pacote para processamento de imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viniciussilvavpp/image-processing",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)