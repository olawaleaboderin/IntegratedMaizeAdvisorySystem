import pandas as pd
from tabulate import tabulate


# ======================================================
# CLIMATE & ENVIRONMENTAL RISK ASSESSMENT
# ======================================================
def climate_class_from_rainfall(climate_df, state, planting_month, months_order):
    """
    Classify climate suitability based on cumulative rainfall
    during the three months following planting.
    """
    # Determine the 3-month window starting from planting month
    start_idx = months_order.index(planting_month)
    months = [months_order[(start_idx + i) % 12] for i in range(3)]
    
    # Aggregate rainfall over the selected window
    rainfall_sum = climate_df[
        (climate_df["state"] == state) &
        (climate_df["month"].isin(months))
    ]["avg_rainfall_mm"].sum()

    # Rule-based classification
    if rainfall_sum < 100:
        return "Low"
    elif rainfall_sum < 200:
        return "Medium"
    return "High"

def drought_risk_from_climate(climate_class):
    """ Infer drought risk and irrigation advice from climate class."""
    c = climate_class.lower()
    if c == "low":
        return "High", "Frequent irrigation required"
    elif c == "medium":
        return "Medium", "Moderate irrigation recommended"
    elif c == "high":
        return "Low", "Irrigation usually not required"
    return "Unknown", "Unknown"

# ======================================================
# SOIL FERTILITY & INPUT RECOMMENDATIONS
# ======================================================

def soil_fertility_risk(soil_level):
    """ Translate soil fertility level into a risk category """
    s = soil_level.lower()
    if s == "low":
        return "High"
    elif s == "medium":
        return "Medium"
    elif s == "high":
        return "Low"
    return "Unknown"

def recommend_fertilizer(soil_level):
    """ Provide fertilizer recommendations based on soil fertility """
    s = soil_level.lower()
    if s == "low":
        return {"N": 120, "P2O5": 60, "K2O": 60,
                "notes":"Basal NPK 15-15-15 at 400 kg/ha + Urea top-dress at 125 kg/ha and MOP 100 kg/ha recommended.\n"
                "Split N: half at planting, half 4–6 weeks later."}
    elif s == "medium":
        return {"N": 60, "P2O5": 30, "K2O": 30,
                "notes":"NPK 15-15-15 at moderate levels required + Split Urea fertilizer application"}
    elif s == "high":
        return {"N": 30, "P2O5": 0, "K2O": 0,
                "notes":"Minimal fertilizer (only urea) input required."}
    return {"N": 0, "P2O5": 0, "K2O": 0, "notes": "No recommendation"}


# ======================================================
# PEST & DISEASE RISK ASSESSMENT
# ======================================================

def pest_disease_risk(drought_risk, soil_risk):
    """Combine drought and soil risks to estimate pest/disease pressure (risk)"""
    if drought_risk == "High" or soil_risk == "High":
        return "High"
    elif drought_risk == "Medium" or soil_risk == "Medium":
        return "Medium"
    return "Low"


def pest_disease_recommendation(risk_level: str) -> str:
    """ Provide pest and disease management advice based on risk level."""
    r = risk_level.lower()
    if r == "high":
        return "Intensive monitoring and timely pesticide application recommended."
    elif r == "medium":
        return "Regular monitoring with targeted interventions if needed."
    return "Routine monitoring sufficient."

# ======================================================
# RISK FORMATTING & CLASSIFICATION
# ======================================================

def color_risk(risk: str) -> str:
    """
    Convert risk level into a color-coded string
    for improved readability in console output.

    """
    r = risk.lower()
    if r == "high":
        return "\033[91m🔴 High\033[0m"
    elif r == "medium":
        return "\033[93m🟡 Medium\033[0m"
    elif r == "low":
        return "\033[92m🟢 Low\033[0m"
    return "Unknown"

# ======================================================
# MAIZE ADVISORY SYSTEM CLASS
# ======================================================

class MaizeAdvisorySystem:
    """
    Integrated decision-support system for maize cultivation.
    Combines climate, soil, and varietal data to generate
    actionable farming recommendations
    """

    def __init__(self, maize_df, state_df, climate_df, soil_df):
        # Store datasets internally
        self.maize_df = maize_df
        self.state_df = state_df
        self.climate_df = climate_df
        self.soil_df = soil_df

        # Fixed month order for rainfall window calculations
        self.months_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def validate_soil_level(self, state, soil_level):
        """
        Ensure the selected soil fertility level is valid for the given state.
        Raises an error if the combination is not allowed.
        """
        available = (
            self.soil_df[self.soil_df["state"] == state]["soil_level"]
            .str.lower()
            .tolist()
        )
        if soil_level.lower() not in available:
            raise ValueError(
                f"Soil fertility level '{soil_level}' not valid for state '{state}'. "
                f"Available levels: {available}"
            )

    def recommend_varieties(self, agro_zone, drought_risk, soil_risk):
        """Recommend top 3 maize varieties based on risks and adaptation zone."""
        df = self.maize_df[self.maize_df["adaptation_zone"] == agro_zone]

        # Apply drought tolerance filtering
        if drought_risk == "High":
            df = df[df["drought_tolerance"].str.lower() == "high"]
        elif drought_risk == "Medium":
            df = df[df["drought_tolerance"].str.lower().isin(["medium", "high"])]

        # Apply low-nitrogen tolerance filtering
        if soil_risk == "High":
            df = df[df["low_n_tolerance"].str.lower() == "high"]
        elif soil_risk == "Medium":
            df = df[df["low_n_tolerance"].str.lower().isin(["medium", "high"])]

        # Rank by yield potential
        return df.sort_values("yield_potential", ascending=False).head(3)

    def generate_report(self, state, planting_month, soil_level):
        """Generate and display the complete maize advisory report """

         # Validate inputs
        self.validate_soil_level(state, soil_level)

        # Extract agro-ecological zone
        agro_zone = self.state_df[self.state_df["state"] == state]["agro_zone"].iloc[0]

        # Risk assessments
        climate_class = climate_class_from_rainfall(
            self.climate_df, state, planting_month, self.months_order
        )
        drought_risk, irrigation_note = drought_risk_from_climate(climate_class)
        soil_risk = soil_fertility_risk(soil_level)
        pest_risk = pest_disease_risk(drought_risk, soil_risk)
        
        # Recommendations
        pest_note = pest_disease_recommendation(pest_risk)
        fertilizer = recommend_fertilizer(soil_level)
        varieties = self.recommend_varieties(agro_zone, drought_risk, soil_risk)

        # =========================
        # REPORT OUTPUT
        # =========================
        print("=" * 50)
        print("🌽 INTEGRATED MAIZE ADVISORY REPORT 🌽")
        print("=" * 50)

        # Summary section
        summary = [
            ["State", state],
            ["Agro-ecological zone", agro_zone],
            ["Planting month", planting_month],
            ["Soil fertility", soil_level],
            ["Climate class", climate_class],
        ]
        print(tabulate(summary, tablefmt="fancy_grid"))

        # Risk indicators
        risks = [
            ["Drought risk", color_risk(drought_risk)],
            ["Soil fertility risk", color_risk(soil_risk)],
            ["Pest/Disease risk", color_risk(pest_risk)],
        ]
        print("\nRISK INDICATORS")
        print("-" * 15)
        print(tabulate(risks, headers=["Risk", "Level"], tablefmt="fancy_grid"))

         # Fertilizer recommendations
        fert_table = [
            ["N", fertilizer["N"]],
            ["P2O5", fertilizer["P2O5"]],
            ["K2O", fertilizer["K2O"]],
        ]
        print("\nFERTILIZER RECOMMENDATION (kg/ha)")
        print("-" * 33)
        print(tabulate(fert_table, headers=["Nutrient", "Amount"], tablefmt="fancy_grid"))
        print(f"Notes: {fertilizer['notes']}")

        # Irrigation advice
        print("\nIRRIGATION RECOMMENDATION")
        print("-" * 25)
        print(irrigation_note)

        # Pest and disease advice
        print("\nPEST/DISEASE RECOMMENDATION")
        print("-" * 28)
        print(pest_note)

        # Variety recommendations
        print("\nRECOMMENDED MAIZE VARIETIES")
        print("-" * 33)

        if varieties.empty:
            print("No suitable varieties found for the selected conditions.")
        else:
            for i, (_, row) in enumerate(varieties.iterrows(), start=1):
                variety_table = [
                    ["Name", row["variety_name"]],
                    ["Maturity group", row["maturity_group"]],
                    ["Drought tolerance", row["drought_tolerance"]],
                    ["Low-N tolerance", row["low_n_tolerance"]],
                    ["Yield potential (t/ha)", row["yield_potential"]],
                    ["Grain type", row["grain_type"]],
                ]
                print(f"\nVariety {i}")
                print(tabulate(variety_table, tablefmt="fancy_grid"))


# ======================================================
# MAIN PROGRAM ENTRY POINT
# ======================================================

def main():
    """
    Load datasets, configure parameters, and run the advisory system.
    """
    maize_df = pd.read_csv("maize_varieties.csv")
    state_df = pd.read_csv("state_profile.csv")
    climate_df = pd.read_csv("climate_monthly.csv")
    soil_df = pd.read_csv("soil_state.csv")

    SELECTED_STATE = "Kaduna"  # Nigerian state for which the advisory is generated
    PLANTING_MONTH = "July"  # Month when maize planting is assumed to start
    SOIL_FERTILITY_LEVEL = "High"  # Soil fertility category used for risk and input recommendations

    advisory = MaizeAdvisorySystem(maize_df, state_df, climate_df, soil_df)
    advisory.generate_report(SELECTED_STATE, PLANTING_MONTH, SOIL_FERTILITY_LEVEL)


if __name__ == "__main__":
    main()
