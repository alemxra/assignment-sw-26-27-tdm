-- Individuazione del giro più veloce valido per ogni Run eseguita
SELECT 
    r.id AS run_id,
    r.run_number,
    d.name AS driver_name,
    MIN(l.lap_time_ms) AS best_lap_ms,
    ROUND(MIN(l.lap_time_ms) / 1000.0, 3) AS best_lap_seconds
FROM Run r
JOIN Driver d ON r.driver_id = d.id
JOIN Lap l ON l.run_id = r.id
WHERE l.is_valid = 1
GROUP BY r.id, r.run_number, d.name;


-- Calcolo della distanza percorsa (giri completati * lunghezza tracciato in km) per ciascun Driver
SELECT 
    d.name AS driver_name,
    COUNT(l.id) AS total_laps_completed,
    tl.length_meters AS track_length_meters,
    ROUND((COUNT(l.id) * tl.length_meters) / 1000.0, 2) AS total_mileage_km
FROM Driver d
JOIN Run r ON r.driver_id = d.id
JOIN Lap l ON l.run_id = r.id
JOIN Test t ON r.test_id = t.id
JOIN TrackLayout tl ON t.track_layout_id = tl.id
WHERE l.is_valid = 1
GROUP BY d.id, d.name, tl.length_meters;


-- Mostra tutte le run del Driver 'Mario Rossi', con tire_compound 'Soft' e temperatura asfalto tra 30°C e 40°C
SELECT 
    r.id AS run_id,
    r.run_number,
    t.test_date,
    d.name AS driver_name,
    ts.compound AS tire_compound,
    r.asphalt_temp_c,
    r.completed_laps
FROM Run r
JOIN Driver d ON r.driver_id = d.id
JOIN TireSet ts ON r.tire_set_id = ts.id
JOIN Test t ON r.test_id = t.id
WHERE d.name = 'Mario Rossi'
  AND ts.compound = 'Soft'
  AND r.asphalt_temp_c BETWEEN 30.0 AND 40.0;


-- Codice quasi interamente scritto con Gemini