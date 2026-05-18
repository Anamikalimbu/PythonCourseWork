# Handles the full sales workflow: build cart, compute totals, update stock

from display import display_all_medicines, display_search_results, display_cart, print_error, print_info
from inventory import find_medicine, update_stock_after_sale
from invoice import generate_sales_invoice
from utils import (
    calculate_tablet_discount, get_valid_int, get_valid_string, get_yes_no,
    get_unit_choice, calculate_strip_discount,
    strips_to_tablets
)


def build_cart(medicines):
    """
    Interactive loop that builds a shopping cart.
    Returns a list of cart_item dicts, or empty list if cancelled.
    """
    cart = []

    print("\n  --- Add items to cart. Enter '0' for medicine number to finish. ---")
    first_time = True 
    while True:
        if first_time:
            display_all_medicines(medicines)  
            first_time = False   

        choice = get_valid_int(
            "\n  Enter medicine number to add (0 = done): ",
            min_val=0,
            max_val=len(medicines)
        )

        if choice == 0:
            break

        med_index = choice - 1
        med = medicines[med_index]

        # Choose unit
        unit = get_unit_choice()

        if unit == "tablet":
            max_qty = med["qty_tablets"]
            if max_qty == 0:
                print_error(f"'{med['name']}' is out of stock.")
                continue

            qty = get_valid_int(
                f"  Enter number of tablets (max {max_qty}): ",
                min_val=1, max_val=max_qty
            )
            subtotal = qty * med["rate_tablet"]
            discount, line_total = calculate_tablet_discount(subtotal, qty)
            unit_rate = med["rate_tablet"]
            tablets_sold = strips_to_tablets(qty, med["tablets_strip"])


        else:  # strip
            max_strips = med["qty_tablets"] // med["tablets_strip"]
            if max_strips == 0:
                print_error(f"'{med['name']}' has no complete strips in stock.")
                continue

            qty = get_valid_int(
                f"  Enter number of strips (max {max_strips}): ",
                min_val=1, max_val=max_strips
            )
            subtotal = qty * med["rate_strip"]
            discount, line_total = calculate_strip_discount(subtotal, qty)
            unit_rate = med["rate_strip"]
            tablets_sold = strips_to_tablets(qty, med["tablets_strip"])

        cart_item = {
            "med_index":    med_index,
            "medicine_name": med["name"],
            "brand":        med["brand"],
            "unit_type":    unit,
            "quantity":     qty,
            "unit_rate":    unit_rate,
            "discount":     discount,
            "line_total":   line_total,
            "tablets_sold": tablets_sold,
        }
        cart.append(cart_item)
        print_info(f"Added: {med['name']} x{qty} {unit}(s)  =>  Rs.{line_total:.2f}")

    return cart


def process_sale(medicines):
    print("\n  === NEW SALE TRANSACTION ===")

    customer_name = get_valid_string("  Customer Name: ")

    cart = build_cart(medicines)

    if not cart:
        print_info("No items in cart. Sale cancelled.")
        return

    display_cart(cart)

    confirmed = get_yes_no("  Confirm this sale?")
    if not confirmed:
        print_info("Sale cancelled.")
        return

    # Update stock for each cart item
    for item in cart:
        success = update_stock_after_sale(
            medicines, item["med_index"], item["tablets_sold"]
        )
        if not success:
            print_error(
                f"Stock conflict for '{item['medicine_name']}'. "
                "Sale aborted. Please re-check inventory."
            )
            return

    # Generate invoice
    generate_sales_invoice(customer_name, cart)
    print_info("Stock updated. Sale completed successfully.")
