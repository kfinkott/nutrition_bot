#kevin fink
#kevin@shorecode.org
#Sept 4 2023
#nutrition_bot/nb.py

#todo
#add to portfolio: video, screenshots, fanfare! include bandit passes

#offer to health canada (explain webhook, offer implementation)

import yaml
import nb_telegram_bot

# Loads the API keys from the YAML file into the program
with open('nb.yaml', 'r', encoding='UTF-8') as stream:
    try:
        result = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

sql_auth = result[0]['mysql_server']
spoon_token = result[1]['spoonacular_api_key']
bottoken = result[2]['telegram_bot_api_key']

nb_telegram_bot.create_bot(bottoken, spoon_token, sql_auth)
