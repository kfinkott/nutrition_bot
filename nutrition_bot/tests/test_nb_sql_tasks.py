# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import nb_sql_tasks
import pandas
import sqlalchemy
import telebot.types
import typing
from hypothesis import given, strategies as st
from pandas import DataFrame
from sqlalchemy import Engine
from telebot.types import CallbackQuery
from typing import Any

# TODO: replace st.nothing() with appropriate strategies


#@given(
    #key=st.one_of(st.binary(), st.text()),
    #backend=st.from_type(typing.Optional[typing.Any]),
#)
#def test_fuzz_Fernet(key: typing.Union[bytes, str], backend: typing.Any) -> None:
    #nb_sql_tasks.Fernet(key=key, backend=backend)


#@given(
    #ing_table=st.from_type(pandas.core.frame.DataFrame),
    #table_name=st.text(),
    #meal_time=st.builds(list),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_add_record(
    #ing_table: pandas.DataFrame,
    #table_name: str,
    #meal_time: list,
    #engine: sqlalchemy.Engine,
#) -> None:
    #nb_sql_tasks.add_record(
        #ing_table=ing_table, table_name=table_name, meal_time=meal_time, engine=engine
    #)


#@given(
    #ing_table=st.text(),
    #userid=st.integers(),
    #username=st.text(),
    #meal=st.text(),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_add_to_diary(
    #ing_table: str, userid: int, username: str, meal: str, engine: sqlalchemy.Engine
#) -> None:
    #nb_sql_tasks.add_to_diary(
        #ing_table=ing_table, userid=userid, username=username, meal=meal, engine=engine
    #)


#@given(
    #ing_table=st.text(),
    #userid=st.integers(),
    #username=st.text(),
    #meal=st.text(),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_add_to_plan(
    #ing_table: str, userid: int, username: str, meal: str, engine: sqlalchemy.Engine
#) -> None:
    #nb_sql_tasks.add_to_plan(
        #ing_table=ing_table, userid=userid, username=username, meal=meal, engine=engine
    #)


#@given(userid=st.integers(), username=st.text(), engine=st.from_type(Engine))
#def test_fuzz_add_weekly_cron_sub(
    #userid: int, username: str, engine: sqlalchemy.Engine
#) -> None:
    #nb_sql_tasks.add_weekly_cron_sub(userid=userid, username=username, engine=engine)


#@given(
    #call=st.from_type(CallbackQuery),
    #weekday=st.text(),
    #table_name=st.text(),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_clear_diary(
    #call: telebot.types.CallbackQuery,
    #weekday: str,
    #table_name: str,
    #engine: sqlalchemy.Engine,
#) -> None:
    #nb_sql_tasks.clear_diary(
        #call=call, weekday=weekday, table_name=table_name, engine=engine
    #)


#@given(
    #call=st.from_type(CallbackQuery),
    #weekday=st.text(),
    #table_name=st.text(),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_clear_plan(
    #call: telebot.types.CallbackQuery,
    #weekday: str,
    #table_name: str,
    #engine: sqlalchemy.Engine,
#) -> None:
    #nb_sql_tasks.clear_plan(
        #call=call, weekday=weekday, table_name=table_name, engine=engine
    #)


@given(text=st.text(), type_=st.none(), is_literal=st.booleans(), _selectable=st.none())
def test_fuzz_column(text, type_, is_literal, _selectable) -> None:
    nb_sql_tasks.column(
        text=text, type_=type_, is_literal=is_literal, _selectable=_selectable
    )


#@given(url=st.nothing())
#def test_fuzz_create_engine(url) -> None:
    #nb_sql_tasks.create_engine(url=url)


#@given(tablename=st.text(), engine=st.from_type(Engine))
#def test_fuzz_create_new_table(tablename: str, engine: sqlalchemy.Engine) -> None:
    #nb_sql_tasks.create_new_table(tablename=tablename, engine=engine)


#@given(engine=st.from_type(Engine))
#def test_fuzz_create_weekly_cron_tables(engine: sqlalchemy.Engine) -> None:
    #nb_sql_tasks.create_weekly_cron_tables(engine=engine)


#@given(env_var=st.text(), passwd_key=st.text())
#def test_fuzz_decrypt_passwd(env_var: str, passwd_key: str) -> None:
    #nb_sql_tasks.decrypt_passwd(env_var=env_var, passwd_key=passwd_key)


#@given(table=st.nothing())
#def test_fuzz_delete(table) -> None:
    #nb_sql_tasks.delete(table=table)


#@given(
    #df=st.from_type(pandas.core.frame.DataFrame),
    #df_title=st.builds(list),
    #engine=st.from_type(Engine),
#)
#def test_fuzz_df_to_sql(
    #df: pandas.DataFrame, df_title: list, engine: sqlalchemy.Engine
#) -> None:
    #nb_sql_tasks.df_to_sql(df=df, df_title=df_title, engine=engine)


#@given(sql_auth=st.nothing(), passwd=st.text(), db=st.text())
#def test_fuzz_engine(sql_auth, passwd: str, db: str) -> None:
    #nb_sql_tasks.engine(sql_auth=sql_auth, passwd=passwd, db=db)


#@given(nutrient_id=st.text(), engine=st.from_type(Engine))
#def test_fuzz_fetch_nutrient_data(nutrient_id: str, engine: sqlalchemy.Engine) -> None:
    #nb_sql_tasks.fetch_nutrient_data(nutrient_id=nutrient_id, engine=engine)


#@given(table_name=st.text(), engine=st.from_type(Engine))
#def test_fuzz_get_weekly_subscribers(
    #table_name: str, engine: sqlalchemy.Engine
#) -> None:
    #nb_sql_tasks.get_weekly_subscribers(table_name=table_name, engine=engine)


#@given(table=st.nothing())
#def test_fuzz_insert(table) -> None:
    #nb_sql_tasks.insert(table=table)


#@given(meal=st.text())
#def test_fuzz_parse_meal(meal: str) -> None:
    #nb_sql_tasks.parse_meal(meal=meal)


#@given(userid=st.integers(), engine=st.from_type(Engine))
#def test_fuzz_remove_weekly_cron(userid: int, engine: sqlalchemy.Engine) -> None:
    #nb_sql_tasks.remove_weekly_cron(userid=userid, engine=engine)


@given(name=st.text())
def test_fuzz_table(name: str) -> None:
    nb_sql_tasks.table(name=name)


@given(text=st.text())
def test_fuzz_text(text: str) -> None:
    nb_sql_tasks.text(text=text)

import unittest
import os
from cryptography.fernet import Fernet
import yaml
import sqlalchemy
from sqlalchemy import text
import env_key

class TestNbSqlTasks(unittest.TestCase):
    with open('nb.yaml', 'r', encoding='UTF-8') as fn:
        config = yaml.safe_load(fn)
    sql_auth = config[0]['mysql_server']
    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
    testing_engine = nb_sql_tasks.engine(sql_auth, passwd, 'testing')
    nutrient_engine = nb_sql_tasks.engine(sql_auth, passwd, 'FNDDS')
    def test_create_new_table(self):
        table_name = 'test'
        test01 = nb_sql_tasks.create_new_table(table_name, self.testing_engine)
        stmt = text('SHOW TABLES;')
        with self.testing_engine.connect() as conn:
            test_tables = conn.execute(stmt)            
        self.assertIn('test', test_tables.all()[0])
        stmt2 = text('DROP TABLE `test`;')
        with self.testing_engine.connect() as conn:
            test_tables = conn.execute(stmt2)

    def test_parse_meal(self):
        value01 = ['d', 'l']
        value02 = ['j', 'd']
        value03 = ['s', 'b']
        test01 = nb_sql_tasks.parse_meal(value01)
        test02 = nb_sql_tasks.parse_meal(value02)
        test03 = nb_sql_tasks.parse_meal(value03)
        self.assertEqual(test01, ['Sunday', 'lunch'])
        self.assertEqual(test02, ['Thursday', 'dinner'])
        self.assertEqual(test03, ['Saturday', 'breakfast'])

    def test_decrypt_passwd(self):
        value01 = 'password'
        key = os.getenv('KEVIN_SQL')
        enc_passwd01 = env_key.encrypt_passwd(passwd=value01, key=key)
        cipher_suite = Fernet(key)
        test_passwd01 = cipher_suite.encrypt(value01.encode()).decode()
        test01 = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', test_passwd01)
        self.assertEqual(test01, value01)

    def test_engine(self):
        passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', self.sql_auth['password_key'])
        test01 = nb_sql_tasks.engine(self.sql_auth, passwd, 'testing')
        stmt = text('SHOW TABLES;')
        with test01.connect() as conn:
            sql_tables = conn.execute(stmt)
        unpacked_tables = []
        for sql_t in sql_tables:
            unpacked_tables.append(sql_t[0])
        self.assertIn('ultimate', unpacked_tables)

    def test_fetch_nutrient_data(self):
        test01 = nb_sql_tasks.fetch_nutrient_data(40, self.nutrient_engine)
        self.assertIsInstance(test01, sqlalchemy.CursorResult)

    def test_add_to_diary(self):
        
if __name__ == '__main__':
    unittest.main()
        
        