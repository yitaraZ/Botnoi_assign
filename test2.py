from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id:int

@app.post("/pokemon/")
async def get_pokemon_data(item: Item):
    id = item.dict()['id']
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    pokemon_form_url = f"https://pokeapi.co/api/v2/pokemon-form/{id}/"

    try:
        pokemon_response = requests.get(pokemon_url)
        pokemon_form_response = requests.get(pokemon_form_url)
        pokemon_response.raise_for_status()
        pokemon_form_response.raise_for_status()

        pokemon_data = pokemon_response.json()
        pokemon_form_data = pokemon_form_response.json()

        stats = [{"base_stat": stat["base_stat"], "effort": stat["effort"], "stat": stat["stat"]} for stat in pokemon_data["stats"]]

        result = {
            "stats": stats,
            "name": pokemon_form_data["name"],
            "sprites": pokemon_form_data["sprites"]
        }

        return result

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from PokeAPI: {str(e)}")
