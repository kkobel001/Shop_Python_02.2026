from loader import Loader
from cleaner import Cleaner
from analyzer import SalesAnalyzer
import visualizer as viz
import os

#zaladowanie i czyszczenie
loader= Loader(data_dir="../darta")
print(loader,"dziala")



try:
    products,customers,sales =loader.load_all()
except Exception as e:
    print("Datta loadeing error:",e)
    raise SystemExit(1)

cleaner=Cleaner()
products=cleaner.clean_products(products)
customers=cleaner.clean__customers(customers)
sales=cleaner.clean_sales(sales)
sales_enriched=cleaner.clean_sales_enriched(sales, products,customers)

#analyze


analyzer=SalesAnalyzer(sales_enriched)
kpis=analyzer.kpis()
by_prod=analyzer.by_product()
by_reg=analyzer.by_region()
by_mon=analyzer.by_month()


os.makedirs("../reports/figures", exisy_ok=True)
out=viz.save_dashboard(
    df_by_product=by_prod,
    df_by_region=by_reg,
    df_by_month=by_mon,
    kpis=kpis,
    n_top_products=10,
    out_dir="../reports/figures",
    filename="dashboard.png"


)

print("Dashboard saved to : {out}")



