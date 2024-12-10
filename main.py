# membuat web kosong
# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd


# buat object/instance for FastAPI class
app = FastAPI()

# buat API key
API_Key = "hck024data"

# buat endpoint
@app.get("/")
def home():
    return {"message": "selamat datang di toko wellfresh"}

# buat endpoint data
@app.get("/data")
def read_data():
    #read data from file csv
    df = pd.read_csv("data.csv")
    #mengembalikan data to dictionary with orient="records" for each row
    return df.to_dict(orient="records")

#buat endpoint data dengan parameter nomor id
@app.get("/data/{number_id}")
def read_item(number_id: int):
    df = pd.read_csv("data.csv")

    # filter data by id
    filter_data = df[df["id"] == number_id]

    # cek filter data is empty
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="barang yang saya cari tidak ada, soryy")


    #mengembalikan data to dictionary with orient="records" for each row
    return filter_data.to_dict(orient="records")


# buat endpoint update file csv data
@app.put("/item/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    #buat dict for updating data
    df = pd.read_csv("data.csv")

    #creat dataframe from updated input
    updated_df = pd.DataFrame({
        "id":number_id,
        "nama_barang":nama_barang,
        "harga":harga
    }, index=[0])
    # merge update dataframe with original dataframe
    df = pd.concat([df, updated_df], ignore_index=True)

    #save updated dataframe to file csv
    df.to_csv("data.csv", index=False)

    return {"message": f"Item with ID {nama_barang} has been updated successfully."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)):

    #read data from file csv
    secret_df =  pd.read_csv("secret_data.csv")
    
    # cek if api key is valid
    if api_key != API_Key:
        # if api key is not valid return error
        raise HTTPException(status_code=401, detail="API key tidak valid")
    
    return secret_df.to_dict(orient="records")