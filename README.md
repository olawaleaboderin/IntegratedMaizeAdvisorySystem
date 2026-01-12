# Integrated Maize Advisory System

## Project Overview
The **Integrated Maize Advisory System** is a Python-based decision-support tool designed to assist maize farmers, agronomists, and agricultural stakeholders in Nigeria with **data-driven cultivation recommendations**. The system integrates agro-ecological information, soil fertility data, climate (rainfall) patterns, and maize varietal characteristics to generate a **comprehensive advisory report** tailored to a selected Nigerian state.

---

## Problem Statement & Motivation
Maize is a staple crop for millions of households across Sub-Saharan Africa, yet its productivity is often constrained by **climate variability, declining soil fertility, and limited access to agronomic decision support** (Aboderin et al., 2025). Smallholder farmers in Nigeria frequently rely on generalized recommendations or traditional knowledge when deciding which maize varieties to plant, as well as on agronomic practices such as fertilizer application, irrigation scheduling, and pest and disease management. This lack of tailored guidance often leads to suboptimal yields and increased production risks.

This project addresses these challenges by providing farmers with **evidence-based recommendations** specific to their location and planting period. The system informs them about the **best planting months**, **fertilizer requirements**, **expected irrigation needs**, **pest and disease management strategies**, and **top-performing maize varieties** suited to their local agro-ecological conditions.

---

## System Architecture & Design
The system follows a **modular, hybrid architecture** that separates data processing, risk assessment, recommendation logic, and report generation into clearly defined components.  

- **Top-level functions:** Handle climate classification, risk assessment, fertilizer recommendation, and pest/disease advice using rule-based logic. These are designed for independent testing and reuse.  
- **`MaizeAdvisorySystem` class:** Coordinates input validation, risk assessment, variety recommendation, and report generation.  
- **`main()` function:** Loads datasets, sets configuration parameters, and runs the advisory workflow, ensuring reproducible execution and a clean entry point.  

---

## Methodology & Decision Logic

The system applies transparent, **rule-based decision rules** to transform environmental and agronomic data into actionable recommendations:

- **Climate Classification:** Average rainfall over the three months following the planting month is summed and classified into Low, Medium, or High climate classes using predefined thresholds.  
- **Drought and Irrigation Risk:** Climate class is mapped to drought risk levels, which in turn determine irrigation recommendations. Lower rainfall results in higher drought risk and increased irrigation requirements.  
- **Soil Fertility Risk & Fertilizer Recommendations:** Soil fertility levels are translated into risk categories that guide fertilizer application. Lower fertility soils receive higher nutrient recommendations, while high-fertility soils require minimal input.  
- **Pest & Disease Risk:** Pest and disease risk is inferred by combining drought and soil fertility risks. Elevated stress conditions trigger more intensive monitoring recommendations.  
- **Maize Variety Recommendation:** Varieties are filtered by agro-ecological adaptation and tolerance to drought and low-nitrogen stress, then ranked by yield potential. Up to **three top-performing varieties** are recommended.

---

## Project File Structure
.  
├── project.py                 
├── test_project.py            
├── maize_varieties.csv        
├── state_profile.csv         
├── climate_monthly.csv        
├── soil_state.csv              
├── requirements.txt           
└── README.md                  


### `project.py`
This is the main program file and entry point of the project. It contains several top-level helper functions responsible for risk classification, climate assessment, fertilizer recommendation, and pest/disease risk estimation. Implements the `MaizeAdvisorySystem` class responsible for input validation, variety recommendation, and report generation.

### `test_project.py`
This file contains automated tests implemented using `pytest`. The tests cover both the top-level helper functions and the class methods within `MaizeAdvisorySystem`. It also includes edge cases and checks for invalid inputs to ensure the system behaves reliably under all conditions.

### `requirements.txt`
This file lists all external Python libraries required for running the project. 

### `state_profile.csv`
This dataset contains information on 20 Nigerian states, representing four major agro-ecological zones (5 states per zone): Rainforest, Southern Guinea Savanna, Northern Guinea Savanna, and Sudan Savanna. Each state is mapped to its corresponding agro-ecological zone.

### `climate_monthly.csv`
This file provides average monthly rainfall and temperature for all 12 months for the 20 states.  

### `soil_state.csv`
This dataset records soil fertility levels for each state, categorized as Low, Medium, or High. These categories are used to validate user-selected soil fertility inputs, derive soil fertility risk levels, and inform fertilizer recommendations within the advisory system.

### `maize_varieties.csv`
This file contains data on 85 maize varieties released in Nigeria. Each variety is described by agronomically relevant attributes, including variety name, maturity group, agro-ecological adaptation zone, drought tolerance level, low-nitrogen tolerance level, yield potential in t/ha, and grain type. 

---

## Testing & Validation
- Automated tests implemented using **pytest**.
- Tests cover **top-level functions** (climate classification, risk assessment, fertilizer recommendation, formatting utilities) and **class methods** (soil fertility validation, maize variety recommendation).
- Deterministic test cases ensure correct outputs under known conditions.
- Error handling is validated, including invalid soil fertility levels.

---

## How to Run the Project

### Setup
1. Clone the repository:  
   
   `git clone <repository_url>`
   `cd python_project`

2.  (Optional) Create and activate a virtual environment:

    `python -m venv venv`. 
    `source venv/bin/activate`   # macOS/Linux. 
    `venv\Scripts\activate`      # Windows. 

3.  Install dependencies:  
    `pip install -r requirements.txt`

4.  Running the Advisory System:  
    `python project.py`. 
    **Note: All datasets must be located in the project root directory.**     
    The system is configured in the `main()` function of `project.py`. Users can modify:

    - `SELECTED_STATE` – The Nigerian state for the advisory report (e.g., `"Oyo"`).  
    - `PLANTING_MONTH` – The intended month of planting (e.g., `"June"`).  
    - `SOIL_FERTILITY_LEVEL` – Soil fertility level (Low, Medium, or High).  

### Output Description (Advisory Report)
The system generates a **console-based report** with the following sections:

- **Summary Table:** Displays the selected state, agro-ecological zone, planting month, soil fertility level, and climate class.
- **Risk Indicators:** Drought, soil fertility, and pest/disease risks with color-coded labels (red for High, yellow for Medium, green for Low).
- **Fertilizer Recommendations:** Lists recommended application rates for N, P₂O₅, and K₂O, with explanatory notes.
- **Irrigation Guidance:** Suggests frequency and intensity based on climate and drought risk.
- **Pest/Disease Advice:** Provides monitoring and intervention recommendations according to assessed risk.
- **Recommended Maize Varieties:** Detailed information on top-ranked varieties, including maturity group, stress tolerance traits, yield potential, and grain type.

---

### Limitations & Assumptions
-   The system is rule-based, not machine-learning; decisions rely on predefined thresholds.
-   Datasets are static, representing historical averages rather than real-time conditions.
-   Fertilizer rates are indicative and generalized per soil fertility level.
-   Climate classification thresholds may not capture microclimatic variations.
-   User inputs are assumed valid unless otherwise validated by the system

### Future Improvements
-   Integration of real-time weather APIs for dynamic climate data.
-   GIS-based spatial visualization of risks and recommendations.
-   Development of a web or mobile interface for smallholder farmers.
-   Incorporation of machine learning models for refined drought, pest, and yield predictions.
-   Expansion to a multi-crop advisory system for broader agricultural decision support.