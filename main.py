import requests
import csv
import sqlite3

# Define the GraphQL query
query = """
{
  pokemon_v2_pokemon {
    name
    id
    height
    base_experience
    pokemon_species_id
    weight
    pokemon_v2_pokemonstats {
      base_stat
    }
    pokemon_v2_pokemonspecy {
      evolution_chain_id
      evolves_from_species_id
      gender_rate
      has_gender_differences
      is_baby
      is_legendary
      is_mythical
      capture_rate
      base_happiness
      hatch_counter
      pokemon_v2_growthrate {
        name
      }
      pokemon_v2_generation {
        name
      }
      pokemon_v2_pokemonhabitat {
        name
      }
    }
    pokemon_v2_pokemontypes {
      pokemon_v2_type {
        name
      }
    }
  }
}
"""

# Set the URL for the GraphQL endpoint
url = 'https://beta.pokeapi.co/graphql/v1beta'

# Set the headers for the HTTP POST request
headers = {'Content-Type': 'application/json'}

# Send the HTTP POST request with the GraphQL query
response = requests.post(url, json={'query': query}, headers=headers)

# Parse the response JSON and extract the data
data = response.json()['data']

# Create a list to hold flattened data
rows = []

# Loop through each row
for pokemon in data['pokemon_v2_pokemon']:
    # Flatten the species data
  row = {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'base_experience': pokemon['base_experience'],
        'pokemon_species_id': pokemon['pokemon_species_id'],
        'weight': pokemon['weight'],
        'hp': pokemon['pokemon_v2_pokemonstats'][0]['base_stat'],
        'attack': pokemon['pokemon_v2_pokemonstats'][1]['base_stat'],
        'defense': pokemon['pokemon_v2_pokemonstats'][2]['base_stat'],
        'special-attack': pokemon['pokemon_v2_pokemonstats'][3]['base_stat'],
        'special-defense': pokemon['pokemon_v2_pokemonstats'][4]['base_stat'],
        'speed': pokemon['pokemon_v2_pokemonstats'][5]['base_stat'],
        'evolution_chain_id': pokemon['pokemon_v2_pokemonspecy']['evolution_chain_id'],
        'evolves_from_species_id': pokemon['pokemon_v2_pokemonspecy']['evolves_from_species_id'],
        'gender_rate': pokemon['pokemon_v2_pokemonspecy']['gender_rate'],
        'has_gender_differences': pokemon['pokemon_v2_pokemonspecy']['has_gender_differences'],
        'is_baby': pokemon['pokemon_v2_pokemonspecy']['is_baby'],
        'is_legendary': pokemon['pokemon_v2_pokemonspecy']['is_legendary'],
        'is_mythical': pokemon['pokemon_v2_pokemonspecy']['is_mythical'],
        'capture_rate': pokemon['pokemon_v2_pokemonspecy']['capture_rate'],
        'base_happiness': pokemon['pokemon_v2_pokemonspecy']['base_happiness'],
        'hatch_counter': pokemon['pokemon_v2_pokemonspecy']['hatch_counter'],
        'growth_rate': pokemon['pokemon_v2_pokemonspecy']['pokemon_v2_growthrate']['name'],
        'generation_name': pokemon['pokemon_v2_pokemonspecy']['pokemon_v2_generation']['name'],
        'habitat_name': pokemon['pokemon_v2_pokemonspecy']['pokemon_v2_pokemonhabitat']['name'] if pokemon['pokemon_v2_pokemonspecy']['pokemon_v2_pokemonhabitat'] is not None else None,
        'type_name_1': pokemon['pokemon_v2_pokemontypes'][0]['pokemon_v2_type']['name'] if len(pokemon['pokemon_v2_pokemontypes']) >= 1 else "",
        'type_name_2': pokemon['pokemon_v2_pokemontypes'][1]['pokemon_v2_type']['name'] if len(pokemon['pokemon_v2_pokemontypes']) >= 2 else ""
    }
    # Add the flattened data to the rows list
  rows.append(row)

# Write the flattened data to a CSV file
with open('pokemon.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

# Connect to the SQLite database
conn = sqlite3.connect('pokemon.db')

# Create a cursor object
c = conn.cursor()

# Create a table to hold the flattened data
c.execute("""CREATE TABLE IF NOT EXISTS pokemon_tbl
             (name TEXT, id INTEGER, height INTEGER, base_experience INTEGER, pokemon_species_id INTEGER,
             weight INTEGER, hp INTEGER, attack INTEGER, defense INTEGER, "special-attack" INTEGER, "special-defense" INTEGER, speed INTEGER,
             evolution_chain_id INTEGER, evolves_from_species_id INTEGER, gender_rate INTEGER, has_gender_differences INTEGER,
             is_baby INTEGER, is_legendary INTEGER, is_mythical INTEGER,
             capture_rate INTEGER, base_happiness INTEGER, hatch_counter INTEGER, growth_rate TEXT,
             generation_name TEXT, habitat_name TEXT, type_name_1 TEXT, type_name_2 TEXT)""")

# Load the flattened data from the CSV file
with open('pokemon.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = [tuple(row.values()) for row in reader]

# Insert the data into the table
c.executemany('INSERT INTO pokemon_tbl VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', rows)

# Commit the changes and close the connection
conn.commit()
conn.close()