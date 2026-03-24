from loader import Loader
from cleaner import Cleaner
from analyzer import SalesAnalyzer
import visualizer as viz
import os


def main():
    # załadowanie i czyszczenie
    loader = Loader(data_dir="../data")

    try:
        products, customers, sales = loader.load_all()
    except Exception as e:
        print("Data loading error:", e)
        raise SystemExit(1)

    cleaner = Cleaner()
    products = cleaner.clean_products(products)
    customers = cleaner.clean_customers(customers)
    sales = cleaner.clean_sales(sales)
    sales_enriched = cleaner.clean_sales_enriched(sales, products, customers)

    # analyze
    analyzer = SalesAnalyzer(sales_enriched)
    kpis = analyzer.kpis()
    by_prod = analyzer.by_product()
    by_reg = analyzer.by_region()
    by_mon = analyzer.by_month()

    out_dir = os.path.join("..", "raport", "figures")
    os.makedirs(out_dir, exist_ok=True)
    out = viz.save_dashboard(
        df_by_product=by_prod,
        df_by_region=by_reg,
        df_by_month=by_mon,
        kpis=kpis,
        n_top_products=10,
        out_dir=out_dir,
        filename="dashboard.png",
    )

    print(f"Dashboard saved to : {out}")


if __name__ == "__main__":
    main()






