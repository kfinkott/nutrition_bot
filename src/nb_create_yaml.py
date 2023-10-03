#kevin fink
#kevin@shorecode.org
#Sept 30 2023
#nutrition_bot/nb_create_yaml.py

import yaml
import env_key

key = env_key.save_key('KEVIN_SQL')
print(f'Your public key is: {key.decode()}. It is saved in envrionment\
variables under the name: "KEVIN_SQL".')
enc_passwd = env_key.encrypt_passwd(key=key.decode())
print(f'Here is your encrypted password key: {enc_passwd}')
print(env_key.decrypt_passwd(passwd=enc_passwd, key=key.decode()))
sql_address = input('Enter the address of your mysql server:')
sql_port = input('Enter the port of your mysql server (Usually 3306):')
sql_uname = input('Enter your SQL username:')
spoon_key = input('Enter your Spoonacular API key:')
telegram_key = input('Enter your Telegram Bot API key:')

yaml_list = [{'mysql_server': {'address': sql_address, 'port': str(sql_port),
            'username': sql_uname, 'password_key': enc_passwd}},
             {'spoonacular_api_key': spoon_key}, {'telegram_bot_api_key': telegram_key}]

with open('nb.yaml', 'w', encoding='UTF-8') as fn:
    info = yaml.dump(yaml_list, fn)

print('Process completed. You must reload the OS for the new environment variable to be loaded')
