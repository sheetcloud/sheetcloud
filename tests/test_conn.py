import sheetcloud as sc

def test_conn():
    sc.sheets.list()
    a = True
    assert a 