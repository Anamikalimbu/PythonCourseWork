# MedStore Wholesale Management System

A simple Python-based medicine inventory management application for wholesale operations.

## Overview

This project provides a command-line system to:
- View current medicine inventory
- Sell medicines and generate sales invoices
- Restock medicines and generate restock notes
- Search medicines by name or brand

## Requirements

- Python 3.8 or newer
- No external Python packages are required

## Install / Setup

1. Open a terminal in the project folder:
   ```bash
   cd "c:\Users\anami\Downloads\PythonCourseWork-main\PythonCourseWork-main"
   ```
2. Install Python if it is not already installed.
3. Run the application:
   ```bash
   python main.py
   ```

## Running the App

When you run `main.py`, the program will:
1. Create `medicines.txt` with sample inventory if it does not exist.
2. Load medicines into memory.
3. Show the main menu.
4. Allow you to choose from:
   - `1` View all medicines in stock
   - `2` Sell medicine
   - `3` Restock medicine
   - `4` Search medicine
   - `0` Exit

The app saves updated inventory back to `medicines.txt` after sales or restocks.

## File / Folder Structure

- `main.py` - Application entrypoint and main loop
- `inventory.py` - Load, save, and manage inventory data
- `display.py` - Print menus and formatted output
- `invoice.py` - Generate sales invoice and restock note text files
- `sales.py` - Sales workflow and stock update logic
- `restock.py` - Restock workflow and stock update logic
- `search.py` - Search medicines by name or brand
- `utils.py` - Validation and utility functions
- `Medicines.txt` - Inventory data file used by the application
- `invoices/` - Folder where generated invoice and restock note files are saved

## Inventory Data Format

Each line in `medicines.txt` should use this format:

```
Name, Brand, Qty(tablets), Rate/tablet, Rate/strip, Tablets/strip
```

Example:
```
Paracetamol 500mg, Lomus, 1200, 5, 45, 10
```

## Notes

- If `medicines.txt` is missing, a sample file is created automatically.
- Generated invoices and restock notes are saved in the `invoices/` directory.
- Use integer values for quantities and valid numeric values for rates.

## Troubleshooting

- If the program cannot find `medicines.txt`, it will create one automatically.
- If an error occurs while saving inventory or invoices, check file permissions in the project folder.

## License

This project is provided as-is for learning and coursework purposes.
