# Algorithm 2: Class Offering Capacity Forecaster

This repository contains a small package, *capacityforecaster*, for
estimating required course offering capacities based on historical enrollment
data. 

This package was authored for the Company 2 course scheduler project by the Company2-Algorithm2 subsystem team.

## Install from TestPyPi Using `pip` (Recommended)
Install this package into your environment from TestPyPi using `pip`. You must specify that
this package is found on the test PyPi index as below.

```bash
$ pip install -i https://test.pypi.org/simple/ capacityforecaster
```
The most recent available version of the package is uploaded to the test PyPi index automatically.
To ensure that you are working with the most recent release upgrade this module before integrating.

```bash
$ python3 -m pip install --upgrade capacityforecaster
```

## Install from Local Archives

Clone this repo into the scheduler (or backend) repository. Inside the algorithm 2 module directory,
build and install the package as shown below. Change the version number from `0.0.1` to the current
 version.

```bash
$ python3 -m build
$ pip3 install ./dist/capacityforecaster-0.0.1.tar.gz
```

## Usage
The algorithm 2 module may then be imported into and called from the backend. Below,
`course_enrollment` `program_enrollment` and `schedule` are expected to be python dictionaries.  A schedule object with capacities assigned is encoded as python dictionary and returned to caller.

```python
from forecaster.forecaster import forecast
schedule = forecast(course_enrollment, program_enrollment, schedule)
```

## Dev 

To make and test changes to the project, navigate into the root level directory 
`/path/to/algorithm2/`. After editing the projet files, in order for the changes to take
effect you must reinstall the local package by the following cmd:

```bash
$ pip install . 
```

To run the tests

```bash
$ cd test
$ python -m pytest
```

# Software Architecture

The following section will highliight the software architecture created, and a breif description of the purpose and function of each module to better aid a new developer in learning inner working of the system, creating faster onboarding. 


![alt text](https://github.com/seng499-company2/algorithm2/blob/40-documentation/AlgOverview.png?raw=true)
