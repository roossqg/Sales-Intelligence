dash:
	poetry run streamlit run /home/augusto2/Sales_inteligence_dh-api/src/app.py

dh:
	poetry run streamlit run /home/augusto2/Sales_inteligence_dh-api/src/main.py

stats:
	poetry run python -m src.Inference.optimization

dt:
	poetry run python -m src.Inference.forecasting

t_data:
	poetry run pytest tests/test_process_data.py

t_fr:
	poetry run pytest tests/test_forecast.py

dt1:
	poetry run streamlit run /home/augusto2/Sales_inteligence_dh-api/app_copy.py
