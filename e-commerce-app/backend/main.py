from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Assuming 'frontend_path' is the path to your 'frontend' directory
frontend_path = Path(__file__).resolve().parent.parent / 'frontend'
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Serve 'index.html' for the root URL
@app.get("/")
async def read_index():
    index_path = frontend_path / 'index.html'
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Index file not found")
    return FileResponse(str(index_path))


DATABASE_URL = 'heelhub.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/product")
async def write_product(service_type: str, amount: float, name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    product_id = uuid.uuid4().hex

    cursor.execute('''
        INSERT INTO products (product_id, service_type, amount, name) VALUES (?, ?, ?, ?)
    ''', (product_id, service_type, amount, name))

    conn.commit()
    conn.close()

    return {'product_id': product_id}


@app.get("/product/{product_id}")
async def read_product(product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    row = cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
    conn.close()
    
    if row:
        return {
            'product_id': row['product_id'],
            'name': row['name'],
            'amount': row['amount'],
            'service_type': row['service_type']
        }
    else:
        return {"error": "Product not found"}


@app.get("/products")
async def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    rows = cursor.execute("SELECT * FROM products").fetchall()
    conn.close()
    
    returnRows = [
        {
            'product_id': row['product_id'],
            'name': row['name'],
            'amount': row['amount'],
            'service_type': row['service_type']
        }
        for row in rows
    ]
    
    return returnRows
