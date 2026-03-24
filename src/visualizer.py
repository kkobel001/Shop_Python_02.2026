import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def save_dashboard(df_by_product: pd.DataFrame,
				   df_by_region: pd.DataFrame,
				   df_by_month: pd.DataFrame,
				   kpis: dict,
				   n_top_products: int=10,
				   out_dir: str="../raport/figures",
				   filename: str = "dashboard.png") -> str:
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    # Prepare data (handle empty dataframes)
    top = pd.DataFrame()
    if df_by_product is not None and not df_by_product.empty:
        if "revenue" in df_by_product.columns:
            top = df_by_product.nlargest(n_top_products, "revenue").copy()

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Top products by revenue
    axs[0, 0].set_title("Top products by revenue")
    if not top.empty:
        axs[0, 0].bar(top["product_name"], top["revenue"])
        plt.setp(axs[0, 0].get_xticklabels(), rotation=45, ha="right")
        axs[0, 0].set_ylabel("Revenue")
        axs[0, 0].grid(axis="y", linestyle="--", alpha=0.7)
    else:
        axs[0, 0].text(0.5, 0.5, "No data", ha="center", va="center")

    # Revenue by region
    axs[0, 1].set_title("Revenue by region")
    if df_by_region is not None and not df_by_region.empty:
        axs[0, 1].bar(df_by_region["region"], df_by_region["revenue"])
        axs[0, 1].set_xlabel("Region")
        axs[0, 1].set_ylabel("Revenue")
        axs[0, 1].grid(axis="y", linestyle="--", alpha=0.3)
    else:
        axs[0, 1].text(0.5, 0.5, "No data", ha="center", va="center")

    # Revenue by month
    axs[1, 0].set_title("Revenue by month")
    if df_by_month is not None and not df_by_month.empty:
        x = df_by_month["year_month"].astype(str)
        y = df_by_month["revenue"]
        axs[1, 0].plot(x, y, marker="o")
        axs[1, 0].set_xlabel("Month")
        plt.setp(axs[1, 0].get_xticklabels(), rotation=45, ha="right")
        axs[1, 0].grid(axis="y", linestyle="--", alpha=0.3)
    else:
        axs[1, 0].text(0.5, 0.5, "No data", ha="center", va="center")

    # KPIs
    axs[1, 1].axis("off")
    lines = [
        f"Total units: {kpis.get('total_units', 0):,}",
        f"Total revenue: {kpis.get('total_revenue', 0):,.2f}",
        f"Average price: {kpis.get('avg_price', 0):.2f}",
        f"Products: {kpis.get('distinct_products', 0)}",
        f"Customers: {kpis.get('distinct_customers', 0)}",
    ]
    text_block = "\n".join(lines)
    axs[1, 1].text(0.02, 0.98, text_block, va="top", ha="left", fontsize=11, family="monospace")

    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


    fig.subtitle("Sales Dashboard", fontsize=16, weight="bold")
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    out_path=os.path.join(out_dir,filename)
    plt.savefig(out_path, dpi=150)

    plt.close(fig)
    return out_path









