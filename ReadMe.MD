An English-to-SQL interface with security confirmation logic and cloud-based audit logging.

Features
Natural Language Querying: Converts English requests into SQL using Groq and Llama 3.3.

Security Guardrails: Hard-coded 2-factor confirmation for any destructive database operations.

Cloud Logging: Synchronizes query history and security status to AWS DynamoDB.

GUI: Modern dark-mode interface for database interaction and log viewing.

Tech Stack
Python: Core logic and CustomTkinter UI.

SQLite: Local database storage.

AWS: DynamoDB for remote metadata logging.

Groq: AI inference engine.

Installation
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Create a .env file with your GROQ_API_KEY, AWS_ACCESS_KEY, and AWS_SECRET_KEY.

Run python main_gui.py.