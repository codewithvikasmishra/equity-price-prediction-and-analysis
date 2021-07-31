FROM python:3.7

MAINTAINER Vikas Kumar Mishra
COPY requirements.txt ./requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && apt-get install -y apt-utils && apt-get clean -y
RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17 \
    && ACCEPT_EULA=Y apt-get -y install mssql-tools

RUN apt-get install unixodbc-dev  && apt-get clean -y

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . /equity_price_prediction/app
WORKDIR /equity_price_prediction/app

CMD ["flask", "run"]