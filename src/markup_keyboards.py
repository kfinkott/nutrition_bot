from telebot.util import quick_markup
from datetime import datetime
from telebot.types import InlineKeyboardMarkup

today = datetime.now()
this_week = today.isocalendar().week # week in numerical form, out of 52 for the year

#for every function below:
#the dictionary key is the lable on the button, the callback data value is what is returned via telegram API
#when teh user presses a button

def main_keys() -> InlineKeyboardMarkup:
    """
    Main menu that lets the user choose which path to take
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Ingredient Search': {'callback_data': 'i'},
    'Nutrient Search': {'callback_data': 'n'},
    'Recipe Search': {'callback_data': 'r'},
    'View Diary': {'callback_data': 'view_diary'},
    'View Diet Plan': {'callback_data': 'view_plan'}, 
    'Nutrition report': {'callback_data': 'compare_nutrition'},
    'Clear diary': {'callback_data': 'clear_diary'},
    'Clear plan': {'callback_data': 'clear_plan'},
    'Download data': {'callback_data': 'downloaddata'},
    }, row_width=2)
    return markup

def ing_unit() -> InlineKeyboardMarkup:
    """
    Inline menu for the user to choose the quantity of an ingredient
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup_dict = {
    '25g': {'callback_data': '25g'},
    '50g': {'callback_data': '50g'},
    '100g': {'callback_data': '100g'},
    '200g': {'callback_data': '200g'},
    '454g': {'callback_data': '454g'},
    '908g': {'callback_data': '908g'},
    '1 pcs': {'callback_data': '1p'},    
    }
    # for loop to add callback data containing a dictionary containing 2pcs to 13pcs as keys, for button labels.
    # also adds dictionary values for the callback data, 2pcs to 13pcs
    for i in range(2,13):
        markup_dict[f'{i}pcs'] = {'callback_data': f'{i}p'}    
    markup = quick_markup(markup_dict, row_width=6)
    return markup

def nutrients() -> InlineKeyboardMarkup:
    """
    Inline menu for the user to chooose a nutrient, indexed by integers. The user is also presented with a .png that has a legend for the indexed values
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    # for loop that creates a dictionary with keys 0 through 65 that label the keyboard buttons
    # the values are also 0 through 65, callback data
    markup_dict = {}
    for x in range(65):
        markup_dict[str(x)] = {'callback_data': str(x)}
    markup = quick_markup(markup_dict, row_width=5)
    return markup

def more_nut() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to see more results from searching by nutrient
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Show more results': {'callback_data': 'more_nut'}, #callback to show more results per nutrient selected
    'Exit': {'callback_data': 'exit_nut'}  
    }, row_width=2)
    return markup

def submit_ing(df_title: list) -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose if they want to add the ingredient that they found to a diary or a diet plan
    
    Args:
    df_title (list) : returns an object that can be used in Telegram API POSTs
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Add to diary': {'callback_data': f'choose_diary+{df_title[0]}'}, #adds the selected ingredient to the user's diary. df_title[0] is the SQL table for the ingredient
    'Add to diet plan': {'callback_data': f'choose_plan+{df_title[0]}'}, #adds the selected ingredient to the user's diet plan. df_title[0] is the SQL table for the ingredient
    'Exit': {'callback_data': 'exit_nut'}  
    }, row_width=2)
    return markup

def choose_diary_meal(df_title: str) -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose a day and meal time for adding an entry to their diary 
    
    Args:
    df_title (str) : The name of the SQL tables representing the entry to be added
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Sun bf': {'callback_data': f'add_diary+{df_title}db'}, #df_title is the SQL table for the ingredient
    'Sun ln': {'callback_data': f'add_diary+{df_title}dl'},
    'Sun dn': {'callback_data': f'add_diary+{df_title}dd'},
    'Mon bf': {'callback_data': f'add_diary+{df_title}mb'},
    'Mon ln': {'callback_data': f'add_diary+{df_title}ml'},
    'Mon dn': {'callback_data': f'add_diary+{df_title}md'},
    'Tue bf': {'callback_data': f'add_diary+{df_title}tb'},
    'Tue ln': {'callback_data': f'add_diary+{df_title}tl'},
    'Tue dn': {'callback_data': f'add_diary+{df_title}td'},
    'Wed bf': {'callback_data': f'add_diary+{df_title}wb'},
    'Wed ln': {'callback_data': f'add_diary+{df_title}wl'},
    'Wed dn': {'callback_data': f'add_diary+{df_title}wd'},
    'Thu bf': {'callback_data': f'add_diary+{df_title}jb'},
    'Thu ln': {'callback_data': f'add_diary+{df_title}jl'},
    'Thu dn': {'callback_data': f'add_diary+{df_title}jd'},    
    'Fri bf': {'callback_data': f'add_diary+{df_title}fb'},   
    'Fri ln': {'callback_data': f'add_diary+{df_title}fl'},    
    'Fri dn': {'callback_data': f'add_diary+{df_title}fd'},    
    'Sat bf': {'callback_data': f'add_diary+{df_title}sb'},    
    'Sat ln': {'callback_data': f'add_diary+{df_title}sl'},    
    'Sat dn': {'callback_data': f'add_diary+{df_title}sd'}    
    }, row_width=5)
    return markup

def choose_plan_meal(df_title: str) -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose a day and meal time for adding an entry to their diary
    
    Args:
    df_title (str) : The name of the SQL table for the entry to be added
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Sun bf': {'callback_data': f'add_plan+{df_title}db'}, #df_title is the SQL table for the ingredient
    'Sun ln': {'callback_data': f'add_plan+{df_title}dl'},
    'Sun dn': {'callback_data': f'add_plan+{df_title}dd'},
    'Mon bf': {'callback_data': f'add_plan+{df_title}mb'},
    'Mon ln': {'callback_data': f'add_plan+{df_title}ml'},
    'Mon dn': {'callback_data': f'add_plan+{df_title}md'},
    'Tue bf': {'callback_data': f'add_plan+{df_title}tb'},
    'Tue ln': {'callback_data': f'add_plan+{df_title}tl'},
    'Tue dn': {'callback_data': f'add_plan+{df_title}td'},
    'Wed bf': {'callback_data': f'add_plan+{df_title}wb'},
    'Wed ln': {'callback_data': f'add_plan+{df_title}wl'},
    'Wed dn': {'callback_data': f'add_plan+{df_title}wd'},
    'Thu bf': {'callback_data': f'add_plan+{df_title}jb'},
    'Thu ln': {'callback_data': f'add_plan+{df_title}jl'},
    'Thu dn': {'callback_data': f'add_plan+{df_title}jd'},    
    'Fri bf': {'callback_data': f'add_plan+{df_title}fb'},   
    'Fri ln': {'callback_data': f'add_plan+{df_title}fl'},    
    'Fri dn': {'callback_data': f'add_plan+{df_title}fd'},    
    'Sat bf': {'callback_data': f'add_plan+{df_title}sb'},    
    'Sat ln': {'callback_data': f'add_plan+{df_title}sl'},    
    'Sat dn': {'callback_data': f'add_plan+{df_title}sd'}
    }, row_width=6)
    return markup

def view_diary() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to receive a daily or weekly diary report or to subscribe/unsubscribe to automatic weekly reports                  
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Day report': {'callback_data': 'diary_daily'},
    'Week report': {'callback_data': 'diary_weekly'},    
    'Auto weekly report': {'callback_data': 'diary_auto_weekly'},
    'Stop weekly report': {'callback_data': 'diary_auto_weekly_rem'}
    }, row_width=2)
    return markup

def view_plan() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to receive a daily or weekly diet plan report or to subscribe/unsubscribe to automatic weekly reports
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Day report': {'callback_data': 'plan_daily'},
    'Week report': {'callback_data': 'plan_weekly'},
    'Auto weekly report': {'callback_data': 'plan_auto_weekly'},
    'Stop weekly report': {'callback_data': 'plan_auto_weekly_rem'}
    }, row_width=2)
    return markup

def diary_choose_weekday() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose the weekday for their diary report
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Sunday': {'callback_data': 'weekday_diarySunday'},
    'Monday': {'callback_data': 'weekday_diaryMonday'},
    'Tuesday': {'callback_data': 'weekday_diaryTuesday'},    
    'Wednesday': {'callback_data': 'weekday_diaryWednesday'},    
    'Thursday': {'callback_data': 'weekday_diaryThursday'},    
    'Friday': {'callback_data': 'weekday_diaryFriday'},    
    'Saturday': {'callback_data': 'weekday_diarySaturday'},
    }, row_width=4)
    return markup

def plan_choose_weekday() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose the weekday for their diet plan report
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Sunday': {'callback_data': 'weekday_planSunday'},
    'Monday': {'callback_data': 'weekday_planMonday'},
    'Tuesday': {'callback_data': 'weekday_planTuesday'},    
    'Wednesday': {'callback_data': 'weekday_planWednesday'},    
    'Thursday': {'callback_data': 'weekday_planThursday'},    
    'Friday': {'callback_data': 'weekday_planFriday'},    
    'Saturday': {'callback_data': 'weekday_planSaturday'},
    }, row_width=4)
    return markup

def diary_choose_week() -> InlineKeyboardMarkup:
    """
     Inline menu that allows the user to choose to view this week's or last week's diary summary
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'This week': {'callback_data': f'week_diary{this_week}'},
    'Last week': {'callback_data': f'week_diary{this_week -1}'}
    }, row_width=2)
    return markup

def plan_choose_week() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to view this week's or last week's diet plan summary
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'This week': {'callback_data': f'week_plan{this_week}'},
    'Last week': {'callback_data': f'week_plan{this_week -1}'}
    }, row_width=2)
    return markup

def diary_nut_choose_week() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to view this week's or last week's diary nutrition report
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'This week': {'callback_data': f'week_nut_diary{this_week}'},
    'Last week': {'callback_data': f'week_nut_diary{this_week -1}'}
    }, row_width=2)
    return markup

def plan_nut_choose_week() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to view this week's or last week's diet plan nutrition report
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'This week': {'callback_data': f'week_nut_plan{this_week}'},
    'Last week': {'callback_data': f'week_nut_plan{this_week -1}'}
    }, row_width=2)
    return markup

def request_legend() -> InlineKeyboardMarkup:
    """
    Inline menu that lets the user choose to view a legend showing the measurement units used for nutrient data
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Nutrient weight units legend': {'callback_data': 'show_legend'}
    }, row_width=1)
    return markup
    
def nutrition_choice() -> InlineKeyboardMarkup:
    """
    Inline menu that allows a user to choose to view this week's or last week's nutrition diary vs diet plan comparison report
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'Report (this week)': {'callback_data': f'show_comparison_weekly{this_week}'},
    'Report (last week)': {'callback_data': f'show_comparison_weekly{this_week-1}'},
    }, row_width=2)
    return markup

def clear_diary_wkday() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to clear all entries for one weekday of this week's diary
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    markup_dict = {}
    for w in weekdays:        
        markup_dict[w] = {'callback_data': f'clear_diary{w}'}
    markup = quick_markup(markup_dict, row_width=4)
    return markup

def clear_plan_wkday() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to clear all entries for one weekday of this week's diet plan
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    markup_dict = {}
    for w in weekdays:        
        markup_dict[w] = {'callback_data': f'clear_plan{w}'}
    markup = quick_markup(markup_dict, row_width=4)
    return markup

def recipe_search_choice() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose to search for a recipe by recipe name, ingrdient name or nutrient name
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    markup = quick_markup({
    'By recipe': {'callback_data': 'recipe_r'},
    'By ingredient': {'callback_data': 'recipe_i'},
    'By nutrient': {'callback_data': 'recipe_n'}    
    }, row_width=3)
    return markup    

def recipe_choice(api_response: list) -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose a recipe from a list of recipes
    
    Args:
    api_response (list) : JSON object that contains the list of recipes and their IDs returned by the spoonacular API
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    titles = [t['title'] for t in api_response] # creates a list of recipe results returned by the spoonacular API
    ids = [i['id'] for i in api_response]
    count = 0
    markup_dict = {}
    for t in titles:
        markup_dict[t] = {'callback_data': f'recipe_id{ids[count]}'}
        count += 1
    markup = quick_markup(markup_dict, row_width=1)
    return markup
    
def recipe_n() -> InlineKeyboardMarkup:
    """
    Inline menu that allows the user to choose from a list of nutrients. The chosen nutrient is used to search for a recipe that is high in that nutrient
    
    Returns:
    InlineKeyboardMarkup: returns an object that can be used in Telegram API POSTs
    """
    nutrient_dict = {'Carbs': 'minCarbs', 'Protein': 'minProtein', 'Calories': 'minCalories', 'Fat': 'minFat', 'Copper': 'minCopper', 
                     'Calcium': 'minCalcium', 'Choline': 'minCholine', 'Sat. fat': 'minSaturatedFat', 
                     'Vit A': 'minVitaminA', 'Vit C': 'minVitaminC', 'Vit D': 'minVitaminD', 'Vit E': 'minVitaminE', 'Vit K': 'minVitaminK',
                     'Vit B1': 'minVitaminB1', 'Vit B2': 'minVitaminB2', 'Vit B3': 'minVitaminB3', 'Vit B5': 'minVitaminB5', 
                     'Vit B6': 'minVitaminB6', 'Vit B12': 'minVitaminB12', 'Fiber': 'minFiber', 'Folate': 'minFolate',
                     'Iodine': 'minIodine', 'Iron': 'minIron', 'Magnesium': 'minMagnesium', 'Manganese': 'minManganese', 
                     'Phosphorus': 'minPhosphorus', 'Potassium': 'minPotassium', 'Selenium': 'minSelenium', 'Sugar': 'minSugar', 'Zinc': 'minZinc'}
    markup_dict = {}
    for n in nutrient_dict.keys():
        markup_dict[n] = {'callback_data': f'recipe_n_choice{nutrient_dict[n]}'}
    markup = quick_markup(markup_dict, row_width=3)
    return markup
        
