# Handles all screen output and menus

W = 120
DIVIDER  = "=" * W
THIN_DIV = "-" * W


def print_header(title):
    print()
    print(DIVIDER)
    print(title.center(W))
    print(DIVIDER)


def print_main_menu():
    print()
    print(DIVIDER)
    print("MedStore Pvt. Ltd.  --  Wholesale Management System".center(W))
    print(DIVIDER)
    print("  [1]  View All Medicines in Stock")
    print("  [2]  Sell Medicine   (Generate Sales Invoice)")
    print("  [3]  Restock Medicine  (Generate Restock Note)")
    print("  [4]  Search Medicine")
    print("  [0]  Exit")
    print(DIVIDER)


def display_all_medicines(medicines):
    if not medicines:
        print("\n  [!] No medicines currently in stock.")
        return

    print_header("Current Medicine Inventory")
    print(f"  {'#':<4}  {'Medicine Name':<25}  {'Brand':<20}  {'Tablets':>8}  {'Rate/Tab':>10}  {'Rate/Strip':>11}  {'Tab/Strip':>9}")
    print(THIN_DIV)

    for i, med in enumerate(medicines, start=1):
        print(
            f"  {i:<4}  {med['name']:<25}  {med['brand']:<20}"
            f"  {med['qty_tablets']:>8}  {med['rate_tablet']:>10.2f}"
            f"  {med['rate_strip']:>11.2f}  {med['tablets_strip']:>9}"
        )

    print(DIVIDER)
    print(f"  Total medicines listed: {len(medicines)}")


def display_search_results(results):
    if not results:
        print("\n  [!] No medicines found matching your search.")
        return

    print_header("Search Results")

    for idx, med in results:
        strips = med["qty_tablets"] // med["tablets_strip"]
        print(f"  [{idx + 1}]  {med['name']}  ({med['brand']})")
        print(THIN_DIV)
        print(f"  {'Tablets in stock:':<22} {med['qty_tablets']}  (~{strips} strips)")
        print(f"  {'Rate per tablet:':<22} Rs.{med['rate_tablet']:.2f}")
        print(f"  {'Rate per strip:':<22} Rs.{med['rate_strip']:.2f}")
        print(f"  {'Tablets per strip:':<22} {med['tablets_strip']}")
        print(DIVIDER)


def display_cart(cart_items):
    if not cart_items:
        print("\n  (Cart is empty)")
        return

    print_header("Current Cart")
    print(f"  {'#':<4}  {'Medicine':<25}  {'Brand':<15}  {'Unit':<7}  {'Qty':>4}  {'Rate':>10}  {'Discount':>10}  {'Total':>10}")
    print(THIN_DIV)

    grand_total    = 0.0
    total_discount = 0.0

    for i, item in enumerate(cart_items, start=1):
        disc = item["discount"]
        lt   = item["line_total"]
        grand_total    += lt
        total_discount += disc
        disc_str = f"Rs.{disc:.2f}" if disc > 0 else "--"
        print(
            f"  {i:<4}  {item['medicine_name']:<25}  {item['brand']:<15}"
            f"  {item['unit_type']:<7}  {item['quantity']:>4}"
            f"  {item['unit_rate']:>10.2f}  {disc_str:>10}  Rs.{lt:>8.2f}"
        )

    print(THIN_DIV)
    print(f"  {'Total Discount:':<60} Rs.{total_discount:>8.2f}")
    print(f"  {'GRAND TOTAL:':<60} Rs.{grand_total:>8.2f}")
    print(DIVIDER)


def print_success(message):
    print(f"\n  [OK]  {message}")

def print_error(message):
    print(f"\n  [ERR] {message}")

def print_info(message):
    print(f"\n  [>>]  {message}")