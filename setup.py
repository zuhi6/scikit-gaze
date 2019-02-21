import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scikit-gaze",
    version="0.0.1",
    author="Zajic Michal",
    author_email="zajicmichal6@gmail.com",
    description="Library for scanpath comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zuhi6/scikit-gaze/code/src",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
