### Steps to run the project
- First step: Run the mongodb database in a new terminal by running `mongod --dbpath {path_to_your_db}`:
  - mongod --dbpath /Users/bergasanargya/Asia_Global/mongodb_data
- Second step: In a new terminal, go to the `Asia_Global` repository:
  - To make sure that the db is running:
    - Create a new mongodb shell: `mongo` or `mongosh`
    - Run these in order: `show dbs`, `use {name_of_db}` usually it's named as financial_data, `show collections` usually it's named as combined_data, `db.combined_data.find().pretty()`
  - If db is running, exit the shell
  - Run `python main.py`
