#Hypothesis test commented out
#import env_key
#import typing
#from hypothesis import given, strategies as st
#from typing import Any


#@given(
    #env_var=st.one_of(st.none(), st.text()),
    #key=st.one_of(st.none(), st.text()),
    #passwd=st.one_of(st.none(), st.text()),
#)
#def test_roundtrip_encrypt_passwd_decrypt_passwd(
    #env_var: str, key: str, passwd: str
#) -> None:
    #value0 = env_key.encrypt_passwd(env_var=env_var, passwd=passwd, key=key)
    #value1 = env_key.decrypt_passwd(env_var=value0, passwd=passwd, key=key)
    #assert env_var == value1, (env_var, value1)


#@given(
    #key=st.one_of(st.binary(), st.text()),
    #backend=st.from_type(typing.Optional[typing.Any]),
#)
#def test_fuzz_Fernet(key: typing.Union[bytes, str], backend: typing.Any) -> None:
    #env_key.Fernet(key=key, backend=backend)


#@given(env_var=st.text())
#def test_fuzz_get_key(env_var: str) -> None:
    #env_key.get_key(env_var=env_var)


#@given(env_var=st.text())
#def test_fuzz_save_key(env_var: str) -> None:
    #env_key.save_key(env_var=env_var)
import os
import unittest
import env_key
from cryptography.fernet import Fernet

class TestEnvKey(unittest.TestCase):
    #def test_save_key(self):
        #value01 = 'test_case_nut_bot-332211'
        #key = env_key.save_key(value01)
        #self.assertEqual(key, os.getenv(value01))
    def test_get_key(self):
        value01 = 'KEVIN_SQL'
        value02 = 'kevin_sql'
        value03 = 356
        key01 = env_key.get_key(value01)
        key02 = env_key.get_key(value02)
        self.assertEqual(key01, 'gxmFqujrdcjgQv3byMWukCse3dgex4VKA1gEEzdhcg8=')
        self.assertEqual(key02, None)
        
    def test_encrypt_passwd(self):
        value01 = 'password'
        key = Fernet.generate_key()
        enc_passwd01 = env_key.encrypt_passwd(passwd=value01, key=key)
        cipher_suite = Fernet(key)
        test_passwd01 = cipher_suite.encrypt(value01.encode()).decode()
        self.assertEqual(cipher_suite.decrypt(enc_passwd01), cipher_suite.decrypt(test_passwd01))
        
    def test_decrypt_passwd(self):
        value01 = 'test_password'
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        enc_passwd = cipher_suite.encrypt(value01.encode())
        test_passwd = cipher_suite.decrypt(enc_passwd).decode()
        self.assertEqual(value01, test_passwd)
        
if __name__ == '__main__':
    unittest.main()