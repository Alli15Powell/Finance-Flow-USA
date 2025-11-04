import sqlite3

def seed_database():
    conn = sqlite3.connect("data/financeflow.db")
    c = conn.cursor()

    # Clear any old data (optional)
    c.execute("DELETE FROM investments")
    c.execute("DELETE FROM projects")

    # Insert sample investments
    investments = [
        ("Alabama", "Mobile", "Port Expansion", "Logistics", 50, 200, 2022, 2025),
        ("Texas", "Houston", "Tech Park", "Technology", 120, 800, 2021, 2024),
        ("California", "Los Angeles", "Green Energy Hub", "Energy", 200, 1000, 2023, 2026),
        ("New York", "Buffalo", "Manufacturing Center", "Industrial", 95, 450, 2021, 2025),
        ("Florida", "Miami", "Innovation Campus", "Business", 150, 600, 2023, 2025),
    ]
    c.executemany("""
        INSERT INTO investments (state, county, project_name, industry, funding, jobs_created, start_year, end_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, investments)

    # Insert sample projects
    projects = [
        ("Port Expansion", "Alabama", "Mobile", "2022-01-01", "2025-01-01", 0),
        ("Tech Park", "Texas", "Houston", "2021-03-01", "2024-06-01", 1),
        ("Green Energy Hub", "California", "Los Angeles", "2023-02-15", "2026-05-15", 0),
        ("Manufacturing Center", "New York", "Buffalo", "2021-05-01", "2025-05-01", 1),
        ("Innovation Campus", "Florida", "Miami", "2023-04-01", "2025-12-01", 0),
    ]
    c.executemany("""
        INSERT INTO projects (project_name, state, county, start_date, end_date, completed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()
    print("✅ Database successfully seeded with example data.")

if __name__ == "__main__":
    seed_database()
