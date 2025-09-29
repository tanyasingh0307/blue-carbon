# Minimal MRV heuristic script for demo purposes.

def estimate_co2(area_ha, biomass_per_ha=120.0):
    """
    Estimate CO2 equivalent emissions from area and biomass.

    Parameters:
        area_ha (float): Area in hectares
        biomass_per_ha (float): Biomass in tonnes carbon per hectare (default = 120.0)

    Returns:
        dict: containing area, biomass density, and CO2 equivalent in tonnes
    """
    biomass_tc = biomass_per_ha
    co2e = biomass_tc * area_ha * 3.667
    return {
        'area_ha': area_ha,
        'biomass_tc_ha': biomass_per_ha,
        'co2e_tons': co2e
    }

if __name__ == '__main__':
    try:
        # Get user input
        area_ha = float(input("Enter area in hectares: "))
        
        biomass_input = input("Enter biomass per hectare (default 120.0): ")
        biomass_per_ha = float(biomass_input) if biomass_input.strip() else 120.0

        result = estimate_co2(area_ha, biomass_per_ha)

        print("\n--- CO2 Estimation Result ---")
        print(f"Area (ha): {result['area_ha']}")
        print(f"Biomass per ha (tC): {result['biomass_tc_ha']}")
        print(f"Estimated CO2e (tons): {result['co2e_tons']:.2f}")

    except ValueError:
        print("⚠️ Please enter numeric values for area and biomass.")
