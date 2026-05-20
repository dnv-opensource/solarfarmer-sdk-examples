"""DNV Solar Resource Compass API client.

Wraps the wcompare, soil and albedo endpoints of the SRC API.
API documentation: https://api.src.dnv.com/

Authentication: pass api_key directly or set the SRC_API_KEY environment variable.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

# --- Constants ---

WCOMPARE_URL = "https://api.src.dnv.com/api/site/wcompare"
SOIL_URL = "https://api.src.dnv.com/api/site/soil"
ALBEDO_URL = "https://api.src.dnv.com/api/site/albedo"

ENV_API_KEY = "SRC_API_KEY"

# Column names used by monthly_values() to extract the primary monthly series
MONTHLY_SOILING_COLUMN = "combined_soil_loss_0" # soiling without manual washes
MONTHLY_ALBEDO_COLUMN = "Albedo"


# ---------------------------------------------------------------------------
# Response types
# ---------------------------------------------------------------------------

class WcompareResult:
    """Parsed response from the /wcompare endpoint.

    Attributes:
        summary          -- high-level comparison stats and src_url link
        metadata         -- annual weather data and quality flags per datasource
        weather_monthly  -- monthly weather data per datasource
        weather_hourly   -- 8760-record TMY hourly dataset (selected median)
        api_metadata     -- rate-limit and quota information
    """

    def __init__(self, data: dict):
        self.summary = data.get("SUMMARY", {})
        self.metadata = data.get("METADATA", {})
        self.weather_monthly = data.get("WEATHER_MONTHLY", {})
        self.weather_hourly = data.get("WEATHER_HOURLY", [])
        self.api_metadata = data.get("APIMetadata", {})
        self._raw = data


class SoilingResult:
    """Parsed response from the /soil endpoint.

    Attributes:
        summary           -- src_url link
        system_attributes -- resolved input parameters (lat, lon, tilt, etc.)
        snow_metadata     -- nearest NOAA station metadata used for snow model
        snow_stations     -- snow data and losses from up to 3 nearby stations
        dust_metadata     -- metadata for the dust model calculation
        monthly_profiles  -- full monthly breakdown (dust, snow, combined losses)
        api_metadata      -- rate-limit and quota information
    """

    def __init__(self, data: dict):
        self.summary = data.get("SUMMARY", {})
        self.system_attributes = data.get("SYSTEM_ATTRIBUTES", {})
        self.snow_metadata = data.get("SNOW_METADATA", {})
        self.snow_stations = data.get("SNOW_STATIONS", [])
        self.dust_metadata = data.get("DUST_METADATA", {})
        self.monthly_profiles = data.get("MONTHLY_PROFILES", {})
        self.api_metadata = data.get("APIMetadata", {})
        self._raw = data

    def monthly_values(self) -> dict:
        """Returns the combined soiling loss by month.

        Returns a dict keyed by month identifier with the combined_soil_loss
        value for each of the 12 months.

        Example:
            losses = client.get_soiling(latitude, longitude).monthly_values()
        """
        return self.monthly_profiles.get(MONTHLY_SOILING_COLUMN, {})


class AlbedoResult:
    """Parsed response from the /albedo endpoint.

    Attributes:
        metadata         -- NOAA station metadata used for snow-cover model
        monthly_profiles -- full monthly breakdown (albedo, snow-cover days)
        api_metadata     -- rate-limit and quota information
    """

    def __init__(self, data: dict):
        self.metadata = data.get("METADATA", {})
        self.monthly_profiles = data.get("MONTHLY_PROFILES", {})
        self.api_metadata = data.get("APIMetadata", {})
        self._raw = data

    def monthly_values(self) -> dict:
        """Returns the albedo value by month.

        Returns a dict keyed by month identifier with the Albedo value for
        each of the 12 months.

        Example:
            albedo = client.get_albedo(latitude, longitude).monthly_values()
        """
        return self.monthly_profiles.get(MONTHLY_ALBEDO_COLUMN, {})


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class SolarResourceCompass:
    """Client for the DNV Solar Resource Compass API.

    Usage:
        client  = SolarResourceCompass(api_key="your-key")
        # or rely on the SRC_API_KEY environment variable:
        client  = SolarResourceCompass()

        weather = client.compare_weather(latitude=40, longitude=-85, elevation=300)
        soiling = client.get_soiling(latitude=40, longitude=-85, elevation=300)
        albedo  = client.get_albedo(latitude=40, longitude=-85, elevation=300)

        monthly_losses = soiling.monthly_values()
        monthly_albedo = albedo.monthly_values()
    """

    def __init__(self, api_key: str = None):
        self._api_key = (api_key or os.environ.get(ENV_API_KEY) or "").strip()
        if not self._api_key:
            raise ValueError(
                f"An API key is required. Pass api_key= or set the {ENV_API_KEY} environment variable."
            )

    def compare_weather(self, latitude: float, longitude: float, elevation: float = None) -> WcompareResult:
        """Calls /wcompare: weather comparison and TMY irradiance/weather data.

        Args:
            latitude:  Decimal degrees. Required. Valid range: -90 to 90.
                       Positive values = north of Equator; negative = south of Equator.
            longitude: Decimal degrees. Required. Valid range: -180 to 180.
                       Positive values = east of Greenwich; negative = west of Greenwich.
            elevation: Meters (m). Optional. Default = derived from coordinates.

        Returns:
            WcompareResult with summary, metadata, weather_monthly, weather_hourly.
        """
        params = {"lat": latitude, "lon": longitude, "elv": elevation}
        data = self._get(WCOMPARE_URL, params)
        return WcompareResult(data)

    def get_soiling(
        self,
        latitude: float,
        longitude: float,
        elevation: float = None,
        # Dust model inputs
        dust_soil_type: str = None,      # light_soil|mild_soil|moderate_soil|heavy_soil|severe_soil
        precip_wash_thresh: float = None, # mm; default 6.25
        ramp_rate: float = None,          # %/day; 0–0.5; default 0.1
        min_soil_thresh: float = None,    # %; 0–30; default 0
        max_soil_thresh: float = None,    # %; 0–50; default 30
        grace_days: int = None,           # days; 1–20; default 14
        # Snow / mounting inputs
        mounting: str = None,             # roof_fixed|carport_fixed|ground_fixed|ground_1axis
        array_tilt: float = None,         # degrees; 0–90
        clearance: float = None,          # inches; lower-edge clearance
        slant_len: float = None,          # inches; module slant length
        mod_type: str = None,             # cSi|fslr_s34|fslr_s6|sf
        mod_config: str = None,           # mod1P|mod2P|mod1L|mod2L|mod3L|mod4L
    ) -> SoilingResult:
        """Calls /soil: monthly dust and snow soiling loss profiles.

        Args:
            latitude:           Decimal degrees. Required. Valid range: -90 to 90.
                                Positive values = north of Equator; negative = south of Equator.
            longitude:          Decimal degrees. Required. Valid range: -180 to 180.
                                Positive values = east of Greenwich; negative = west of Greenwich.
            elevation:          Meters (m). Optional. Default = derived from coordinates.
            dust_soil_type:     Dust accumulation rate. Options: light_soil (0.05%/day),
                                mild_soil (0.1%/day), moderate_soil (0.15%/day),
                                heavy_soil (0.2%/day), severe_soil (0.3%/day). Default = mild_soil.
            precip_wash_thresh: mm. Precipitation threshold for a wash event. Default = 6.25.
            ramp_rate:          %/day. Soiling accumulation rate. Valid range: 0–0.5. Default = 0.1.
            min_soil_thresh:    %. Minimum soiling floor. Valid range: 0–30. Default = 0.
            max_soil_thresh:    %. Maximum soiling cap. Valid range: 0–50. Default = 30.
            grace_days:         Days after a wash event before soiling resumes. Range: 1–20. Default = 14.
            mounting:           System mounting type. Options: roof_fixed, carport_fixed,
                                ground_fixed, ground_1axis. Default = roof_fixed.
            array_tilt:         Degrees. Panel tilt from horizontal (0 = flat, 90 = vertical).
                                For trackers, specify the maximum rotation angle. Default = 10.
            clearance:          Inches. Distance between lower module edge and ground/roof.
                                Default = estimated from mounting selection.
            slant_len:          Inches. Module/array length in the slant direction.
                                Default = estimated from mod_type and mod_config.
            mod_type:           PV module type. Options: cSi, fslr_s34, fslr_s6, sf. Default = cSi.
            mod_config:         Module orientation on racking. Options: mod1P, mod2P, mod1L,
                                mod2L, mod3L, mod4L. Default = mod1P.

        Returns:
            SoilingResult with monthly_profiles and monthly_values().
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "elv": elevation,
            "dust_soil_type": dust_soil_type,
            "precip_wash_thresh": precip_wash_thresh,
            "ramp_rate": ramp_rate,
            "min_soil_thresh": min_soil_thresh,
            "max_soil_thresh": max_soil_thresh,
            "grace_days": grace_days,
            "mounting": mounting,
            "array_tilt": array_tilt,
            "clearance": clearance,
            "slant_len": slant_len,
            "mod_type": mod_type,
            "mod_config": mod_config,
        }
        data = self._get(SOIL_URL, params)
        return SoilingResult(data)

    def get_albedo(self, latitude: float, longitude: float, elevation: float = None) -> AlbedoResult:
        """Calls /albedo: monthly albedo profile.

        Args:
            latitude:  Decimal degrees. Required. Valid range: -90 to 90.
                       Positive values = north of Equator; negative = south of Equator.
            longitude: Decimal degrees. Required. Valid range: -180 to 180.
                       Positive values = east of Greenwich; negative = west of Greenwich.
            elevation: Meters (m). Optional. Default = derived from coordinates.

        Returns:
            AlbedoResult with monthly_profiles and monthly_values().
        """
        # The albedo endpoint uses PascalCase parameter names (API behaviour)
        params = {"Latitude": latitude, "Longitude": longitude, "Elevation": elevation}
        data = self._get(ALBEDO_URL, params)
        return AlbedoResult(data)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, url: str, params: dict) -> dict:
        """Makes an authenticated GET request and returns the parsed JSON body."""
        query_string = urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}
        )
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url, headers={"X-ApiKey": self._api_key})
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            body = exc.read().decode()
            raise RuntimeError(
                f"SRC API request failed [{exc.code}] for {url}: {body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"SRC API connection error for {url}: {exc.reason}"
            ) from exc
