# Python discord bot for getting messages 

# Configuration

To configure the bot:

1. Adjust settings in the `setting.py` file, following the descriptions within.
3. Create `.env` file based on `.env.example`
4. Configurate [crontab](crontab) file if run with docker
5. Execute the `main.py` file.

# Installation

Install the required libraries by running: `poetry install`

# How to run 
1. `docker compose up -d redis`
2. `python main.py`

# How to run with Docker
`docker compose up -d --build`