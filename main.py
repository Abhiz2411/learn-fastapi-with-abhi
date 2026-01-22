from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello from Abhi"

products = [
    Product(1,"phone","budget phone",99, 10),
    Product(2,"Laptop","Gaming laptop",999, 5)
]

@app.get("/products")
def get_all_products():
    return products