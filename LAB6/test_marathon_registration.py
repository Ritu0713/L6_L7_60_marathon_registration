import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marathon_registration import entry_fee, start_wave, finisher_status

# Import all tests from the official code coverage suite
from CodeCoverageTest_PES1UG24CS928_marathon_registration import *

# Example test cases:
def test_10k_standard():
    assert entry_fee("10k", 30, False, False) == 800

def test_first_timer_wave():
    assert start_wave(None, "full") == "D"
