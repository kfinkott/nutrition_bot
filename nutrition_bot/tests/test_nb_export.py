import unittest
import os
import pandas as pd
import nb_export

class TestNbExport(unittest.TestCase):
    empty_df = pd.DataFrame()
    def test_to_csv(self):
        test01 = nb_export.to_csv('34', self.empty_df, 'test')
        self.assertTrue(os.path.isfile(test01))

    def test_to_xcel(self):
        test01 = nb_export.to_xcel('345', self.empty_df, 'test')
        self.assertTrue(os.path.isfile(test01))

    def test_to_html(self):
        test01 = nb_export.to_html('345', self.empty_df, 'test')
        self.assertTrue(os.path.isfile(test01))

    def test_to_json(self):
        test01 = nb_export.to_json('345', self.empty_df, 'test')
        self.assertTrue(os.path.isfile(test01))

    def test_zip_all(self):        
        test01 = nb_export.zip_all('234', *os.listdir())
        self.assertTrue(os.path.isfile(test01))
