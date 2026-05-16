# race_simulator/what_if.py

class WhatIfSimulator:
    def simulate(self, scenario: dict, telemetry_sim, tyre_engine, pit_engine) -> dict:
        """
        scenario = {
          "safety_car_lap": 30,       # or None
          "driving_mode": "aggressive", # "balanced", "fuel_save"
          "tyre_compound": "SOFT",
          "pit_lap": 25,
          "fuel_mode": "rich"
        }
        """
        total_time = 0
        positions_lost = 0
        tyre_age = 0

        compound = scenario.get("tyre_compound", "MEDIUM")
        pit_lap = scenario.get("pit_lap", 25)
        driving_mode = scenario.get("driving_mode", "balanced")

        mode_effect = {"aggressive": -0.3, "balanced": 0, "fuel_save": +0.4}
        pace_delta = mode_effect.get(driving_mode, 0)

        for lap in range(1, 58):
            deg = tyre_engine.calculate(compound, tyre_age)
            lap_time = 90 + deg["lap_time_penalty_sec"] + pace_delta
            total_time += lap_time
            tyre_age += 1

            if lap == pit_lap:
                total_time += 22  # pit loss
                tyre_age = 0
                compound = "HARD" if scenario.get("tyre_compound") == "SOFT" else "SOFT"

        return {
            "scenario": scenario,
            "estimated_race_time_sec": round(total_time, 1),
            "estimated_finish_position": max(1, 10 - positions_lost),
        }