"""
Example usage of the Solar Resource Compass API client.

This demonstrates calling each of the three endpoints:
  - compare_weather()  : wcompare endpoint
  - get_soiling()      : soil endpoint
  - get_albedo()       : albedo endpoint

Set the SRC_API_KEY environment variable with your API key, or pass it directly.
"""
#%%
import os
from solar_resource_compass import SolarResourceCompass

# ---------------------------------------------------------------------------
# Initialize the client
# ---------------------------------------------------------------------------

# Option 1: Use the SRC_API_KEY environment variable (recommended for production)
client = SolarResourceCompass()

# Option 2: Pass the API key directly (for testing/scripts)
#API_KEY = os.environ.get("SRC_API_KEY")
#API_KEY = "YOUR TOKEN HERE"

#if not API_KEY:
#    print("warning: src_api_key environment variable not set.")
#    print("to test, set: set src_api_key=your-key-here")
#    exit(1)

#client = SolarResourceCompass(api_key=API_KEY)

# Location parameters (Denver, Colorado example)
latitude = 39.74
longitude = -104.99
elevation = 1609

print("=" * 70)
print("Solar Resource Compass API Examples")
print("=" * 70)
print(f"Location: {latitude}°, {longitude}°, {elevation}m elevation\n")

#%%
# ---------------------------------------------------------------------------
# Example 1: Weather Comparison (wcompare endpoint)
# ---------------------------------------------------------------------------

print("1. WEATHER COMPARISON (wcompare)")
print("-" * 70)
try:
    weather = client.compare_weather(
        latitude=latitude,
        longitude=longitude,
        elevation=elevation
    )
    
    print("\nSummary:")
    for key, value in weather.summary.items():
        print(f"  {key}: {value}")
    
    print("\nMetadata (datasource comparison):")
    if weather.metadata:
        for datasource, attrs in list(weather.metadata.items())[:3]:  # Show first 3
            print(f"\n  {datasource}:")
            for attr, val in list(attrs.items())[:4]:  # Show first 4 attributes
                print(f"    {attr}: {val}")
    
    print("\n  (Full metadata and hourly weather available via weather.metadata)")
    print(f"                                       and weather.weather_hourly)")
    
except Exception as e:
    print(f"Error: {e}")

#%%
# ---------------------------------------------------------------------------
# Example 2: Soiling Profile (soil endpoint)
# ---------------------------------------------------------------------------

print("\n\n2. SOILING PROFILE (soil)")
print("-" * 70)
try:
    soiling = client.get_soiling(
        latitude=latitude,
        longitude=longitude,
        elevation=elevation,
        dust_soil_type="mild_soil",        # Dust accumulation rate
        mounting="ground_1axis",            # 1-axis tracker
        array_tilt=30,                      # Tilt angle in degrees
        precip_wash_thresh=6.25             # Minimum rain for wash event (mm)
    )
    
    print("\nSystem Attributes:")
    for key, value in list(soiling.system_attributes.items())[:6]:
        print(f"  {key}: {value}")
    
    print("\nMonthly Soiling Profiles:")
    monthly_losses = soiling.monthly_values()
    if monthly_losses:
        # Display combined_soil_loss (the main column of interest)
        for month, loss in monthly_losses.items():
            print(f"  {month}: {loss}%")
    
    print(f"\nFull profiles available via:")
    print(f"  - soiling.monthly_profiles (all dust, snow, and combined losses)")
    print(f"  - soiling.snow_metadata (NOAA station used)")
    print(f"  - soiling.snow_stations (up to 3 nearby stations)")
    
except Exception as e:
    print(f"Error: {e}")

#%%
# ---------------------------------------------------------------------------
# Example 3: Albedo Profile (albedo endpoint)
# ---------------------------------------------------------------------------

print("\n\n3. ALBEDO PROFILE (albedo)")
print("-" * 70)
try:
    albedo = client.get_albedo(
        latitude=latitude,
        longitude=longitude,
        elevation=elevation
    )
    
    print("\nMetadata:")
    for key, value in list(albedo.metadata.items())[:4]:
        print(f"  {key}: {value}")
    
    print("\nMonthly Albedo Values:")
    monthly_albedo = albedo.monthly_values()
    if monthly_albedo:
        # Display Albedo (the main column of interest)
        for month, value in monthly_albedo.items():
            print(f"  {month}: {value}")
    
    print(f"\nFull profiles available via:")
    print(f"  - albedo.monthly_profiles (albedo and snow-cover days)")
    
except Exception as e:
    print(f"Error: {e}")
# %%
