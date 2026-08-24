app:
	poetry run streamlit run /home/augusto2/Sales_inteligence_dh-api/src/app/main.py

#tests
tests_data:
	poetry run pytest tests/test_process_data.py

tests_forecast:
	poetry run pytest tests/test_forecast.py

tests_optimization:
	poetry run pytest tests/tests_optimization.py

tests_stats:
	poetry run pytest tests/test_statistics.py
