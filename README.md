# HappyMeals
Find the recipes you like to lose weight

## Motivation
I have a background in Nutrition and I want to build a web app (https://happy-meal-plan.herokuapp.com/) to generate a 5-day dinner plan based on users' food preferences and calorie needs. I scraped 5,000 recipes from Allrecipes.com and built a recipe recommender system based on ingredient similarity. I embedded a calculator to calculate daily calorie need based on each user's gender, age, height, current weight and goal weight. I also set filters for recipes with optimal nutrition values (less than 40% fat and meet the mininum protein requirement of each user) and for quick meals (optional). This project is a reflection of the combination of my domain knowledge and data science skills. 

## Built with
Python\n
Gensim\n
Streamlit\n
Heroku

## How to use the app
A user will type in gender, age, height, current weight and goal weight. HappyMeals will calculate daily calorie need and weeks to reach goal weight. Then the user will choose if quick meals are preferred and at least 3 preferred meals. Finally, the app will generate a 5-day dinner plan with recipe name, user's portion, calorie, link and a pie chart for macronutrient distribution.

## Feedback
This project was completed in 3 weeks and definately needs improvements. If you have any thoughts or suggestions, please email me at yangli102514@gmail.com.

