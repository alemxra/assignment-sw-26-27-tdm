# Thought Process

I'm currently at the second year of Computer Engineering. I have not yet taken courses like "Databases" or "Software Engineering", but I wanted to do this assignment anyway to demonstrate my commitment to this reality, Race Up.

First of all, I want to say that I am not an expert in anything, but those topics that I covered doing this assignment were something that I've heard at least sometimes in my life, so with some research and using Gemini AI to guide me, I tried to do as much as I could despite the limited time and university courses to study for.

This has highlighted something I have always noticed throughout my academic journey: I'm able to adapt very well when I'm doing something I enjoy, or when I'm doing it for a significant reason. 

If I google these "symptoms" I find that I am a "multipotentialite" person, but I think I am just a guy who wants to do something different and cool, and not only those boring school projects.

---

## Database Design Choices

### The Hierarchy
The relationship between entities follows the real-life workflow on track:
- A Season has multiple Tests.
- A Test happens at a specific track and contains multiple Runs.
- Each Run consists of multiple Laps.

### Why Setup and Tires are linked to the Run
I decided to link the car setup and tires to the `Run` table, and NOT to the individual `Lap`, because IN MY OPINION (I don't know how the things go in Race Up's races):
- In the real world, you cannot change mechanical settings or tires while the car is racing.
- For example, if the mechanics need to change wheels, the car must return to the pits. That means the current Run is over, and a new Run begins. (I think it works like that, correct me if I'm wrong)
- Linking Setup to each Lap could create duplicate data in the database.

### Avoiding a "Flat" Setup Table
Instead of creating a single table with a lot of columns for all suspension parameters, I split the setup into two tables:
1. `Setup`: Contains overall vehicle settings (power limit, driving mode, and the reason for the change).
2. `CornerSetup`: Contains specific settings for each of the four corners (FL, FR, RL, RR).
This makes the database clean, easy to read, and simple to expand in the future.

### Tire Measurements
Tire pressure and temperatures are stored in `TireMeasurement`. I added a field to distinguish between measurements taken before the run (PRE_RUN) and after the run (POST_RUN), tracking temperatures across three zones (inner, center, outer). 

### Automatic Mileage Calculation
Instead of manually typing the total distance run by a driver, the system calculates it automatically using SQL:
`Total Distance = Count of Valid Laps * Track Layout Length`
In this way we can avoid human calculation mistakes.

---

## Technology Choices

### SQLite
I chose SQLite because it requires no server installation or setup. Everything is stored in a single local `.db` file, which makes the project completely reproducible and easy to test on any computer. (I chose that also because I saw something about that when I was in High School) (I used AI: it was the fastest way to learn instead of watching flat youtube videos)

### Python Seed Script
To test if the database worked, I wrote a Python script using standard sqlite3. It populates the database with realistic sample data:
- It includes runs with different drivers, tires and track temperatures.
- This allowed me to test the multi-filter historical query and make sure it returned the correct runs.

### FastAPI for the Backend
I used FastAPI to expose simple API endpoints for the data:
- It connects directly to SQLite and returns data as JSON.
- It automatically creates an interactive documentation page at `/docs` (Swagger UI). This allows anyone testing the project to test queries and filters in their browser with buttons and inputs, without needing a separate frontend. 
(In the future, this UI can be obviously changed, but again, this was a fast way to do it)

---

I want to clarify that, even though I used AI for something like 'seed_data.py' or 'queries.sql', I didn't copy blindly, instead, I wanted to understand line by line the entire code and its meaning.

