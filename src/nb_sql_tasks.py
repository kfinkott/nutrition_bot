#kevin fink
#kevin@shorecode.org
#Sept 4 2023
#nutrition_bot/nb_to_sql.py

import os
from datetime import datetime
from typing import Generator
from sqlalchemy import create_engine, text, insert, table, column, delete, select
import sqlalchemy
from cryptography.fernet import Fernet
import pandas as pd
import telebot

today = datetime.now()
this_week = today.isocalendar().week
this_year = today.strftime('%-y') #returns the last two digits of the year (ex: 2023 -> 23)

def create_new_table(tablename: str, engine: sqlalchemy.engine.base.Engine):
    """
    Creates a new table in the SQL server
    
    Args:
    tablename (str) : Name of the SQL table
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect to
    the databse
    
    Returns:
    Does not return
    """
    stmt = f'CREATE TABLE IF NOT EXISTS {tablename} (ID INT NOT NULL AUTO_INCREMENT, \
weekday VARCHAR (20), breakfast VARCHAR (80), lunch VARCHAR (80), dinner VARCHAR (80), \
PRIMARY KEY (ID))'
    with engine.connect() as conn:
        conn.execute(text(stmt))

def add_record(ing_table: pd.DataFrame, table_name: str, meal_time: list,
               engine: sqlalchemy.engine.base.Engine) -> sqlalchemy.CursorResult:
    """
    Adds mealtime data to the SQL database. Checks to see if the data exists first to 
    avoid accidental duplicating.
    
    Args:
    ing_table (pd.DataFrame) : Pandas dataframe that contains the food to be added
    table_name (str) : Name of the SQL table to add the record to
    meal_time (list) : List that contains the meal time(breakfast, lunch, dinner) and the
      day of the week for the meal
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect to
      the databse
    
    Returns:
    Generator[str, None, None]: Returns the SQL result
    """
    stmt1 = f'SELECT {meal_time[1]} FROM {table_name} WHERE `weekday`="{meal_time[0]}"'
    stmt2 = f'UPDATE {table_name} SET `{meal_time[1]}`="{ing_table}" WHERE \
`weekday`="{meal_time[0]}" AND `{meal_time[1]}` IS NULL LIMIT 1'
    stmt3 = f'INSERT INTO {table_name} (`weekday`, `{meal_time[1]}`) VALUES \
("{meal_time[0]}", "{ing_table}")'
    result = None
    with engine.connect() as conn:
        exists = conn.execute(text(stmt1))
        validate = []
        for e in exists.all():
            for e2 in e:
                validate.append(e2)
        if None in validate:
            result = conn.execute(text(stmt2))
        else:
            result = conn.execute(text(stmt3))
        conn.commit()
        return result

def parse_meal(meal: list) -> list:
    """
    Parses the callback data from the inline keyboard into explicit names of the days of
    the week
    
    Args:
    meal (list) : List that contains the day of the week and time of the meal (breakfast,
      lunch, dinner)
    
    Returns:
    list: Returns a list containing the explicit name of the day of the week
    """
    meal_time = []
    if meal[0]  == 'd':
        meal_time.append('Sunday')
    if meal[0]  == 'm':
        meal_time.append('Monday')
    if meal[0]  == 't':
        meal_time.append('Tuesday')
    if meal[0]  == 'w':
        meal_time.append('Wednesday')
    if meal[0]  == 'j':
        meal_time.append('Thursday')
    if meal[0]  == 'f':
        meal_time.append('Friday')
    if meal[0]  == 's':
        meal_time.append('Saturday')
    if meal[1] == 'b':
        meal_time.append('breakfast')
    if meal[1] == 'l':
        meal_time.append('lunch')
    if meal[1] == 'd':
        meal_time.append('dinner')
    return meal_time

def decrypt_passwd(env_var: str, passwd_key: str) -> str:
    """
    Decrypts the SQL password
    
    Args:
    env_var (str) : Linux environment variable name
    passwd_key (str): Encrypted password key
    
    Returns:
    str: Returns the string of the decrypted password
    """
    # Retrieves the encryption key from linux ENV variables.
    # Not secure if more than one person has access to the linux environment
    key = os.getenv(env_var)
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(passwd_key).decode()

def engine(sql_auth, passwd: str, db: str) -> sqlalchemy.Engine:
    """
    Function to create the SQL alchemy class object that is used to connect to SQL
    databases
    
    Args:
    passwd (str) : Password for the SQL database
    db (str) : Name of the SQL database
    
    Returns:
    sqlalchemy.Engine: SQL alchemy engine object, used to connect to the databse
    """
    host = sql_auth['address']
    user = sql_auth['username']
    port = sql_auth['port']
    engine = create_engine(f'mysql://{user}:{passwd}@{host}:{port}/{db}')
    return engine

def df_to_sql(df: pd.DataFrame, df_title: list, engine: sqlalchemy.Engine ):
    """
    Converts a pandas dataframe into a SQL table
    
    Args:
    df (pd.DataFrame) : Pandas dataframe
    df_title (list) : List of titles used for the dataframe. Used here to choose a name
    for the SQL table.
    engine (sqlalchemy.Engine) : SQL alchemy engine object, used to connect to the databse
    
    Returns:
    Does not return
    """
    table_title = df_title[0]
    df.to_sql(table_title, engine, if_exists='replace')

def fetch_nutrient_data(nutrient_id: str,
        engine: sqlalchemy.engine.base.Engine) -> sqlalchemy.engine.cursor.CursorResult:
    """
    Function that gets a nutrient name based on a numeric nutrient ID from a SQL table. 
    THe function then fetches the foods that contain the nutrient from the FNDDS database
    and returns them sorted by the highest nutritional value
    
    Args:
    nutrient_id (str) : Numeric ID representing a nutrient
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect
      to the database
    
    Returns:
    sqlalchemy.engine.cursor.CursorResult: Returns a generator object containing foods
      that contain a specified nutrient sorted by the highest nutritional value
    """
    stmt = f'select nutrient_nbr from nutrients_legend where `index`={nutrient_id};'
    with engine.connect() as conn:
        nutrient_curs = conn.execute(text(stmt))
        nutrient_nbr = float(next(nutrient_curs)[0])
        stmt2 = f'select ingredients.name, ingredients.nutrient_val, nutrients.unit_name,\
nutrients.nutrient_name from ingredients LEFT JOIN nutrients on \
(ingredients.nutrient_id = nutrients.nutrient_nbr) WHERE nutrients.nutrient_nbr\
={nutrient_nbr} ORDER BY (ingredients.nutrient_val) DESC;'
        result = conn.execute(text(stmt2))
    return result

def add_to_diary(ing_table: str, userid: int, username: str, meal: str,
                 engine: sqlalchemy.engine.base.Engine) ->  sqlalchemy.engine.cursor.CursorResult:
    """
    Adds a new entry to the food diary
    
    Args:
    ing_table (str) : Table name of the food item to be added
    userid (int) : Telegram user ID for the user
    username (str) : First name of the Telegram user
    meal (str) : Time of the meal (breakfast, lunch, dinner)
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect\
    to the databse
    
    Returns:
    Generator[str, None, None]: Returns a generator object that contains the SQL returned\
    string
    """
    #meal is 2 digits, ex: ml
    table_name = username + '_DD_' + str(userid) + '_week' + str(this_week) + \
'_year' + str(this_year)
    create_new_table(table_name, engine)
    meal_time = parse_meal(meal)
    result = add_record(ing_table, table_name, meal_time, engine)
    return result

def add_to_plan(ing_table: str, userid: int, username: str, meal: str,
                engine: sqlalchemy.engine.base.Engine) -> sqlalchemy.engine.cursor.CursorResult:
    """
    Adds a new entry to the diet plan SQL table
    
    Args:
    ing_table (str) : Table name of the food item to be added
    userid (int) : Telegram user ID for the user
    username (str) : First name of the Telegram user
    meal (str) : Time of the meal (breakfast, lunch, dinner)
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect 
    to the databse
    
    Returns:
    Generator[str, None, None]:  Returns a generator object that contains the SQL 
      returned string
    """
    table_name = username + '_PP_' + str(userid) + '_week' + str(this_week) + '_year' \
+ str(this_year)
    create_new_table(table_name, engine)
    meal_time = parse_meal(meal)
    result = add_record(ing_table, table_name, meal_time, engine)
    return result

def clear_diary(call: telebot.types.CallbackQuery, weekday: str, table_name: str,
                engine: sqlalchemy.engine.base.Engine) -> bool:
    """
    Erases all diary entries in the SQL table for the specified day of the week
    
    Args:
    call (telebot.types.CallbackQuery) : JSON string that contains the callback data 
      sent to the Telegram API from the inline keyboard
    weekday (str) : Day of the week to be cleared
    table_name (str) : Name of the table to be used (name included user id)
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect 
      to the databse
    
    Returns:
    bool: Returns True if the Delete functions succeeds
    """
    stmt = f'DELETE FROM `{table_name}` WHERE `weekday`="{weekday}";'
    with engine.connect() as conn:
        try:
            conn.execute(text(stmt))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

def clear_plan(call: telebot.types.CallbackQuery, weekday: str, table_name: str,
               engine: sqlalchemy.engine.base.Engine) -> bool:
    """
    Erases all diet plan entries in the SQL table for the specified day of the week
    
    Args:
    call (telebot.types.CallbackQuery) : JSON string that contains the callback data
      sent to the Telegram API from the inline keyboard
    weekday (str) : Day of the week to be cleared
    table_name (str) : Name of the table to be used (name included user id)
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect
      to the databse
    
    Returns:
    bool: Returns True if the Delete functions succeeds
    """
    stmt = f'DELETE FROM `{table_name}` WHERE `weekday`="{weekday}";'
    with engine.connect() as conn:
        try:
            conn.execute(text(stmt))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

def create_weekly_cron_tables(engine: sqlalchemy.engine.base.Engine):
    """
    Creates a table that stores all the Telegram user IDs and usernames for users that 
    request to have a weekly report sent to them
    
    Args:
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect
      to the databse
    
    Returns:
    Does not return
    """
    stmt = 'CREATE TABLE `weekly_cron`(`userid` BIGINT NOT NULL, `username` varchar(255), \
PRIMARY KEY(`userid`));'
    try:
        with engine.connect() as conn:
            conn.execute(text(stmt))
    except sqlalchemy.exc.OperationalError as e:
        print(e)

def add_weekly_cron_sub(userid: int, username: str, engine: sqlalchemy.engine.base.Engine):
    """
    Adds a table entry that specifies the user id and username to send a weekly report to
    
    Args:
    userid (int) : Telegram user ID
    username (str) : first name of the Telegram user
    engine (sqlalchemy.engine.base.Engine) : SQL alchemy engine object, used to connect 
      to the databse
    
    Returns:
    Does not return
    """
    with engine.connect() as conn:
        cron_table = table('weekly_cron', column('userid'), column('username'))
        ins = insert(cron_table).values(userid=userid, username=username)
        conn.execute(ins)
        conn.commit()

def remove_weekly_cron(userid: int, engine: sqlalchemy.engine.base.Engine):
    """
    Removes a user from the weekly report table based on Telegram user ID
    
    Args:
    userid (int) : Telegram user ID
    engine (sqlalchemy.engine.base.Engine) :  SQL alchemy engine object, used to connect
      to the databse
    
    Returns:
    Does not return
    """
    with engine.connect() as conn:
        cron_table = table('weekly_cron', column('userid'), column('username'))
        rem = delete(cron_table).where(cron_table.c.userid==userid)
        conn.execute(rem)
        conn.commit()

def get_weekly_subscribers(table_name: str,
        engine: sqlalchemy.engine.base.Engine) -> sqlalchemy.engine.cursor.CursorResult:
    """
    Retrieves the users that subscribed to receive a weekly report
    
    Args:
    table_name (str) : SQL table to retrieve the data from
    engine (sqlalchemy.engine.base.Engine) :  SQL alchemy engine object, used to connect
    to the databse
    
    Returns:
    sqlalchemy.engine.cursor.CursorResult: Returns the SQL result
    """
    cron_table = table(table_name, column('userid'), column('username'))
    with engine.connect() as conn:
        stmt = select(cron_table)
        users = conn.execute(stmt)
    return users
