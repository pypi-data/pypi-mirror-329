from setuptools import setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="vedro-spec-compare",
    version="0.9.0",
    description="OpenAPI spec compare",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konstantin Shefer",
    author_email="kostya.shefer.999@gmail.com",
    python_requires=">=3.8",
    url="https://github.com/kvs8/vedro-spec-compare",
    license="Apache-2.0",
    packages=['vedro_spec_compare'],
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "vsc = vedro_spec_compare:command",
        ],
    },
    include_package_data=True,
)
