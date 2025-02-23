import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="promptgraphtools",
    version="0.1.1",
    author="Tucker Weed",
    author_email="tuckerweed@gmail.com",
    description="A lightweight, highly concurrent execution graph framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tucker-weed/prompt-graph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'jinja2',
    ],
)
