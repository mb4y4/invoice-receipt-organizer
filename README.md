# Invoice & Receipt Organizer 🧾

This project automates organising invoices and receipts:
- Watches the `invoices/` folder for new PDFs.
- Extracts vendor, amount, and date from the PDF text.
- Renames and moves the invoice into `organized/`.
- Logs the details into `expenses.csv`.

---

## 🚀 How to Run
1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/invoice-receipt-organizer.git
   cd invoice-receipt-organizer
   
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Run the Script
   ```bash
   python main.py
   
4. Drop any PDF invoices into the `invoices/` folder.
They will be renamed, moved to `organized/`, and logged in `expenses.csv`

