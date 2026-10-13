import sqlite3

def seed_database():
    conn = sqlite3.connect("tdm.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Season e TestingObjective
    cursor.execute("INSERT INTO Season (year, name) VALUES (2027, 'Season 2026/2027')")
    season_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO TestingObjective (season_id, title, description, priority, desired_repetitions)
        VALUES (?, 'Validazione EBS & Setup Aerodinamico', 'Test di frenata di emergenza e correlazione angoli camber', 'ALTA', 3)
    """, (season_id,))

    # Vehicle e Driver
    cursor.execute("INSERT INTO Vehicle (name, generation) VALUES ('MG-01 Evo', 'EV 2026/2027')")
    vehicle_id = cursor.lastrowid

    cursor.execute("INSERT INTO Driver (name, racing_number) VALUES ('Mario Rossi', 46)")
    driver_1_id = cursor.lastrowid

    cursor.execute("INSERT INTO Driver (name, racing_number) VALUES ('Luigi Bianchi', 12)")
    driver_2_id = cursor.lastrowid

    # Track Location e Track Layout 
    cursor.execute("INSERT INTO TrackLocation (name, city) VALUES ('Circuito di Pomposa', 'San Giuseppe FE')")
    track_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO TrackLayout (track_location_id, layout_name, length_meters, activity_type)
        VALUES (?, 'Layout Endurance Principale', 1250.0, 'Endurance')
    """, (track_id,))
    layout_id = cursor.lastrowid

    # Tire Set
    cursor.execute("INSERT INTO TireSet (serial_number, compound) VALUES (101, 'Soft')")
    tires_soft_id = cursor.lastrowid

    cursor.execute("INSERT INTO TireSet (serial_number, compound) VALUES (102, 'Medium')")
    tires_medium_id = cursor.lastrowid

    # Setup e Corner Setup
    cursor.execute("""
        INSERT INTO Setup (power_limit_kw, mode, change_reason)
        VALUES (80.0, 'Qualifying Full Power', 'Baseline setup for dry condition test')
    """)
    setup_1_id = cursor.lastrowid

    for corner, camber, toe, spring in [('FL', -2.5, 0.2, 85.0), ('FR', -2.5, 0.2, 85.0), ('RL', -1.5, -0.1, 95.0), ('RR', -1.5, -0.1, 95.0)]:
        cursor.execute("""
            INSERT INTO CornerSetup (setup_id, corner, camber_deg, toe_deg, spring_rate_n_mm)
            VALUES (?, ?, ?, ?, ?)
        """, (setup_1_id, corner, camber, toe, spring))

    # Test Day
    cursor.execute("""
        INSERT INTO Test (season_id, vehicle_id, track_layout_id, test_date, weather_conditions, notes, status)
        VALUES (?, ?, ?, '2026-10-10', 'Soleggiato, 24°C', 'Sessione dedicata alla validazione setup con Mario e Luigi', 'COMPLETED')
    """, (season_id, vehicle_id, layout_id))
    test_id = cursor.lastrowid

    # Run 1
    cursor.execute("""
        INSERT INTO Run (test_id, driver_id, vehicle_id, tire_set_id, setup_id, run_number, run_type, asphalt_temp_c, ambient_temp_c, planned_laps, completed_laps)
        VALUES (?, ?, ?, ?, ?, 1, 'ACTUAL', 34.5, 23.0, 4, 4)
    """, (test_id, driver_1_id, vehicle_id, tires_soft_id, setup_1_id))
    run_1_id = cursor.lastrowid

    # Run 2
    cursor.execute("""
        INSERT INTO Run (test_id, driver_id, vehicle_id, tire_set_id, setup_id, run_number, run_type, asphalt_temp_c, ambient_temp_c, planned_laps, completed_laps)
        VALUES (?, ?, ?, ?, ?, 2, 'ACTUAL', 36.0, 25.0, 3, 3)
    """, (test_id, driver_1_id, vehicle_id, tires_soft_id, setup_1_id))
    run_2_id = cursor.lastrowid

    # Run 3
    cursor.execute("""
        INSERT INTO Run (test_id, driver_id, vehicle_id, tire_set_id, setup_id, run_number, run_type, asphalt_temp_c, ambient_temp_c, planned_laps, completed_laps)
        VALUES (?, ?, ?, ?, ?, 3, 'ACTUAL', 27.0, 20.0, 5, 5)
    """, (test_id, driver_2_id, vehicle_id, tires_medium_id, setup_1_id))
    run_3_id = cursor.lastrowid

    # Laps per Run 1
    laps_run_1 = [
        (run_1_id, 1, 52100, 0.0, 1),
        (run_1_id, 2, 49850, 0.0, 1), 
        (run_1_id, 3, 50400, 0.0, 1),
        (run_1_id, 4, 55200, 2.0, 1)  # Noto: penalità +2s
    ]
    cursor.executemany("INSERT INTO Lap (run_id, lap_number, lap_time_ms, penalty_seconds, is_valid) VALUES (?, ?, ?, ?, ?)", laps_run_1)

    # Laps per Run 2 
    laps_run_2 = [
        (run_2_id, 1, 51300, 0.0, 1),
        (run_2_id, 2, 49200, 0.0, 1), # Best Lap Assoluto
        (run_2_id, 3, 50100, 0.0, 1)
    ]
    cursor.executemany("INSERT INTO Lap (run_id, lap_number, lap_time_ms, penalty_seconds, is_valid) VALUES (?, ?, ?, ?, ?)", laps_run_2)

    # Laps per Run 3 
    laps_run_3 = [
        (run_3_id, 1, 53200, 0.0, 1),
        (run_3_id, 2, 51800, 0.0, 1),
        (run_3_id, 3, 51400, 0.0, 1),
        (run_3_id, 4, 52000, 0.0, 1),
        (run_3_id, 5, 51600, 0.0, 1)
    ]
    cursor.executemany("INSERT INTO Lap (run_id, lap_number, lap_time_ms, penalty_seconds, is_valid) VALUES (?, ?, ?, ?, ?)", laps_run_3)

    # Tire Measurements (esempio per Run 1)
    for corner in ['FL', 'FR', 'RL', 'RR']:
        cursor.execute("""
            INSERT INTO TireMeasurement (run_id, corner, measurement_type, pressure_bar, temp_inner_c, temp_center_c, temp_outer_c)
            VALUES (?, ?, 'PRE_RUN', 0.85, 23.0, 23.0, 23.0)
        """, (run_1_id, corner))
        cursor.execute("""
            INSERT INTO TireMeasurement (run_id, corner, measurement_type, pressure_bar, temp_inner_c, temp_center_c, temp_outer_c)
            VALUES (?, ?, 'POST_RUN', 1.05, 68.5, 65.2, 59.4)
        """, (run_1_id, corner))

    # Telemetry Log
    cursor.execute("""
        INSERT INTO TelemetryLog (run_id, file_path, file_type)
        VALUES (?, '/logs/2026-10-10/run_01_can_dump.csv', 'CSV')
    """, (run_1_id,))

    conn.commit()
    conn.close()
    print("Database popolato con successo!")

if __name__ == "__main__":
    seed_database()


# Codice quasi interamente scritto con Gemini