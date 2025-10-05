
FROM python:3.13-slim-bookworm


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install "fastapi[standard]"
RUN pip install langchain_chroma  
COPY ./app /code/app


CMD ["uvicorn", "app.apphandler:app", "--host", "0.0.0.0", "--port", "80"]
