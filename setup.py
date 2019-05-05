import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scikit-gaze",
    version="0.0.9",
    author="Zajic Michal",
    author_email="zajicmichal6@gmail.com",
    description="Library for scanpath comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zuhi6/scikit-gaze/",
    packages=["skgaze","skgaze.core","skgaze.EMDAT","skgaze.common_scanpath","skgaze.pattern_search","skgaze.RQA","skgaze.similarity_algorithms","skgaze.RQA.CustomPythonModules"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
