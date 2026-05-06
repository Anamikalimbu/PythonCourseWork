# Handles reading and writing the medicine inventory file

INVENTORY_FILE = "medicines.txt"

def load_inventory(filepath=INVENTORY_FILE):
    """
    Reads the inventory text file and returns a list of medicine dictionaries.
    Each line format: Name, Brand, Qty(tablets), Rate/tablet, Rate/strip, Tablets/strip
    """
    medicines = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 6:
                    print(f"[WARNING] Skipping malformed line: {line}")
                    continue
                try:
                    medicine = {
                        "name":           parts[0],
                        "brand":          parts[1],
                        "qty_tablets":    int(parts[2]),
                        "rate_tablet":    float(parts[3]),
                        "rate_strip":     float(parts[4]),
                        "tablets_strip":  int(parts[5]),
                    }
                    medicines.append(medicine)
                except ValueError as e:
                    print(f"[WARNING] Could not parse line '{line}': {e}")
    except FileNotFoundError:
        print(f"[ERROR] Inventory file '{filepath}' not found. Starting with empty inventory.")
    return medicines

def save_inventory(medicines, filepath=INVENTORY_FILE):
    """
    Writes the current inventory list back to the text file.
    """
    try:
        with open(filepath, "w") as f:
            for med in medicines:
                line = (
                    f"{med['name']}, "
                    f"{med['brand']}, "
                    f"{med['qty_tablets']}, "
                    f"{med['rate_tablet']}, "
                    f"{med['rate_strip']}, "
                    f"{med['tablets_strip']}\n"
                )
                f.write(line)
    except IOError as e:
        print(f"[ERROR] Could not save inventory: {e}")
def find_medicine(medicines, search_term):
    """
    Searches medicines list by name (case-insensitive partial match).
    Returns list of matching medicines with their indices.
    """
    results = []
    term = search_term.strip().lower()
    for idx, med in enumerate(medicines):
        if term in med["name"].lower() or term in med["brand"].lower():
            results.append((idx, med))
    return results
def update_stock_after_sale(medicines, index, qty_tablets_sold):
    """
    Reduces the stock of a medicine after a sale.
    Returns True if successful, False if not enough stock.
    """
    if medicines[index]["qty_tablets"] < qty_tablets_sold:
        return False
    medicines[index]["qty_tablets"] -= qty_tablets_sold
    return True
def update_stock_after_restock(medicines, index, qty_tablets_added):
    """
    Increases the stock of a medicine after a restock.
    """
    medicines[index]["qty_tablets"] += qty_tablets_added
def create_medicine_file_if_missing(filepath=INVENTORY_FILE):
    """
    Creates a sample inventory file if none exists.
    """
    import os
    if not os.path.exists(filepath):
        sample = (
            "Paracetamol 500mg, Lomus, 1200, 5, 45, 10\n"
            "Cetirizine 10mg, Quest, 800, 4, 35, 12\n"
            "Amoxicillin 500mg, Nepal Remedies, 500, 12, 110, 15\n"
            "Pantoprazole 40mg, Deurali-Janta, 600, 7, 60, 8\n"
            "ORS Sachet, Time Pharma, 300, 20, 180, 12\n"
        )
        with open(filepath, "w") as f:
            f.write(sample)
        print(f"[INFO] Sample inventory file '{filepath}' created.")
