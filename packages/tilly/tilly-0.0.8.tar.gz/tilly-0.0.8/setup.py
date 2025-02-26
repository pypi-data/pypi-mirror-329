import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requirements = [line.strip().split('#')[0] for line in f.read().split('\n') if line.strip().split('#')[0]]

setuptools.setup(
    name="tilly",
    version="0.0.8",
    author="Ronald Luitwieler",
    author_email="ronald.luitwieler@gmail.com",
    description="A cli for tracking Things I Learned (TIL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tilly-pub/tilly",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "til = tilly.main:cli",
            "tilly = tilly.main:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)