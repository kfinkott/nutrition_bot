# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from hypothesis import given, strategies as st
import nb_api_fetch
import nb_recipe_tasks
from nb_api_fetch import Nb_api


@given(nb_api=st.builds(Nb_api, token=st.text()))
def test_fuzz_RecipeSearch(nb_api: nb_api_fetch.Nb_api) -> None:
    nb_recipe_tasks.RecipeSearch(nb_api=nb_api)


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
    nb_recipe_tasks.dataclass(
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

import yaml
import requests
import unittest

with open('nb.yaml', 'r', encoding='UTF-8') as fn:
    config = yaml.safe_load(fn)
sql_auth = config[0]['mysql_server']
nb_api = nb_api_fetch.Nb_api(config[1]['spoonacular_api_key'])

class TestNbRecipeTasks(unittest.TestCase):
    recipe_test = nb_recipe_tasks.RecipeSearch(nb_api=nb_api)
    def test_recipe_search(self):
        tests = [self.recipe_test.recipe_search(''), self.recipe_test.recipe_search('taco'),
                 self.recipe_test.recipe_search('mashed potato')]
        for t in tests:
            self.assertIsInstance(t, dict)

    def test_ing_search(self):
        tests = [self.recipe_test.ing_search('bean'),
                 self.recipe_test.ing_search('green onion')]
        for t in tests:
            self.assertIsInstance(t, list)

    def test_nutrient_search(self):
        tests = [self.recipe_test.nutrient_search('minVitaminB2'),
                 self.recipe_test.nutrient_search('minCalcium')]
        for t in tests:
            self.assertIsInstance(t, list)

    def test_id_search(self):
        test01, title01 = self.recipe_test.id_search('634434')
        test02, title02 = self.recipe_test.id_search(634434)
        self.assertIsInstance(test01, requests.Response)
        self.assertIsInstance(test02, requests.Response)
        self.assertIsInstance(title01, list)
        self.assertIsInstance(title02, list)

    def test_get_recipe_card(self):
        test01 = self.recipe_test.get_recipe_card('634434')
        self.assertIsInstance(test01, dict)

if __name__ == '__main__':
    unittest.main()