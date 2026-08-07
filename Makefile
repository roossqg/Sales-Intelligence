dash:
	poetry run streamlit run /home/augusto2/Sales_inteligence_dh-api/src/app.py

stats:
	poetry run python -m src.Inference.optimization

dt:
	poetry run python -m src.data_flow

t_data:
	poetry run pytest tests/test_process_data.py