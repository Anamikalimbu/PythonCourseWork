# Handles medicine search functionality

from display import display_search_results, print_info
from inventory import find_medicine
from utils import get_valid_string


def search_medicine(medicines):
    print("\n  === SEARCH MEDICINE ===")

    term = get_valid_string("  Enter medicine name or brand to search: ")
    results = find_medicine(medicines, term)

    if results:
        display_search_results(results)
        print_info(f"Found {len(results)} result(s) for '{term}'.")
    else:
        print_info(f"No medicines found matching '{term}'.")