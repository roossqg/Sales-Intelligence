#!/bin/bash

case "$1" in
  test)
    poetry run pytest tests/test_import.py -v
    ;;
  streamlit)
    poetry run streamlit run sc/analyst.py
    ;;
  app)
    poetry run python -m src/analyst.py
    ;;
  *)
    echo "use: ./run.sh [test|streamlit|app]"
    ;;
esac

poetry run python src/save_data_in_db.py

poetry run python src/database/database_create.py

poetry run python -m src.save_data_in_db.py

#format
INSERT INTO Sales_data (client_id,age,price,quantity,age_range,category,datetime,Year,Month,Day) 
VALUES (1,22,44,2,20,'sport',12-02-2022,2022,12,02);
