import requests
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("API fetch successful")
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print("API fetch failed:", e)
        return []
def create_product_mapping(api_products):
    """
    Creates mapping of product IDs to product info
    Returns: dictionary
    """
    mapping = {}

    for product in api_products:
        pid = product.get("id")
        mapping[pid] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return mapping
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Returns: list of enriched transactions
    """
    enriched = []

    for t in transactions:
        record = t.copy()

        # Extract numeric product ID (P101 → 101)
        try:
            numeric_id = int(t["ProductID"][1:])
        except:
            numeric_id = None

        if numeric_id in product_mapping:
            api_product = product_mapping[numeric_id]
            record["API_Category"] = api_product["category"]
            record["API_Brand"] = api_product["brand"]
            record["API_Rating"] = api_product["rating"]
            record["API_Match"] = True
        else:
            record["API_Category"] = None
            record["API_Brand"] = None
            record["API_Rating"] = None
            record["API_Match"] = False

        enriched.append(record)

    return enriched
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID")),
                str(t.get("Date")),
                str(t.get("ProductID")),
                str(t.get("ProductName")),
                str(t.get("Quantity")),
                str(t.get("UnitPrice")),
                str(t.get("CustomerID")),
                str(t.get("Region")),
                str(t.get("API_Category")),
                str(t.get("API_Brand")),
                str(t.get("API_Rating")),
                str(t.get("API_Match")),
            ]
            file.write("|".join(row) + "\n")
