# HappyMeals
Find the recipes you like to lose weight

## Motivation
A lot of people want to lose weight but many of them fail because it is hard to stick to a diet they don't like. I want to build a web app to recommend recipes based on users' food preferences and calorie needs. In my opinion, people like a recipe because they like the certain combination of ingredients. Thus, I want to build a recipe recommender system based on ingredient similarity. 

In the actual app, 20 random recipes will be provided for users to choose based on their preferences. The app will then recommend 5 similar recipes filtered by calorie and nutrition values based on users' gender, age, height, weight and activity level. I will use Mifflin St. Jeor equation to calculate the daily calorie need of each user. If their goal is to lose weight, I will minus 500 kcal from their daily calorie need according to the healthy weight loss guideline [1] of losing 1-2 lbs per week. I will use the recommended daily protein requirement (>=0.8 g/kg/day) [2] to filter for recipes that meet each user's protein need. I will filter for recipes with no more than 40% fat according the the dietary guideline [3] (ideally no more than 35% but I increase it a little given the primary goal is to lose weight but not to control fat at this moment). I will also add an optional filter for cook time if users prefer quick meals.

## Data
- I scraped over 5,000 recipes from Allrecipes.com with recipe titles, ingredients, ratings, cook time, servings, calorie, protein, fat, carbohydrate, cholesterol and sodium using Selenium (saved as `recipe_data.csv`). Scraper code is not shown here. 

- I cleaned recipe titles, ratings, cook time, servings, calorie, protein, fat, carbohydrate, cholesterol and sodium using Numpy and Pandas (saved as `Clean.ipynb` and `recipe_clean.csv`).

## Approaches
- I cleaned and preprocessed ingredients using natural language processing (NLTK and Gensim) resulting in over 1,000 unique words (saved as `LDA.ipynb`). 

- I decided to use topic modeling (Latent Dirichlet Allocation) 1) to group 1,000+ words to fewer topics and 2) to generate tags for each recipe. Based on coherence score, a measure of semantic similarity among words in a topic, I tuned the hyperparameters including number of topics (k), recipe-topic density (alpha) and topic-word density (beta) (result saved as `lda_tuning_results.csv`). 

- I used pyLDAvis to visualize the result of topic modeling in an interative two-dimensional graph (saved as `recipe_lda.html`).

- I checked the top words in each topic and the recipe titles with high probabilities in each topic and assigned a human readable name to each topic. As a result, I created a dataframe holding all recipes with their probability distribution across all topics (saved as `recipe_lda.csv`). 

- I built a content-based recommender system using cosine similarity and added filters for calorie, nutrition and cook time (saved as `Recommender.ipyng`).

- I created another dataframe holding all recipess with calorie, nutrition and cook time (saved as `recipe_nutrient.csv`).

- I developed a Streamlit-based web app deployed on Heroku (saved as `happy_meals.py` and `helper.py`).

## How to use the app
HappyMeals is accessible at https://happy-meal-plan.herokuapp.com/. 

1. First type in your gender, age, height and current weight and you will see your daily calorie need to maintain your current weight. If you want to lose weight, adjust the goal weight and you will se the time to reach your goal weight. 

2. Decide if you prefer quick meals and choose at least 3 preferred meals from the provided recipe list. Then you will see a recommended 5-day dinner plan with recipe name, your portion from the whole recipe, calorie, link and a pie chart of macronutrient distribution.

## Feedback
This project was completed in 3 weeks and definately needs improvements. If you have any thoughts or suggestions, please email me at yangli102514@gmail.com.

References:
1. https://www.cdc.gov/healthyweight/losing_weight/index.html
2. https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t4/?report=objectonly
3. https://health.gov/our-work/food-nutrition/2015-2020-dietary-guidelines/guidelines/appendix-7/
