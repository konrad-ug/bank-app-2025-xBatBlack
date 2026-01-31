[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: Michał

surname: Downarowicz

group: 4

## How to start the app
1. python and docker installed
2. pip install -r requirements.txt
3. docker compose -f mongo.yml up -d
4. python -m flask -app src/app/api.py --debug run

## How to execute tests
1. python -m pytest