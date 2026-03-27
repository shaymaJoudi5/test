from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import httpx # type: ignore

app = FastAPI()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"http://localhost:8000/users/{user_id}"
            )
            return response.json()
        except httpx.ConnectError:
            return {"error": "Service unavailable"}
        except Exception as e:
            return {"error": str(e)}

@app.get("/api/products/{user_id}")
async def get_products(user_id: int):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"http://localhost:8001/products/{user_id}"
            )
            return response.json()
        except httpx.ConnectError:
            return {"error": "Service unavailable"}
        except Exception as e:
            return {"error": str(e)}

# EN DERNIER
app.mount("/", StaticFiles(directory="static", html=True), name="static")