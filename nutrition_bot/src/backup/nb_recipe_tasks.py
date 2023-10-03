#kevin fink
#kevin@shorecode.org
#Sept 19 2023
#nutrition_bot/nb_recipe_tasks.py

from dataclasses import dataclass
import requests
import pandas as pd
import nb_api_fetch
import nb_data_viz

@dataclass
class RecipeSearch:
    nb_api: nb_api_fetch.Nb_api
    def recipe_search(self, query: str) -> dict:
        """
        Searches the spoonacular API using the recipe name provided
        
        Args:
        self ( _obj_ ) : class object
        query (str) : Recipe name
        
        Returns:
        dict:  Spoonacular API response
        """
        # number of recipes returned by teh spoonacular API
        number_of_results = 12
        api_response = self.nb_api.fetch_recipes(query, number_of_results, self.nb_api.token)
        return api_response
    def ing_search(self, query: str) -> list:
        """
        Searches the spoonacular API using the ingredient name provided
        
        Args:
        self ( _obj_ ) : class object
        query (str) : Ingredient name
        
        Returns:
        list:  Spoonacular API response
        """
        # number of recipes returned by teh spoonacular API
        number_of_results = 12
        api_response = self.nb_api.fetch_recipe_by_ing(query, number_of_results, self.nb_api.token)
        return api_response
    def nutrient_search(self, query: str) -> list:
        """
        Searches the spoonacular API using the nutrient name provided
        
        Args:
        self ( _obj_ ) : class object
        query (str) : Nutrient name
        
        Returns:
        list:  Spoonacular API response
        """
        # number of recipes returned by teh spoonacular API
        number_of_results = 12
        api_response = self.nb_api.fetch_recipe_by_nutrient(query, number_of_results,
                                                            self.nb_api.token)
        return api_response
    def id_search(self, query: str) -> requests.Response:
        """
        Searches the spoonacular API for a specific recipe by ID
        
        Args:
        self ( _obj_ ) : class object
        query (str) : Recipe ID
        
        Returns:
        requests.Response:  Spoonacular API response
        """
        self.api_response = self.nb_api.fetch_recipe_id(str(query), self.nb_api.token)
        # Dataframe title
        df_title = self.nb_api.fetch_recipe_title(query, self.nb_api.token)
        return self.api_response, df_title
    def recipe_df(self, response: requests.Response) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Creates a dataframe from the Spoonacular response and splits it in two
        
        Args:
        self ( _obj_ ) : class object
        response (requests.Response) : Spoonacular API response
        
        Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Returns the complete dataframe
          and the dataframe split in two
        """
        # Creates a dataframe using the combined json sections from the spoonacular API
        self.recipe_df = pd.DataFrame(response.json()['nutrition']['nutrients'] +
                                      response.json()['nutrition']['flavonoids'] +
                                      [response.json()['nutrition']['properties'][2]] +
                                      [{'amount': response.json()['pricePerServing'],
                                        'name': 'Estimated cost', 'unit': 'US cents'}])
        self.recipe_df.set_index('name')
        # Splits the Dataframe for another function that places the splits side by side in an image
        df_len = len(self.recipe_df.index)
        df1 = self.recipe_df.iloc[:df_len//2]
        df2 = self.recipe_df.iloc[df_len//2:]
        return self.recipe_df, df1, df2
    def recipe_img(self, df1: pd.DataFrame, df2: pd.DataFrame, df_title: list) -> str:
        """
        Creates an image showing the nutritional value of the recipe
        
        Args:
        self ( _obj_ ) : class object
        df1 (pd.DataFrame) : Dataframe
        df2 (pd.DataFrame) : Dataframe;
        df_title (list) : Title of the dataframe
        
        Returns:
        str: File path for the recipe image
        """
        fn = nb_data_viz.export_png(df1, df_title, page2=False)
        fn2 = nb_data_viz.export_png(df2, df_title, page2=True)
        final_img = nb_data_viz.collate_photos(fn, fn2)
        return final_img
    def get_recipe_card(self, recipe_id: str) -> dict:
        """
        Retrieves a recipe card from the Spoonacular API that shows 
        ingredients and instructions to cook
        
        Args:
        self ( _obj_ ) : class object
        recipe_id (str) : Recipe ID
        
        Returns:
        dict: Spoonacular API response
        """
        api_response = self.nb_api.fetch_recipe_card(recipe_id, self.nb_api.token)
        return api_response
