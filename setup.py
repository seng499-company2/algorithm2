import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Class-Capacity-Forecaster",
    version="0.0.2",
    author="Algorithm 2 SubTeam",
    author_email="seanmcauliffe42@gmail.com",
    description="An algorithm for predicting future class capacities based on historical enrollment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seng499-company2/algorithm2",
    project_urls={
        "Bug Tracker": "https://github.com/seng499-company2/algorithm2/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
