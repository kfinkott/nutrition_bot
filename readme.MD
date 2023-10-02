# Nutrition Bot
A telegram bot that feeds the user nutrition data

***
This project is made possible by the available nutrient data in the [fooddb](www.foodb.ca)  database 

and

[The United States Department of Agriculture](https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fndds/) 

***

The Spoonacular API and Telegram API were used to create this bot

[https://spoonacular.com/food-api](https://spoonacular.com/food-api)  
[https://core.telegram.org/bots/api](https://core.telegram.org/bots/api) 


***
####  How to use this? (Linux)
1 - Install dependencies:  
pip install requirements.txt  
2 - [Get a Spoonacular API key](https://spoonacular.com/food-api)  
3 - [Create a Telegram bot and get a Telegram Bot API key](https://core.telegram.org/bots/tutorial)  
4 - [Setup a mysql server](https://dev.mysql.com/doc/mysql-getting-started/en/)   
5 - Create the 'nb.yaml' configuration file using 'src/nb_create_yaml.py'  
6 - Run 'src/cronjobs/nb_create_weekly_cron_jobs.py'  
6 - Run 'src/nb_main.py'

***
This project was created using the Wing IDE. The project file is 'nutrition_bot.wpr'

***
Created by the team @ https://www.shorecode.org
