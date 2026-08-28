# Sales Intelligence - Beta 1.1

## Overview
Data web application that **imports**,**process** and **analyzes** your sales data from differents sources and provides an dashboard to track typical sale metrics like **Time Series Revenue** and **Sold Stock**.

Also,its possible make inferences and understand data better using **Statistical Analyses and Tests**,**Forecatsing** and **Optimization**.

## Tech
- **Python**: data processing and analysis
- **Streamlit**: dashboard design and graphs
- **Sqlite3**: local data storage and updating
- **poetry**: environment management

## Project Workflow

1. **Data importing**: input tables with supported formats with the following columns.

| Column | Format |
| :--- | ---:|
| client_id | int |
| age | int |
| product_name | str |
| price | float |
| quantity | int |
| category | category |
| datetime | datetime |

**Suported Formats**:
- csv
- tsv
- excel
- parquet
- json

The importing pipeline automatically converts the data which you passed, to a **Pandas DataFrame** which will be passed to processing pipeline.

2. **Data Processing** : Clean,convert and standarlizes the dataframe using following business _Rules_: 

| Column | Missing values | Incosistent Categories |
| :---: | :---: | ---:  |
| client_id | keep null | |
| age | mean  | |
| product_name | keep null | remove incosistent chars,lower text
| price | mean | |
| quantity | mean | |
| category | mean | remove incosistent chars,lower text |
| datetime | keep null | convert to format: %Y-%m-%d : %H |

You are free to modify the _Rules_ of data conversion according business purpouses.

**Feature engineering**:  creates new features from sales data for analyst purpouses.

Model:

| Column | Format |
| :--- | ---:|
| client_id | int |
| age | int |
| product_name | str |
| price | float |
| quantity | int |
| category | category |
| datetime | datetime |
| age_range| category |
| Day | int |
| Day_of_week | str/datetime |
| Month | int |
| Year | int |


- **Dashboard/Analyst**: provides a dashboard with graphs and metrics to show pattners about the sales,
which helps to improving **decision-making** process about the business like **Stock Selection**,**Promotions** or **Seazonality** for example. 


## How Use

### Configuration

1. Set database url in **.env**

```
DATABASE_URL = 'sqlite:///{path to create your table}'
```

2. Run database model and create **Sales** table
```
poetry run python src/Models/database.py
```
- You can delete the table and create a new or delete the data into it using **sqlite3** terminal.

3. Pass the path of your desired dataset containing required columns and its format to  the function **get_data** and run the script :
```
poetry run python src/save_data_in_db
```
- each new data precessed will be saved in **Sales.db** for full analyst in the dashboard.

4. Run the streamlit application dashboard:
```
poetry run streamlit run src/app.py
```

After step 4,unless you want add more data,just run streamlit app to initialize the dashboard application.

**Disclaimer**: Not final software,can include:
- Bugs
- Wrong Tests
- Irregular architecture
- Documentation errors
