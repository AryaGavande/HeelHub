from fastapi import FastAPI, HTTPException, Response
from starlette.responses import RedirectResponse
import sqlite3
import uuid

conn = sqlite3.connect('heelhub.db')
cursor = conn.cursor()

app = FastAPI()

# Create the user table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

@app.post("/signup")
async def signup(username: str, password: str):

    # Generate a unique user_id
    user_id = uuid.uuid4().hex

    # Write the new user data into the database
    cursor.execute(f'''
        INSERT INTO users (user_id, username, password) VALUES ('{user_id}', '{username}', '{password}')
    ''')
    conn.commit()

    return {"message": "User signed up successfully"}

@app.post("/login")
async def login(username: str, password: str):

    # Check if the username exists in the database
    cursor.execute(f'''
        SELECT * FROM users WHERE username = '{username}'
    ''')
    user = cursor.fetchone()

    # Verify the password if the user exists
    if user and user[2] == password:
        response = RedirectResponse(url="http://localhost:5501/e-commerce-app/frontend/homescreen.html")
        response.set_cookie(key="username", value=username)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/")
async def read_root():
    return {"Hello": "World"}
