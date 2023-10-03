# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import nb_data_viz
import os
import pandas
import pandas.io.formats.style_render
import sqlalchemy
import telebot.types
import typing
from hypothesis import given, strategies as st
from pandas import DataFrame, Series
from pathlib import PurePath
from sqlalchemy import Engine
from telebot.types import CallbackQuery
from typing import Any, Callable

# TODO: replace st.nothing() with appropriate strategies


#@given(
    #data=st.from_type(types.pandas.core.frame.DataFrame | pandas.core.series.Series),
    #precision=st.one_of(st.none(), st.integers()),
    #table_styles=st.one_of(
        #st.none(),
        #st.lists(
            #st.fixed_dictionaries(
                #{
                    #"selector": st.text(),
                    #"props": st.one_of(
                        #st.lists(
                            #st.tuples(st.text(), st.one_of(st.floats(), st.text()))
                        #),
                        #st.text(),
                    #),
                #},
                #optional={},
            #)
        #),
    #),
    #uuid=st.one_of(st.none(), st.text()),
    #caption=st.one_of(st.none(), st.builds(list), st.text(), st.builds(tuple)),
    #table_attributes=st.one_of(st.none(), st.text()),
    #cell_ids=st.booleans(),
    #na_rep=st.one_of(st.none(), st.text()),
    #uuid_len=st.integers(),
    #decimal=st.one_of(st.none(), st.text()),
    #thousands=st.one_of(st.none(), st.text()),
    #escape=st.one_of(st.none(), st.text()),
    #formatter=st.from_type(
        #typing.Union[
            #str,
            #typing.Callable,
            #typing.Dict[typing.Any, typing.Union[str, typing.Callable, NoneType]],
            #NoneType,
        #]
    #),
#)
#def test_fuzz_Styler(
    #data: typing.Union[pandas.DataFrame, pandas.Series],
    #precision: typing.Union[int, None],
    #table_styles: typing.Optional[typing.List[pandas.io.formats.style_render.CSSDict]],
    #uuid: typing.Union[str, None],
    #caption: typing.Union[str, tuple, list, None],
    #table_attributes: typing.Union[str, None],
    #cell_ids: bool,
    #na_rep: typing.Union[str, None],
    #uuid_len: int,
    #decimal: typing.Union[str, None],
    #thousands: typing.Union[str, None],
    #escape: typing.Union[str, None],
    #formatter: typing.Union[
        #str,
        #typing.Callable,
        #typing.Dict[typing.Any, typing.Union[str, typing.Callable, None]],
        #None,
    #],
#) -> None:
    #nb_data_viz.Styler(
        #data=data,
        #precision=precision,
        #table_styles=table_styles,
        #uuid=uuid,
        #caption=caption,
        #table_attributes=table_attributes,
        #cell_ids=cell_ids,
        #na_rep=na_rep,
        #uuid_len=uuid_len,
        #decimal=decimal,
        #thousands=thousands,
        #escape=escape,
        #formatter=formatter,
    #)


#@given(
    #searchpath=st.one_of(st.text(), st.builds(list)),
    #html_table=st.one_of(st.none(), st.text()),
    #html_style=st.one_of(st.none(), st.text()),
#)
#def test_fuzz_Styler_from_custom_template(
    #searchpath, html_table: typing.Union[str, None], html_style: typing.Union[str, None]
#) -> None:
    #nb_data_viz.Styler.from_custom_template(
        #searchpath=searchpath, html_table=html_table, html_style=html_style
    #)


@given(
    flags=st.just([]),
    size=st.just((None, None)),
    quality=st.none(),
    delay=st.none(),
    config=st.none(),
    params=st.just({}),
)
def test_fuzz_WebShot(flags, size, quality, delay, config, params) -> None:
    nb_data_viz.WebShot(
        flags=flags,
        size=size,
        quality=quality,
        delay=delay,
        config=config,
        params=params,
    )


#@given(
    #photo1=st.builds(PurePath, st.text()),
    #photo2=st.builds(PurePath, st.text()),
    #photo3=st.builds(PurePath, st.text()),
#)
#def test_fuzz_collate_3photos(
    #photo1: os.PathLike, photo2: os.PathLike, photo3: os.PathLike
#) -> None:
    #nb_data_viz.collate_3photos(photo1=photo1, photo2=photo2, photo3=photo3)


#@given(photo1=st.builds(PurePath, st.text()), photo2=st.builds(PurePath, st.text()))
#def test_fuzz_collate_photos(photo1: os.PathLike, photo2: os.PathLike) -> None:
    #nb_data_viz.collate_photos(photo1=photo1, photo2=photo2)


#@given(engine=st.from_type(Engine))
#def test_fuzz_create_nutrients_units_legend(engine: sqlalchemy.Engine) -> None:
    #nb_data_viz.create_nutrients_units_legend(engine=engine)


#@given(df=st.from_type(pandas.core.frame.DataFrame))
#def test_fuzz_create_nutrients_units_legend_png(df: pandas.DataFrame) -> None:
    #nb_data_viz.create_nutrients_units_legend_png(df=df)


#@given(
    #call=st.from_type(CallbackQuery),
    #html=st.builds(PurePath, st.text()),
    #css=st.text(),
    #week=st.text(),
#)
#def test_fuzz_export_html_to_png(
    #call: telebot.types.CallbackQuery, html: os.PathLike, css: str, week: str
#) -> None:
    #nb_data_viz.export_html_to_png(call=call, html=html, css=css, week=week)


#@given(
    #df=st.from_type(pandas.core.frame.DataFrame),
    #df_title=st.builds(list),
    #page2=st.booleans(),
#)
#def test_fuzz_export_nut_search_png(
    #df: pandas.DataFrame, df_title: list, page2: bool
#) -> None:
    #nb_data_viz.export_nut_search_png(df=df, df_title=df_title, page2=page2)


#@given(
    #df=st.from_type(pandas.core.frame.DataFrame),
    #df_title=st.builds(list),
    #page2=st.booleans(),
#)
#def test_fuzz_export_png(df: pandas.DataFrame, df_title: list, page2: bool) -> None:
    #nb_data_viz.export_png(df=df, df_title=df_title, page2=page2)


#@given(
    #call=st.from_type(CallbackQuery),
    #table_name=st.text(),
    #week=st.text(),
    #engine=st.from_type(Engine),
    #sql_auth=st.nothing(),
#)
#def test_fuzz_nutrient_report_chart(
    #call: telebot.types.CallbackQuery,
    #table_name: str,
    #week: str,
    #engine: sqlalchemy.Engine,
    #sql_auth,
#) -> None:
    #nb_data_viz.nutrient_report_chart(
        #call=call, table_name=table_name, week=week, engine=engine, sql_auth=sql_auth
    #)


@given(text=st.text())
def test_fuzz_text(text: str) -> None:
    nb_data_viz.text(text=text)


#@given(
    #call=st.from_type(CallbackQuery),
    #table_name=st.text(),
    #week=st.text(),
    #engine=st.from_type(Engine),
    #sql_auth=st.nothing(),
#)
#def test_fuzz_weekly_dv_chart(
    #call: telebot.types.CallbackQuery,
    #table_name: str,
    #week: str,
    #engine: sqlalchemy.Engine,
    #sql_auth,
#) -> None:
    #nb_data_viz.weekly_dv_chart(
        #call=call, table_name=table_name, week=week, engine=engine, sql_auth=sql_auth
    #)

import os
import shutil
import yaml
import unittest
import pandas as pd
import numpy as np
import nb_data_viz
import nb_sql_tasks

class TestNbDataViz(unittest.TestCase):
    test_df = pd.DataFrame()
    test_html = test_df.to_html()
    test_html_fn = 'test_input_files/test.html'
    with open(test_html_fn, 'w', encoding='UTF-8') as fn:
        fn.write(test_html)
    test_title = ['test_title', 'test_title2']
    test_img1 = 'test_input_files/img1.png'
    test_img2 = 'test_input_files/img2.png'
    test_img3 = 'test_input_files/img3.png'
    with open('nb.yaml', 'r', encoding='UTF-8') as fn:
        config = yaml.safe_load(fn)
    sql_auth = config[0]['mysql_server']    
    
    def test_export_png(self):
        test_img_fn = nb_data_viz.export_png(self.test_df, self.test_title)
        self.assertTrue(os.path.isdir('dataviz'))
        self.assertTrue(os.path.isfile(test_img_fn))

    def test_export_nut_search_png(self):
        test_img_fn = nb_data_viz.export_nut_search_png(self.test_df, self.test_title)
        self.assertTrue(os.path.isdir('dataviz'))
        self.assertTrue(os.path.isfile(test_img_fn))

    def test_collate_photos(self):
        shutil.copy(self.test_img1, 'tmp_img1.png')
        shutil.copy(self.test_img2, 'tmp_img2.png')      
        test_img_fn = nb_data_viz.collate_photos('tmp_img1.png', 'tmp_img2.png')
        self.assertTrue(os.path.isfile(test_img_fn))

    def test_collate_3photos(self):
        shutil.copy(self.test_img1, 'tmp_img1.png')
        shutil.copy(self.test_img2, 'tmp_img2.png')
        shutil.copy(self.test_img3, 'tmp_img3.png')
        test_img_fn = nb_data_viz.collate_3photos('tmp_img1.png', 'tmp_img2.png', 'tmp_img3.png')
        self.assertTrue(os.path.isfile(test_img_fn))

    def test_export_html_to_png(self):
        test_img_fn = nb_data_viz.export_html_to_png('test_call', self.test_html_fn, css='', week=np.random.randint(52))
        self.assertTrue(os.path.isdir('dataviz'))
        self.assertTrue(os.path.isfile(test_img_fn))

    def test_create_nutrients_units_legend(self):
        passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', self.sql_auth['password_key'])
        test_engine = nb_sql_tasks.engine(self.sql_auth, passwd, 'nb_ing')
        test_df = nb_data_viz.create_nutrients_units_legend(test_engine)
        self.assertIsInstance(test_df, pd.DataFrame)

    def test_create_nutrients_units_legend_png(self):
        test_img_fn = nb_data_viz.create_nutrients_units_legend_png(self.test_df)
        self.assertTrue(os.path.isfile(test_img_fn))

if __name__ == '__main__':
    unittest.main()