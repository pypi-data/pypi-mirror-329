from setuptools import setup, find_packages

setup(
    name="beautiful-captions",
    version="0.1.3",
    package_dir={"beautiful_captions": "src/beautiful_captions"},
    packages=["beautiful_captions"] + [
        "beautiful_captions." + pkg 
        for pkg in find_packages(where="src/beautiful_captions")
    ],
    python_requires=">=3.8",
) 