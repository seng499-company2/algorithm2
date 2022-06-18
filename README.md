# Algorithm 2: Class Offering Capacity Forecaster

This repository contains a small package, *Class-Capacity-Forecaster*, for
estimating required course offering capacities based on historical enrollment
data. 

This package was authored for the Company 2 course scheduler project by the Company2-Algorithm2 subsystem team.

## Install from PiPy Using `pip` (Recommended)
Download this repo from TestPyPi using pip

```bash
$ pip install -i https://test.pypi.org/simple/ Class-Capacity-Forecaster
```

The algorithm 2 module may then be imported into and called from the backend.

```python
from Class-Capacity-Forecaster import forecaster
forecaster.forecast(course_enrollment, program_enrollment, schedule)
```

## Install from Local Build

Clone this repo into the scheduler (or backend) repository. Inside the algorithm 2 module directory,
build and install the package as shown below. Change the version number from `0.0.1` to the current
version (specified) in `setup.py`.

```bash
$ python3 -m build
$ pip3 install ./dist/Class-Capacity-Forecaster-0.0.1.tar
```

The algorithm 2 module may then be imported into and called from the backend.

```python
from Class-Capacity-Forecaster import forecaster
forecaster.forecast(course_enrollment, program_enrollment, schedule)
```

## Dev 

To use the changed code in forecaster dir, you need to pip install the package first.
Make sure your current working directory is `~/algorithm2`

```bash
$ pip install . 
```

To run the tests

```bash
$ cd test
$ python -m pytest
```
