# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import nb_sql_reports
import pandas
import pandas.io.formats.style_render
import typing
from hypothesis import given, strategies as st
from pandas import DataFrame, Series
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
##)
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
    #nb_sql_reports.Styler(
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
    #nb_sql_reports.Styler.from_custom_template(
        #searchpath=searchpath, html_table=html_table, html_style=html_style
    #)


#@given(url=st.nothing())
#def test_fuzz_create_engine(url) -> None:
    #nb_sql_reports.create_engine(url=url)


@given(
    cls=st.none(),
    init=st.booleans(),
    repr=st.booleans(),
    eq=st.booleans(),
    order=st.booleans(),
    unsafe_hash=st.booleans(),
    frozen=st.booleans(),
    match_args=st.booleans(),
    kw_only=st.booleans(),
    slots=st.booleans(),
)
def test_fuzz_dataclass(
    cls, init, repr, eq, order, unsafe_hash, frozen, match_args, kw_only, slots
) -> None:
    nb_sql_reports.dataclass(
        cls,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
        match_args=match_args,
        kw_only=kw_only,
        slots=slots,
    )


#@given(
    #function=st.nothing(),
    #iterable=st.one_of(st.iterables(st.integers()), st.iterables(st.text())),
    #initial=st.nothing(),
#)
#def test_fuzz_reduce(function, iterable, initial) -> None:
    #nb_sql_reports.reduce(function, iterable, initial)


@given(text=st.text())
def test_fuzz_text(text: str) -> None:
    nb_sql_reports.text(text=text)

import yaml
import os
import unittest
from sqlalchemy import text
import pandas as pd
import numpy as np
import nb_sql_reports
import nb_sql_tasks

class TestNbSqlReports(unittest.TestCase):
    test_sql_rep = nb_sql_reports.Sql_reports()
    with open('nb.yaml', 'r', encoding='UTF-8') as fn:
        config = yaml.safe_load(fn)
    sql_auth = config[0]['mysql_server']
    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
    reports = nb_sql_reports.Sql_reports()
    engine1 = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
    engine2 = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')
    stmt = text('SHOW TABLES;')
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday']
    with engine1.connect() as conn:
        tables01 = conn.execute(stmt)
    with engine2.connect() as conn:
        tables02 = conn.execute(stmt)
    empty_df = pd.DataFrame()

    def test_get_daily(self):
        for w in self.weekdays:
            test_result01 = self.reports.get_daily(str(self.tables01)[0], w, self.engine1)
            test_result02 = self.reports.get_daily(str(self.tables02)[0], w, self.engine2)
            self.assertIsInstance(test_result02, pd.DataFrame)
            self.assertIsInstance(test_result01, pd.DataFrame)

    def test_get_daily_png(self):
        for w in self.weekdays:
            test_result01 = self.reports.get_daily_png(str(self.tables01)[0], w, self.engine1)
            test_result02 = self.reports.get_daily_png(str(self.tables02)[0], w, self.engine2)
            if test_result01 is not None:
                self.assertTrue(os.path.isfile(test_result01))
            else:
                self.assertIsNone(test_result01)
            if test_result02 is not None:
                self.assertTrue(os.path.isfile(test_result02))
            else:
                self.assertIsNone(test_result02)

    def test_get_weekly(self):
        test_result01 = self.reports.get_weekly(str(self.tables01)[0], self.engine1)
        test_result02 = self.reports.get_weekly(str(self.tables01)[0], self.engine2)
        self.assertIsInstance(test_result01, pd.DataFrame)
        self.assertIsInstance(test_result02, pd.DataFrame)

    def test_get_weekly_png(self):
        test_result01, test_df01 = self.reports.get_weekly_png('test', str(self.tables01)[0], 'test',
                                                    self.engine1)
        test_result02, test_df02 = self.reports.get_weekly_png('test', str(self.tables02)[0], 'test',
                                                    self.engine2)
        self.assertIsInstance(test_df01, pd.DataFrame)
        self.assertIsInstance(test_df02, pd.DataFrame)
        self.assertTrue(os.path.isfile(test_result01))
        self.assertTrue(os.path.isfile(test_result02))

    def test_get_daily_nutrition(self):
        for w in self.weekdays:
            test_df01 = self.reports.get_daily_nutrition(str(self.tables01)[0], w,
                                                    self.engine1, self.engine2)
        self.assertIsInstance(test_df01, pd.DataFrame)

    def test_get_weekly_nutrition(self):
        test01 = self.reports.get_weekly_nutrition('test', str(self.tables01)[0], 'test',
        self.engine1, self.sql_auth)
        test02 = self.reports.get_weekly_nutrition('test', str(self.tables02)[0],'test',
        self.engine1, self.sql_auth)
        self.assertIsInstance(test01, pd.DataFrame)
        self.assertIsInstance(test02, pd.DataFrame)

    def test_get_nutrients_legend_png(self):
        test01 = self.reports.get_nutrients_legend_png(self.sql_auth)
        self.assertTrue(os.path.isfile(test01))

    def test_kevin_divide(self):
        test01 = self.reports.kevin_divide(50,20)
        test02 = self.reports.kevin_divide(10,-3)
        self.assertTrue(test02 is np.nan)
        self.assertEqual(test01, 250)

    def test_group_weekdays_in_df(self):
        value01 = pd.Series(['breakfast', 'dinner', 'lunch'])
        test01 = self.reports.group_weekdays_in_df(value01)
        self.assertEqual(test01, 'breakfast, dinner, lunch')

if __name__ == '__main__':
    unittest.main()        