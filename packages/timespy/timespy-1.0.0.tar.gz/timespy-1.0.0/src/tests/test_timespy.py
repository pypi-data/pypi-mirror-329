from timespy import timer
import time

def test_profile():
    @timer
    def fast_function():
        pass

    fast_function()
    assert fast_function.exec_time >= 0

def test_slow_function():
    @timer
    def slow_function():
        time.sleep(1)

    slow_function()
    assert slow_function.exec_time >= 1.0
