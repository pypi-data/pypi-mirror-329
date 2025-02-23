from setuptools import setup, find_packages

setup(
    name="fastbrick",
    version="0.1",
    author="Sandeep Singh Negi",  # 👈 
    author_email="sandeepnegi1710@gmail.com",  # 👈 
    description="A CLI tool for generating FastAPI projects and apps",
    long_description="FastAPI-CLI created by Sandeep Singh Negi on 2025-02-19.",  # 👈 
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=["fastapi", "click", "jinja2"],
    entry_points={
        "console_scripts": [
            "fastbrick = fastapi_cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
