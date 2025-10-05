# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
# from mangum import Mangum
from pydantic import BaseModel
# from finalee import query_rag
from .yoji import query_rag
app = FastAPI()

class QueryResponse(BaseModel):
    answer: str

class SubmitQueryRequest(BaseModel):
    query_text: str

@app.get("/")
def index():
    return {"Hello": "World"}
# from pydantic import BaseModel

# Assuming your models are defined like this
# class QueryResponse(BaseModel):
#     answer: str

# class SubmitQueryRequest(BaseModel):
#     query_text: str

# Your query_rag function goes here...
# def query_rag(query_text: str) -> dict:
#     ...

# --- Replace your endpoint with this one ---
@app.post("/submit_query", response_model=QueryResponse)
def submit_query_endpoint(request: SubmitQueryRequest):
    print("\n--- Endpoint called. Calling query_rag function... ---")
    
    # Call your function to get the result
    result_from_rag = query_rag(request.query_text)
    
    # --- DEBUGGING CHECKS ---
    print(f"--- DEBUG: Value returned from query_rag is: {result_from_rag}")
    print(f"--- DEBUG: The TYPE of this value is: {type(result_from_rag)}")

    # Check 1: Is the result a dictionary?
    if not isinstance(result_from_rag, dict):
        print("--- FATAL ERROR: query_rag did NOT return a dictionary! ---")
        # We raise a clean error instead of letting FastAPI crash.
        raise HTTPException(status_code=500, detail="Internal function failed to return a valid dictionary.")

    # Check 2: Does the dictionary have the required 'answer' key?
    if "answer" not in result_from_rag:
        print("--- FATAL ERROR: The returned dictionary is MISSING the 'answer' key! ---")
        raise HTTPException(status_code=500, detail="Internal function returned a dictionary without the required 'answer' key.")
    
    print("--- SUCCESS: Returning a valid dictionary to FastAPI. ---")
    return result_from_rag


if __name__ == "__main__":
    # Run this as a server directly.
    port = 5000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("apphandler:app", host="0.0.0.0", port=port)
