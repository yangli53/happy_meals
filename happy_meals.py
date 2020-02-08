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
age = st.number_input('Age', value=18, step=1)
ht = st.number_input('Height (in)', value=60, step=1)
wt = st.number_input('Current weight (lb)', value=100, step=1)
active = st.radio(label='Activity level', 
         options=('Sedentary (little or no exercise)', 
         'Lightly active (light exercise/sports 1-3 days/week)', 
         'Moderately active (moderate exercise/sports 3-5 days/week)', 
         'Very active (hard exercise/sports 6-7 days a week)',
         'extra active (very hard exercise/sports & physical job or 2x training)'))
goal_wt = st.number_input('Goal weight (lb)', value=wt, step=1)

# calculate current daily calorie need based on Mifflin St. Jeor equation
ht_cm = ht * 2.54
wt_kg = wt / 2.2

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

# output daily calorie need
if goal_wt == wt:
    st.write('Your daily calorie need is', calorie, 'to maintain your current weight.')

# calculate weeks to reach goal based on recommendation that losing 1 lb/week
elif goal_wt < wt:
    week = wt - goal_wt 
    new_calorie = calorie - 500
    if new_calorie >= 1200:
        st.write('Your daily calorie need is', new_calorie, 
                 'to lose weight and you need', week, 
                 'weeks to reach your goal.')
    else:
        st.write('Warning! You daily calorie need is lower than 1200. Please either', 
                 'increase your goal weight or increase your activity level to',
                 'ensure adequate daily nutrition.')

else:
    st.write('Oops! Your goal weight is over your current weight.')


# user input meal preferences
# load data
lda_matrix = pd.read_csv('recipe_lda.csv')
lda_matrix.set_index('title', inplace=True)
df_nutrient = pd.read_csv('recipe_nutrient.csv')
df_nutrient.set_index('title', inplace=True)

quick_meal = st.radio('Do you prefer only quick meals (ready in 30 minutes)?',
                     ('Yes', 'No'))
    
# provide meal choices randomly
@st.cache()
def recipe_choices():
    return np.random.choice(lda_matrix.index.tolist(), 20)
options = st.multiselect('Please choose at least 3 meals you like.', 
                         options=(recipe_choices()))

        
if st.button('Submit'):

    # use recommender
    ## calculate cosine similarity
    lda_array = lda_matrix.to_numpy()
    cosine_sim = cosine_similarity(lda_array)
    
    ## creating a Series for recipe titles
    indices = pd.Series(lda_matrix.index)

    ## get top 100 similar recipes for each option
    rec_recipes = []
    for title in options:
        top_recipes = helper.recommender(title, indices, lda_matrix, cosine_sim, 100)
        rec_recipes.extend(top_recipes)
    
    rec_recipes = list(set(rec_recipes))
                        
    # use optimizer
    ## calculate protein and calorie needs per meal
    protein_lower = np.round(wt_kg * 0.8 / 3, 1)
    if goal_wt < wt:
        calorie_need = np.round(new_calorie / 3)
    else:
        calorie_need = np.round(calorie / 3)

    ## use optimizer
    if quick_meal == 'Yes':
        helper.optimizer(rec_recipes, df_nutrient, protein_lower, calorie_need, time='on')
    else:
        helper.optimizer(rec_recipes, df_nutrient, protein_lower, calorie_need)
        
        
