![Pepy Total Downloads](https://img.shields.io/pepy/dt/timespy) |  ![PyPI - Downloads](https://img.shields.io/pypi/dm/timespy) | ![PyPI - Downloads](https://img.shields.io/pypi/dd/timespy) | ![GitHub License](https://img.shields.io/github/license/croketillo/timespy) | ![PyPI - License](https://img.shields.io/pypi/l/timespy) | ![PyPI - Format](https://img.shields.io/pypi/format/timespy) | ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/timespy) | ![PyPI - Wheel](https://img.shields.io/pypi/wheel/timespy) | ![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/timespy?color=00a135) | ![GitHub file size in bytes](https://img.shields.io/github/size/croketillo/timespy/src%2Ftimespy%2Ftimespy.py) | ![GitHub Release](https://img.shields.io/github/v/release/croketillo/timespy)


# TimeSpy ⏱
Timespy is a lightweight Python decorator that measures the execution time of functions, providing an easy way to analyze and optimize performance.

## Installation
```sh
pip install timespy
```

## Usage

```sh
from timespy import timer

@timer
def my_function():
    import time
    time.sleep(1)

my_function()
print(f"Execution time: {my_function.exec_time:.6f}s")
```

## License

TimeSpy is licensed under the GNU General Public License v3 (GPLv3).
See LICENSE for more details.