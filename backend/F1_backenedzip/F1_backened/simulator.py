# telemetry_engine
import random, time, math

class TelemetrySimulator:
    def __init__(self, total_laps=57):
        self.lap = 1
        self.total_laps = total_laps
        self.tyre_age = 0
        self.fuel = 110.0          # kg, starts full
        self.ers_battery = 100.0  
         # percentage

    def generate_lap_data(self, driver_name="Max Verstappen") -> dict:
        base_laptime = 90.0  # seconds
        tyre_deg_effect = self.tyre_age * 0.08
        fuel_effect = -self.fuel * 0.03
        random_variation = random.uniform(-0.3, 0.3)

        lap_time = base_laptime + tyre_deg_effect + fuel_effect + random_variation

        self.fuel = max(0, self.fuel - 1.8)
        self.ers_battery = min(100, self.ers_battery - 5 + random.uniform(3, 7))
        self.tyre_age += 1

        return {
            "lap": self.lap,
            "driver": driver_name,
            "lap_time": round(lap_time, 3),
            "sector_1": round(lap_time * 0.31, 3),
            "sector_2": round(lap_time * 0.38, 3),
            "sector_3": round(lap_time * 0.31, 3),
            "tyre_age": self.tyre_age,
            "fuel_remaining": round(self.fuel, 2),
            "ers_battery": round(self.ers_battery, 1),
            "gap_to_leader": round(random.uniform(0, 25), 3),
        }
