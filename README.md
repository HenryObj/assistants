# Assistants GPT

👋

This is a prototype. 
I am sharing it as I decided to pursue other opportunities.

The goal was to create a SaaS platform designed for easy white-labeling. 
This SaaS platform was destined to companies needing "Custom GPTs".

It is no longer maintained since the 10th of Jan.
Feel free to use the code the way you want 🤝


## Last Code update - 10th of January 2024

## Introduction
This repo is a SaaS to allow companies to have and manage their own custom GPT (assistants).

The product is comprised of:
1. An API, coded in Python and using Fast API. The database is PostgreSQL and all the queries were written in SQL.
2. The front-end, using Vite JS.

## File presentation
- To initialize and clear the DB: admin_initdb.py and admin_cleardb.py
- The Fast API routes are in app.py. The classes are in app_classes.py
- All the functions to manage Open AI assistants are in ast_base.py and ast_main.py
- All db functions are in ast_db_base.py and ast_db.py
- Configurations and Support functions are in the modules called config.py and utilities.py

## Video of the prototype

[![Youtube video](https://img.youtube.com/vi/CbrtrumQj84/maxresdefault.jpg)](https://www.youtube.com/watch?v=CbrtrumQj84)


### 2023 Open AI performance issues ###
The assistants are not consistently providing answers to the documents attached. The issue seems known in the OAI community. 
We need to monitor this and if the issue persists, we will move to an internally developed RAG. 

"Says that the issue exists and that some files are sometimes not found":
  Nov 23 - [Link Open AI Community](https://community.openai.com/t/assistant-api-retriever-sometimes-cannot-read-pdf/481692/2)
  Dec 23 - [Link Open AI Community](https://community.openai.com/t/inconsistent-file-access-using-assistant-api/552352)

"Says that JSON files are less reliable than regular TXT" 
  Nov 23 - [Link Open AI Community](https://community.openai.com/t/using-assistant-api-retrieval-hallucinates/491857)

"Says that the issue occurs about 10% of the time" 
  Dec 23 [Link Open AI Community](https://community.openai.com/t/inconsistent-file-access-in-assistant-api/540213/3)

