FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["lambda_function.lambda_handler"]