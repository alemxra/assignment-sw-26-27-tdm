from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
import sqlite3

app = FastAPI(
    title="Race UP - Test Data Manager API",
    description="Backend API per la consultazione e l'analisi dei dati di test Formula Student.",
    version="1.0.0"
)

DB_PATH = "tdm.db"

def get_db_connection():
    """Crea una connessione a SQLite configurata per restituire dizionari."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Consente l'accesso alle colonne per nome chiave
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Race UP Test Data Manager (TDM)",
        "docs_url": "http://localhost:8000/docs"
    }

# 1. QUERY STORICA MULTI-FILTRO (Driver, Compound, Temp Asfalto)
@app.get("/runs", summary="Recupera le run con filtri storici avanzati")
def get_runs(
    driver_name: Optional[str] = Query(None, description="Nome del pilota (es. Mario Rossi)"),
    compound: Optional[str] = Query(None, description="Mescola gomme (es. Soft, Medium)"),
    min_asphalt_temp: Optional[float] = Query(None, description="Temp minima asfalto in °C"),
    max_asphalt_temp: Optional[float] = Query(None, description="Temp massima asfalto in °C")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            r.id AS run_id,
            r.run_number,
            r.run_type,
            t.test_date,
            d.name AS driver_name,
            v.name AS vehicle_name,
            ts.compound AS tire_compound,
            r.asphalt_temp_c,
            r.ambient_temp_c,
            r.completed_laps
        FROM Run r
        JOIN Driver d ON r.driver_id = d.id
        JOIN Vehicle v ON r.vehicle_id = v.id
        JOIN TireSet ts ON r.tire_set_id = ts.id
        JOIN Test t ON r.test_id = t.id
        WHERE 1=1
    """
    params = []

    if driver_name:
        query += " AND d.name LIKE ?"
        params.append(f"%{driver_name}%")
    if compound:
        query += " AND ts.compound = ?"
        params.append(compound)
    if min_asphalt_temp is not None:
        query += " AND r.asphalt_temp_c >= ?"
        params.append(min_asphalt_temp)
    if max_asphalt_temp is not None:
        query += " AND r.asphalt_temp_c <= ?"
        params.append(max_asphalt_temp)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# 2. CALCOLO AUTOMATICO DEL CHILOMETRAGGIO (MILEAGE)
@app.get("/mileage/drivers", summary="Calcolo chilometraggio totale per ciascun pilota")
def get_driver_mileage():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            d.id AS driver_id,
            d.name AS driver_name,
            COUNT(l.id) AS total_laps_completed,
            ROUND((COUNT(l.id) * tl.length_meters) / 1000.0, 2) AS total_mileage_km
        FROM Driver d
        JOIN Run r ON r.driver_id = d.id
        JOIN Lap l ON l.run_id = r.id
        JOIN Test t ON r.test_id = t.id
        JOIN TrackLayout tl ON t.track_layout_id = tl.id
        WHERE l.is_valid = 1
        GROUP BY d.id, d.name, tl.length_meters;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# 3. DERIVAZIONE AUTOMATICA DEL BEST LAP PER UNA SPECIFICA RUN
@app.get("/runs/{run_id}/best-lap", summary="Estrae il miglior tempo sul giro di una specifica Run")
def get_best_lap(run_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            r.id AS run_id,
            r.run_number,
            d.name AS driver_name,
            l.lap_number,
            MIN(l.lap_time_ms) AS best_lap_time_ms,
            ROUND(MIN(l.lap_time_ms) / 1000.0, 3) AS best_lap_time_seconds
        FROM Run r
        JOIN Driver d ON r.driver_id = d.id
        JOIN Lap l ON l.run_id = r.id
        WHERE r.id = ? AND l.is_valid = 1
        GROUP BY r.id, r.run_number, d.name, l.lap_number
        ORDER BY best_lap_time_ms ASC
        LIMIT 1;
    """
    cursor.execute(query, (run_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Nessun giro valido trovato per questa Run.")

    return dict(row)
