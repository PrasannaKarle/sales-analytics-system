from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)

from utils.report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read raw data
        print("\n[1/10] Reading and cleaning sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")

        # 2. Parse
        parsed = parse_transactions(raw_lines)

        # 3. Validate
        valid_transactions, invalid_count, summary = validate_and_filter(parsed)

        print("Validation Summary:")
        print(summary)

        # 4. Analysis
        print("\n[2/10] Performing sales analysis...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)

        # 5. API
        print("\n[3/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        # 6. Enrichment
        print("\n[4/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        # 7. Report
        print("\n[5/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)

        print("\nPROCESS COMPLETED SUCCESSFULLY")
        print("Files generated:")
        print("- data/enriched_sales_data.txt")
        print("- output/sales_report.txt")

    except Exception as e:
        print("\nERROR OCCURRED")
        print("Something went wrong during execution.")
        print("Error:", e)


if __name__ == "__main__":
    main()
