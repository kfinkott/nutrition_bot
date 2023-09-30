#kevin fink
#kevin@shorecode.org
#Sept 12 2023
#nutrition_bot/nb_sql_reports.py
import pandas as pd
from pandas.io.formats.style import Styler
import nb_data_viz
from datetime import datetime
from dataclasses import dataclass
import os
import sqlalchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import telebot
import numpy as np
import nb_sql_tasks
from functools import reduce
from typing import Union

@dataclass
class Sql_reports:
    today = datetime.now()
    def get_daily(self, table_name: str, weekday: str, engine: sqlalchemy.types.TypeEngine) -> pd.DataFrame:
        """
        Gets a daily report for diary or diet plan
        
        Args:
        self ( _obj_ ) : class objet
        table_name (str) : Name of the SQL table
        weekday (str) : Day of the week
        engine (sqlalchemy.types.TypeEngine) : SQL alchemy engine
        
        Returns:
        pd.DataFrame: Dataframe
        """
        try:
            df: pd.DataFrame = pd.read_sql(table_name, engine)
            df_daily: pd.DataFrame = self.filter_days(df, weekday)
            return df_daily
        except sqlalchemy.exc.ProgrammingError:
            # Returns an empty Dataframe if there is no SQL data for the day provided
            return pd.DataFrame()
    def get_daily_png(self, table_name: str, weekday: str, engine: sqlalchemy.types.TypeEngine) -> Union[str, None]:
        """
        Creates an image of the daily report for the diary or diet plan
        
        Args:
        self ( _obj_ ) : class object
        table_name (str) : SQL table name
        weekday (str) : Day of the week
        engine (sqlalchemy.types.TypeEngine) : SQL alchemy engine
        
        Returns:
        Union[os.path, None]: Returns None if the dataframe is empty, returns a file path to the image if the Dataframe has content
        """
        df_daily: DataFrame = self.get_daily(table_name, weekday, engine)
        # if statement checks to see if the Dataframe is empty
        if df_daily.empty == False:
            bf_df = pd.Series.to_frame(df_daily['breakfast'].dropna())
            ln_df = pd.Series.to_frame(df_daily['lunch'].dropna())
            dn_df = pd.Series.to_frame(df_daily['dinner'].dropna())
            df_title = [weekday, 'Report', 'shorecode.org']
            bf_img = nb_data_viz.export_png(bf_df, [df_title[0]])
            ln_img = nb_data_viz.export_png(ln_df, [df_title[1]])
            dn_img = nb_data_viz.export_png(dn_df, [df_title[2]])
            final_img = nb_data_viz.collate_3photos(bf_img, ln_img, dn_img)
        else:
            # Returns None if the dataframe is empty
            final_img = None
        return final_img
    def filter_days(self, df: pd.DataFrame, weekday: str) -> pd.DataFrame:
        """
        Selects rows from the Dataframe that contain the user supplied weekday
        
        Args:
        self ( _obj_ ) : class object
        df (pd.DataFrame) : Dataframe
        weekday (str) : Day of the week
        
        Returns:
        pd.DataFrame: Dataframe
        """
        filter = df['weekday'].isin([weekday]) #selects the rows from the dataframe for the user selected day
        return df[filter]
    def get_weekly(self, table_name: str, engine: sqlalchemy.types.TypeEngine) -> pd.DataFrame:
        """
        Gets a dataframe for a weekly report for the diary or diet plan
        
        Args:
        self ( _obj_ ) : class object
        table_name (str) : SQL table name
        engine (sqlalchemy.types.TypeEngine) : SQL alchemy engine
        
        Returns:
        pd.DataFrame: Dataframe for weekly report for diary or diet plan
        """
        df_weekly = pd.read_sql(table_name, engine)       
        return df_weekly          
    def get_weekly_png(self, call: telebot.types.CallbackQuery, table_name: str, week: str, engine: sqlalchemy.types.TypeEngine) -> tuple[os.path, pd.DataFrame]:
        """
        Creates an image for the weekly report for diary or diet plan
        
        Args:
        self ( _obj_ ) : class object
        call (telebot.types.CallbackQuery) : Telebot API callback object
        table_name (str) : SQL table name
        week (str) : Week for which the report is to be retrieved
        engine (sqlalchemy.types.TypeEngine) : SQL alchemy engine
        
        Returns:
        tuple[os.path, pd.DataFrame]: Returns the file path for the report image and a Dataframe containing the report data
        """
        if not os.path.isdir('dataviz'):
            os.mkdir('dataviz')        
        df_weekly = self.get_weekly(table_name, engine)
        df_grouped = df_weekly.groupby('weekday')        
        bf_sr = df_grouped['breakfast'].apply(self.group_weekdays_in_df)
        ln_sr = df_grouped['lunch'].apply(self.group_weekdays_in_df)
        dn_sr = df_grouped['dinner'].apply(self.group_weekdays_in_df)
        bf_df = pd.Series.to_frame(bf_sr)       
        ln_df = pd.Series.to_frame(ln_sr)
        dn_df = pd.Series.to_frame(dn_sr)
        final_df = pd.concat([bf_df, ln_df, dn_df], axis=1)
        final_df.rename(columns={'breakfast': 'Breakfast', 'lunch': 'Lunch', 'dinner': 'Dinner'}, inplace=True)
        final_df.index.rename(name='Day of the Week', inplace=True)
        final_df = final_df.style.set_caption(f'Week {week}')
        # try/except that names teh file based on diary (DD) or diet plan (PP) flag
        # except block is for an unexpected use of this function. a callback object could not be provided, so a raw string is used instead
        try:
            if 'DD' in table_name:
                html_fn = f'dataviz/weekly_report_{call.from_user.id}_diary.html'
            elif 'PP' in table_name:
                html_fn = f'dataviz/weekly_report_{call.from_user.id}_plan.html'
        except:
            if 'DD' in table_name:
                html_fn = f'dataviz/weekly_report_{call}_diary.html'
            elif 'PP' in table_name:
                html_fn = f'dataviz/weekly_report_{call}_plan.html'                               
        final_df.to_html(html_fn)     
        # table = table, td = table data (cells), th = table header
        css = "body {background: #ffe0cc;} table {border: 1.3mm ridge #661a00;} td {width: 600;} td {font-size: 12px;} th {font-size:15px;} td {border: 1px solid black;}"
        final_img = nb_data_viz.export_html_to_png(call, html_fn, css, week)
        os.remove(html_fn)
        return final_img, final_df
    
    def get_daily_nutrition(self, table_name: str, weekday: str, engine: sqlalchemy.types.TypeEngine, engine2) -> pd.DataFrame:        
        """
        
        
        Args:
        self ( _obj_ ) : 
        table_name (str) : y
        weekday (str) : 
        engine (sqlalchemy.types.TypeEngine) : y
        engine2 ( _obj_ ) : 
        
        Returns:
        pd.DataFrame: 
        """
        daily_df_with_meals= self.get_daily(table_name, weekday, engine)
        if daily_df_with_meals.empty == False:
            daily_sr = pd.concat([daily_df_with_meals['breakfast'], daily_df_with_meals['lunch'], daily_df_with_meals['dinner']]).dropna()
        else:
            daily_sr = pd.Series()
        if daily_sr.empty == False:
            stmt = 'select nl.name, sum(coalesce(dn.amount, 0)), sum(coalesce(dn.percentOfDailyNeeds, 0)) from ('
            for t in daily_sr:
                stmt += f'select name, amount, percentOfDailyNeeds from `{t}` union all '
            stmt = stmt[:-11] + ') as dn RIGHT JOIN `nut_legend` nl ON dn.name=nl.name group by nl.name;'                        
            with engine2.connect() as conn:      
                result = conn.execute(text(stmt))
            df = pd.DataFrame(result.all(), columns=['Name', 'Amount', 'Percent of DV'])
            return df
        else:
            return pd.DataFrame([], columns=['Name', 'Amount', 'Percent of DV'])
        
    def get_weekly_nutrition(self, call, table_name: str, week: str, engine: sqlalchemy.types.TypeEngine, sql_auth) -> pd.DataFrame:
        """
        Creates a dataframe that contains the nutrient amount and daily value for each day of the week for all nutrients. Also contains an average for the week for both amount and DV
        
        Args:
        self ( _obj_ ) : class object
        call ( _obj_ ) : telebot callback object
        table_name (str) : SQL table name
        week (str) : Week for which the report should be made
        engine (sqlalchemy.types.TypeEngine) : SQL alchemy engine
        
        Returns:
        pd.DataFrame: Dataframe containing a weekly summary of nutrients amount and Daily value
        """
        passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
        engine2 = nb_sql_tasks.engine(sql_auth, passwd, 'nb_ing')
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        col = ['amount', 'percent of DV']
        final_col = []
        for w in weekdays:
            for c in col:
                final_col.append(f'{w} {c}')
        dfdict = {}
        nut_names = pd.Series()
        for d in weekdays:            
            daily_df = self.get_daily_nutrition(table_name, d, engine, engine2)            
            if daily_df['Name'].empty == False:
                nut_names = daily_df['Name']
            if len(daily_df['Amount']) > 0:
                np.set_printoptions(suppress=True)
                dfdict[f'{d} amount'] = daily_df['Amount'].values.round(2)
                dfdict[f'{d} percent of DV'] = daily_df['Percent of DV'].values
        
        week_df = pd.DataFrame(dfdict, index=nut_names.values, columns=final_col)
        week_df['Daily average amount'] = week_df.iloc[::,::2].agg('mean', axis=1)
        week_df['Daily average DV'] = week_df.iloc[::,1::2].agg('mean', axis=1)        
        return week_df
    
    def get_weekly_nutrition_png(self, call, df: pd.DataFrame, week: str, engine: sqlalchemy.types.TypeEngine, title: str, sql_auth) -> str:
        """
        Creates an image displaying a weekly report of nutrients amount and daily value. Also contains an average amount and daily value for the week
        
        Args:
        self ( _obj_ ) : class object
        call ( _obj_ ) : Telebot callback object
        df (pd.DataFrame) : Dataframe containing the nutrient data for amount and daily value
        week (str) : Week for which the report should be made
        engine (sqlalchemy.types.TypeEngine) : sQL alchemy engine
        title (str) : Title for the iamge
        
        Returns:
        str: File path for the weekly nutrition report image
        """
        df.fillna(0, inplace=True)
        html_fn = f'dataviz/weekly_nut_report_{call.from_user.id}.html'
        df_styled = Styler(df, caption=f'Week {week} {title} nutrition report')
        df_styled.set_table_styles([{
         'selector': 'td',
         'props': 'width:50px;'},{
         'selector': 'th scope="row"',
         'props': 'width:80px;'},{
         'selector': 'caption',
         'props': 'font-size:2.00em;'             
     }], overwrite=False)
        df_styled.format(precision=2)        
        df_styled.to_html(html_fn)      
        css = "tbody tr:nth-child(odd) {background-color: #dbbdbd;} body {background: #ffe0cc;} table {border: 1.3mm ridge #661a00;} \
td {width: 5.3%;} td {font-size: 12px;} th {font-size:15px;} td {border: 1px solid black;} th {border: 1px solid black;} table {border-collapse: collapse;} table {table-layout: fixed}"
        final_img = nb_data_viz.export_html_to_png(call, html_fn, css, week)
        os.remove(html_fn)
        return final_img
    def get_nutrients_legend_png(self, sql_auth) -> str:
        """
        Produces a nutrient legend image that indicates the measurement units for each nutrient that is contained in the daily value data
        
        Args:
        self ( _obj_ ) : class object
        
        Returns:
        str: File path for the legend representing unit measurements of nutrients
        """
        passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
        engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_ing')  
        df = nb_data_viz.create_nutrients_units_legend(engine)
        fn = nb_data_viz.create_nutrients_units_legend_png(df)
        return fn
    def kevin_divide(self, x: float, y: float):
        """
        Creates a percentage of x compared to y if y is not zero
        
        Args:
        self ( _obj_ ) : class object
        x (float) : subject object of ratio
        y (float) : divisor of ratio
        
        Returns:
        Union[float, np.nan]: Returns np.nan if the divisor is zero. Returns a percentage otherwise
        """
        if y > 0:
            return x/y*100
        else:
            return np.nan # Returns nan if the divisor is zero
    def get_compare_diary_plan_weekly_png(self, call: telebot.types.CallbackQuery, diary_table_name: str, plan_table_name: str, week: str, enginediary: sqlalchemy.types.TypeEngine, engineplan: sqlalchemy.types.TypeEngine, sql_auth) -> tuple[str, pd.DataFrame]:
        """
        Creates and image that shows a comparison between diary and diet plan for a specified week
        
        Args:
        self ( _obj_ ) : class object
        call (telebot.types.CallbackQuery) : Telebot callback object
        diary_table_name (str) : SQL table name for the diary
        plan_table_name (str) : SQL table name for the diet plan
        week (str) : Week for which the report should be generated
        enginediary (sqlalchemy.types.TypeEngine) : SQL alchemy engine for the diary database
        engineplan (sqlalchemy.types.TypeEngine) : SQL alchemy engine for the diet plan database
        
        Returns:
        tuple[str, pd.DataFrame]: Returns a file path for the report image and a dataframe containing the comparison data
        """
        pd.options.display.float_format = '{:.2f}'.format
        diary_df = self.get_weekly_nutrition(call, diary_table_name, week, enginediary, sql_auth)
        plan_df = self.get_weekly_nutrition(call, plan_table_name, week, engineplan, sql_auth)
        df = pd.concat([diary_df.iloc[::,:-2:2], plan_df.iloc[::,:-2:2]])
        pd.options.display.max_rows = 110
        pd.options.display.max_columns =20
        df_computed = df.groupby(df.index).agg(lambda L: reduce(self.kevin_divide, L))
        df_computed['Daily average % of diet plan'] = df_computed.mean(axis=1)
        df_computed.rename(columns={'Sunday amount': 'Sunday % of diet plan', 'Monday amount': 'Monday % of diet plan', 'Tuesday amount': 'Tuesday % of diet plan', 'Wednesday amount': 'Wednesday % of diet plan', 'Thursday amount': 'Thursday % of diet plan', 'Friday amount': 'Friday % of diet plan', 'Saturday amount': 'Saturday % of diet plan'}, inplace=True)
        html_fn = f'dataviz/weekly_nut_compare_{call.from_user.id}.html'
        df_styled = Styler(df_computed, caption=f'Week {week} Diary vs. Diet plan comparison')
        df_styled.set_table_styles([{
         'selector': 'td',
         'props': 'width:50px;'},{
         'selector': 'th scope="row"',
         'props': 'width:80px;'},{
         'selector': 'caption',
         'props': 'font-size:2.00em;'             
     }], overwrite=False)
        df_styled.format(precision=2)        # rounds all values to 2 decimal places
        df_styled.to_html(html_fn)      
        css = "tbody tr:nth-child(odd) {background-color: #dbbdbd;} body {background: #ffe0cc;} table {border: 1.3mm ridge #661a00;} \
td {width: 5.3%;} td {font-size: 12px;} th {font-size:15px;} td {border: 1px solid black;} th {border: 1px solid black;} table {border-collapse: collapse;} table {table-layout: fixed}"
        final_img = nb_data_viz.export_html_to_png(call, html_fn, css, week)
        os.remove(html_fn)
        return final_img, df_computed        
    def group_weekdays_in_df(self, meal: pd.Series) -> str:
        """
        Combines the data for all meals in a single day (breakfast, lunch and dinner combined)
        
        Args:
        self ( _obj_ ) : class object
        meal (pd.Series) : 
        
        Returns:
        str: 
        """
        result = []
        for m in meal:
            if m != None:
                result.append(m)
        result = ', '.join(result)
        return result    

