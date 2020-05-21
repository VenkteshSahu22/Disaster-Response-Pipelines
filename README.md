# Disaster-Response-Pipelines

 ### Libraries needed:

Pandas,
Numpy,
Scikitlearn,
Flask,
SQL Alchemy,
Plotly,
NLTK,


### Files
The project is divided into 3 folders: one for data and data processing; another one is for building a machine learning pipeline; and the third is for the web app.

#### Files in the Data Folder
1. Messages data: disaster_messages.csv
2. Categories data: disaster_categories.csv
3. SQL Database: DisasterResponse.db
4. Python script for processing the data: process_data.py
5. A file that counts words:counts.npz
#### Files in the Models Folder

1. Python script for training the classifier: train_classifier.py
2. A pickle file that contains the trained model: classifier.pkl
#### Files in the App Folder
Python script for running the web app: run.py
templates folder that contains 2 HTML files for the app front-end: go.html and master.html

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

####  The main findings of the code can be found at the [repo](https://github.com/VenkteshSahu22/Disaster-Response-Pipelines/) available here.


### Screenshots



![Alt text](https://github.com/VenkteshSahu22/Disaster-Response-Pipelines/blob/master/Screenshot%20(29).png)


![Alt text](https://github.com/VenkteshSahu22/Disaster-Response-Pipelines/blob/master/Screenshot%20(28).png)

![Alt text](https://github.com/VenkteshSahu22/Disaster-Response-Pipelines/blob/master/Screenshot%20(27).png)
