from typing import Union

from fastapi import FastAPI, HTTPException

from db_queries import Country, CountryQueries, SupabaseClient

app = FastAPI()
country_queries = CountryQueries(SupabaseClient())


@app.post("/countries")
async def create_country(country: Country):
    result = country_queries.add_country(country)
    if result["error"]:
        handle_error(result["error"], 'error adding country')
    return {"data": "added country successfully"}


@app.put("/countries/{cid}")
async def edit_country(country: Country, cid: int):
    result = country_queries.update_country(country, cid)
    if result["error"]:
        handle_error(result["error"], 'error adding country')
    return {"data": "edited country successfully"}


@app.delete("/countries/{cid}")
async def remove_country(cid: int):
    result = country_queries.delete_country(cid)
    if result["error"]:
        handle_error(result["error"], 'error deleting a country')
    return {"data": "deleted country successfully"}


@app.get("/countries")
async def read_countries():
    result = country_queries.get_countries()
    if result["error"]:
        handle_error(result["error"], 'error fetching supabase table')
    return result["data"]


@app.get("/countries/{cid}")
async def read_country(cid: int, q: Union[str, None] = None):
    result = country_queries.get_country(cid)
    if result["error"]:
        handle_error(result["error"], 'error fetching single item supabase table')
    return {"data": result["data"], "q": q}


def handle_error(error, error_message):
    if error:
        raise HTTPException(status_code=500, detail=f'{error_message}: {error}')
