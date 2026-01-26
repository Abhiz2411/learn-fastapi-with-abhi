from math import prod
from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello from Abhi"

products = [
    Product(id=1,name="phone",description="budget phone",price=99, quantity=10),
    Product(id=2,name="laptop",description="budget laptop",price=98, quantity=30),
    Product(id=3,name="game",description="expensive game",price=999, quantity=60),
    Product(id=4,name="movie",description="mid movie",price=997, quantity=6),
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    else:
        return "Product not found!"
