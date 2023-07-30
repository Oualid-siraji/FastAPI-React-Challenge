from fastapi import FastAPI,HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
import db.connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


collection = db.connection.get_collection()


#Test pour récupérer tous les clients :
@app.get("/clients")
async def get_clients():
    
    url = "https://techtest.hiboutik.com/api/customers/?p=1"
    
    async with httpx.AsyncClient() as client : response = await client.get(url, auth=("techtest@gmail.com", "2OZ58K8MYZV56SFA59NG2PQ2HYW4C6280IT"))
    
    return response.json()

#Challenge 2 : 
#Dans ce défi, lorsque l'utilisateur saisit le nom d'un client,
#les informations du client retrouvées sont affichées dans la base de données.
@app.get("/client/{last_name}")
async def get_client(last_name : str):
    url="https://techtest.hiboutik.com/api/customers/?p=1"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=("techtest@gmail.com", "2OZ58K8MYZV56SFA59NG2PQ2HYW4C6280IT"))

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not retrieve data from the external API.")

    all_customers = response.json()

    filtered = [customer for customer in all_customers if customer['last_name'] == last_name]

    if not filtered: 
        raise HTTPException(status_code=404, detail="No customers found with this last name")

   
    for customer in filtered:
        if not collection.find_one(customer):  # if the customer is not found in the collection
            collection.insert_one(customer)  # insert it

    return filtered


#Challenge 3 : Récupérer les ventes d'un Client à partir de son Id .

@app.get("/sales/{customer_id}")
async def get_sales_for_customer(customer_id: int):
    url = f"https://techtest.hiboutik.com/api/customer/{customer_id}/sales/?p=1"
   
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=("techtest@gmail.com", "2OZ58K8MYZV56SFA59NG2PQ2HYW4C6280IT"))
            response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Challenge 4 :

@app.get("/sales/{customer_id}/sales")
async def get_sales_for_customer(customer_id: int, page : int=1, limit: int=5):
    url = f"https://techtest.hiboutik.com/api/customer/{customer_id}/sales/?p={page}&limit={limit}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=("techtest@gmail.com", "2OZ58K8MYZV56SFA59NG2PQ2HYW4C6280IT"))
            response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


