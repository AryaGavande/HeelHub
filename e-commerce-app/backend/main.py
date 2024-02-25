from fastapi import FastAPI
import sqlite3
import uuid

conn = sqlite3.connect('heelhub.db')

cursor = conn.cursor()

conn.row_factory = sqlite3.Row

app = FastAPI()


# @app.get("/")
# async def read_root():
#     return {"Hello", "World"}

@app.post("/product")
async def write_product(service_type: str, amount: float, name: str):

    # Write code here to write data we get from endpoint into database

    product_id = uuid.uuid4().hex

    cursor.execute(f'''
        INSERT INTO products (product_id, service_type, amount, name) VALUES ('{product_id}', '{service_type}', {amount}, '{name}')
    ''')

    conn.commit()

    return {
        'product_id':product_id
    }

    return product_id


@app.get("/product/{product_id}")
async def read_product(product_id):
    rows = cursor.execute(f"SELECT * FROM products where product_id = '{product_id}'").fetchone()
    return {
        'product_id': rows[0],
        'name': rows[1],
        'amount': rows[2],
        'service_type':rows[3]
    }


@app.get("/products")
async def get_all_products():
    rows = cursor.execute(f"SELECT * FROM products")
    returnRows = []
    for row in rows:
        returnRows.append(
            {
                'product_id': row[0],
                'name': row[1],
                'amount': row[2],
                'service_type': row[3]
            }
        )