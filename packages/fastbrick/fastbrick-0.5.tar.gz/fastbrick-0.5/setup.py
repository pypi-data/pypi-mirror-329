from setuptools import setup, find_packages


# Read README.md as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastbrick",
    version="0.5",
    author="Sandeep Singh Negi",  # 👈 
    author_email="sandeepnegi1710@gmail.com",  # 👈 
    description="A CLI tool for generating FastAPI projects and apps",
    long_description=long_description,  # Use the README content
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["fastapi", "click", "jinja2"],
    entry_points={
        "console_scripts": [
            "fastbrick = fastbrick:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
