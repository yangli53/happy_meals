import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

st.header("Happy Meals")

age = st.number_input('Age')
gender = st.radio(label='Gender', options=('M', 'F'))
ht = st.number_input('Height (cm)')
wt = st.number_input('Current weight (kg)')
active = st.radio(label='Activity level', 
options=('Sedentary', 'Lightly active', 'Moderately active', 'Very active'))
goal_wt = st.number_input('Goal weight (kg)')

# calculate daily calorie need
if gender == 'M':
	calorie = 10 * wt + 6.25 * ht - 5 * age + 5
else:
	calorie = 10 * wt + 6.25 * ht - 5 * age - 161

if active == 'Sedentary':
	calorie *= 1.2
elif active == 'Lightly active':
	calorie *= 1.375
elif active == 'Moderately active':
	calorie *= 1.55
else:
	calorie *= 1.725

st.write('Your daily calorie need is', calorie, '.')
st.write('Your need', 0, 'days to reach your goal weight.')


meal = st.radio(label="Which meal looks more appealing to you?", 
options=('Baked Dijon Salmon', 'Sukis Spinach And Feta Pasta', 
'Grilled Korean Style Beef Short Ribs'))

# build prediction model
df_model = pd.read_csv('dinner_model.csv')
df_model = df_model.set_index('title')
drop_0 = df_model[df_model.category == 0].index.tolist()[11:]
drop_1 = df_model[df_model.category == 1].index.tolist()[11:]
drop_0_1 = drop_0 + drop_1
df_model.drop(drop_0_1, inplace=True)

X = df_model.iloc[:,:-1]
y = df_model.iloc[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
knn_3 = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)

# input recipe to predict
df_predict = pd.read_csv('dinner_predict.csv')
df_predict.set_index('title', inplace=True)
X_predict = pd.DataFrame(columns=df_predict.columns.tolist())
X_predict = X_predict.append(df_predict.loc[meal])
y_predict = knn_3.predict(X_predict)

labels = {'American': 0, 'Italian': 1, 'Asian': 2, 'Mexican': 3, 'Other': 4}

if y_predict == 0:
	st.write('This is an American dish.')
elif y_predict == 1:
	st.write('This is an Italian dish.')
elif y_predict == 2:
	st.write('This is an Asian dish.')
elif y_predict == 3:
	st.write('This is a Mexican dish.')
else:
	st.write('This is an Other dish.')