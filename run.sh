#!/bin/bash

case "$1" in
  test)
    poetry run pytest tests/test_import.py -v
    ;;
  streamlit)
    poetry run streamlit run Scripts/analyst.py
    ;;
  app)
    poetry run python -m Scripts.analyst
    ;;
  *)
    echo "use: ./run.sh [test|streamlit|app]"
    ;;
esac