import logging
logger = logging.getLogger('SHEETCLOUD USER')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)

import webbrowser

from typing import *

from sheetcloud.conn import service, ENV_SHEETCLOUD_USERNAME, ENV_SHEETCLOUD_PASSWORD


def request_recovery_token(email: str=None) -> None:
    if email is None:
        email = ENV_SHEETCLOUD_USERNAME
    logger.info(f'Requesting password recovery token for account {email}.')
    _ = service('/users/password/recovery', params={'email': email}, method='post')
    logging.info('Please check your sheetcloud dashboard spreadsheet. You\'ll find the recovery token on the \'Settings\ worksheet.')


def password_reset(recovery_token: str) -> None:
    pass


def change_password(new_password: str) -> None:
    pass


def activate_license_key(key: str) -> None:
    pass


def open_sheetcloud_website() -> None:
    webbrowser.open(f'https://sheetcloud.org')



if __name__ == "__main__":
    print('Test user connection...')
    open_sheetcloud_website()
    print('Done')