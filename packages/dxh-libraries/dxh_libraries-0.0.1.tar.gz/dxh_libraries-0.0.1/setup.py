import os
from setuptools import setup, find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def read_file(filepath, default=""):
    full_path = os.path.join(BASE_DIR, filepath)
    if os.path.exists(full_path):
        with open(full_path, encoding="utf-8") as f:
            return f.read().strip()
    return default


long_description = read_file(
    "README.md", "A common utility package for Django projects.")

version = {}
with open(os.path.join(BASE_DIR, "dxh_libraries/__version__.py")) as f:
    exec(f.read(), version)

install_requires = [
    line.strip() for line in read_file("requirements.txt").splitlines() if line.strip() and not line.startswith("#")
]

setup(
    name="dxh_libraries",
    version=version["__version__"],
    description="A common package for Django projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Devxhub Limited",
    author_email="info@devxhub.com",
    url="https://github.com/devxhub/dxh_libraries",
    license="MIT",
    # packages=find_packages(exclude=["tests", "docs"]),
    packages=find_packages(include=["dxh_libraries", "dxh_libraries.*"]),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django common library",
    python_requires=">=3.8",
)
