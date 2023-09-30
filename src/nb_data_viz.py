#kevin fink
#kevin@shorecode.org
#Sept 4 2023
#nutrition_bot/nb_data_viz.py

import dataframe_image as dfi
from pandas.io.formats.style import Styler
import pandas as pd
import os
from PIL import Image
import seaborn as sns
from htmlwebshot import WebShot
import telebot
from sqlalchemy import text
import sqlalchemy
import nb_sql_reports
import matplotlib.pyplot as plt
import numpy as np

def export_png(df: pd.DataFrame, df_title: list, page2: bool=False) -> os.path:           
    """
    Creates a png image from a provided dataframe
    
    Args:
    df (pd.DataFrame) : Pandas dataframe
    df_title (list) : A list of titles for the images
    page2 (bool=False) : Flag to determine which title to use
    
    Returns:
    os.path: Returns a string representing the file path of the image
    """
    if not os.path.isdir('dataviz'):
        os.mkdir('dataviz')
    # page2 variable is used to determine which title is given to the table img and the filename
    if page2 == False:
        fn_path = f'dataviz/{df_title[0]}nutrients.png'
        df_styled = Styler(df, caption=df_title[0])
    elif page2 == True:
        fn_path = f'dataviz/{df_title[0]}nutrients2.png'    
        df_styled = Styler(df, caption=df_title[1])
    df_styled.set_table_styles([{
         'selector': 'caption',
         'props': 'font-size:2.00em;' # Changes the 'caption' css object to 2.00em font size
     }], overwrite=False)
    df_styled.format(precision=2) # Rounds all the numeric values in the table to two decimal places
    df_styled.export_png(fn_path) # Exports an image of a dataframe
    optimized_im = Image.open(fn_path)
    optimized_im.save(fn_path, optimize=True, quality=85)
    return fn_path

def export_nut_search_png(df: pd.DataFrame, df_title: list, page2: bool=False) -> os.path: 
    """
     Creates a png image from a provided dataframe
    
    Args:
    df (pd.DataFrame) : Pandas dataframe
    df_title (list) : A list of titles for the images
    page2 (bool=False) : Flag to determine which title to use
    
    Returns:
    os.path: Returns a string representing the file path of the image
    """
    if not os.path.isdir('dataviz'):
        os.mkdir('dataviz')
    # page2 variable is used to determine which title is given to the table img and the filename
    if page2 == False:
        fn_path = f'dataviz/{df_title[0]}ing.png'
        df_styled = Styler(df, caption=df_title[0])
    elif page2 == True:
        fn_path = f'dataviz/{df_title[0]}ing2.png'    
        df_styled = Styler(df, caption=df_title[1])
    df_styled.set_table_styles([{
         'selector': 'caption',
         'props': 'font-size:2.00em;'
     }], overwrite=False)
    df_styled.format(precision=2) # Rounds all the numeric values in the table to two decimal places
    df_styled.export_png(fn_path)   # Exports an image of a dataframe
    optimized_im = Image.open(fn_path)
    optimized_im.save(fn_path, optimize=True, quality=85)    
    return fn_path
        
def collate_photos(photo1: os.path, photo2: os.path) -> os.path:
    """
    Combines two images into a single image. the images are placed side by side
    
    Args:
    photo1 (os.path) : The file name of the first image
    photo2 (os.path) : The file name of the second image
    
    Returns:
    os.path: Returns a string representing the file path of the image
    """
    fn_path = photo1[:-4] + 'final' + photo1[-4:] # The collated image filename
    im1 = Image.open(photo1) # Opens the first table image
    im2 = Image.open(photo2) # Opens the second table image
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color='white') # color=white == background color
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))    
    dst.save(fn_path)    
    optimized_im = Image.open(fn_path)
    optimized_im.save(fn_path, optimize=True, quality=85)    
    os.remove(photo1)
    os.remove(photo2)
    return fn_path

def collate_3photos(photo1: os.path, photo2: os.path, photo3: os.path) -> os.path:
    """
    Combines 3 images into a single image. The images are placed side by side
    
    Args:
    photo1 (os.path) : The file name of the first image
    photo2 (os.path) : The file name of the second image
    photo3 (os.path) : THe file name of the third image
    
    Returns:
    os.path:  Returns a string representing the file path of the image
    """
    fn_path = photo1[:-4] + 'final' + photo1[-4:] # The collated image filename
    im1 = Image.open(photo1) # Opens the first table image
    im2 = Image.open(photo2) # Opens the second table image
    im3 = Image.open(photo3) # Opens the third table image
    dst = Image.new('RGB', (im1.width + im2.width + im3.width, max(im1.height, im2.height, im3.height)), color='white') # color=white == background color
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (im1.width + im2.width, 0))
    dst.save(fn_path)
    optimized_im = Image.open(fn_path)
    optimized_im.save(fn_path, optimize=True, quality=85)    
    os.remove(photo1) # cleans up the images used to make the collated image
    os.remove(photo2)
    os.remove(photo3)
    return fn_path

def export_html_to_png(call: telebot.types.CallbackQuery, html: os.path, css: str, week: str) -> os.path:
    """
    Creates a png image from a provided HTML file
    
    Args:
    call (telebot.types.CallbackQuery) : Telebot callback object
    html (os.path) : File name of the html file
    css (str) : CSS parameters to format the HTML file
    week (str) : The week for the report, used for the filename
    
    Returns:
    os.path: Returns a string representing the file path of the image
    """
    if not os.path.isdir('dataviz'):
        os.mkdir('dataviz')    
    shot=WebShot()
    shot.quality = 65
    try:
        output = f'dataviz/report_week{week}_{call.from_user.id}{html[-9:-5]}.png'
    except:
        output = f'dataviz/report_week{week}_{call}{html[-9:-5]}.png'        
    shot.create_pic(html=html, output=output, css=css)
    return output

def create_nutrients_units_legend(engine: sqlalchemy.Engine) -> pd.DataFrame:
    """
    Creates a dataframe of the measurement units for nutrients
    
    Args:
    engine (sqlalchemy.Engine) : SQL alchemy engine
    
    Returns:
    pd.DataFrame: Returns a dataframe containing unit measurements relations to nutrient names
    """
    with engine.connect() as conn:
        stmt = f'select name,unit from `nut_legend`;'
        result = conn.execute(text(stmt))
        df = pd.DataFrame(result.all())
    return df

def create_nutrients_units_legend_png(df: pd.DataFrame) -> str:
    """
     Creates an image that shows which unit measurements correspond to a nutrient.
    
    Args:
    df (pd.DataFrame) : Pandas dataframe
    
    Returns:
    str:  Returns a string representing the file path of the image
    """
    fn_path = 'dataviz/nutrients_legend.png'
    df_styled = Styler(df, caption='Nutrient Legend')
    df_styled.set_table_styles([{
     'selector': 'caption',
     'props': 'font-size:2.00em;'
     }], overwrite=False)
    df_styled.export_png(fn_path)
    optimized_im = Image.open(fn_path)
    optimized_im.save(fn_path, optimize=True, quality=85)
    return fn_path    

def nutrient_report_chart(call: telebot.types.CallbackQuery, table_name: str, week: str, engine: sqlalchemy.Engine, sql_auth) -> str:
    """
    Creates a matplotlib chart that shows the % of daily value consumed for each nutrient
    
    Args:
    call (telebot.types.CallbackQuery) : telebot callback object
    table_name (str) : SQL table name to retrieve teh data from
    week (str) : Detemines which week of the year the data is retrieved for
    engine (sqlalchemy.Engine) : SQL alchemy engine
    
    Returns:
    str: Returns a file path for the png chart image
    """
    reports = nb_sql_reports.Sql_reports()
    df = reports.get_weekly_nutrition(call, table_name, week, engine, sql_auth)
    # copies of the dataframe are made to be sliced later then concatenated. this is done to remove undesirable rows that are in the middle
    df3 = df.copy(deep=True)
    df2 = df.copy(deep=True)    
    df1 = df.copy(deep=True)    
    final_df = pd.concat([df1.iloc[1:5,:], df2.iloc[6:-35,:], df3.iloc[-34:-28,:]])
    final_df.fillna(0, inplace=True) # fills NA so mean is properly calculated for days with no consumption
    final_df['Daily average DV'].plot(kind='barh', title='Weekly Average Nutrient Consumption', yticks=range(0, len(df.index)), xticks=range(0,101,10), figsize=(15,9), ylabel='Nutrients', xlabel='% of DV',
                            rot=20, fontsize=6, color='Orange', antialiased=True,xlim=(0,100), grid=True, width=0.77) #width is the width of teh bars
    # if statements that use the table_name flag to determine if the table is a diary or diet plan
    if 'DD' in table_name:
        fn = f'dataviz/{call.from_user.id}nutrientdv_diary.png'
    if 'PP' in table_name:
        fn = f'dataviz/{call.from_user.id}nutrientdv_plan.png'
    plt.savefig(fn)
    plt.close()
    return fn

def weekly_dv_chart(call: telebot.types.CallbackQuery, table_name: str, week: str, engine: sqlalchemy.Engine, sql_auth) -> str:
    """
    Creates a matplotlib chart that displays the % of daily nutrition consumed for each day of the week
    
    Args:
    call (telebot.types.CallbackQuery) : telebot callback object
    table_name (str) : SQL table name to retrieve the data from
    week (str) : Determines which week of the year the data is retrieved for
    engine (sqlalchemy.Engine) : SQL alchemy engine
    
    Returns:
    str: Returns a file path for the png chart image
    """
    reports = nb_sql_reports.Sql_reports()
    df = reports.get_weekly_nutrition(call, table_name, week, engine, sql_auth)
    # copies of the dataframe are made to be sliced later then concatenated. this is done to remove undesirable rows that are in the middle
    df3 = df.copy(deep=True)
    df2 = df.copy(deep=True)    
    df1 = df.copy(deep=True)    
    final_df = pd.concat([df1.iloc[1:5,:], df2.iloc[6:-35,:], df3.iloc[-34:-28,:]])    
    final_df = df.iloc[:,1::2].agg(np.mean)
    final_df.plot(kind='bar', title='Daily Average Consumption For All Nutrients', xticks=range(0, len(final_df.index)), yticks=range(0,101, 10), ylim=(0,100), figsize=(9,9), ylabel='% of DV', 
                  color='Orange', width = 0.85, rot=90, antialiased=True).set_xticklabels(['Sun', 'Mon', 'Tue', 'Wed','Thu', 'Fri', 'Sat', 'Avg'])
     # if statements that use the table_name flag to determine if the table is a diary or diet plan
    if 'DD' in table_name:
        fn = f'dataviz/{call.from_user.id}weekdvdiary.png'
    if 'PP' in table_name:
        fn = f'dataviz/{call.from_user.id}weekdvplan.png'    
    plt.savefig(fn)
    plt.close()
    return fn
