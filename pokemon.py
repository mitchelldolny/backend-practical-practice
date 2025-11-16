import requests

class PokemonNotFound(Exception):
    pass

class PokemonClient:
    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.timeout = timeout
    
    def get_pokemon(self, name):

        url = f"{self.BASE_URL}/pokemon/{name}"

        resp = self.session.get(url, timeout=self.timeout)

        if resp.status_code == 404: 
            raise PokemonNotFound(f"Pokemon {name} not found!")

        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            print("Request Failed")
            print(f"Has status {resp.status_code}")
        
        return resp.json()

    def format_information(self, pokemon_data):

        stats_list = pokemon_data.get("stats", [])

        for i in range(len(stats_list)):

            info = {
                "value": stats_list[i].get("base_stat"),
                "name": stats_list[i].get("stat").get("name").capitalize()

            }
            stats_list[i] = f"Stat {info['name']}: {info['value']}"

        return stats_list

    def get_all_pokemon_paginated(self):
        offset = 0
        limit = 50
        max_limit = 2000

        
        pages = []
        while offset < max_limit:
            url = f"{self.BASE_URL}/pokemon?limit={limit}&offset={offset}"
            resp = self.session.get(url).json()
            data = resp.get("results", [])
            if data == []: return pages

            cur_page = []
            for pokemon in data:
                cur_page.append(pokemon.get("name", ""))
                
            pages.append(cur_page)
            offset += limit
        return pages








import sys

if __name__ == "__main__":
    client = PokemonClient()
    if len(sys.argv) < 2:
        print("Usage: python pokemon_client.py <pokemon_name>")
        raise SystemExit(1)
    
    name = sys.argv[1]
    
    print(client.get_all_pokemon_paginated()[0])
    data = client.get_pokemon(name)
    try:
        print(client.format_information(data))
    except PokemonNotFound as e:
        print(f"Pokemon {name} not found")
        raise SystemExit(1)
    except Exception as e:
        print("Unexpected error:", e)
        raise SystemExit(2)