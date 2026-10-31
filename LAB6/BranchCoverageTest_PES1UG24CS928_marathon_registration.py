import os
import sys
import pytest

# Ensure the LAB6 directory is on sys.path for direct imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marathon_registration import entry_fee, start_wave, finisher_status


# ==============================================================================
# Branch Coverage Tests: entry_fee
# ==============================================================================

def test_branch_entry_fee_unknown_race():
    """Branch: race not in ENTRY_FEE (True) -> raises ValueError."""
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra_marathon", 25, False, False)


def test_branch_entry_fee_valid_race_and_too_young():
    """Branch: race in ENTRY_FEE (False for not in) and age < 12 (True) -> raises ValueError."""
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_branch_entry_fee_distance_too_young_half():
    """Branch: race in ('half', 'full') [True for half] and age < 18 [True] -> raises ValueError."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)


def test_branch_entry_fee_distance_too_young_full():
    """Branch: race in ('half', 'full') [True for full] and age < 18 [True] -> raises ValueError."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 16, False, False)


def test_branch_entry_fee_distance_valid_age():
    """Branch: race in ('half', 'full') and age >= 18 (Condition evaluates to False)."""
    assert entry_fee("half", 18, False, False) == 1200
    assert entry_fee("full", 21, False, False) == 1800


def test_branch_entry_fee_non_distance_under_18():
    """Branch: race NOT in ('half', 'full') and 12 <= age < 18 (Condition evaluates to False)."""
    assert entry_fee("10k", 15, False, False) == 800
    assert entry_fee("5k", 12, False, False) == 500


def test_branch_entry_fee_early_bird():
    """Branch: is_early_bird True vs False."""
    # is_early_bird = True -> 800 - 200 = 600
    assert entry_fee("10k", 30, True, False) == 600
    # is_early_bird = False -> 800
    assert entry_fee("10k", 30, False, False) == 800


def test_branch_entry_fee_senior_discount():
    """Branch: age >= 65 True vs False."""
    # age >= 65 (True) -> 800 // 2 = 400
    assert entry_fee("10k", 65, False, False) == 400
    assert entry_fee("10k", 75, False, False) == 400
    # age >= 65 (False: age 64) -> 800
    assert entry_fee("10k", 64, False, False) == 800


def test_branch_entry_fee_needs_tshirt():
    """Branch: needs_tshirt True vs False."""
    # needs_tshirt = True -> 800 + 300 = 1100
    assert entry_fee("10k", 30, False, True) == 1100
    # needs_tshirt = False -> 800
    assert entry_fee("10k", 30, False, False) == 800


def test_branch_entry_fee_all_branches_combined():
    """Branch: all boolean modifiers True simultaneously."""
    # base 10k: 800 -> early bird (-200) = 600 -> senior (//2) = 300 -> tshirt (+300) = 600
    assert entry_fee("10k", 65, True, True) == 600


# ==============================================================================
# Branch Coverage Tests: start_wave
# ==============================================================================

def test_branch_start_wave_none_best_time():
    """Branch: best_time_minutes is None (True) -> returns 'D'."""
    assert start_wave(None, "full") == "D"
    assert start_wave(None, "10k") == "D"


def test_branch_start_wave_full_marathon_branches():
    """Branch: race == 'full' (True) with wave A, B, and C branches (cutoff = 240)."""
    # Wave A: best_time * 4 <= 240 * 3 => best_time <= 180 (True)
    assert start_wave(180, "full") == "A"
    assert start_wave(150, "full") == "A"

    # Wave B: Wave A False, best_time <= 240 (True)
    assert start_wave(181, "full") == "B"
    assert start_wave(240, "full") == "B"

    # Wave C: Wave A False, Wave B False -> return 'C'
    assert start_wave(241, "full") == "C"


def test_branch_start_wave_other_race_branches():
    """Branch: race == 'full' (False) with wave A, B, and C branches (cutoff = 120)."""
    # Wave A: best_time * 4 <= 120 * 3 => best_time <= 90 (True)
    assert start_wave(90, "half") == "A"
    assert start_wave(60, "10k") == "A"

    # Wave B: Wave A False, best_time <= 120 (True)
    assert start_wave(91, "half") == "B"
    assert start_wave(120, "half") == "B"

    # Wave C: Wave A False, Wave B False -> return 'C'
    assert start_wave(121, "half") == "C"


# ==============================================================================
# Branch Coverage Tests: finisher_status
# ==============================================================================

def test_branch_finisher_status_checkpoints_missed():
    """Branch: checkpoints_missed > 0 (True) -> returns 'DSQ'."""
    assert finisher_status(100, "full", 1) == "DSQ"
    assert finisher_status(50, "5k", 2) == "DSQ"


def test_branch_finisher_status_full_marathon():
    """Branch: race == 'full' (True, limit = 360) -> finisher vs DNF."""
    # elapsed_minutes <= 360 (True) -> 'finisher'
    assert finisher_status(360, "full", 0) == "finisher"
    assert finisher_status(300, "full", 0) == "finisher"

    # elapsed_minutes <= 360 (False) -> 'DNF'
    assert finisher_status(361, "full", 0) == "DNF"


def test_branch_finisher_status_half_marathon():
    """Branch: race == 'full' (False), race == 'half' (True, limit = 180) -> finisher vs DNF."""
    # elapsed_minutes <= 180 (True) -> 'finisher'
    assert finisher_status(180, "half", 0) == "finisher"
    assert finisher_status(120, "half", 0) == "finisher"

    # elapsed_minutes <= 180 (False) -> 'DNF'
    assert finisher_status(181, "half", 0) == "DNF"


def test_branch_finisher_status_other_races():
    """Branch: race == 'full' (False), race == 'half' (False, limit = 90) -> finisher vs DNF."""
    # elapsed_minutes <= 90 (True) -> 'finisher'
    assert finisher_status(90, "10k", 0) == "finisher"
    assert finisher_status(45, "5k", 0) == "finisher"

    # elapsed_minutes <= 90 (False) -> 'DNF'
    assert finisher_status(91, "10k", 0) == "DNF"

