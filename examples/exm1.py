""" 
   EXAMPLE 1: BASIC READING AND WRITING
   ====================================

   Here you'll find examples of the most common use cases. 


   NO ACCOUNT? START HERE...
   =========================

   You'll need your sheetcloud username and password to get started. If you don't how, here are the steps:

    1. Head over to `https://sheetcloud.org` and connect your account with Sheetcloud. 
       Sheetcloud offers a free trial and no credit card is required to connect your account.
    2. Once you connected your account successfully, the redirect should take you to your 
       Sheetcloud settings spreadsheet in your account. On the `Settings` page, you'll find your username and
       initial password (you can change this later if you'd like).
    3. Before runnning the examples, create the following environment variables from your username and password:
        SHEETCLOUD_USERNAME
        SHEETCLOUD_PASSWORD
       Most commonly, people create `.env` files in the ROOT of the project folder containing all environment variables
       needed to run the project. Due to security reasons, we strongly advice you to NOT store your username and password 
       in your python files directly.

    How to check?
    Check the logs when you run the example. Sheetcloud will tell you whether or not it could find username and password.

"""
import pandas as pd
import sheetcloud as sc

from datetime import datetime


if __name__ == "__main__":
    # Load some data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    )

    print(df)
    print(df.info())

    # Alright! So, this is the classic 150x5 iris data set. Lets add another datetime column and an integer to it.
    df["a_datetime_column"] = datetime.now()
    df["an_int_column"] = 42

    # Lets store it as a new spreadsheet in our account. Shall we?

    spreadsheet_name = "Sheetcloud-Examples"  # This is the name of the target spreadsheet. If it does not exist, `write` will
    # create a new one, no further action required.
    worksheet_name = "Exm1"  # Each spreadsheet contains a number of worksheets (well, you probably used spreadsheet before).
    # If this worksheet already exists, the default behavior of `write` will overwrite any existing data.
    sc.sheets.write(
        spreadsheet_name, worksheet_name, df, cache=False
    )  # Don't worry about the last parameter. We will get
    # to this later.

    # Perfect! Lets read it.
    df2 = sc.sheets.read(
        spreadsheet_name, worksheet_name, cache=False
    )  # The read function will also try to infer the dtype of the DataFrame columns automatically.

    print(df2)
    print(df2.info())
    # Same format, same data. Yay.

    # Now, show the differences
    diff = df.compare(df2)
    print(f"There are {diff.size} differences to the original dataframe: {diff}")
