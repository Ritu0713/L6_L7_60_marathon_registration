import os
import sys
import pytest

# Ensure the LAB6 directory is on sys.path for direct imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marathon_registration import entry_fee, start_wave, finisher_status


# ==============================================================================
# 1. Normal Valid Inputs
# ==============================================================================

def test_entry_fee_5k_normal():
    """Test 5k standard registration without discounts or addons."""
    assert entry_fee("5k", 25, False, False) == 500


def test_entry_fee_10k_normal():
    """Test 10k standard registration without discounts or addons."""
    assert entry_fee("10k", 30, False, False) == 800


def test_entry_fee_half_normal():
    """Test half marathon standard registration without discounts or addons."""
    assert entry_fee("half", 25, False, False) == 1200


def test_entry_fee_full_normal():
    """Test full marathon standard registration without discounts or addons."""
    assert entry_fee("full", 30, False, False) == 1800


def test_entry_fee_early_bird_discount():
    """Test 25% discount applied for early bird registration."""
    # 800 - (800 // 4) = 600
    assert entry_fee("10k", 30, True, False) == 600


def test_entry_fee_senior_discount():
    """Test 50% senior discount applied for age >= 65."""
    # 800 // 2 = 400
    assert entry_fee("10k", 70, False, False) == 400


def test_entry_fee_tshirt_addon():
    """Test t-shirt add-on fee of 300 added to total."""
    # 800 + 300 = 1100
    assert entry_fee("10k", 30, False, True) == 1100


def test_entry_fee_all_options_combined():
    """Test combination of early bird, senior discount, and t-shirt add-on."""
    # 800 - 200 = 600 -> 600 // 2 = 300 -> 300 + 300 = 600
    assert entry_fee("10k", 65, True, True) == 600


# ==============================================================================
# 2. Invalid Inputs & Exception Handling
# ==============================================================================

def test_entry_fee_unknown_race():
    """Test exception raised for unregistered/invalid race category."""
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 25, False, False)


def test_entry_fee_too_young_general():
    """Test exception raised for runners younger than 12 years."""
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 10, False, False)


def test_entry_fee_half_too_young():
    """Test exception raised for half marathon runner under 18 years."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 16, False, False)


def test_entry_fee_full_too_young():
    """Test exception raised for full marathon runner under 18 years."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


# ==============================================================================
# 3. Boundary Conditions
# ==============================================================================

def test_entry_fee_age_boundary_12():
    """Test boundary conditions for minimum overall participation age (12)."""
    # Just below boundary (11) must raise ValueError
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)

    # Exactly at boundary (12) must succeed
    assert entry_fee("5k", 12, False, False) == 500


def test_entry_fee_age_boundary_18():
    """Test boundary conditions for distance races (half/full) minimum age (18)."""
    # Just below boundary (17) for half marathon must raise ValueError
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)

    # Exactly at boundary (18) for half marathon must succeed
    assert entry_fee("half", 18, False, False) == 1200

    # Age 15 in non-distance race (10k) is valid (12 <= age < 18)
    assert entry_fee("10k", 15, False, False) == 800


def test_entry_fee_age_boundary_65():
    """Test boundary conditions for senior discount eligibility (65)."""
    # Age 64 (just below boundary) gets no senior discount
    assert entry_fee("10k", 64, False, False) == 800

    # Age 65 (exactly at boundary) gets 50% discount
    assert entry_fee("10k", 65, False, False) == 400


# ==============================================================================
# 4. Different Functions: start_wave
# ==============================================================================

def test_start_wave_no_qualifying_time():
    """Test runners without qualifying time assigned to wave D."""
    assert start_wave(None, "full") == "D"
    assert start_wave(None, "half") == "D"


def test_start_wave_full_marathon():
    """Test start wave assignment for full marathon (cutoff = 240, 75% = 180)."""
    # Wave A: best_time * 4 <= 240 * 3 => best_time <= 180
    assert start_wave(150, "full") == "A"
    assert start_wave(180, "full") == "A"  # Boundary

    # Wave B: 180 < best_time <= 240
    assert start_wave(181, "full") == "B"
    assert start_wave(240, "full") == "B"  # Boundary

    # Wave C: best_time > 240
    assert start_wave(241, "full") == "C"


def test_start_wave_other_race():
    """Test start wave assignment for non-full races (cutoff = 120, 75% = 90)."""
    # Wave A: best_time * 4 <= 120 * 3 => best_time <= 90
    assert start_wave(75, "half") == "A"
    assert start_wave(90, "half") == "A"  # Boundary

    # Wave B: 90 < best_time <= 120
    assert start_wave(91, "half") == "B"
    assert start_wave(120, "half") == "B"  # Boundary

    # Wave C: best_time > 120
    assert start_wave(121, "half") == "C"


# ==============================================================================
# 5. Different Functions: finisher_status
# ==============================================================================

def test_finisher_status_disqualified():
    """Test missing any checkpoints leads to disqualification (DSQ)."""
    assert finisher_status(150, "full", 1) == "DSQ"
    assert finisher_status(60, "10k", 3) == "DSQ"


def test_finisher_status_full_marathon():
    """Test finisher status for full marathon (limit = 360)."""
    # Finished within limit
    assert finisher_status(360, "full", 0) == "finisher"  # Boundary
    assert finisher_status(250, "full", 0) == "finisher"

    # Did not finish within limit
    assert finisher_status(361, "full", 0) == "DNF"  # Boundary


def test_finisher_status_half_marathon():
    """Test finisher status for half marathon (limit = 180)."""
    # Finished within limit
    assert finisher_status(180, "half", 0) == "finisher"  # Boundary
    assert finisher_status(120, "half", 0) == "finisher"

    # Did not finish within limit
    assert finisher_status(181, "half", 0) == "DNF"  # Boundary


def test_finisher_status_other_races():
    """Test finisher status for other races (e.g. 10k/5k, limit = 90)."""
    # Finished within limit
    assert finisher_status(90, "10k", 0) == "finisher"  # Boundary
    assert finisher_status(45, "5k", 0) == "finisher"

    # Did not finish within limit
    assert finisher_status(91, "10k", 0) == "DNF"  # Boundary

