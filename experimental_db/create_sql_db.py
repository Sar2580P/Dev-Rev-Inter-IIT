import sqlite3
import random

# Connect to SQLite database (create a new one if it doesn't exist)
conn = sqlite3.connect('experimental_db/sample_database.db')
cursor = conn.cursor()

# Create the student table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        sprint_id INT,
        applies_to_part TEXT,
        created_by TEXT,
        issue_priority TEXT,
        issue_rev_orgs TEXT,
        owned_by TEXT,
        stage_name TEXT,
        ticket_needs_response BOOLEAN,
        ticket_rev_org TEXT,
        ticket_severity TEXT,
        ticket_source_channel TEXT,
        type TEXT,
        work_id VARCHAR(255)
    )
''')

# Insert sample data into the student table (for 100 rows)
for _ in range(100):
    sample_row = {
        'sprint_id': random.randint(100, 999),
        'applies_to_part': f'"FEAT-{random.randint(100, 999)}"',
        'created_by': f"DEVU-{random.randint(100, 999)}",
        'issue_priority': f"p{random.randint(0, 3)}",
        'issue_rev_orgs': f"REV-{random.randint(100, 999)}",
        'owned_by': random.choice(['Aa' , 'Bb' , 'Cc' , 'Dd' , 'Ee' , 'Ff' , 'Gg']),
        'stage_name': f"triage-{random.randint(1, 10)}",
        'ticket_needs_response': random.choice([True, False]),
        'ticket_rev_org': f"REV-{random.randint(100, 999)}",
        'ticket_severity': random.choice(["blocker" , "high" , "low" , "medium"]),
        'ticket_source_channel': f"slack",
        'type': f"issue",
        'work_id': f"don:core:dvrv-us-1:devo/0:issue/{random.randint(1, 100)}"
    }

    cursor.execute('''
        INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sample_row['sprint_id'],
        sample_row['applies_to_part'],
        sample_row['created_by'],
        sample_row['issue_priority'],
        sample_row['issue_rev_orgs'],
        sample_row['owned_by'],
        sample_row['stage_name'],
        sample_row['ticket_needs_response'],
        sample_row['ticket_rev_org'],
        sample_row['ticket_severity'],
        sample_row['ticket_source_channel'],
        sample_row['type'],
        sample_row['work_id']
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()