# Input validation, date/time helpers, and general utilities

from datetime import datetime

def get_current_datetime():
    """Returns current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date():
    """Returns current date as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d")

def generate_invoice_id(prefix="INV"):
    """
    Generates a unique invoice ID using timestamp.
    e.g., INV_20260420_143512
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"

def get_valid_int(prompt, min_val=None, max_val=None):
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  [!] Input cannot be empty. Please try again.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print(f"  [!] '{raw}' is not a valid integer. Please enter a whole number.")
            continue
        if min_val is not None and value < min_val:
            print(f"  [!] Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"  [!] Value must be at most {max_val}.")
            continue
        return value


def get_valid_float(prompt, min_val=None):
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  [!] Input cannot be empty. Please try again.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print(f"  [!] '{raw}' is not a valid number.")
            continue
        if min_val is not None and value < min_val:
            print(f"  [!] Value must be at least {min_val}.")
            continue
        return value


def get_valid_string(prompt, min_length=1):
    while True:
        raw = input(prompt).strip()
        if len(raw) < min_length:
            print(f"  [!] Input must be at least {min_length} character(s). Try again.")
            continue
        return raw


def get_yes_no(prompt):
    while True:
        raw = input(f"{prompt} (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  [!] Please enter 'y' for yes or 'n' for no.")


def get_unit_choice():
    while True:
        raw = input("  Unit type -- Enter [T] for Tablet or [S] for Strip: ").strip().upper()
        if raw == "T":
            return "tablet"
        if raw == "S":
            return "strip"
        print("  [!] Invalid choice. Enter T or S.")


def calculate_strip_discount(subtotal, num_strips):
    """
    Applied 5% discount if customer buys 2 or more strips of the same medicine.
    Returns (discount_amount, final_price).
    """
    if num_strips >= 2:
        discount = subtotal * 0.05
        return round(discount, 2), round(subtotal - discount, 2)
    return 0.0, round(subtotal, 2)

def calculate_tablet_discount(subtotal, num_tablets, threshold=20):
    """5% discount if customer buys 20 or more tablets."""
    if num_tablets >= threshold:
        discount = subtotal * 0.05
        return round(discount, 2), round(subtotal - discount, 2)
    return 0.0, round(subtotal, 2)

def tablets_to_strips(qty_tablets, tablets_per_strip):
    """Converts tablets count to number of complete strips."""
    return qty_tablets // tablets_per_strip


def strips_to_tablets(num_strips, tablets_per_strip):
    """Converts number of strips to equivalent tablets."""
    return num_strips * tablets_per_strip
