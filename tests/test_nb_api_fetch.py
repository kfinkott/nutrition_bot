# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import yaml
import requests
from typing import TypeVar
import numpy as np
import unittest
from hypothesis import given, strategies as st
import pandas as pd
import nb_api_fetch

@given(token=st.text())
def test_fuzz_Nb_api(token: str) -> None:
    nb_api_fetch.Nb_api(token=token)

class TestNbApiFetch(unittest.TestCase):
    with open('nb.yaml', 'r', encoding='UTF-8') as fn:
        config = yaml.safe_load(fn)
    sql_auth = config[0]['mysql_server']
    class_obj = nb_api_fetch.Nb_api(config[1]['spoonacular_api_key'])
    
    def test_validate_ingred(self):        
        test_ing = ['carrot',['green', 'pepper'], ['the', 'carrot']]
        tested = [self.class_obj.validate_ingred(t) for t in test_ing]
        for r in tested:
            self.assertIsInstance(r, int)
            
    def test_clean_query(self):
        test_query = '(test) to:remove, "punctuation"'
        tested = self.class_obj.clean_query(test_query)
        self.assertEqual(tested, ['test', 'to', 'remove', 'punctuation'])
        
    def test_fetch_whole_food(self):
        tested01 = self.class_obj.fetch_whole_food('green pepper', 100, 'g')
        tested02 = self.class_obj.fetch_whole_food('', 100, 'g')
        tested03 = self.class_obj.fetch_whole_food('rotten poop', 200, 'p')
        self.assertIsInstance(tested01, dict)
        self.assertIsNone(tested02)
        self.assertIsNone(tested03)        

    def test_clean_response(self):
        response = self.class_obj.fetch_whole_food('green pepper', 100, 'g')
        tested = self.class_obj.clean_response(response)
        self.assertIsInstance(tested, list)    

    def test_create_dataframes(self):
        self.class_obj.food_result = self.class_obj.clean_response(
            self.class_obj.fetch_whole_food('green pepper', 100, 'g'))
        tested_df1, tested_df2, tested_dftitle = self.class_obj.create_dataframes(self.sql_auth)
        self.assertIsInstance(tested_df1, pd.DataFrame)
        self.assertIsInstance(tested_df2, pd.DataFrame)
        self.assertIsInstance(tested_dftitle, list)

    def test_fetch_recipes(self):
        tested = self.class_obj.fetch_recipes('banana', 12, self.class_obj.token)
        self.assertIsInstance(tested, dict)

    def test_fetch_recipe_by_ing(self):
        tested = self.class_obj.fetch_recipe_by_ing('tomato', 12, self.class_obj.token)
        self.assertIsInstance(tested, list)

    def test_fetch_recipe_by_nutrient(self):
        tested = self.class_obj.fetch_recipe_by_nutrient('minVitaminC', 12, self.class_obj.token)
        self.assertIsInstance(tested, list)

    def test_fetch_recipe_id(self):
        tested = self.class_obj.fetch_recipe_id('634434', self.class_obj.token)
        self.assertIsInstance(tested, requests.Response)

    def fetch_recipe_title(self):
        tested = self.class_obj.fetch_recipes_title('634434', self.class_obj.token)
        self.assertIsInstance(tested, list)

    def test_fetch_recipe_card(self):
        tested = self.class_obj.fetch_recipe_card('634434', self.class_obj.token)
        self.assertIsInstance(tested, dict)
        
if __name__ == '__main__':
    unittest.main()