#Hypothesis test commented out
## This test code was written by the `hypothesis.extra.ghostwriter` module
## and is provided under the Creative Commons Zero public domain dedication.

#import markup_keyboards
#import typing
#from hypothesis import given, strategies as st
#from typing import Any


#@given(keyboard=st.none(), row_width=st.just(3))
#def test_fuzz_InlineKeyboardMarkup(keyboard, row_width) -> None:
    #markup_keyboards.InlineKeyboardMarkup(keyboard=keyboard, row_width=row_width)


#@given(json_string=st.text())
#def test_fuzz_InlineKeyboardMarkup_de_json(json_string) -> None:
    #markup_keyboards.InlineKeyboardMarkup.de_json(json_string=json_string)


#@given(df_title=st.text())
#def test_fuzz_choose_diary_meal(df_title: str) -> None:
    #markup_keyboards.choose_diary_meal(df_title=df_title)


#@given(df_title=st.text())
#def test_fuzz_choose_plan_meal(df_title: str) -> None:
    #markup_keyboards.choose_plan_meal(df_title=df_title)


#@given(
    #values=st.from_type(typing.Dict[str, typing.Dict[str, typing.Any]]),
    #row_width=st.integers(),
#)
#def test_fuzz_quick_markup(
    #values: typing.Dict[str, typing.Dict[str, typing.Any]], row_width: int
#) -> None:
    #markup_keyboards.quick_markup(values=values, row_width=row_width)


#@given(api_response=st.builds(list))
#def test_fuzz_recipe_choice(api_response: list) -> None:
    #markup_keyboards.recipe_choice(api_response=api_response)


#@given(df_title=st.builds(list))
#def test_fuzz_submit_ing(df_title: list) -> None:
    #markup_keyboards.submit_ing(df_title=df_title)

import unittest
import markup_keyboards as mk
from telebot.types import InlineKeyboardMarkup as InlineKey

class TestMarkupKeyboards(unittest.TestCase):
    def test_main_keys(self):
        test_object01 = mk.main_keys()
        self.assertIsInstance(test_object01, InlineKey)
        
    def test_ing_unit(self):
        test_object01 = mk.ing_unit()
        self.assertIsInstance(test_object01, InlineKey)

    def test_nutrients(self):
        test_object01 = mk.nutrients()
        self.assertIsInstance(test_object01, InlineKey)

    def test_more_nut(self):
        test_object01 = mk.more_nut()
        self.assertIsInstance(test_object01, InlineKey)

    def test_submit_ing(self):
        test_object01 = mk.submit_ing(['test df title'])
        self.assertIsInstance(test_object01, InlineKey)

    def test_choose_diary_meal(self):
        test_object01 = mk.choose_diary_meal(['test df title'])
        self.assertIsInstance(test_object01, InlineKey)

    def test_choose_plan_meal(self):
        test_object01 = mk.choose_plan_meal(['test df title'])
        self.assertIsInstance(test_object01, InlineKey)

    def test_view_diary(self):
        test_object01 = mk.view_diary()
        self.assertIsInstance(test_object01, InlineKey)

    def test_view_plan(self):
        test_object01 = mk.view_plan()
        self.assertIsInstance(test_object01, InlineKey)

    def test_diary_choose_weekday(self):
        test_object01 = mk.diary_choose_weekday()
        self.assertIsInstance(test_object01, InlineKey)

    def test_plan_choose_weekday(self):
        test_object01 = mk.plan_choose_weekday()
        self.assertIsInstance(test_object01, InlineKey)

    def test_diary_choose_week(self):
        test_object01 = mk.diary_choose_week()
        self.assertIsInstance(test_object01, InlineKey)

    def test_plan_choose_week(self):
        test_object01 = mk.plan_choose_week()
        self.assertIsInstance(test_object01, InlineKey)

    def test_diary_nut_choose_week(self):
        test_object01 = mk.diary_nut_choose_week()
        self.assertIsInstance(test_object01, InlineKey)

    def test_plan_nut_choose_week(self):
        test_object01 = mk.plan_nut_choose_week()
        self.assertIsInstance(test_object01, InlineKey)

    def test_request_legend(self):
        test_object01 = mk.request_legend()
        self.assertIsInstance(test_object01, InlineKey)

    def test_nutrition_choice(self):
        test_object01 = mk.nutrition_choice()
        self.assertIsInstance(test_object01, InlineKey)

    def test_clear_diary_wkday(self):
        test_object01 = mk.clear_diary_wkday()
        self.assertIsInstance(test_object01, InlineKey)

    def test_recipe_search_choice(self):
        test_object01 = mk.recipe_search_choice()
        self.assertIsInstance(test_object01, InlineKey)

    def test_recipe_choice(self):
        test_api_response = [{'title': 'test', 'id': 1}]
        test_object01 = mk.recipe_choice(test_api_response)
        self.assertIsInstance(test_object01, InlineKey)

    def test_recipe_n(self):
        test_object01 = mk.recipe_n()
        self.assertIsInstance(test_object01, InlineKey)



if __name__ == '__main__':
    unittest.main()