# Final Project - Bike Sharing
## Description
The final project of dicoding "Belajar Analisis Data dengan Python" this project analyzed the bike rental system. 

## Table of Contents
1. [File Structure](#File-Structure)
2. [Installation](#Installation)
  

## File Structure
submission
├───dashboard
| ├───all_data.csv
| └───dashboard.py
├───data
| ├───day.csv
| └───hour.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

## Installation
To run this project locally, follow these steps:

**For notebook.ipynb:**
1. Download this project.
2. Launch your IDE such as Jupyter Notebook or Google Colaboratory.
3. Upload the notebook file with a .ipynb extension that you have downloaded from this project.
4. If you are using Google Colab, click on the "Connect" button to connect to the hosted runtime.
5. Execute the code cells in the notebook to analyze and visualize this project. 

**For dashboard.py:**

1. Download this project.
2. Open your terminal or command prompt and install Streamlit along with other required libraries using the following commands: 

```bash
pip install streamlit pandas numpy scipy matplotlib seaborn
```
3. Ensure not to relocate the CSV file as it serves as the data source. Keep it in the same folder as your dashboard.py.
4. Launch VSCode and navigate to the terminal.
5. Execute the following command in the terminal to run the Streamlit dashboard:

```bash
streamlit run dashboard.py
```
This will launch the Bike Sharing Dashboard in your default web browser.
