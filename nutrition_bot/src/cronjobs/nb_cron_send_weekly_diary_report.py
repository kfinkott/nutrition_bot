#kevin fink
#kevin@shorecode.org
#Sept 25 2023
#nutrition_bot/cronjobs/nb_cron_send_weekly_diary._report.py

from datetime import datetime
import json
import sys
import telebot
sys.path.append('..')
import nb_sql_tasks
import nb_sql_reports

passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL')
engine = nb_sql_tasks.engine(passwd, 'nb_diary_cron')

weekly_subscribers = nb_sql_tasks.get_weekly_subscribers('weekly_cron', engine)

user_list = weekly_subscribers.all()

today = datetime.now()
this_week = today.isocalendar().week # gets the numerical week of the year out of 52
this_year = str(today.isocalendar().year)[-2:]  # gets last two digits of year (ex: 2023 = 23)

with open('API_keys.json', 'r', encoding='UTF-8') as fn:
    keys = json.load(fn)
bottoken = keys['bottoken']
bot = telebot.TeleBot(bottoken)

for u in user_list:
    reports = nb_sql_reports.Sql_reports()
    table_name = f'{u[1]}_DD_{str(u[0])}_week{str(this_week)}_year{this_year}'
    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL')
    engine = nb_sql_tasks.engine(passwd, 'nb_diary')
    fn = reports.get_weekly_png(u[0], table_name, this_week, engine)
    bot.send_photo(u[0], open(fn, 'rb'))
