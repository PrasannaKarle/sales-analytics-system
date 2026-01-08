from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted({t["Date"] for t in transactions})
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_success = [t for t in enriched_transactions if t.get("API_Match")]
    enrichment_rate = (len(enriched_success) / len(enriched_transactions) * 100) if enriched_transactions else 0

    with open(output_file, "w", encoding="utf-8") as f:

        # 1. HEADER
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("=" * 50 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Transactions':>15}\n")
        for region, data in sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True):
            f.write(
                f"{region:<10}"
                f"₹{data['total_sales']:>14,.2f}"
                f"{data['percentage']:>14.2f}%"
                f"{data['transaction_count']:>15}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Product':<25}{'Qty':>8}{'Revenue':>15}\n")
        for i, (name, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{i:<6}{name:<25}{qty:>8}₹{rev:>14,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<15}{'Spent':>15}{'Orders':>10}\n")
        for i, (cid, data) in enumerate(list(customers.items())[:5], start=1):
            f.write(
                f"{i:<6}{cid:<15}"
                f"₹{data['total_spent']:>14,.2f}"
                f"{data['purchase_count']:>10}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Txns':>10}{'Customers':>12}\n")
        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}"
                f"₹{data['revenue']:>14,.2f}"
                f"{data['transaction_count']:>10}"
                f"{data['unique_customers']:>12}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Sales Day: {peak_day[0]} | Revenue: ₹{peak_day[1]:,.2f}\n")
        f.write("Low Performing Products:\n")
        for name, qty, rev in low_products:
            f.write(f"- {name} | Qty: {qty} | Revenue: ₹{rev:,.2f}\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Records Enriched: {len(enriched_transactions)}\n")
        f.write(f"Successful Enrichments: {len(enriched_success)}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")

    print("Sales report generated successfully.")
