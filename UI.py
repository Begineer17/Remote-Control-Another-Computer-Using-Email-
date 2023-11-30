import tkinter as tk
from tkinter import ttk
import json

class Email:
    def __init__(self, sender, subject, snippet, read):
        self.sender = sender
        self.subject = subject
        self.snippet = snippet
        self.read = read

def create_email_frame(email, frame, row):
    font_style = "normal"
    if not email.read:
        font_style = "bold"
    sender_label = ttk.Label(frame, text=email.sender, font=("Arial", 12, font_style), anchor="w", foreground="#1a0dab")
    sender_label.grid(row=row, column=0, sticky="w", pady=(0, 5))
    subject_label = ttk.Label(frame, text=email.subject, font=("Arial", 11, font_style), anchor="w")
    subject_label.grid(row=row + 1, column=0, sticky="w", pady=(0, 5))
    snippet_label = ttk.Label(frame, text=email.snippet, font=("Arial", 10, font_style), anchor="w", wraplength=600)
    snippet_label.grid(row=row + 2, column=0, sticky="w", pady=(0, 5))
    line = ttk.Separator(frame, orient="horizontal")
    line.grid(row=row + 3, column=0, sticky="ew", pady=(5, 0))

def extract_email_address(sender):
    # Assuming the email address is within angle brackets
    start = sender.find('<')
    end = sender.find('>')
    if start != -1 and end != -1:
        return sender[start + 1:end]
    else:
        return sender

def save_emails_to_json(emails, file_path):
    with open(file_path, 'w') as file:
        data = [
            {"sender": extract_email_address(email.sender), "subject": email.subject, "snippet": email.snippet, "read": email.read}
            for email in emails
        ]
        json.dump(data, file, ensure_ascii=False, default=str)

def load_emails_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if not data:
            return []
        emails = [Email(email["sender"], email["subject"], email["snippet"], email["read"]) for email in data]
        return emails

def search_emails(keyword, emails, inner_frame):
    for widget in inner_frame.winfo_children():
        widget.destroy()
    filtered_emails = [email for email in emails if keyword.lower() in email.sender.lower() or keyword.lower() in email.subject.lower() or keyword.lower() in email.snippet.lower()]
    for i, email in enumerate(filtered_emails):
        create_email_frame(email, inner_frame, row=i * 4)

def main():
    emails = load_emails_from_json('email.json')

    root = tk.Tk()
    root.title("Inbox - Google Email")

    search_frame = ttk.Frame(root)
    search_frame.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=0, padx=5)
    search_button = ttk.Button(search_frame, text="Search", command=lambda: search_emails(search_entry.get(), inner_frame))
    search_button.grid(row=0, column=1, padx=5)

    email_frame = ttk.Frame(root, borderwidth=2, relief="groove")
    email_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    canvas = tk.Canvas(email_frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(email_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    for i, email in enumerate(emails):
        create_email_frame(email, inner_frame, row=i * 4)

    horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    horizontal_scrollbar.grid(row=2, column=0, sticky="ew")

    canvas.configure(xscrollcommand=horizontal_scrollbar.set)
    ttk.Label(root).grid(row=3, column=0, pady=(10, 0))

    root.mainloop()

def extract_email_address(sender):
    # Assuming the email address is within angle brackets
    start = sender.find('<')
    end = sender.find('>')
    if start != -1 and end != -1:
        return sender[start + 1:end]
    else:
        return sender

def save_emails_to_json(emails, file_path):
    with open(file_path, 'w') as file:
        data = [
            {"sender": extract_email_address(email.sender), "subject": email.subject, "snippet": email.snippet, "read": email.read}
            for email in emails
        ]
        json.dump(data, file, ensure_ascii=False, default=str)

def load_emails_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:
                return []
            emails = [Email(email["sender"], email["subject"], email["snippet"], email["read"]) for email in data]
            return emails
    except:
        return []

if __name__ == '__main__':
    main()
