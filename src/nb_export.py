#kevin fink
#kevin@shorecode.org
#Sept 25 2023
#nutrition_bot/nb_export.py

import pandas as pd
import nb_sql_tasks
import zipfile
import pygsheets

def to_csv(userid: str, df: pd.DataFrame, data_name: str) -> str:
    """
    Exports a dataframe to CSV
    
    Args:
    userid (str) : Telegram user id
    df (pd.DataFrame) : Dataframe
    data_name (str) : Name indicating the type of data being exported
    
    Returns:
    str: File path for the exported file
    """
    fn = f'dataviz/{data_name}{userid}.csv'
    df.to_csv(fn)
    return fn

def to_xcel(userid: str, df: pd.DataFrame, data_name: str) -> str:
    """
    Exports a dataframe to XLSX
    
    Args:
    userid (str) : Telegram user id
    df (pd.DataFrame) : Dataframe
    data_name (str) : Name indicating the type of data being exported
    
    Returns:
    str: File path for the exported file
    """
    fn = f'dataviz/{data_name}{userid}.xlsx'
    df.to_excel(fn)
    return fn

def to_html(userid: str, df: pd.DataFrame, data_name: str) -> str:
    """
    Exports a dataframe to HTML
    
    Args:
    userid (str) : Telegram user id
    df (pd.DataFrame) : Dataframe
    data_name (str) : Name indicating the type of data being exported
    
    Returns:
    str: File path for the exported filey
    """
    fn = f'dataviz/{data_name}{userid}.html'
    df.to_html(fn)
    return fn

def to_json(userid: str, df: pd.DataFrame, data_name: str) -> str:
    """
    Exports a dataframe to JSON
    
    Args:
    userid (str) : Telegram user id
    df (pd.DataFrame) : Dataframe
    data_name (str) : Name indicating the type of data being exported
    
    Returns:
    str: File path for the exported file
    """
    fn = f'dataviz/{data_name}{userid}.json'
    df.to_json(fn)
    return fn

def zip_all(userid: str, *files: list) -> str:
    """
    Creates a zip file containing all the files whose file paths are passed as a list as an argument
    
    Args:
    userid (str) : Telegram user id
    *files (list) : List containing all the file paths for the files to be zipped
    
    Returns:
    str: File path for the exported file
    """
    fn = f'dataviz/{userid}_nutritionbot_data.zip'
    zipped = zipfile.ZipFile(fn, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=2)
    for f in files:
        zipped.write(f)
    return fn
