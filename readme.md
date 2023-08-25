# Pokémon API and Data Science Tutorial

Here is a (work-in-progress) tutorial and guide of general data science principles using Pokémon data! I plan to cover things such as:

- Statistics and Statistical Models
- Data Visualization
- Machine Learning
- Model Evaluation

## Requirements

- Python 3.x
- requests library
- csv library
- sqlite3 library
- pandas
- numpy
- matplotlib
- seaborn
- scikitlearn

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo.git
```

2. Install the required libraries:

```
pip install -r requirements.txt
```

## Usage

1. Open the terminal and navigate to the project directory:

```
cd path/to/project-directory
```

2. Run the script:

```
python main.py
```

3. The script will fetch the Pokémon data from the PokeAPI GraphQL endpoint, flatten it, and save it to a CSV file named `pokemon.csv`.

4. It will then create an SQLite database file named `pokemon.db` in the project directory.

5. The script will create a table named `pokemon_tbl` in the SQLite database and import the flattened data from the CSV file into the table.

## Configuration

- You can modify the GraphQL query in the `query` variable in the code to customize the data you want to extract.

- If you want to change the names of the CSV file or the SQLite database file, you can modify the respective file names in the code.

## License

This project is licensed under the [MIT License](LICENSE).
