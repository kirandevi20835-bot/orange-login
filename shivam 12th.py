import streamlit  as st
import pndas as pd
from skleaarn.model_selection import train_test_split
from skleaarn.linear-model import linearRegression
df = pd.read_csv("data.csv")
X = df[['hoursStudied']]
Y = df['examScore']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
model=LinearRegression()
model.fit(X_train, y_train)
st.title("exam score predictor")
st.write("Enter hours studied to predict the exam score.")
hours = st.number_input("Hours Studied:",min_value=0.0, step=0.1)
if st.button("predicted score")
   predicted_score = model.predict([[hours]])[0]
` st.sucess(f"predicted score:{predicted_score}")
st.wreitter("###Sample Training Data")
st.dataframe(df)
