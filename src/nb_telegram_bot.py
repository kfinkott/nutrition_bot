#kevin fink
#kevin@shorecode.org
#Sept 4 2023
#nutrition_bot/nb_telegram_bot.py

import telebot
import nb_api_fetch
from pprint import pprint
import nb_data_viz
import markup_keyboards as mk
import nb_sql_tasks
import pandas as pd
import nb_sql_reports
import nb_export
from datetime import datetime
from sqlalchemy.exc import ProgrammingError
import os
import nb_recipe_tasks
import requests
    
def create_bot(bottoken: str, spoon_token: str, sql_auth: dict):
    """
    Root function for the main loop of the bot. Creates the telegram bot and at the end of the function initiates the polling loop. Contains all the code logic for the bot within functions, classes and IF/ELIF/ELSE blocks.
    
    Args:
    bottoken (str) : Api key for the telegram bot API
    spoon_token (str) : Api key for the Spoonacular API
    sql_auth (dict) : Contains the address, username and port for the SQL server. Also contains an encrypted key for the SQL password.
    
    Returns:
    Does not return
    """
    bot = telebot.TeleBot(bottoken)
    # create a class object for the spoontacular API and data storage
    nb_api = nb_api_fetch.Nb_api(spoon_token)    
    sql_reports = nb_sql_reports.Sql_reports()
    
    def send_food(message: telebot.types.Message, amount: int, unit: str, bot: telebot.TeleBot):        
        """
        Function to process the user request for nutritional information for a simple food (aka ingredient). The function also sends the result in the form of an image via the Telegram bot./
        
        Args:
        message (telebot.types.Message) : JSON information retrieved from teh Telegram API via getupdates()
        amount (int) : Quantity of the simple food to be inquired about
        unit (str) : Measurement unit type for the quantity of food
        bot (telebot.TeleBot) : Telebot API class object. Contains methods to interact with the Telegram API
        
        Returns:
        Does not return
        """
        response = nb_api.fetch_whole_food(message.text, amount, unit)
        if response == None:
            bot.send_message(message.chat.id, 'Could not find the item, please try another search.')
        else:
            nb_api.clean_response(response)
            df1, df2, df_title = nb_api.create_dataframes(sql_auth)
            final_photo = get_ing_photos(df1, df2, df_title)
            bot.send_photo(message.chat.id, open(final_photo, 'rb'), reply_markup=mk.submit_ing(df_title))  

    def get_ing_photos(df1: pd.DataFrame, df2: pd.DataFrame, df_title: list) -> os.path:
        """
        Function that retrieves two seperate images that are made from the contents of a single dataframe. THe images contain nutritional information for a simple food. Both images are concatenated within this function to produce a single image which has both original images side by side
        
        Args:
        df1 (pd.DataFrame) : Pandas Dataframe that contains nutritional data for a simple food
        df2 (pd.DataFrame) : Pandas Dataframe that contains nutritional data for a simple food
        df_title (list) : List of titles to be used at the top of the images
        
        Returns:
        os.path: File path that points to the completed image to be sent to the user
        """
        photo1 = nb_data_viz.export_png(df1, df_title, page2=False)        
        photo2 = nb_data_viz.export_png(df2, df_title, page2=True)        
        final_photo = nb_data_viz.collate_photos(photo1, photo2)        
        return final_photo        
    
    def get_nutrient_data(nutrient_id: str) -> list:
        """
        Retrieves a list of foods that contain the specified nutrient
        
        Args:
        nutrient_id (str) : Numeric ID that represents a specific nutrient
        
        Returns:
        list: List of foods that contain the specified nutrient
        """
        passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
        engine = nb_sql_tasks.engine(sql_auth, passwd, 'FNDDS')   
        nutrient_list = nb_sql_tasks.fetch_nutrient_data(nutrient_id, engine)
        nutrient_result = []
        for n in nutrient_list:
            nutrient_result.append(n)        
        return nutrient_result
    
    def get_nutrient_photo(nutrient_result: list, start_indx: int=0) -> os.path:
        """
        Function that retrieves two seperate images that are made from the contents of a single dataframe. THe images contain food that contains a specified nutrient. Both images are concatenated within this function to produce a single image which has both original images side by side
        
        Args:
        nutrient_result (list) : List of foods that contain the specified nutrient
        start_indx (int=0) : Indicates where in the list to begin retrieving results from. Used primarily when the user wants to view additional results after receiving the first batch of results
        
        Returns:
        os.path: File path that points to the completed image to be sent to the user
        """
        df = pd.DataFrame(nutrient_result[start_indx:start_indx+100], columns=['Food name', 'Amount', 'Unit', 'Nutrient'])
        df_title = [df.iloc[0,3], 'shorecode.org']
        df1img = nb_data_viz.export_nut_search_png(df[:50], df_title, page2=False)
        df2img = nb_data_viz.export_nut_search_png(df[50:], df_title, page2=True)
        final_img = nb_data_viz.collate_photos(df1img, df2img)
        return final_img        
        
    def send_nutrient(call: telebot.types.CallbackQuery, nutrient_id: str, start_indx: int = 0):
        """
        Function that processes the users request to view food by nutrient. Sends the user the result in the form of an image via the Telegram bot
        
        Args:
        call (telebot.types.CallbackQuery) : JSON information retrieved from teh Telegram API via getupdates()
        nutrient_id (str) : Numeric ID that represents a specific nutrient
        start_indx (int = 0) : Indicates where in the list to begin retrieving results from. Used primarily when the user wants to view additional results after receiving the first batch of results
        
        Returns:
        Does not return
        """
        get_nutrient_data(nutrient_id)
        nutrient_result = get_nutrient_data(nutrient_id)
        final_img = get_nutrient_photo(nutrient_result, start_indx)
        bot.send_photo(call.from_user.id, open(final_img, 'rb'), reply_markup=mk.more_nut())       
        
    def week_nut_diary(call: telebot.types.CallbackQuery, week: str):
        """
        Function that retrieves the users diary for a specified week. The function also creates an image of the diary and sends it to the user via the Telegram bot.
        
        Args:
        call (telebot.types.CallbackQuery) :  JSON information retrieved from teh Telegram API via getupdates(). Contains the callback data sent by the inline keyboard
        week (str) : The numeric week (out of 52) that the user specifies. Indicates which section of teh diary to process and send to the user
        
        Returns:
        Does not return
        """
        today = datetime.now()
        this_year = today.strftime('%-y')
        try:
            print(week)
            table_name = f'{call.from_user.first_name}_DD_{str(call.from_user.id)}_week{str(week)}_year{str(this_year)}'
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')   
            nb_api.dfdiary = sql_reports.get_weekly_nutrition(call, table_name, week, engine, sql_auth)
            fn = sql_reports.get_weekly_nutrition_png(call, nb_api.dfdiary, week, engine, 'diary')
            bot.send_photo(call.from_user.id, open(fn, 'rb'))
        except ProgrammingError as e:
            bot.send_message(call.from_user.id, 'Cannot find a diary for the week chosen')        
            print(e)
            
    def week_nut_plan(call: telebot.types.CallbackQuery, week: str):    
        """
        Function that retrieves the users diet plan for a specified week. The function also creates an image of the diet plan and sends it to the user via the Telegram bot.
        
        Args:
        call (telebot.types.CallbackQuery) :  JSON information retrieved from teh Telegram API via getupdates(). Contains the callback data sent by the inline keyboard
        week (str) : The numeric week (out of 52) that the user specifies. Indicates which section of teh diary to process and send to the user
        
        Returns:
        Does not return
        """
        today = datetime.now()
        this_year = today.strftime('%-y')
        try:
            table_name = f'{call.from_user.first_name}_PP_{str(call.from_user.id)}_week{str(week)}_year{str(this_year)}'
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')   
            nb_api.dfplan = sql_reports.get_weekly_nutrition(call, table_name, week, engine, sql_auth)
            fn = sql_reports.get_weekly_nutrition_png(call, nb_api.dfplan, week, engine, 'diet plan')
            bot.send_photo(call.from_user.id, open(fn, 'rb'))
        except ProgrammingError:
            bot.send_message(call.from_user.id, 'Cannot find a diet plan for the week chosen')        
    
    def comparison_file_export(userid: int, df: pd.DataFrame) -> tuple[str, str, str, str]:
        """
        Creates exported files of the diet plan vs diary comparison dataframe\
        
        Args:
        userid (int) : Numeric ID of the Telegram user
        df (pd.DataFrame) : Pandas dataframe containing comparison data for diet plan vs diary
        
        Returns:
        tuple[str, str, str, str]: Returns file paths for the exported files
        """
        compare_csv = nb_export.to_csv(userid, df, 'comparision')
        compare_xlsx = nb_export.to_xcel(userid, df, 'comparision')
        compare_html = nb_export.to_html(userid, df, 'comparision')
        compare_json = nb_export.to_json(userid, df, 'comparision')        
        return compare_csv, compare_xlsx, compare_html, compare_json
    
    def diary_file_export(userid: int, df: pd.DataFrame) -> tuple[str, str, str, str]:
        """
        Creates exported files of the diary dataframe
        
        Args:
        userid (int) : Numeric ID of the Telegram user
        df (pd.DataFrame) : Pandas dataframe containing  diary data
        
        Returns:
        tuple[str, str, str, str]: Returns file paths for the exported files
        """
        diary_csv = nb_export.to_csv(userid, df, 'diary')
        diary_xlsx = nb_export.to_xcel(userid, df, 'diary')
        diary_html = nb_export.to_html(userid, df, 'diary')
        diary_json = nb_export.to_json(userid, df, 'diary')        
        return diary_csv, diary_xlsx, diary_html, diary_json
    
    def plan_file_export(userid: int, df: pd.DataFrame) -> tuple[str, str, str, str]:
        """
        Creates exported files of the diet plan dataframe
        
        Args:
        userid (int) : Numeric user ID of the Telegram user
        df (pd.DataFrame) : Pandas dataframe containing diet plan data
        
        Returns:
        tuple[str, str, str, str]: Returns file paths for the exported files
        """
        plan_csv = nb_export.to_csv(userid, df, 'diet_plan')
        plan_xlsx = nb_export.to_xcel(userid, df, 'diet_plan')
        plan_html = nb_export.to_html(userid, df, 'diet_plan')
        plan_json = nb_export.to_json(userid, df, 'diet_plan')       
        return plan_csv, plan_xlsx, plan_html, plan_json,
        
        
    def callback_logic(call: telebot.types.CallbackQuery):
        """
        Function contains a very large block of IF statements. used to filter callback data sent by the various inline keyboards.
        
        Args:
        call (telebot.types.CallbackQuery) :  JSON information retrieved from teh Telegram API via getupdates(). Contains the callback data sent by the inline keyboard
        
        Returns:
        Does not return
        """
        '''This function executes after the telegram user selects an amount of days from the inline keyboard
        args:
            call: callback_query object. See the link below for JSON structure.
            https://pytba.readthedocs.io/en/latest/types.html#telebot.types.CallbackQuery
        '''
        choice: telebot.callback_data = call.data
        today = datetime.now()
        this_week = today.isocalendar().week # Gets the numeric week of the year out of 52
        this_weekday = today.strftime('%A') # Gets the literal week day name
        this_year = today.strftime('%-y') # Gets the last two digits of year (2023 = 23)
        
        
        if choice == 'i':
            nb_api.ing_search_user_list.append(call.from_user.id)
            bot.send_message(call.from_user.id, "Please choose an option from the following:", reply_markup=mk.ing_unit())
        elif choice[:-1].isdigit() and call.from_user.id in nb_api.ing_search_user_list:
            nb_api.user_unit_choice[call.from_user.id] = choice
            bot.send_message(call.from_user.id, "Please type the name of the simple food:")
        else:
            if call.from_user.id in nb_api.ing_search_user_list:
                nb_api.ing_search_user_list.remove(call.from_user.id)
        if "add_diary" or 'add_plan' in choice:
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])   
        if 'choose_plan' in choice:
            df_title = choice[11:]
            bot.send_message(call.from_user.id, "Please choose the day and time for the meal you want to add to(bf=breakfast, ln=lunch, dn=dinner):", reply_markup=mk.choose_plan_meal(df_title))
        if 'choose_diary' in choice:
            df_title = choice[12:]
            bot.send_message(call.from_user.id, "Please choose the day and time for the meal you want to add to(bf=breakfast, ln=lunch, dn=dinner):", reply_markup=mk.choose_diary_meal(df_title))
        if 'add_diary' in choice:
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])            
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
            result = nb_sql_tasks.add_to_diary(choice[11:-2], call.from_user.id, call.from_user.first_name, choice[-2:], engine)
            if result != None:
                bot.send_message(call.from_user.id, "Succesfully added entry to diary")
        if 'add_plan' in choice:
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])            
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')
            result = nb_sql_tasks.add_to_plan(choice[10:-2], call.from_user.id, call.from_user.first_name, choice[-2:], engine)           
            if result != None:
                bot.send_message(call.from_user.id, "Succesfully added entry to diary")            
        if choice == 'n':
            nb_api.nutrient_search_user_list.append(call.from_user.id)
            bot.send_message(call.from_user.id, "The following image shows which number to enter for your desired nutrient search:")
            bot.send_photo(call.from_user.id, open('data/nutrient_index.png', 'rb'))
            bot.send_message(call.from_user.id, "Please select the number that corresponds to your desired nutrient:", reply_markup=mk.nutrients())
        if choice.isdigit() and call.from_user.id in nb_api.nutrient_search_user_list:
            nb_api.user_nutrient_choice[call.from_user.id] = choice
            nb_api.more_nut = 0
            send_nutrient(call, choice)
            nb_api.nutrient_search_user_list.remove(call.from_user.id)            
        if choice == 'more_nut':
            choice = nb_api.user_nutrient_choice[call.from_user.id]
            nb_api.more_nut += 100
            send_nutrient(call, choice, nb_api.more_nut)
        if choice == 'exit_nut':
            bot.send_message(call.from_user.id, "Please choose an option from the following:", reply_markup=mk.main_keys())
        if choice == 'view_diary':
            bot.send_message(call.from_user.id, 'Please choose the diary report you want to see:', reply_markup=mk.view_diary())
        if choice == 'view_plan':
            bot.send_message(call.from_user.id, 'Please choose the diet plan report you want to see:', reply_markup=mk.view_plan())
        if choice == 'plan_daily':
            bot.send_message(call.from_user.id, 'Please choose a day of the week:', reply_markup=mk.plan_choose_weekday())
        if 'weekday_plan' in choice:            
            table_name = f'{call.from_user.first_name}_PP_{str(call.from_user.id)}_week{str(this_week)}_year{str(this_year)}'
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')
            fn = sql_reports.get_daily_png(table_name, choice[12:], engine)
            bot.send_photo(call.from_user.id, open(fn, 'rb'))                
        if choice == 'diary_daily':
            bot.send_message(call.from_user.id, 'Please choose a day of the week:', reply_markup=mk.diary_choose_weekday())
        if 'weekday_diary' in choice:            
            table_name = f'{call.from_user.first_name}_DD_{str(call.from_user.id)}_week{str(this_week)}_year{str(this_year)}'
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
            fn = sql_reports.get_daily_png(table_name, choice[13:], engine)
            if fn != None:                
                bot.send_photo(call.from_user.id, open(fn, 'rb'))
            else:
                bot.send_message(call.from_user.id, 'A daily plan for that day was not found')
        if choice == 'diary_weekly':
            bot.send_message(call.from_user.id, 'Please choose a week or type XX (where XX is the two digit week number of the year):', reply_markup=mk.diary_choose_week())
            nb_api.diary_flag.append(call.from_user.id)
        if choice == 'plan_weekly':
            bot.send_message(call.from_user.id, 'Please choose a week or type XX (where XX is the two digit week number of the year):', reply_markup=mk.plan_choose_week())
            nb_api.plan_flag.append(call.from_user.id)
        if 'week_diary' in choice:
            nb_api.diary_flag.append(call.from_user.id) 
            try:
                table_name = f'{call.from_user.first_name}_DD_{str(call.from_user.id)}_week{str(choice[10:])}_year{str(this_year)}'
                passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
                fn, df = sql_reports.get_weekly_png(call, table_name, choice[10:], engine)
                bot.send_photo(call.from_user.id, open(fn, 'rb'))
            except ProgrammingError:
                bot.send_message(call.from_user.id, 'Cannot find a diary for the week chosen')
        if 'week_plan' in choice:
            nb_api.plan_flag.remove(call.from_user.id)
            try:
                table_name = f'{call.from_user.first_name}_PP_{str(call.from_user.id)}_week{str(choice[9:])}_year{str(this_year)}'
                passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')   
                fn, df = sql_reports.get_weekly_png(call, table_name, choice[9:], engine)
                bot.send_photo(call.from_user.id, open(fn, 'rb'))
            except ProgrammingError:
                bot.send_message(call.from_user.id, 'Cannot find a diet plan for the week chosen')             
        if 'compare_nutrition' in choice:
            bot.send_message(call.from_user.id, 'Please choose the report:', reply_markup=mk.nutrition_choice()) 
        if 'show_comparison_weekly' in choice:
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            enginediary = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')   
            engineplan = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')   
            week = choice[22:]
            week_nut_diary(call, week)
            week_nut_plan(call, week)
            diary_table_name = f'{call.from_user.first_name}_DD_{str(call.from_user.id)}_week{str(week)}_year{str(this_year)}'
            plan_table_name = f'{call.from_user.first_name}_PP_{str(call.from_user.id)}_week{str(week)}_year{str(this_year)}'                                    
            fn, df = sql_reports.get_compare_diary_plan_weekly_png(call, diary_table_name, plan_table_name, choice[22:], enginediary, engineplan, sql_auth)            
            bot.send_photo(call.from_user.id, open(fn, 'rb'), reply_markup=mk.request_legend())     
        if 'show_legend' in choice:
            fn = sql_reports.get_nutrients_legend_png(sql_auth)
            bot.send_photo(call.from_user.id, open(fn, 'rb'))
        if 'clear_diary' in choice:
            if len(choice) > 11:
                passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
                table_name = f'{call.from_user.first_name}_DD_{call.from_user.id}_week{this_week}_year{this_year}'
                result = nb_sql_tasks.clear_diary(call,choice[11:], table_name, engine)
                if result == True:
                    bot.send_message(call.from_user.id, 'Diary cleared successfully.')
                else:
                    bot.send_message(call.from_user.id, 'Could not clear, data for this day may not exist.')
            else:
                bot.send_message(call.from_user.id, 'Choose which weekday to delete from the diary:', reply_markup=mk.clear_diary_wkday())
        if 'clear_plan' in choice:
            if len(choice) > 10:
                passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')   
                table_name = f'{call.from_user.first_name}_PP_{call.from_user.id}_week{this_week}_year{this_year}'
                result = nb_sql_tasks.clear_plan(call, choice[10:], table_name, engine)
                if result == True:
                    bot.send_message(call.from_user.id, 'Diet plan cleared successfully.')
                else:
                    bot.send_message(call.from_user.id, 'Could not clear, data for this day may not exist.')
            else:
                bot.send_message(call.from_user.id, 'Choose which weekday to delete from the plan:', reply_markup=mk.clear_plan_wkday())
        if choice == 'r':            
            bot.send_message(call.from_user.id, 'Please choose which criteria you want to search by:', reply_markup=mk.recipe_search_choice())
        if choice == 'recipe_r':
            nb_api.recipe_r_flag[call.from_user.id] = True
            bot.send_message(call.from_user.id, 'Enter the name of the recipe:')
        if choice == 'recipe_i':
            nb_api.recipe_i_flag[call.from_user.id] = True            
            bot.send_message(call.from_user.id, 'Enter the name of the ingredient:')        
        if choice == 'recipe_n':            
            bot.send_message(call.from_user.id, 'Please choose a nutrient:', reply_markup=mk.recipe_n())            
        if 'recipe_n_choice' in choice:
            n_choice = choice[15:]
            recipe = nb_recipe_tasks.RecipeSearch(nb_api)
            api_response = recipe.nutrient_search(n_choice)
            bot.send_message(call.from_user.id, 'Please choose a recipe from the following:', reply_markup=mk.recipe_choice(api_response))
        if 'recipe_id' in choice:
            recipe_id = choice[9:]
            recipe = nb_recipe_tasks.RecipeSearch(nb_api)
            api_response, df_title = recipe.id_search(recipe_id)
            recipe_df, df1, df2 = recipe.recipe_df(api_response)
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_ing')
            nb_sql_tasks.df_to_sql(recipe_df, df_title, engine)
            img = recipe.recipe_img(df1, df2, df_title)
            card_response = recipe.get_recipe_card(recipe_id)
            try:
                url_response = requests.get(card_response['url'])
                with open(f'temp{call.from_user.id}.png', 'wb') as fn:
                    fn.write(url_response.content)
                    bot.send_photo(call.from_user.id, open(f'temp{call.from_user.id}.png', 'rb'))
                    os.remove(f'temp{call.from_user.id}.png')
            except:
                pass
            bot.send_photo(call.from_user.id, open(img, 'rb'), reply_markup=mk.submit_ing(df_title))
        if choice == 'diary_auto_weekly':
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary_cron')
            nb_sql_tasks.create_weekly_cron_tables(engine)
            nb_sql_tasks.add_weekly_cron_sub(call.from_user.id, call.from_user.first_name, engine)            
        if choice == 'plan_auto_weekly':
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan_cron')
            nb_sql_tasks.create_weekly_cron_tables(engine)
            nb_sql_tasks.add_weekly_cron_sub(call.from_user.id, call.from_user.first_name, engine)
        if choice == 'diary_auto_weekly_rem':
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary_cron')
            nb_sql_tasks.remove_weekly_cron(call.from_user.id, engine)
        if choice == 'plan_auto_weekly_rem':
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan_cron')
            nb_sql_tasks.remove_weekly_cron(call.from_user.id, engine)        
        if choice == 'downloaddata':
            passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
            enginediary = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')            
            engineplan = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')            
            nut_legend = sql_reports.get_nutrients_legend_png(sql_auth)
            diary_table_name = f'{call.from_user.first_name}_DD_{str(call.from_user.id)}_week{str(this_week)}_year{str(this_year)}'
            plan_table_name = f'{call.from_user.first_name}_PP_{str(call.from_user.id)}_week{str(this_week)}_year{str(this_year)}'                                    
            compare_img_fn, compare_df = sql_reports.get_compare_diary_plan_weekly_png(call, diary_table_name, plan_table_name, str(this_week), enginediary, engineplan, sql_auth)
            compare_csv, compare_xlsx, compare_html, compare_json = comparison_file_export(call.from_user.id, compare_df)
            diary_img_fn, diary_df = sql_reports.get_weekly_png(call, diary_table_name, str(this_week), enginediary)
            plan_img_fn, plan_df = sql_reports.get_weekly_png(call, plan_table_name, str(this_week), engineplan)
            diary_csv, diary_xlsx, diary_html, diary_json = diary_file_export(call.from_user.id, compare_df)
            plan_csv, plan_xlsx, plan_html, plan_json= plan_file_export(call.from_user.id, compare_df)
            diary_nutrient_chart_fn = nb_data_viz.nutrient_report_chart(call, diary_table_name, this_week, enginediary, sql_auth)
            plan_nutrient_chart_fn = nb_data_viz.nutrient_report_chart(call, plan_table_name, this_week, engineplan, sql_auth)
            diary_weekday_chart_fn = nb_data_viz.weekly_dv_chart(call, diary_table_name, this_week, enginediary, sql_auth)
            plan_weekday_chart_fn = nb_data_viz.weekly_dv_chart(call, plan_table_name, this_week, engineplan, sql_auth)
            files = [nut_legend, compare_img_fn, compare_csv, compare_xlsx, compare_html, compare_json,diary_csv, diary_xlsx,
                     diary_html, diary_json, plan_csv, plan_xlsx, plan_html, plan_json, diary_img_fn, plan_img_fn,
                     diary_nutrient_chart_fn, plan_nutrient_chart_fn, diary_weekday_chart_fn, plan_weekday_chart_fn]
            nb_zip = nb_export.zip_all(call.from_user.id, *files)
            bot.send_document(call.from_user.id, open(nb_zip, 'rb'))                                        
        
        
    @bot.callback_query_handler(func=lambda call: True)    
    def main_callback(call: telebot.types.CallbackQuery):
        """
        Function that is necessary to interact with the Telebot API. Calls the 'callback_logic' function to for readability.
        
        Args:
        call (telebot.types.CallbackQuery) :  JSON information retrieved from teh Telegram API via getupdates(). Contains the callback data sent by the inline keyboard
        
        Returns:
        Does not return
        """
        callback_logic(call)
        
    @bot.message_handler(commands=['ingredient'])
    def fire_ingredient(message: telebot.types.Message):
        """
        Function that retrieves simple food (aka ingredient) data from the Spoonacular API. Also sends the resulting image to the Telegram user
        
        Args:
        message (telebot.types.Message) :  JSON information retrieved from teh Telegram API via getupdates()y
        
        Returns:
        Does not return
        """
        nb_api.ing_search_user_list.append(message.from_user.id)
        bot.send_message(message.from_user.id, "Please choose an option from the following:", reply_markup=mk.ing_unit())    
        
    @bot.message_handler(commands=['recipe'])
    def send_recipe(message: telebot.types.Message):
        """
        Function to process the user request for nutritional information for a recipe. The function also sends the result in the form of an image via the Telegram bot
        
        Args:
        message (telebot.types.Message) :  JSON information retrieved from teh Telegram API via getupdates()
        
        Returns:
        Does not return
        """
        bot.send_message(message.from_user.id, 'Please choose which criteria you want to search by:', reply_markup=mk.recipe_search_choice())   

    @bot.message_handler(commands=['nutrient'])
    def send_nutrients(message: telebot.types.Message):        
        """
        Function to process the user request for foods that contain a specified nutrient. The function also sends the result in the form of an image via the Telegram bot
        
        Args:
        message (telebot.types.Message) :  JSON information retrieved from teh Telegram API via getupdates()
        
        Returns:
        Does not return
        """
        nb_api.nutrient_search_user_list.append(message.from_user.id)
        bot.send_message(message.from_user.id, "The following image shows which number to enter for your desired nutrient search:")
        bot.send_photo(message.from_user.id, open('data/nutrient_index.png', 'rb'))
        bot.send_message(message.from_user.id, "Please select the number that corresponds to your desired nutrient:", reply_markup=mk.nutrients())        
    
    @bot.message_handler(commands=['menu'])
    def main_menu(message: telebot.types.Message):
        """
        Function that presents the inline keyboard containing the main menu for the bot.
        
        Args:
        message (telebot.types.Message) :  JSON information retrieved from teh Telegram API via getupdates()
        
        Returns:
        Does not return
        """
        bot.send_message(message.chat.id, "Please choose an option from the following:", reply_markup=mk.main_keys())                    
                
    #Default message for when the user input does not match any bot functions, also triggers the main menu 
    @bot.message_handler(func=lambda msg: True)
    def default(message: telebot.types.Message):
        """
        Function that processes Telegram user input of any raw text (not prefixed by a '/')
        
        Args:
        message (telebot.types.Message) :  JSON information retrieved from teh Telegram API via getupdates()
        
        Returns:
        Does not return
        """
        today = datetime.now()
        this_week = today.isocalendar().week
        this_weekday = today.strftime('%A')
        this_year = today.strftime('%-y')        
        
        if message.chat.id in nb_api.ing_search_user_list:        
            nb_api.ing_search_user_list.remove(message.from_user.id)
            amount = nb_api.user_unit_choice[message.from_user.id][:-1]
            unit = nb_api.user_unit_choice[message.from_user.id][-1:]
            send_food(message, amount, unit, bot)            
        elif message.from_user.id in nb_api.recipe_r_flag.keys():
            del nb_api.recipe_r_flag[message.from_user.id]
            recipe = nb_recipe_tasks.RecipeSearch(nb_api)
            api_response = recipe.recipe_search(message.text)            
            bot.send_message(message.from_user.id, 'Please choose a recipe from the following:', reply_markup=mk.recipe_choice(api_response['results']))
        elif message.from_user.id in nb_api.recipe_i_flag.keys():
            del nb_api.recipe_i_flag[message.from_user.id]
            recipe = nb_recipe_tasks.RecipeSearch(nb_api)            
            api_response = recipe.ing_search(message.text)
            bot.send_message(message.from_user.id, 'Please choose a recipe from the following:', reply_markup=mk.recipe_choice(api_response))
        
        elif len(message.text) <= 2 and message.text.isdigit() and (message.from_user.id in nb_api.diary_flag or message.from_user.id in nb_api.plan_flag or message.from_user.id in nb_api.diary_nut_flag or message.from_user.id in nb_api.plan_nut_flag):
            if len(message.text) == 1:
                message.text = '0' + message.text
            if message.from_user.id in nb_api.diary_flag:
                nb_api.diary_flag.remove(message.from_user.id)
                try:
                    table_name = f'{message.from_user.first_name}_DD_{str(message.from_user.id)}_week{message.text}_year{str(this_year)}'
                    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                    engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
                    fn, df = sql_reports.get_weekly_png(message, table_name, message.text, engine)
                    bot.send_photo(message.from_user.id, open(fn, 'rb'))
                except ProgrammingError:
                    bot.send_message(message.from_user.id, 'Cannot find a diary for the week chosen')

            if  message.from_user.id in nb_api.plan_flag:
                nb_api.plan_flag.remove(message.from_user.id)
                try:
                    table_name = f'{message.from_user.first_name}_PP_{str(message.from_user.id)}_week{message.text}_year{str(this_year)}'
                    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                    engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')
                    fn, df = sql_reports.get_weekly_png(message, table_name, message.text, engine)
                    bot.send_photo(message.from_user.id, open(fn, 'rb'))
                except ProgrammingError:
                    bot.send_message(message.from_user.id, 'Cannot find a diary for the week chosen')                
            if  message.from_user.id in nb_api.diary_nut_flag:
                nb_api.diary_nut_flag.remove(message.from_user.id)
                try:
                    table_name = f'{message.from_user.first_name}_DD_{str(message.from_user.id)}_week{message.text}_year{str(this_year)}'
                    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                    engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diary')
                    fn,df = sql_reports.get_weekly_nutrition_png(message, table_name, message.text, engine, sql_auth)
                    bot.send_photo(message.from_user.id, open(fn, 'rb'))
                except ProgrammingError:
                    bot.send_message(message.from_user.id, 'Cannot find a diary for the week chosen')                

            if  message.from_user.id in nb_api.plan_nut_flag:
                nb_api.plan_nut_flag.remove(message.from_user.id)
                try:
                    table_name = f'{message.from_user.first_name}_PP_{str(message.from_user.id)}_week{message.text}_year{str(this_year)}'
                    passwd = nb_sql_tasks.decrypt_passwd('KEVIN_SQL', sql_auth['password_key'])
                    engine = nb_sql_tasks.engine(sql_auth, passwd, 'nb_diet_plan')
                    fn, df = sql_reports.get_weekly_nutrition_png(message, table_name, message.text, engine, sql_auth)
                    bot.send_photo(message.from_user.id, open(fn, 'rb'))
                except ProgrammingError:
                    bot.send_message(message.from_user.id, 'Cannot find a diet plan for the week chosen')
                                
        else:
            bot.send_message(message.chat.id, "Please choose an option from the following:", reply_markup=mk.main_keys())                    
    
    bot.infinity_polling()

