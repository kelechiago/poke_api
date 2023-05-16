import requests
import csv
import sqlite3

# Define the GraphQL query
query = """
{
  gen_species: pokemon_v2_pokemonspecies {
    name
    id
    is_baby
    is_legendary
    is_mythical
    evolution_chain_id
    pokemon_v2_generation {
      name
      id
    }
    evolves_from_species_id
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

# Loop through each species
for species in data['gen_species']:
    # Flatten the species data
    row = {
        'name': species['name'],
        'id': species['id'],
        'is_baby': species.get('is_baby', None),
        'is_legendary': species.get('is_legendary', None),
        'is_mythical': species.get('is_mythical', None),
        'evolution_chain_id': species.get('evolution_chain_id', None),
        'generation_name': species['pokemon_v2_generation'].get('name', None),
        'generation_id': species['pokemon_v2_generation'].get('id', None),
        'evolves_from_species_id': species.get('evolves_from_species_id', None)
    }
    # Add the flattened data to the rows list
    rows.append(row)

# Write the flattened data to a CSV file
with open('poke_file.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

# Connect to the SQLite database
conn = sqlite3.connect('pokemon.db')

# Create a cursor object
c = conn.cursor()

# Create a table to hold the flattened data
c.execute('''CREATE TABLE IF NOT EXISTS pokemon_species
             (name TEXT, id INTEGER, is_baby INTEGER, is_legendary INTEGER, is_mythical INTEGER,
             evolution_chain_id INTEGER, generation_name TEXT, generation_id INTEGER,
             evolves_from_species_id INTEGER)''')

# Load the flattened data from the CSV file
with open('poke_file.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = [tuple(row.values()) for row in reader]

# Insert the data into the table
c.executemany('INSERT INTO pokemon_species VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', rows)

# Commit the changes and close the connection
conn.commit()
conn.close()