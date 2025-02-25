import os
from flexfillsapi import initialize


def login_flexfills():
    flexfills_username = 'xxx'
    flexfills_password = 'xxx'

    flexfills_api = initialize(flexfills_username, flexfills_password, True)

    asset_list = flexfills_api.get_asset_list()

    print("Login Successful")


if __name__ == "__main__":
    login_flexfills()
