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

        df["units"] = df["price"].fillna(0) #jesli jest 0 to tez jest to informacja i wstawiony po prostu zero
        df = df[df["units"] >=0] 

        df = df[df["price"].notna()]     #usuwamy wszystkie reokrdy ktore nie maja daty   


        df=self.drop_duplicates(df,subset=["sales_id"])

        return df
    

        def clean_sales_enriched(self, df_sales,df_products,df_customers):



            #left-joint products
            merged=df_sales.merge(
                df_products[["product_id","product_name","category","price"]],
                on="customer_id",
                how="left"
            )

            matged=marged.dropna(subset=["product_name","customer_name"])

            return marged



