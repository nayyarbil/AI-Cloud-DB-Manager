import os
import sqlite3
import boto3
from dotenv import load_dotenv
from groq import Groq
import time
import uuid

load_dotenv()
# Initialize the AWS DynamoDB Resource
db = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name='us-east-1'
)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

import time
import uuid

def log_to_aws(query, sql):
    # This connects to the table you created earlier
    table = db.Table('AI_Database_Manager')
    
    try:
        table.put_item(
            Item={
                'db_id': str(uuid.uuid4()), # Unique ID for the log
                'timestamp': str(time.time()),
                'user_query': query,
                'generated_sql': sql
            }
        )
        print("Log synced to AWS DynamoDB.")
    except Exception as e:
        print(f"AWS Sync Failed: {e}")

def get_schema():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema = cursor.fetchall()
    conn.close()
    return schema

def ask_ai(user_query):
    schema = get_schema()
    prompt = f"Schema: {schema}. Request: {user_query}. If destructive, return 'CONFIRMATION_REQUIRED'. Otherwise, return ONLY the raw SQL code. No markdown, no backticks, no text."
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    # This strip removes any accidental markdown backticks
    return completion.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()

def execute_query(sql, original_query, confirmed=False):
    destructive_keywords = ["DELETE", "DROP", "UPDATE", "INSERT", "CREATE"]
    if any(word in sql.upper() for word in destructive_keywords) and not confirmed:
        return "CONFIRMATION_REQUIRED"

    log_to_aws(original_query, sql)
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    try:
        # Use executescript to allow multiple SQL statements
        cursor.executescript(sql) 
        conn.commit()
        
        # Since script doesn't return rows easily, we manually check for SELECT
        if "SELECT" in sql.upper():
            cursor.execute(sql) # Re-run just the SELECT part if needed
            return cursor.fetchall()
        return "Success: Database updated."
    except Exception as e:
        return f"Database Error: {str(e)}"
    finally:
        conn.close()