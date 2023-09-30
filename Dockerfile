FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /Pykan_last_version
COPY ./requierments.txt /Pykan_last_version/

RUN python -m pip install --upgrade pip
RUN pip install -r requierments.txt

COPY . /Pykan_last_version/
