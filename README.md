# fastAPIPlayground

# Summary
This is an API built using Fast API and PyMySQL from data on John Hopkins Github about Corona Virus statistics. This is hosted on Google Cloud, and is updated on a chron job to keep the data up to date. 

# Link: https://api-app-pjblaypjta-uc.a.run.app/docs
Note - This link was updated on 6.20.2020 and any previous links to the API are no longer valid. 

# To run
FastAPI/s '/docs' route takes you to an interactive API that makes it easy to explore and test the routes. For a full article to explore the functionality of FastAPI, see this article https://itnext.io/building-a-data-api-with-fastapi-and-sqlalchemy-a36baf247120

# Update Frequency
Due to the size of the database and the cost of running on gcloud, the chron jobs have been temporarily disabled on this application. 

# Data Sources
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
https://data.worldbank.org/indicator/sp.pop.65up.to.zs
