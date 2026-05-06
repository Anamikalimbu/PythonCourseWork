# Handles the full restock workflow: select medicines, enter quantities, update stock

from display import display_all_medicines, display_cart, print_error, print_info
from inventory import update_stock_after_restock
from invoice import generate_restock_note
from utils import (
    get_valid_int, get_valid_float, get_valid_string,
    get_yes_no, get_unit_choice, strips_to_tablets
)

def build_restock_list(medicines):
    """
    Interactive loop to build a restock order.
    Returns a list of restock_item dicts.
    """
    restock_items = []

    print("\n  --- Add medicines to restock. Enter '0' to finish. ---")
    print("  --- Enter '-1' to ADD A NEW MEDICINE. ---")

    while True:
        display_all_medicines(medicines)

        choice = get_valid_int(
            "\n  Enter medicine number to restock (0 = done, -1 = add new): ",
            min_val=-1,
            max_val=len(medicines)
        )

        if choice == 0:
            break

        if choice == -1:
            print("\n  --- Add New Medicine ---")
            name = get_valid_string("  Medicine Name: ")
            brand = get_valid_string("  Brand: ")
            rate_tablet = get_valid_float("  Selling rate per tablet (Rs.): ", min_val=0.0)
            rate_strip = get_valid_float("  Selling rate per strip (Rs.): ", min_val=0.0)
            tablets_strip = get_valid_int("  Tablets per strip: ", min_val=1)
            
            new_med = {
                "name": name,
                "brand": brand,
                "qty_tablets": 0,
                "rate_tablet": rate_tablet,
                "rate_strip": rate_strip,
                "tablets_strip": tablets_strip,
            }
            medicines.append(new_med)
            
            med_index = len(medicines) - 1
            med = medicines[med_index]
            print_info(f"Added new medicine '{name}' to list. Now please enter restock quantity.")
        else:
            med_index = choice - 1
            med = medicines[med_index]

        # Choose unit for restock
        unit = get_unit_choice()

        if unit == "tablet":
            qty = get_valid_int("  Enter number of tablets to restock: ", min_val=1)
            unit_rate = get_valid_float(
                f"  Purchase rate per tablet (current list: Rs.{med['rate_tablet']:.2f}): ",
                min_val=0.0
            )
            tablets_added = qty
            line_total = round(qty * unit_rate, 2)

        else:  # strip
            qty = get_valid_int("  Enter number of strips to restock: ", min_val=1)
            unit_rate = get_valid_float(
                f"  Purchase rate per strip (current list: Rs.{med['rate_strip']:.2f}): ",
                min_val=0.0
            )
            tablets_added = strips_to_tablets(qty, med["tablets_strip"])
            line_total = round(qty * unit_rate, 2)

        restock_item = {
            "med_index":    med_index,
            "medicine_name": med["name"],
            "brand":        med["brand"],
            "unit_type":    unit,
            "quantity":     qty,
            "unit_rate":    unit_rate,
            "tablets_added": tablets_added,
            "line_total":   line_total,
        }
        restock_items.append(restock_item)
        print_info(
            f"Added to restock: {med['name']} x{qty} {unit}(s)"
            f"  (+{tablets_added} tablets)  =>  Rs.{line_total:.2f}"
        )

    return restock_items


def process_restock(medicines):
    print("\n  === NEW RESTOCK TRANSACTION ===")

    supplier_name = get_valid_string("  Supplier / Vendor Name: ")

    restock_items = build_restock_list(medicines)

    if not restock_items:
        print_info("No items selected. Restock cancelled.")
        return

    # Display summary
    print("\n  --- Restock Summary ---")
    grand_total = 0.0
    for item in restock_items:
        grand_total += item["line_total"]
        print(
            f"  {item['medicine_name']:<25} {item['quantity']} {item['unit_type']}(s)"
            f"  +{item['tablets_added']} tabs  Rs.{item['line_total']:.2f}"
        )
    print(f"  {'TOTAL':<40} Rs.{grand_total:.2f}")

    confirmed = get_yes_no("  Confirm this restock?")
    if not confirmed:
        print_info("Restock cancelled.")
        return

    # Update inventory
    for item in restock_items:
        update_stock_after_restock(medicines, item["med_index"], item["tablets_added"])

    # Generate note
    generate_restock_note(supplier_name, restock_items)
    print_info("Stock updated. Restock completed successfully.")