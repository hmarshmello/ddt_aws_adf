FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a symbolic link to the ddt_aws_adf package
RUN ln -s /ddt_aws_adf /app/ddt_aws_adf

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
