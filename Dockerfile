FROM python:3.9-slim

COPY . .

# INSTALL REQUIRED LIBRARIES
RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]







