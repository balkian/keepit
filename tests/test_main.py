import sys
import os
import subprocess
from unittest import TestCase

from keepit import keepit, diff, hash_df
from keepit.backends import Pickle

import pandas as pd

# df = pd.DataFrame([[0, 'hola', True, None], [1, 'adiós', False, 5]], columns=['int', 'str', 'bool', 'other'])

this_directory = os.path.abspath(os.path.dirname(__file__))


count = 0

@keepit()
def prueba(first, name='something', value=29):
    global count
    count += 1
    return pd.DataFrame([[count, first, name, value], ], columns=['time', 'first', 'name', 'value'])


@keepit()
def prueba_df():
    return pd.read_csv(os.path.join(this_directory, 'test.tsv'), sep='\t')


@keepit()
def prueba_df_argument(df):
    return count


class TestMain(TestCase):


    def setUpClass():
        back = Pickle()
        back.erase_all()
        assert not back.find()
        assert (not os.path.exists(back.res_folder)) or (not os.listdir(back.res_folder))

    def tearDownClass():
        back = Pickle()
        back.erase_all()

    def test_basic(self):

        try:
            prueba()
        except TypeError:
            pass

        p1 = prueba('hello')
        print(p1)
        p2 = prueba('hello')
        print(p2)
        print(diff(p1, p2))
        assert p1.equals(p2)  # Columns and rows are equal

        p3 = prueba('other')
        print(p3)
        assert not p1.equals(p3)

        p4 = prueba('hello', name='different')
        print(p4)
        assert not p1.equals(p4)

    def test_list_and_drop(self):
        assert len(prueba.list()) > 0
        prueba.drop_all()
        assert len(prueba.list()) == 0

    def test_df(self):
        df1 = prueba_df()
        df2 = prueba_df()

        assert df1.equals(df2)
        assert hash_df(df1) == hash_df(df2)
        prueba_df.drop_all()

    def test_different_program(self):
        '''A value saved by a different interpreter should be reusable.'''
        from create_custom import custom_function
        custom_function.drop_all()
        subprocess.check_call([sys.executable, os.path.join(this_directory, 'create_custom.py')])
        # create_custom returns different results when run as a script.
        # We make sure we are using the "stored" value, and not the result from the imported function
        assert custom_function() == 'main'

    def test_df_arg(self):

        df1 = pd.read_csv(os.path.join(this_directory, 'test.tsv'), sep='\t')
        res1 = prueba_df_argument(df1)
        df2 = pd.read_csv(os.path.join(this_directory, 'test.tsv'), sep='\t')
        res2 = prueba_df_argument(df2)
        assert res1 == res2
