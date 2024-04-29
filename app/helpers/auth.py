import httpx


async def verify_token(token: str):
    url = "http://localhost:8000/verify-token"  # проставить нужный адрес
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"message": "Token is invalid"}

