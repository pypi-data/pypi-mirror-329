from setuptools import setup, find_packages

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prag-matic-image-converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Pillow>=9.0.0",
    ],
    python_requires=">=3.7",
    author="Pavan Tikkani",
    author_email="pavan@prag-matic.com",
    description="A tool for optimizing images and converting to WebP format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pktikkani/image_converter",
    project_urls={
        "Bug Tracker": "https://github.com/pktikkani/image_converter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
    ],
    keywords="image, converter, webp, conversion, image processing",
)