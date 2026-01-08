def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    """
    total_revenue = 0.0
    for t in transactions:
                total_revenue += t['Quantity'] * t['UnitPrice']
    return total_revenue
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)
    for t in transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']
        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1
    for region in region_data:
        region_data[region]['percentage'] = (
            region_data[region]['total_sales'] / total_revenue
        ) * 100
    return region_data
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    """
    product_data = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }
        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue
    result = []
    for name, data in product_data.items():
        result.append((name, data['quantity'], data['revenue']))

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    """
    customers = {}
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        if cid not in customers:
            customers[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }
        customers[cid]['total_spent'] += amount
        customers[cid]['purchase_count'] += 1
        customers[cid]['products'].add(t['ProductName'])
    result = {}
    for cid, data in customers.items():
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': data['total_spent'] / data['purchase_count'],
            'products_bought': list(data['products'])
        }
    return dict(
        sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    )
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_data = {}
    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(t['CustomerID'])
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(daily_data[date]['customers'])
        del daily_data[date]['customers']
    return dict(sorted(daily_data.items()))
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_data = daily_sales_trend(transactions)
    peak_date = None
    max_revenue = 0.0
    transaction_count = 0
    for date, data in daily_data.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date
            transaction_count = data['transaction_count']
    return (peak_date, max_revenue, transaction_count)
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    """
    product_data = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }
        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue
    result = []

    for name, data in product_data.items():
        if data['quantity'] < threshold:
            result.append((name, data['quantity'], data['revenue']))
    result.sort(key=lambda x: x[1])
    return result
