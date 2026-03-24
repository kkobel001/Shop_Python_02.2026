import pandas as pd


class Cleaner:

    def __init__(self):
        pass

    def standarize_columns(self, df):
        """ 
         zeby byly wszytskie male litery, ujednolicenie kolumn
        """    
         
        df = df.copy()
        new_cols = []
        for column in df.columns:
            clean_name = column.strip().lower()  #usuwa biale wciecia i lower zmiana na male litery
            new_cols.append(clean_name) #zbieramy wszystkie nazwy wyczyszczonych kolumn

        df.columns = new_cols #przypisujemy do naszego datasetu nowae czyli zamienione (nadpisujemy)
        return df

    def drop_duplicates(self, df, subset=None):
        """
        usuniecie duplikatów
        """
        #before-zapisujemy ile duplikatów mamy na początku
        before = len(df)
        df = df.drop_duplicates(subset=subset)
        after = len(df) #zapisuje ile duplikatów było na końcu
        print(f"Dropped duplicates: {before - after}") #wyłapanie rónicy
        return df

    def clean_products(self, df_products): #tutaj juz przekazujemy nowy dataset ten zmieniony i wtedy bedziemy pewni ze czyste sa wartosci
        df = self.standarize_columns(df_products)

        #sprawdzamy czy cena jest rzeczywiscie w formacie danych numerem, a nie stringiem. jesli  jest Nan wtedy dopisz albo usun 
        df["price"] = pd.to_numeric(df["price"], errors="coerce") #coarce , jesli jest error to wstaw nan

        df = df[df["price"].notna()] #notna maska boolean
        df = df[df["price"] > 0] #jesli nie ma ceny bardz jest ujemna wyrzuc ja

        df = self.drop_duplicates(df, subset=["product_id"])

        return df

    def clean_customers(self, df_customers):
        df = self.standarize_columns(df_customers)

        #sprawdzamy czy wiek jest numerem
        df["age"] = pd.to_numeric(df["age"], errors="coerce")

        median_age = df["age"].median() #jesli dany customer nie ma wieku to mozemy mu przypisac po prostu mediana wieku
        df["age"] = df["age"].fillna(median_age)

        df=self.drop_duplicates(df,subset=["customer_id"])

        return df


    def clean_sales(self,df_sales):
        """
        -standarize column,
        -parsujemy date do datatime
        -jesli blad na unitach zawiera NaN to uzupelnij 0 
        -units wiekszy nic 0
        - usun duplikaty na sale_id
        """
        df = self.standarize_columns(df_sales)

        df["date"]=pd.to_datetime(df["date"],errors="coerce")

        df["units"]=pd.to_numeric(df["units"],errors="coerce")

        df["units"] = df["units"].fillna(0)
        df = df[df["units"] >= 0]

        df = self.drop_duplicates(df, subset=["sale_id"])

        return df

    def clean_sales_enriched(self, df_sales, df_products, df_customers):
        # merge products (on product_id) and customers (on customer_id)
        merged = df_sales.merge(
            df_products[["product_id", "product_name", "category", "price"]],
            on="product_id",
            how="left",
        )

        merged = merged.merge(
            df_customers[["customer_id", "customer_name", "region", "age"]],
            on="customer_id",
            how="left",
        )

        merged = merged.dropna(subset=["product_name", "customer_name"]) 

        return merged




