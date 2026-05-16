# pit_strategy.py

PIT_LOSS_SECONDS = 22.0  # average time lost in pit lane

class PitStrategy:
    def calculate_undercut(self, my_lap_time, rival_lap_time, gap_to_rival,
                            tyre_deg_engine, my_compound, my_tyre_age,
                            new_compound="SOFT") -> dict:
        """Pit one lap before rival to get fresh tyre advantage."""
        fresh_tyre = tyre_deg_engine.calculate(new_compound, 0)
        my_new_laptime = my_lap_time - fresh_tyre["lap_time_penalty_sec"] + \
                          tyre_deg_engine.calculate(my_compound, my_tyre_age)["lap_time_penalty_sec"]

        # After pit stop, do we come out ahead?
        time_loss = PIT_LOSS_SECONDS
        laps_to_make_up = time_loss / max(0.01, rival_lap_time - my_new_laptime)

        return {
            "strategy": "UNDERCUT",
            "new_compound": new_compound,
            "pit_loss_sec": PIT_LOSS_SECONDS,
            "laps_to_recover": round(laps_to_make_up, 1),
            "recommended": laps_to_make_up < 8,
            "my_new_lap_time": round(my_new_laptime, 3),
        }

    def optimal_pit_window(self, current_lap, tyre_age, compound, total_laps, tyre_engine) -> dict:
        deg_data = tyre_engine.calculate(compound, tyre_age)
        latest_safe_lap = current_lap + deg_data["recommended_pit_in_laps"]
        optimal_lap = max(current_lap + 1, latest_safe_lap - 3)

        return {
            "optimal_pit_lap": int(min(optimal_lap, total_laps - 5)),
            "latest_safe_lap": int(min(latest_safe_lap, total_laps - 3)),
            "urgency": "URGENT" if tyre_age > 30 else "NORMAL",
        } 
    for i in range(10):
        print(i)