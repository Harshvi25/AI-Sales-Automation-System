import sqlite3


def initialize_database():

    conn = sqlite3.connect("database/leads.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        phone TEXT,

        message TEXT,

        intent TEXT,

        budget TEXT,

        location TEXT,

        requirement TEXT,

        timeline TEXT,

        lead_score INTEGER,

        priority TEXT,

        escalation_required TEXT
    )
    """)

    conn.commit()

    conn.close()
    

def save_lead(
    phone,
    message,
    intent,
    extracted_data,
    lead_result,
    escalation
):

    conn = sqlite3.connect("database/leads.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leads (

        phone,
        message,
        intent,
        budget,
        location,
        requirement,
        timeline,
        lead_score,
        priority,
        escalation_required

    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        phone,
        message,
        intent,
        extracted_data.get("budget"),
        extracted_data.get("location"),
        extracted_data.get("requirement"),
        extracted_data.get("timeline"),
        lead_result.get("lead_score"),
        lead_result.get("priority"),
        str(escalation)
    ))

    conn.commit()

    conn.close()