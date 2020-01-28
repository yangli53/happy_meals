import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity


st.header("Happy Meals")

# user input personal info
gender = st.radio(label='Gender', options=('M', 'F'))
age = st.number_input('Age')
ht = st.number_input('Height (in)')
wt = st.number_input('Current weight (lb)')
active = st.radio(label='Activity level', 
         options=('Sedentary (little or no exercise)', 
         'Lightly active (light exercise/sports 1-3 days/week)', 
         'Moderately active (moderate exercise/sports 3-5 days/week)', 
         'Very active (hard exercise/sports 6-7 days a week)',
         'extra active (very hard exercise/sports & physical job or 2x training)'))
goal_wt = st.number_input('Goal weight (lb)')

# calculate current daily calorie need
ht_cm = np.round(ht * 2.54)
wt_kg = np.round(wt / 2.2)

if gender == 'M':
    calorie = 10 * wt_kg + 6.25 * ht_cm - 5 * age + 5
else:
    calorie = 10 * wt_kg + 6.25 * ht_cm - 5 * age - 161

if active == 'Sedentary (little or no exercise)':
    calorie *= 1.2
elif active == 'Lightly active (light exercise/sports 1-3 days/week)':
    calorie *= 1.375
elif active == 'Moderately active (moderate exercise/sports 3-5 days/week)':
    calorie *= 1.55
elif active == 'Very active (hard exercise/sports 6-7 days a week)':
    calorie *= 1.725
else:
    calorie *= 1.9

calorie = np.round(calorie)
st.write('Your daily calorie need is', calorie, 'kcal to maintain your current weight.')

# calculate days to reach goal wt
if goal_wt:
    week = (wt - goal_wt) / 1
    new_calorie = calorie - 500
    if new_calorie >= 1200:
        st.write('Your daily calorie need is', new_calorie, 
                 'kcal to lose weight and you need', week, 
                 'weeks to reach your goal weight.')
    else:
        st.write('Warning! You daily calorie need is lower than 1200 kcal. Please', 
                 'either increase your goal weight or increase your activity level to',
                 'ensure adequate daily nutrition.')


# user input meal preferences
# load data
lda_matrix = pd.read_csv('lda_matrix.csv')
lda_matrix.set_index('title', inplace=True)

# choose 2 most relevant recipes from each topic to show as choices
recipe_options = []
for topic in lda_matrix.columns.tolist():
    dish_ls = lda_matrix[topic][lda_matrix[topic] >= 0.8].index.tolist()
    recipe_ls = dish_ls[:2]
    recipe_options.extend(recipe_ls)
    
options = st.multiselect('Please choose at least 3 meals that fit into your usual diet well.', 
          options=(recipe_options))


if st.button('submit'):

    # use recommender
    ## calculate cosine similarity
    lda_array = lda_matrix.to_numpy()
    cosine_sim = cosine_similarity(lda_array)

    ## creating a Series for recipe titles
    indices = pd.Series(lda_matrix.index)

    ## define a function to take in recipe title and return the top recommended recipes
    def recommender(title, df=lda_matrix, cosine_sim=cosine_sim, top_n=10):   
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

    ## get top 100 similar recipes for each option
    total_rec_recipes = []
    for title in options:
        rec_recipes = recommender(title, top_n=100)
        total_rec_recipes.extend(rec_recipes)
            
            
    # use optimizer
    ## load data
    df_nutrient = pd.read_csv('dinner_nutrient.csv')
    df_nutrient = df_nutrient.set_index('title')
    
    ## define a function to print recommended meals
    def print_rec(df, i):
        """
        Print recommendation
        """
        serving = df['your serving'][i]
        recipe = df['recipe'][i]
        calorie = df['calorie'][i]
        link = df['link'][i]
        st.write(f'Your day {i+1} meal is {serving} serving(s) of "{recipe}" with {calorie} kcal at:\n{link}.')
    
    ## define a function to plot macronutrient ratio
    def plot_nutrient(df, i):
        """
        Plot nutrient ratios
        """
        labels = ['Carbohydrate', 'Protein', 'Fat']
        sizes = [df['carb ratio'][i], df['protein ratio'][i], df['fat ratio'][i]]
        colors = ['lightcoral', 'lightskyblue', 'gold']

        # plot
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                startangle=150, counterclock=False)
        plt.axis('square')
        st.pyplot();
    
    
    ## define a function to take in recommended recipe list and return optimized recipes
    def optimizer(rec_recipes, protein, calorie):
        """
        Optimize recipes by setting nutrition thresholds
        """
        protein_cut = protein # set protein threshold
        fat_cut = 0.35 # set fat_ratio threshold
        calorie_cut = calorie # set calorie threshold 

        # create a new rec dict
        new_rec = {'recipe': [], 'link': [], 'calorie': [], 'protein': [], 'protein ratio': [], 'fat ratio': [], 
                   'carb ratio': [], 'your serving': [], 'recipe serving': []}

        while len(rec_recipes) > 0:
            if len(new_rec['recipe']) == 3:
                df = pd.DataFrame(new_rec, index=[['Day 1','Day 2','Day 3']])
                for i in range(3):
                    print_rec(df, i)
                    plot_nutrient(df, i)
                return 

            recipe = np.random.choice(rec_recipes)  
            rec_recipes.remove(recipe)      

            # check fat
            if df_nutrient.loc[recipe].fat_ratio > fat_cut:
                continue
            # check calorie
            if df_nutrient.loc[recipe].calorie > calorie_cut:
                portion = np.round(calorie_cut/df_nutrient.loc[recipe].calorie, 2) 
                protein = np.round(df_nutrient.loc[recipe].protein_g * portion)
                # check protein
                if protein < protein_cut:
                    continue
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

        st.write('Running out of recipes. Please start over and choose more preferred meals.')
        return
               

    ## calculate protein and calorie
    protein_need = wt_kg * 0.8
    if goal_wt:
        calorie_need = new_calorie / 3
    else:
        calorie_need = calorie / 3

    ## use optimizer
    optimizer(total_rec_recipes, protein_need, calorie_need)

