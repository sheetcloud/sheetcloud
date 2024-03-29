# Sheetcloud

Simplify your data workflow

Website: https://sheetcloud.org

[![Tests](https://github.com/sheetcloud/sheetcloud/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/sheetcloud/sheetcloud/actions/workflows/continuous_integration.yml)
[![PYPI](https://github.com/sheetcloud/sheetcloud/actions/workflows/deploy_to_pypi.yml/badge.svg)](https://github.com/sheetcloud/sheetcloud/actions/workflows/deploy_to_pypi.yml)
[![deploy_documentation](https://github.com/sheetcloud/sheetcloud/actions/workflows/build_and_deploy_docs.yml/badge.svg)](https://github.com/sheetcloud/sheetcloud/actions/workflows/build_and_deploy_docs.yml)

## What is Sheetcloud?

Transform Your Spreadsheets into a powerful Cloud Database with SheetCloud

Say goodbye to the headaches of managing clunky offline spreadsheets and files, or setting up and maintaining a costly SQL database. With sheetcloud, you can turn your Google Sheets into a powerful cloud-based database with history, analytics, and online collaboration built in. Plus, it is completely free to use. No hidden fees or charges and you avoid the high costs of third-party databases.

Keep your data secure and accessible by storing it within your own Google Drive account, protected by robust security measures against potential breaches. Say goodbye to version control issues and data silos, and work seamlessly with your team, including non-developers such as business analysts who use spreadsheets. Whether you need to process, read, or write data, build powerful dashboards and automated reports, handle secrets and environment variables sheetcloud has got you covered. Easy to setup, a breeze to use with simple one-line commands from Python.

[Visit our website to start](https://sheetcloud.org)


## Setup

Sheetcloud expects the following environment variables to be present:

1. `SHEETCLOUD_USERNAME`

2. `SHEETCLOUD_PASSWORD`

You can find both in your Sheetcloud dashboard spreadsheet. If you have no account yet, you can create your free account in less than 30sec (no credit card required). Head over to [Sheetcloud website](https://sheetcloud.org) and connect your account. That's it! You will be re-directed to the Sheetcloud dashboard spreadsheet containing the username and password.

## Supported functionality

Sheetcloud supports Pandas DataFrames. Most functions are easy-to-use, self-explanatory, one-liners.

Spreadsheets

- Read/write/append spreadsheets in batches
- List spreadsheets and worksheets of a spreadsheet
- Get modification time
- Formatting
- Caching

Drive

- Read/write CSVs in batches

ORM

- map bidirectional data classes to spreadsheets

Environment Variables

- read/write environment variables to spreadsheets
- load variables into local environment

Templates

- load pre-defined templates
- customize templates

User

- request recovery token
- reset and change passwords
- validate license key
- authentication/authorization

REST:

- language agnostic API and documentation available
