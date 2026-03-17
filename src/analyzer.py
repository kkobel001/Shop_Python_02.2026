import pandas as pd


class SalesAnalyzer:


    def __init__(self,sales_enriched_df): #dodajemy te dane, które dostaliśmy od ostatecznej klasy cleaner czyli procducts,sales, customers
        self.df=sales_enriched_df.copy() #tworzymy kopie, jest to dobra praktyka. Tak zebysmy nie wprowadzali niepotrzebnych zmian


        required=["units","price","product_name","region", "date"] #sprawdzamy czy nie brakuje nam zadnej kolumny i piszemy wyjątek jesli jakiejs kolumny brakuje
        missing=[]
        for c in required:
            if c in self.df.columns:
                missing.append(c)
        if missing:
            raise ValueError(f"SalesAnalyzer:missing required columns: {missing}")
        
        self.df=self.df[self.df["date"].notna()] #pozbywamy sie rekordów tam gdzie brakuje nam daty. maska boolean

        self._add_revenue() #dodajemy ponizsza funkcje add revenue na poziomie initu

    def _add_revenue(self):
        self.df["revenue"]=self.df["units"] * self.df["price"]



    """KPI"""

    def kpis(self):
        """
        KPI:
        total_units
        total_revenue
        avg_price
        distinct_products
        """
        out={} #tworzymy sobie dict do ktorego bede przypisywac kolejne wartosci
        out["total_units"]=int(self.df["units"].sum())
        out["total_revenue"]=float(self.df["revenue"].sum())
        out["avg_price"]=float(self.df["price"].mean())
        out["distinct_products"]=int(self.df["products_name"].nunigue())
        out["total_units"]=int(self.df["units"].sum()).nunigue()
        return out
    
    def by_product(self):
        agg=(
          self.df.groupby("product_name", as_index=False)      

        )