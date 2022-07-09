import setuptools
from urllib.request import urlopen
from lxml import etree

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Inspect current most recent version on PyPi index
url = "https://test.pypi.org/project/capacityforecaster/"
response = urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
element = tree.xpath("/html/body/main/div[2]/div/div[1]/h1")
text = element[0].text.strip()
pypi_version = text.split(' ')[1]

major = int(pypi_version[0])
minor = int(pypi_version[2])
patch = int(pypi_version[4])
patch += 1
if patch > 9:
    patch = 0
    minor += 1
if minor > 9:
    minor = 0
    major += 1

release_version = f"{major}.{minor}.{patch}"

setuptools.setup(
    name="capacityforecaster",
    version=release_version,
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
    package_data={'forecaster': ['./static_files/*.json']},
    include_package_data=True,
    install_requires=['pmdarima'],
    python_requires=">=3.6",
)
