"""
Test suite for the Integrated Maize Advisory System.

These tests validate:
- Core rule-based functions (climate, soil, pest risk, fertilizer)
- Proper behaviour of the MaizeAdvisorySystem class
- Correct filtering and ranking of maize varieties

The tests are written using pytest for clarity and simplicity.
"""

import pandas as pd
import pytest

from project import (
    climate_class_from_rainfall,
    drought_risk_from_climate,
    soil_fertility_risk,
    recommend_fertilizer,
    pest_disease_risk,
    pest_disease_recommendation,
    color_risk,
    MaizeAdvisorySystem
)

# ======================================================
# FIXTURES: SMALL, CONTROLLED DATASETS FOR TESTING
# ======================================================

@pytest.fixture
def months_order():
    """Standard month ordering used across climate calculations."""
    return [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]


@pytest.fixture
def climate_df():
    """
    Minimal climate dataset.
    Rainfall values are chosen to make classification deterministic.
    """
    return pd.DataFrame({
        "state": ["Kaduna"] * 3,
        "month": ["July", "August", "September"],
        "avg_rainfall_mm": [40, 50, 60]  # Total = 150 → Medium climate
    })


@pytest.fixture
def soil_df():
    """Soil fertility levels available for Kaduna."""
    return pd.DataFrame({
        "state": ["Kaduna", "Kaduna", "Kaduna"],
        "soil_level": ["Low", "Medium", "High"]
    })


@pytest.fixture
def state_df():
    """Agro-ecological zone mapping."""
    return pd.DataFrame({
        "state": ["Kaduna"],
        "agro_zone": ["Northern Guinea Savanna"]
    })


@pytest.fixture
def maize_df():
    """
    Small maize variety dataset with controlled attributes.
    Yield potential is used for ranking.
    """
    return pd.DataFrame({
        "variety_name": ["V1", "V2", "V3", "V4"],
        "adaptation_zone": ["Northern Guinea Savanna"] * 4,
        "drought_tolerance": ["High", "Medium", "High", "Low"],
        "low_n_tolerance": ["High", "Medium", "High", "High"],
        "yield_potential": [6.0, 5.0, 7.0, 4.0],
        "maturity_group": ["Early", "Medium", "Late", "Early"],
        "grain_type": ["White", "Yellow", "White", "Yellow"]
    })


# ======================================================
# TESTS: CLIMATE & DROUGHT LOGIC
# ======================================================

def test_climate_class_from_rainfall_medium(climate_df, months_order):
    """150 mm rainfall over 3 months should classify as Medium climate."""
    result = climate_class_from_rainfall(
        climate_df, "Kaduna", "July", months_order
    )
    assert result == "Medium"


def test_drought_risk_from_climate():
    """Medium climate should imply medium drought risk."""
    risk, note = drought_risk_from_climate("Medium")
    assert risk == "Medium"
    assert "Moderate" in note


# ======================================================
# TESTS: SOIL & FERTILIZER LOGIC
# ======================================================

def test_soil_fertility_risk_mapping():
    """Low soil fertility must translate to High risk."""
    assert soil_fertility_risk("Low") == "High"


def test_recommend_fertilizer_low_soil():
    """Low soil fertility should require high fertilizer input."""
    fert = recommend_fertilizer("Low")
    assert fert["N"] == 120
    assert fert["P2O5"] == 60
    assert fert["K2O"] == 60


# ======================================================
# TESTS: PEST & DISEASE LOGIC
# ======================================================

def test_pest_disease_risk_high_condition():
    """
    High drought OR high soil risk must result in high pest risk.
    """
    risk = pest_disease_risk("High", "Low")
    assert risk == "High"


def test_pest_disease_recommendation_medium():
    """Medium pest risk should recommend regular monitoring."""
    note = pest_disease_recommendation("Medium")
    assert "Regular monitoring" in note


# ======================================================
# TESTS: FORMATTING UTILITIES
# ======================================================

def test_color_risk_high_contains_label():
    """Color formatting must preserve readable risk label."""
    colored = color_risk("High")
    assert "High" in colored


# ======================================================
# TESTS: MAIZE ADVISORY SYSTEM CLASS
# ======================================================

def test_validate_soil_level_valid(
    maize_df, state_df, climate_df, soil_df
):
    """Valid soil level for a state should not raise errors."""
    system = MaizeAdvisorySystem(
        maize_df, state_df, climate_df, soil_df
    )
    system.validate_soil_level("Kaduna", "High")


def test_validate_soil_level_invalid_raises_error(
    maize_df, state_df, climate_df, soil_df
):
    """Invalid soil level should raise a ValueError."""
    system = MaizeAdvisorySystem(
        maize_df, state_df, climate_df, soil_df
    )
    with pytest.raises(ValueError):
        system.validate_soil_level("Kaduna", "Very High")


def test_recommend_varieties_returns_top_three(
    maize_df, state_df, climate_df, soil_df
):
    """
    System should return at most three varieties,
    ranked by yield potential.
    """
    system = MaizeAdvisorySystem(
        maize_df, state_df, climate_df, soil_df
    )

    varieties = system.recommend_varieties(
        "Northern Guinea Savanna",
        drought_risk="High",
        soil_risk="High"
    )

    assert len(varieties) <= 3
    assert varieties.iloc[0]["yield_potential"] >= varieties.iloc[-1]["yield_potential"]
