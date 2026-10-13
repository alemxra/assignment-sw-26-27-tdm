PRAGMA foreign_keys = ON;

--I valori che ho inserito nei CHECK sono a titolo d'esempio
--La stessa cosa vale per qualche tipo di valore, per semplicità ho generalizzato con TEXT, INTEGER, REAL...
CREATE TABLE Season (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    year INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TestingObjective (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('BASSA', 'MEDIA', 'ALTA')),
    desired_repetitions INTEGER DEFAULT 1, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (season_id) REFERENCES Season(id) ON DELETE CASCADE
);

CREATE TABLE Vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL UNIQUE,
    generation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    racing_number INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TrackLocation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TrackLayout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_location_id INTEGER NOT NULL,
    layout_name TEXT NOT NULL,
    length_meters REAL NOT NULL CHECK(length_meters > 0),
    activity_type TEXT CHECK(activity_type IN ('Skidpad', 'Acceleration', 'Testing', 'Endurance', 'Autocross')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_location_id) REFERENCES TrackLocation(id) ON DELETE CASCADE
);

CREATE TABLE Setup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    power_limit_kw REAL NOT NULL CHECK(power_limit_kw > 0),
    mode TEXT NOT NULL,
    change_reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CornerSetup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setup_id INTEGER NOT NULL,
    corner TEXT NOT NULL CHECK(corner IN ('FL', 'FR', 'RL', 'RR')),
    toe_deg REAL NOT NULL,
    spring_rate_n_mm REAL NOT NULL,
    camber_deg REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (setup_id) REFERENCES Setup(id) ON DELETE CASCADE
);

CREATE TABLE TireSet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number INTEGER NOT NULL UNIQUE,
    compound TEXT NOT NULL CHECK(compound IN ('Soft', 'Medium', 'Hard', 'Wet')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    track_layout_id INTEGER NOT NULL,
    test_date DATE NOT NULL,
    weather_conditions TEXT NOT NULL,
    notes TEXT,
    status TEXT NOT NULL CHECK(status IN ('COMPLETED', 'FAILED', 'MODIFIED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (season_id) REFERENCES Season(id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id),
    FOREIGN KEY (track_layout_id) REFERENCES TrackLayout(id)
);

CREATE TABLE Run (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    tire_set_id INTEGER NOT NULL,
    setup_id INTEGER NOT NULL,
    run_number INTEGER NOT NULL,
    run_type TEXT NOT NULL CHECK(run_type IN ('PLANNED', 'ACTUAL')), --Le ho scritte in inglese come erano scritte nel README.md
    asphalt_temp_c REAL NOT NULL,
    ambient_temp_c REAL NOT NULL,
    planned_laps INTEGER NOT NULL,
    completed_laps INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES Test(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES Driver(id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id),
    FOREIGN KEY (tire_set_id) REFERENCES TireSet(id),
    FOREIGN KEY (setup_id) REFERENCES Setup(id)
);

CREATE TABLE Lap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    lap_number INTEGER NOT NULL,
    lap_time_ms REAL NOT NULL CHECK(lap_time_ms > 0),
    penalty_seconds REAL DEFAULT 0.0 CHECK(penalty_seconds >= 0.0),
    is_valid INTEGER DEFAULT 1 CHECK(is_valid IN (0, 1)), -- in SQLite non c'è boolean
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES Run(id) ON DELETE CASCADE
);

CREATE TABLE TireMeasurement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    corner TEXT NOT NULL CHECK(corner IN ('FL', 'FR', 'RL', 'RR')),
    measurement_type TEXT NOT NULL CHECK(measurement_type IN ('PRE_RUN', 'POST_RUN')),
    pressure_bar REAL NOT NULL CHECK(pressure_bar > 0),
    temp_inner_c REAL NOT NULL,
    temp_center_c REAL NOT NULL,
    temp_outer_c REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES Run(id) ON DELETE CASCADE
);

CREATE TABLE TelemetryLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES Run(id) ON DELETE CASCADE
);

