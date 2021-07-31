# equity-price-prediction-and-analysis
Creating a machine learning model for prediction of equity price from NSE dataset.

<!-- What is the problem statement? -->
We are trying to predict the equity/share price from NSE data set (https://www.nseindia.com/).

<!-- Challenges -->
It provides the data on daily basis, i.e. you can not fetch the data for a whole year or given range. You need to go day by day basis from below link.
"https://archives.nseindia.com/products/content/sec_bhavdata_full_01012020.csv"

Also, you need to eliminate staurday, sunday and Bank holidays from it, else it will stop working there.

<!-- Steps followed -->

<!-- Created a MSSQL database connection using Docker and container. -->
I have used microsoft docker database to establish the connection between my SQL server on prem and docker. I have not used pre defined docker images as its not a good behavior in productionize code.

<!-- How I kept all data in my on prem sql database -->
I created a python API using flask to get all data for a year where you need to pass the year and bank holidays.
Also, I created an API to store the data on daily basis if required, where you need to pass the date only.

EDA and Model building is left now where I am working now.

