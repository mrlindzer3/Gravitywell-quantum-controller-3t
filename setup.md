# Module: `setup.py`
### Package Distribution Manifest for the Aethel 3T Core Engine

```python
from setuptools import setup, find_packages

setup(
    name="gravitywell_quantum_controller_3t",
    version="1.0.0",
    author="Ryan Taylor Lindsey",
    description="A 3-Tier Hardware-Software Co-Design Engine for Non-Euclidean Optomechanical Control",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.9",
)
```
