import pandas as pd

file_path =  "E:\\VLU\\Chuyen_de_1\\Chuyen_de_1\\dataset\\customers_raw.csv"

df = pd.read_csv(file_path)

print("số dòng" , df.shape[0])
print("số cột" , df.shape[1])