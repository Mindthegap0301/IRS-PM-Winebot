# IRS-Winebot

## Description

We aim to develop a Chatbot system that provides users with ideal wine recommendations through natural language conversations, leveraging extensive wine domain knowledge, advanced algorithms, and data processing techniques. The chatbot will be designed to suggest wines that are most likely to align with the users' preferences. In essence, it will serve as an intuitive wine advisor, bridging the gap between wine enthusiasts and their ideal wine selections.
This innovative system aims to empower consumers, particularly those less experienced in the world of wine, with personalized wine recommendations, enhancing their wine selection experiences and fostering a deeper appreciation of this culturally rich and diverse beverage.

## Installation

To install IRS-Winebot, follow these steps:

1. git clone from https://github.com/Mindthegap0301/IRS-PM-Winebot
2. Install packages from requirements.txt
3. Install PostgreSQL Database
4. If you want to reproduce the results of model training, please install Pytorch 2.1.0 and Cuda 12.1

## Usagec

To use IRS-Winebot, follow these steps:

### database configure

1. cd to .\IRS-Winebot\src\backend
2. create your database locally and configure environment variables using

```
Get-Content .env | ForEach-Object { $_ -split '\n' } | ForEach-Object { [System.Environment]::SetEnvironmentVariable($_.Split('=')[0], $_.Split('=')[1], [System.EnvironmentVariableTarget]::Process) }
```

### Apply migrations (assuming you are in the Flask project directory)

alembic upgrade head # This will import migrations from app.migrations

### Run the seed script

flask seed run

### Run the Flask application

flask run

### Access http://localhost:5000 in your browser
