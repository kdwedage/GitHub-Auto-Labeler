FROM python:3.8.10-slim
COPY Scripts/model_training.py model_training.py
COPY Scripts/model_evaluating.py model_evaluating.py
COPY Scripts/performance_comparison.py performance_comparison.py
COPY requirements.txt requirements.txt
RUN pip3 install -upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3", "model_evaluating.py", "--host=0.0.0.0"]