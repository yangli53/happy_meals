import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# define a function to take in recipe title and return the top recommended recipes
def recommender(title, indices, df, cosine_sim, top_n):
    # initialize an empty list of recommended recipes
    top_recipes = []
    
    # get the index of the recipe that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the n most similar recipes
    top_idx = score_series.iloc[1:top_n+1].index.tolist()
    
    # get the title of the top n matching recipes
    for i in top_idx:
        top_recipes.append(df.index[i])
        
    return top_recipes

# define a function to print recommended meals
def print_rec(df, i):
    recipe = df['recipe'][i]
    serving = df['serving'][i]    
    calorie = df['calorie'][i]
    link = df['link'][i]
    st.subheader(f'Day {i+1} : {recipe}')
    st.subheader(f'Your serving: {serving}')
    st.subheader(f'Calorie: {calorie}')
    st.write(link)
    
# define a function to plot macronutrient ratio
def plot_nutrient(df, i):
    labels = ['Carbohydrate', 'Protein', 'Fat']
    sizes = [df['carb ratio'][i], df['protein ratio'][i], df['fat ratio'][i]]
    colors = ['lightcoral', 'lightskyblue', 'gold']

    # plot
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
            startangle=90, counterclock=False)
    plt.axis('square')
    st.pyplot();
    
# define a function to take in recommended recipe list and return optimized recipes
def optimizer(rec_recipes, df, protein_lower, protein_upper, calorie, time='off'):
    protein_lower = protein_lower # set protein min
    protein_upper = protein_upper # set protein max 
    fat_limit = 0.35 # set fat_ratio limit
    calorie_limit = calorie # set calorie limit 

    # create a new rec dict
    new_rec = {'recipe': [], 'link': [], 'serving': [], 'calorie': [], 'protein': [], 
               'fat ratio': [], 'protein ratio': [], 'carb ratio': []}

    while len(rec_recipes) > 0:
        if len(new_rec['recipe']) == 5:
            df = pd.DataFrame(new_rec, index=[['Day 1','Day 2','Day 3', 'Day 4', 'Day 5']])
            st.header('Your 5-day dinner plan is ready.')
            for i in range(5):
                print_rec(df, i)
                plot_nutrient(df, i)
            return 

        recipe = np.random.choice(rec_recipes)
        rec_recipes.remove(recipe) 
        
        # check time
        if time == 'on':
            if df.loc[recipe].cook_time > 30 or df.loc[recipe].cook_time == 0:
                continue
            
        # check fat
        if df.loc[recipe].fat_ratio > fat_limit:
            continue
            
        # check calorie
        if df.loc[recipe].calorie > calorie_limit:
            portion = np.round(calorie_limit/df.loc[recipe].calorie, 2) 
            protein = np.round(df.loc[recipe].protein_g * portion)
            
            # check protein
            if protein < protein_lower or protein > protein_upper:
                continue
            calorie = np.round(df.loc[recipe].calorie * portion) 
            serving = np.round(portion/df.loc[recipe].servings, 1)
            fat_ratio = df.loc[recipe].fat_ratio
            protein_ratio = df.loc[recipe].protein_ratio            
            carb_ratio = df.loc[recipe].carb_ratio            
            link = df.loc[recipe].link            
            new_rec['recipe'].append(recipe)
            new_rec['link'].append(link)
            new_rec['serving'].append(serving)
            new_rec['calorie'].append(calorie)
            new_rec['protein'].append(protein)
            new_rec['fat ratio'].append(fat_ratio)
            new_rec['protein ratio'].append(protein_ratio)
            new_rec['carb ratio'].append(carb_ratio)
            
        else:
            portion = np.round(calorie_limit/df.loc[recipe].calorie, 2) 
            protein = np.round(df.loc[recipe].protein_g * portion)
            
            # check protein
            if protein < protein_lower or protein > protein_upper:
                continue
            calorie = np.round(df.loc[recipe].calorie * portion) 
            serving = np.round(portion/df.loc[recipe].servings, 1)
            fat_ratio = df.loc[recipe].fat_ratio
            protein_ratio = df.loc[recipe].protein_ratio            
            carb_ratio = df.loc[recipe].carb_ratio            
            link = df.loc[recipe].link
            new_rec['recipe'].append(recipe)
            new_rec['link'].append(link)
            new_rec['serving'].append(serving)
            new_rec['calorie'].append(calorie)
            new_rec['protein'].append(protein)
            new_rec['fat ratio'].append(fat_ratio)
            new_rec['protein ratio'].append(protein_ratio)
            new_rec['carb ratio'].append(carb_ratio)

    st.write('Running out of recipes. Please start over and choose more preferred meals.')
    return