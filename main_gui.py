import customtkinter as ctk
from nlp_to_sql import ask_ai, execute_query
from tkinter import messagebox, simpledialog

def handle_query():
    user_input = entry.get()
    sql = ask_ai(user_input)
    
    # 1. First attempt to run (Python will catch if it's destructive)
    results = execute_query(sql, user_input, confirmed=False)
    
    # 2. If Python blocked it, ask for 2FA
    if results == "CONFIRMATION_REQUIRED":
        check = simpledialog.askstring("Security Check", "Destructive command! Type 'YES' to confirm:", parent=app)
        if check == "YES":
            results = execute_query(sql, user_input, confirmed=True)
        else:
            results = "Operation Aborted."
    
    output_label.configure(text=f"SQL: {sql}\n\nResults: {results}")

# --- NEW: Fetch Logs Function ---
def fetch_logs():
    from nlp_to_sql import db
    table = db.Table('AI_Database_Manager')
    
    try:
        # Fetch data from AWS DynamoDB
        response = table.scan()
        items = response.get('Items', [])
        
        # Sort by timestamp (newest first)
        items.sort(key=lambda x: float(x.get('timestamp', 0)), reverse=True)
        
        log_text = "--- SECURITY AUDIT LOGS (AWS) ---\n"
        for item in items[:5]: # Show the last 5 logs
            # Flag errors or unauthorized attempts in the log text
            status = "⚠️ BLOCKED" if "ERROR" in item['generated_sql'].upper() else "✅ SAFE"
            log_text += f"{status} | Query: {item['user_query']}\n"
        
        output_label.configure(text=log_text)
    except Exception as e:
        output_label.configure(text=f"AWS Fetch Error: {e}")

app = ctk.CTk()
app.geometry("600x700") # Slightly taller to fit the audit logs
app.title("AI Database Manager")

label = ctk.CTkLabel(app, text="Ask your Database (English):")
label.pack(pady=10)

entry = ctk.CTkEntry(app, width=400)
entry.pack(pady=10)

btn = ctk.CTkButton(app, text="Run Query", command=handle_query)
btn.pack(pady=10)

# --- NEW: Audit Log Button ---
log_btn = ctk.CTkButton(app, text="View Security Audit (Cloud)", command=fetch_logs, fg_color="green")
log_btn.pack(pady=5)

output_label = ctk.CTkLabel(app, text="", wraplength=500)
output_label.pack(pady=20)

app.mainloop()