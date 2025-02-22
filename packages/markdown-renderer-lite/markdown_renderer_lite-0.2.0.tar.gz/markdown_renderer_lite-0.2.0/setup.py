from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="markdown-renderer-lite",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["markdown"],
    entry_points={
        "console_scripts": [
            "markdown_renderer_lite=markdown_renderer_lite.converter:convert_markdown"
        ],
    },
    include_package_data=True,
    package_data={"markdown_renderer_lite": ["static/*.css"]},
    author="Orhan Cavus",
    author_email="orhancv@gmail.com",
    description="A lightweight Markdown to HTML converter with syntax highlighting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orhancavus/markdown_renderer_lite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
