# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("File not found:", filename)
            return []

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("TransactionID"):
            continue
        cleaned_lines.append(line)

    return cleaned_lines


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue

        transaction_id = parts[0].strip()
        date = parts[1].strip()
        product_id = parts[2].strip()
        product_name = parts[3].strip().replace(',', '')
        quantity = parts[4].strip().replace(',', '')
        unit_price = parts[5].strip().replace(',', '')
        customer_id = parts[6].strip()
        region = parts[7].strip()

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            continue

        transactions.append({
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0

    for t in transactions:
        if t['Quantity'] <= 0 or t['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        if not t['TransactionID'].startswith('T'):
            invalid_count += 1
            continue
        if not t['ProductID'].startswith('P'):
            invalid_count += 1
            continue
        if not t['CustomerID'].startswith('C'):
            invalid_count += 1
            continue

        amount = t['Quantity'] * t['UnitPrice']

        if region and t['Region'] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid_transactions.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
