import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import helper
from sklearn.metrics.pairwise import cosine_similarity


st.header("Happy Meals")

# user input demographic info
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

df_nutrient = pd.read_csv('dinner_nutrient.csv')
df_nutrient.set_index('title', inplace=True)

quick_meal = st.radio('Do you prefer only quick meals (ready in 30 minutes)?',
                     ('Yes', 'No'))
    
# choose 2 most relevant recipes from each topic to show as choices
recipe_option_1 = []
for topic in lda_matrix.columns.tolist():
    dish_ls = lda_matrix[topic][lda_matrix[topic] >= 0.8].index.tolist()
    recipe_ls = dish_ls[:2]
    recipe_option_1.extend(recipe_ls)
    
options = st.multiselect('Please choose at least 3 meals that fit into your usual diet well.', 
                         options=(recipe_option_1))

# provide more meal choices
recipe_option_2 = []
for topic in lda_matrix.columns.tolist():
    dish_ls = lda_matrix[topic][lda_matrix[topic] >= 0.85].index.tolist()
    recipe_ls = dish_ls[2:4]
    recipe_option_2.extend(recipe_ls)

options_2 = st.multiselect('More choices', options=(recipe_option_2))

recipe_option_3 = []
for topic in lda_matrix.columns.tolist():
    dish_ls = lda_matrix[topic][lda_matrix[topic] >= 0.85].index.tolist()
    recipe_ls = dish_ls[4:6]
    recipe_option_3.extend(recipe_ls)

options_3 = st.multiselect('And more', options=(recipe_option_3))

options.extend(options_2)
options.extend(options_3)

        
if st.button('Submit'):

    # use recommender
    ## calculate cosine similarity
    lda_array = lda_matrix.to_numpy()
    cosine_sim = cosine_similarity(lda_array)

    ## creating a Series for recipe titles
    indices = pd.Series(lda_matrix.index)

    ## get top 100 similar recipes for each option
    total_rec_recipes = []
    for title in options:
        rec_recipes = helper.recommender(title, indices, lda_matrix, cosine_sim, 100)
        total_rec_recipes.extend(rec_recipes)
                        
    # use optimizer
    ## calculate protein and calorie needs per meal
    protein_lower = wt_kg * 0.8 / 3
    protein_upper = wt_kg * 2.2 / 3
    if goal_wt:
        calorie_need = new_calorie / 3
    else:
        calorie_need = calorie / 3

    ## use optimizer
    if quick_meal == 'Yes':
        helper.optimizer(total_rec_recipes, df_nutrient, protein_lower, protein_upper, 
                         calorie_need, time='on')
    else:
        helper.optimizer(total_rec_recipes, df_nutrient, protein_lower, protein_upper, 
                         calorie_need)
        
        
