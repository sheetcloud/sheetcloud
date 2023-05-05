# Sheetcloud

Turn Spreadsheets into a Cloud Database with SheetCloud! Python library for easy access.

Website: https://sheetcloud.org


## NOTE: We are still in beta testing phase. If you like to become a Sheetcloud  beta tester (with some perks attached), write us an email at `contact[at]sheetcloud.org`.

## Status

Tests
[![Tests](https://github.com/sheetcloud/sheetcloud/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/sheetcloud/sheetcloud/actions/workflows/continuous_integration.yml)

Deploy to PYPI
[![PYPI](https://github.com/sheetcloud/sheetcloud/actions/workflows/deploy_to_pypi.yml/badge.svg)](https://github.com/sheetcloud/sheetcloud/actions/workflows/deploy_to_pypi.yml)

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

## What is Sheetcloud?

Transform Your Spreadsheets into a powerful Cloud Database with SheetCloud

Unlock the full potential of your data with SheetCloud! Say goodbye to the headaches of managing clunky offline spreadsheets and files, or setting up and maintaining a costly SQL database. With SheetCloud, you can turn your Google Sheets into a powerful cloud-based database with history, analytics, and online collaboration built in. Plus, with no hidden fees or charges, our simple and transparent pricing model will help you avoid the high costs of third-party databases.

Keep your data secure and accessible by storing it within your own Google Drive account, protected by robust security measures against potential breaches. Say goodbye to version control issues and data silos, and work seamlessly with your team, including non-developers such as business analysts who use spreadsheets. Whether you need to process, read, or write data in batches, build powerful dashboards and automated reports, handle secrets and environment variables, or schedule workflows, SheetCloud has got you covered, all with a single command from Python.

## [Test it now for free! No credit card required!](https://sheetcloud.org)
