
## How to Run the Database & API

Make sure you have Python 3.10+ and SQLite installed. Install the minimal dependencies:
```bash
pip install fastapi uvicorn
```

### Create Schema and Seed the Database
Run the following commands in the root directory of the project to create all tables and populate them with realistic test scenarios:

On Linux / macOS / Git Bash:
```bash
sqlite3 tdm.db < database/schema.sql
python seed_data.py
```

On Windows PowerShell:
```powershell
Get-Content database/schema.sql | sqlite3 tdm.db
python seed_data.py
```

### Start the FastAPI Backend
Launch the web server:
```bash
uvicorn main:app --reload
```

### Open the Interactive UI
Once running, open your web browser at:
[http://localhost:8000/docs](http://localhost:8000/docs)

Using the Swagger UI interface, you can test all data queries interactively:
- `GET /runs`**: Query test runs with dynamic filters (Driver name, tire compound, and track temperature range, e.g., 30°C–40°C).
- `GET /mileage/drivers`**: Calculate total accumulated mileage per driver dynamically.
- `GET /runs/{run_id}/best-lap`**: Extract the best lap time for any specific run.

### Step 4: Run Analytical SQL Queries Directly (CLI)
You can also execute the analytical queries directly against SQLite:
```bash
sqlite3 -header -column tdm.db < database/queries.sql
```

---