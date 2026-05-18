# Generates and writes sales invoices and restock notes
import os
# Utility functions for generating invoice ID and current date/time
from utils import generate_invoice_id, get_current_datetime

INVOICE_DIR = "invoices"

def _ensure_invoice_dir():
    """Creates the invoices directory if it does not exist."""
    if not os.path.exists(INVOICE_DIR):
        os.makedirs(INVOICE_DIR)
def generate_sales_invoice(customer_name, cart_items, invoice_id=None):
    """
    Generates a sales invoice .txt file for a customer purchase.

    Parameters:
        customer_name (str): Name of the customer.
        cart_items (list): List of dicts with keys:
            medicine_name, brand, unit_type, quantity,
            unit_rate, discount, line_total.
        invoice_id (str): Optional custom ID; auto-generated if None.

    Returns:
        filepath (str): Path to the created invoice file.
    """
    _ensure_invoice_dir()

    if not invoice_id:
        invoice_id = generate_invoice_id("SALE")

    filepath = os.path.join(INVOICE_DIR, f"{invoice_id}.txt")
    date_time = get_current_datetime()

    grand_total = sum(item["line_total"] for item in cart_items)
    total_discount = sum(item["discount"] for item in cart_items)

    lines = []
    lines.append("=" * 100
    )
    lines.append("          MEDSTORE PVT. LTD.")
    lines.append("       MedStore Wholesale Medicine Distributor")
    lines.append("=" * 100
    )
    lines.append(f"  Invoice No : {invoice_id}")
    lines.append(f"  Date/Time  : {date_time}")
    lines.append(f"  Customer   : {customer_name}")
    lines.append("-" * 100
    )
    lines.append(f"  {'Medicine':<20} {'Brand':<15} {'Unit':<7} {'Qty':>4} {'Rate':>8} {'Disc':>8} {'Total':>9}")
    lines.append("-" * 100
    )
    for item in cart_items:
        lines.append(
            f"  {item['medicine_name']:<20} {item['brand']:<15} {item['unit_type']:<7}"
            f" {item['quantity']:>4} {item['unit_rate']:>8.2f}"
            f" {item['discount']:>8.2f} {item['line_total']:>9.2f}"
        )

    lines.append("-" * 100
    )
    lines.append(f"  {'Total Discount:':<35} Rs. {total_discount:>9.2f}")
    lines.append(f"  {'GRAND TOTAL:':<35} Rs. {grand_total:>9.2f}")
    lines.append("=" * 100
    )
    lines.append("       Thank you for your purchase!")
    lines.append("=" * 100
    )
    content = "\n".join(lines) + "\n"

    try:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"\n  [OK] Sales invoice saved: {filepath}")
    except IOError as e:
        print(f"\n  [ERR] Could not write invoice: {e}")

    return filepath
def generate_restock_note(supplier_name, restock_items, invoice_id=None):
    """
    Generates a restock/purchase note .txt file.

    Parameters:
        supplier_name (str): Name of the supplier/vendor.
        restock_items (list): List of dicts with keys:
            medicine_name, brand, unit_type, quantity,
            tablets_added, unit_rate, line_total.
        invoice_id (str): Optional custom ID; auto-generated if None.

    Returns:
        filepath (str): Path to the created note file.
    """
    _ensure_invoice_dir()

    if not invoice_id:
        invoice_id = generate_invoice_id("RESTOCK")

    filepath = os.path.join(INVOICE_DIR, f"{invoice_id}.txt")
    date_time = get_current_datetime()

    grand_total = sum(item["line_total"] for item in restock_items)

    lines = []
    lines.append("=" * 100
    )
    lines.append("          MEDSTORE PVT. LTD.")
    lines.append("         Stock Purchase / Restock Note")
    lines.append("=" * 100
    )
    lines.append(f"  Note No    : {invoice_id}")
    lines.append(f"  Date/Time  : {date_time}")
    lines.append(f"  Supplier   : {supplier_name}")
    lines.append("-" * 100
    )
    lines.append(f"  {'Medicine':<20} {'Brand':<15} {'Unit':<7} {'Qty':>4} {'Rate':>8} {'Total':>9}  {'Info':<15}")
    lines.append("-" * 100
    )

    for item in restock_items:
        added_info = f"(+{item['tablets_added']} tabs)"
        lines.append(
            f"  {item['medicine_name']:<20} {item['brand']:<15} {item['unit_type']:<7}"
            f" {item['quantity']:>4} {item['unit_rate']:>8.2f}"
            f" {item['line_total']:>9.2f}  {added_info:<15}"
        )

    lines.append("-" * 100
    )
    lines.append(f"  {'GRAND TOTAL:':<35} Rs. {grand_total:>9.2f}")
    lines.append("=" * 100
    )
    lines.append("      Stock updated successfully.")
    lines.append("=" * 100
    )

    content = "\n".join(lines) + "\n"

    try:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"\n  [OK] Restock note saved: {filepath}")
    except IOError as e:
        print(f"\n  [ERROR] Could not write restock note: {e}")

    return filepath
