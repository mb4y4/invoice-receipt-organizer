import os
import re
import shutil
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfReader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

INVOICE_DIR = "invoices"
ORG_DIR = "organized"
CSV_FILE = "expenses.csv"

# Ensure folders exist
os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(ORG_DIR, exist_ok=True)

def extract_invoice_data(file_path):
    """Extract vendor, amount, and date from PDF text (simple regex-based)."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Example regex patterns (adjust to your invoices)
        vendor = re.search(r"(?i)(Invoice from|Vendor|Company):?\s*(.*)", text)
        amount = re.search(r"(\d+[.,]?\d*)\s*(USD|KES|EUR)?", text)
        date = re.search(r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", text)

        vendor_name = vendor.group(2).strip() if vendor else "UnknownVendor"
        amount_value = amount.group(1) if amount else "0"
        currency = amount.group(2) if amount and amount.group(2) else ""
        invoice_date = date.group(1) if date else datetime.now().strftime("%Y-%m-%d")

        return vendor_name, amount_value, currency, invoice_date

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "Unknown", "0", "", datetime.now().strftime("%Y-%m-%d")

def process_invoice(file_path):
    """Process a single invoice and move it to organized folder."""
    vendor, amount, currency, date = extract_invoice_data(file_path)

    # Format new filename
    filename = f"{vendor}_{amount}{currency}_{date}.pdf".replace(" ", "_")
    new_path = os.path.join(ORG_DIR, filename)

    shutil.move(file_path, new_path)

    # Save record to CSV
    df = pd.DataFrame([[vendor, amount, currency, date, filename]],
                      columns=["Vendor", "Amount", "Currency", "Date", "File"])
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print(f"Processed: {filename}")

class InvoiceHandler(FileSystemEventHandler):
    """Watchdog event handler for new invoices."""
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            process_invoice(event.src_path)

def watch_folder():
    event_handler = InvoiceHandler()
    observer = Observer()
    observer.schedule(event_handler, INVOICE_DIR, recursive=False)
    observer.start()
    print(f"Watching folder: {INVOICE_DIR} for new invoices... Press CTRL+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_folder()
