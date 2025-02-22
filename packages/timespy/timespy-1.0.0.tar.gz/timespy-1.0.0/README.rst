.. image:: https://img.shields.io/pepy/dt/timespy
   :alt: Pepy Total Downloads
.. image:: https://img.shields.io/pypi/dm/timespy
   :alt: PyPI - Downloads
.. image:: https://img.shields.io/pypi/dd/timespy
   :alt: PyPI - Downloads
.. image:: https://img.shields.io/github/license/croketillo/timespy
   :alt: GitHub License
.. image:: https://img.shields.io/pypi/l/timespy
   :alt: PyPI - License
.. image:: https://img.shields.io/pypi/format/timespy
   :alt: PyPI - Format
.. image:: https://img.shields.io/pypi/pyversions/timespy
   :alt: PyPI - Python Version
.. image:: https://img.shields.io/pypi/wheel/timespy
   :alt: PyPI - Wheel
.. image:: https://img.shields.io/librariesio/sourcerank/pypi/timespy?color=00a135
   :alt: Libraries.io SourceRank
.. image:: https://img.shields.io/github/size/croketillo/timespy/src%2Ftimespy%2Ftimespy.py
   :alt: GitHub file size in bytes
.. image:: https://img.shields.io/github/v/release/croketillo/timespy
   :alt: GitHub Release


TimeSpy ⏱
=========

Timespy is a lightweight Python decorator that measures the execution
time of functions, providing an easy way to analyze and optimize
performance.

Installation
------------

.. code:: sh

   pip install timespy

Usage
-----

.. code:: sh

   from timespy import timer

   @timer
   def my_function():
       import time
       time.sleep(1)

   my_function()
   print(f"Execution time: {my_function.exec_time:.6f}s")

License
-------

TimeSpy is licensed under the GNU General Public License v3 (GPLv3). See
LICENSE for more details.
