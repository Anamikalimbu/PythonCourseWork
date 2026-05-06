# Import core inventory functions (load, save, initialize file)
from inventory import load_inventory, save_inventory, create_medicine_file_if_missing
# Import display utilities for UI (menus, headers, messages)
from display import print_main_menu, print_header, print_error, print_info
# Handles selling workflow
from sales import process_sale
# Handles restocking workflow
from restock import process_restock
# Handles searching medicines
from search import search_medicine
from display import display_all_medicines

def run():
    """Main application loop."""
    # Ensure inventory file exists (creates sample if missing)
    create_medicine_file_if_missing()

    # Load inventory into memory
    medicines = load_inventory()

    if not medicines:
        print_info("Inventory is empty. Please add medicines to 'medicines.txt'.")

    while True:
        print_main_menu()

        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            # ---- View all medicines ----
            display_all_medicines(medicines)

        elif choice == "2":
            # ---- Sell medicines ----
            if not medicines:
                print_error("No medicines in inventory. Cannot process sale.")
            else:
                process_sale(medicines)
                # Save updated inventory after sale
                save_inventory(medicines)

        elif choice == "3":
            # ---- Restock medicines ----
            process_restock(medicines)
            # Save updated inventory after restock
            save_inventory(medicines)

        elif choice == "4":
            # ---- Search medicine ----
            if not medicines:
                print_error("No medicines in inventory to search.")
            else:
                search_medicine(medicines)

        elif choice == "0":
            # ---- Exit ----
            print_info("Saving inventory and exiting..."
                       "\n Thank you for using MedStore Wholesale Management System"
                       "\n Goodbye!")
            save_inventory(medicines)
            break

        else:
            print_error(f"Invalid choice '{choice}'. Please enter a number from the menu.")

        input("\n  Press ENTER to continue...")

if __name__ == "__main__":
    run()
