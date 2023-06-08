# Apartment_Price_Prediction
This repository contains code related to apartment data extraction and analysis. It consists of three files: `Apartment_Data_Extraction.py`, `Apartment_INFO.csv`, and `Apartment_Price_Prediction.ipyn`.

## `Apartmen_Data_Extraction.py`
The `Apartment_Data_Extraction.py` file contains Python code that extracts data related to apartments from the [Divar](/divar.ir/s/tehran/buy-apartment)
 website and saves it to a MySQL database named `DB_APT_Info`. The script extracts information such as apartment area, build date, number of rooms, parking availability, etc.

## `Apartment_INFO.csv`
The `Apartment_INFO.csv` file contains information about apartments that was extracted using `Apartment_Data_Extraction.py`. This file is used for apartment price prediction in the `Apartment_Price_Prediction.ipynb` notebook.

## `Apartment_Price_Prediction.ipynb`
The `Apartment_Price_Prediction.ipynb` notebook contains Python code that predicts apartment prices based on features such as area, build date, number of rooms, parking availability, etc. The notebook uses the `Apartment_INFO.csv` file as input, preprocesses the data, trains a linear regression model on the training set, and evaluates the model on the testing set. Finally, the notebook makes a prediction for a new input using the trained model.

## Dependencies
* Python 3.6 or higher
* requests library
* re library
* beautifulsoup4 library
* mysql-connector-python library
* pandas library
* numpy library
* scikit-learn library
* matplotlib library
