#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import sys
import redis

sys.path.append(os.path.join(os.environ['D4_HOME'], 'lib'))
import ConfigLoader

from Role_Manager import create_user_db, edit_user_db, get_default_admin_token, gen_password

### Config ###
config_loader = ConfigLoader.ConfigLoader()
r_serv = config_loader.get_redis_conn("Redis_SERV", decode_responses=False)
config_loader = None
###  ###

if __name__ == "__main__":

    # create role_list
    if not r_serv.exists('d4:all_role'):
        role_dict = {'admin': 1, 'user': 2, 'sensor_register': 20}
        r_serv.zadd('d4:all_role', role_dict)

    username = 'admin@admin.test'
    password = gen_password()
    if r_serv.exists('user_metadata:admin@admin.test'):
        edit_user_db(username, password=password, role='admin')
    else:
        create_user_db(username, password, role='admin', default=True)


    username2 = 'config_generator@register.test'
    password2 = gen_password()
    if r_serv.exists('user_metadata:config_generator@register.test'):
        edit_user_db(username2, password=password2, role='sensor_register')
    else:
        create_user_db(username2, password2, role='sensor_register', default=True)


    token = get_default_admin_token()

    default_passwd_file = os.path.join(os.environ['D4_HOME'], 'DEFAULT_PASSWORD')
    to_write_str = '# Password Generated by default\n# This file is deleted after the first login\n#\nemail=admin@admin.test\npassword='
    to_write_str = to_write_str + password + '\nAPI_Key=' + token
    with open(default_passwd_file, 'w') as f:
        f.write(to_write_str)

    print('new user created: {}'.format(username))
    print('password: {}'.format(password))
    print('token: {}'.format(token))
