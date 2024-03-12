# Assistants GPT

Create and manage Open AI assistants. 

## Introduction

I am sharing the prototype as I decided to pursue other opportunities.
The objective was to create a SaaS platform for companies needing "Custom GPTs". 
The prototype is made in a way that easily allows white-labeling. 

Feel free to use the code the way you want 🤝


## Repo presentation

1. Backend: Coded in Python. Uses Fast API. The database is PostgreSQL and all the queries are written in SQL.
2. Frontend: Vite JS.

- To initialize and clear the DB: admin_initdb.py and admin_cleardb.py
- The Fast API routes are in app.py. The classes are in app_classes.py
- All the functions to manage Open AI assistants are in ast_base.py and ast_main.py
- All db functions are in ast_db_base.py and ast_db.py
- Configurations and Support functions are in the modules called config.py and utilities.py

## Video of the prototype

[![Youtube video](https://img.youtube.com/vi/CbrtrumQj84/maxresdefault.jpg)](https://www.youtube.com/watch?v=CbrtrumQj84)


### 🚨 Code is no longer maintained since the 10th of January 2024 ###


### 2023 Open AI performance issues ###
The assistants do not consistently provide answers to the attached documents. The issue seems known in the OAI community. 

"Says that the issue exists and that some files are sometimes not found":
  Nov 23 - [Link Open AI Community](https://community.openai.com/t/assistant-api-retriever-sometimes-cannot-read-pdf/481692/2)
  Dec 23 - [Link Open AI Community](https://community.openai.com/t/inconsistent-file-access-using-assistant-api/552352)

"Says that JSON files are less reliable than regular TXT" 
  Nov 23 - [Link Open AI Community](https://community.openai.com/t/using-assistant-api-retrieval-hallucinates/491857)

"Says that the issue occurs about 10% of the time" 
  Dec 23 [Link Open AI Community](https://community.openai.com/t/inconsistent-file-access-in-assistant-api/540213/3)

