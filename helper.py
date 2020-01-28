import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# load data
df_cluster = pd.read_csv('dinner_cluster.csv')
df_cluster = df_cluster.rename(columns={'Unnamed: 0': 'title'}).set_index('title')

# calculate cosine similarity
ingred_maxtrix = df_cluster.to_numpy()
cosine_sim = cosine_similarity(ingred_maxtrix)

# creating a Series for recipe titles
indices = pd.Series(df_cluster.index)

# define a function to take in recipe title and return the top 10 recommended recipes
def recommender(title, df=df_cluster, cosine_sim=cosine_sim, top_n=10):   
    # initialize an empty list of recommended recipes
    rec_recipes = []
    
    # get the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the n most similar movies
    top_n_idx = score_series.iloc[1:top_n+1].index.tolist()
    
    # get the title of the top n matching recipes
    for i in top_n_idx:
        rec_recipes.append(df.index[i])
        
    return rec_recipes

# load data
df_nutrient = pd.read_csv('dinner_nutrient.csv')
df_nutrient = df_nutrient.set_index('title')

# optimize recommendation
def optimize_recipe(rec_recipes, protein, calorie, fat=0.35):
    protein_cut = protein # set protein threshold
    fat_cut = fat # set fat_ratio threshold
    calorie_cut = calorie # set calorie threshold 
    
    # create a new rec dict
    new_rec = {'recipe':[],'link':[],'calorie':[],'protein':[],'protein ratio':[],
    		   'fat ratio':[],'carb ratio':[],'your serving':[],'recipe serving':[]}
    
    while len(rec_recipes) > 0:
        if len(new_rec['recipe']) == 5:
            print('Please find your 5-day dinner plan below.')
            df = pd.DataFrame(new_rec, index=[['Day 1','Day 2','Day 3','Day 4','Day 5']])
            print(df)
            return df
        else:
            recipe = np.random.choice(rec_recipes)
            rec_recipes.remove(recipe)

            recipe = recipe             

            # check fat
            if df_nutrient.loc[recipe].fat_ratio > fat_cut:
                continue
            else:
                # check calorie
                if df_nutrient.loc[recipe].calorie > calorie_cut:
                    portion = np.round(calorie_cut/df_nutrient.loc[recipe].calorie, 2) 
                    protein = np.round(df_nutrient.loc[recipe].protein_g * portion)
                    # check protein
                    if protein < protein_cut:
                        continue
                    else:
                        calorie = np.round(df_nutrient.loc[recipe].calorie * portion) 
                        protein_ratio = df_nutrient.loc[recipe].protein_ratio
                        fat_ratio = df_nutrient.loc[recipe].fat_ratio
                        carb_ratio = df_nutrient.loc[recipe].carb_ratio
                        serving = df_nutrient.loc[recipe].servings
                        link = df_nutrient.loc[recipe].link
                        new_rec['recipe'].append(recipe)
                        new_rec['link'].append(link)
                        new_rec['calorie'].append(calorie)
                        new_rec['protein'].append(protein)
                        new_rec['protein ratio'].append(protein_ratio)
                        new_rec['fat ratio'].append(fat_ratio)
                        new_rec['carb ratio'].append(carb_ratio)
                        new_rec['your serving'].append(portion)
                        new_rec['recipe serving'].append(serving)
                else:
                    portion = np.round(calorie_cut/df_nutrient.loc[recipe].calorie, 2) 
                    protein = np.round(df_nutrient.loc[recipe].protein_g * portion)
                    # check protein
                    if protein < protein_cut:
                        continue
                    else:
                        calorie = np.round(df_nutrient.loc[recipe].calorie * portion) 
                        protein_ratio = df_nutrient.loc[recipe].protein_ratio
                        fat_ratio = df_nutrient.loc[recipe].fat_ratio
                        carb_ratio = df_nutrient.loc[recipe].carb_ratio
                        serving = df_nutrient.loc[recipe].servings
                        link = df_nutrient.loc[recipe].link
                        new_rec['recipe'].append(recipe)
                        new_rec['link'].append(link)
                        new_rec['calorie'].append(calorie)
                        new_rec['protein'].append(protein)
                        new_rec['protein ratio'].append(protein_ratio)
                        new_rec['fat ratio'].append(fat_ratio)
                        new_rec['carb ratio'].append(carb_ratio)
                        new_rec['your serving'].append(portion)
                        new_rec['recipe serving'].append(serving)
    
    print('Running of recipes. Please choose more appealing meals.')