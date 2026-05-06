# Handles all screen output and menus

DIVIDER = "=" * 60
THIN_DIV = "-" * 60

def print_header(title):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def print_main_menu():
    print_header("MedStore Pvt. Ltd. — MedStore Wholesale Management System")
    print("  [1]  View All Medicines in Stock")
    print("  [2]  Sell Medicine (Generate Sales Invoice)")
    print("  [3]  Restock Medicine (Generate Restock Note)")
    print("  [4]  Search Medicine")
    print("  [0]  Exit")
    print(THIN_DIV)


def display_all_medicines(medicines):
    """Prints the full inventory in a formatted table."""
    if not medicines:
        print("\n  [!] No medicines currently in stock.")
        return

    print_header("Current Medicine Inventory")
    header = (
        f"  {'#':<4} {'Medicine Name':<25} {'Brand':<20}"
        f" {'Stock':>8} {'Rate/Tab':>10} {'Rate/Strip':>12} {'Tab/Strip':>10}"
    )
    print(header)
    print(THIN_DIV)

    for i, med in enumerate(medicines, start=1):
        print(
            f"  {i:<4} {med['name']:<25} {med['brand']:<20}"
            f" {med['qty_tablets']:>8} {med['rate_tablet']:>10.2f}"
            f" {med['rate_strip']:>12.2f} {med['tablets_strip']:>10}"
        )
    print(THIN_DIV)
    print(f"  Total medicines: {len(medicines)}")


def display_search_results(results):
    """Displays search results."""
    if not results:
        print("\n  [!] No medicines found matching your search.")
        return
    print_header("Search Results")
    for idx, med in results:
        strips = med["qty_tablets"] // med["tablets_strip"]
        print(f"  [{idx + 1}] {med['name']} ({med['brand']})")
        print(
            f"       Stock: {med['qty_tablets']} tablets  |  "
            f"~{strips} strips  |  "
            f"Rate/tab: Rs.{med['rate_tablet']:.2f}  |  "
            f"Rate/strip: Rs.{med['rate_strip']:.2f}"
        )
    print(THIN_DIV)

def display_cart(cart_items):
    """Displays the current sales cart."""
    if not cart_items:
        print("\n  (Cart is empty)")
        return
    print_header("Current Cart")
    total = 0.0
    for item in cart_items:
        line_total = item["line_total"]
        total += line_total
        discount_str = f"  [Discount: Rs.{item['discount']:.2f}]" if item["discount"] > 0 else ""
        print(f"  - {item['medicine_name']} ({item['brand']})")
        print(
            f"    {item['quantity']} {item['unit_type']}(s) "
            f"@ Rs.{item['unit_rate']:.2f}{discount_str}  =>  Rs.{line_total:.2f}"
        )
    print(THIN_DIV)
    print(f"  Cart Total: Rs.{total:.2f}")
    print(THIN_DIV)

def print_success(message):
    print(f"\n  [OK] {message}")

def print_error(message):
    print(f"\n  [ERR] {message}")

def print_info(message):
    print(f"\n {message}")
