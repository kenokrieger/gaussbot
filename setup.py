import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gaussbot", # Replace with your own username
    version="1.0.0",
    author="Keno Krieger",
    author_email="kriegerk@uni-bremen.de",
    description="A bot for our physicists discord server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenokrieger/gaussbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)