import webbrowser
import logging
logger = logging.getLogger('SHEETCLOUD USER')
logging.basicConfig(format='\x1b[38;5;224m %(levelname)8s \x1b[0m | \x1b[38;5;39m %(name)s \x1b[0m | %(message)s', level=logging.DEBUG)


from typing import *

from sheetcloud.conn import service, ENV_SHEETCLOUD_USERNAME, ENV_SHEETCLOUD_LICENSE



def request_recovery_token(email: str=None) -> None:
    if email is None:
        email = ENV_SHEETCLOUD_USERNAME
    logger.info(f'Requesting password recovery token for account {email}.')
    _ = service('/users/password/recovery', params={'email': email}, method='post')
    logging.info('Please check your sheetcloud dashboard spreadsheet. You\'ll find the recovery token on the \'Settings\ worksheet.')


def password_reset(recovery_token: str, new_password: str) -> None:
    _ = service('/users/password/reset', params={'recovery_token': recovery_token, 'new_password': new_password}, method='post')
    logging.info('Password reset attempted. Please change your environment variables accordingly. Please note that due to security reasons the response does not contain information about the success of the attempt.')


def change_password(new_password: str) -> None:
    response = service('/users/password/change', params={'new_password': new_password}, method='post')
    if 'password_updated' in response:
        logging.info(f'Password updated {response["password_updated"]}.')


def activate_license_key(key: str) -> None:
    response = service('/users/license/update', params={'key': key}, method='post')
    if 'is_valid' in response:
        logging.info(f'License is valid: {response["is_valid"]}.')


def open_sheetcloud_website() -> None:
    webbrowser.open(f'https://sheetcloud.org')


if ENV_SHEETCLOUD_LICENSE is not None:
    logger.info(f'License found. Attempting to verify. Note: This only has to be done once.')
    activate_license_key(ENV_SHEETCLOUD_LICENSE)


if __name__ == "__main__":
    print('Test user connection...')
    # open_sheetcloud_website()
    # password_reset('jkdhsfjklasjhjkdfh', 'abb')
    activate_license_key('dskljklasfjd')

    print('Done')