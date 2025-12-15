import pandas as pd 
import pandasql as ps 
from pandasql import sqldf

filepath = "products.csv"
df = pd.read_csv(filepath) 

print ("Dataframe colume Types : ")
print (df.dtypes)
print("\n Product data :")
print (df)

query = input("Enter the query : ")

#print(df["gender"].unique())

result = ps.sqldf(query,{"data": df })
print("\n Query Result : ")
print (result)

