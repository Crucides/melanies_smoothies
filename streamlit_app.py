# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in yout custom smoothie !"""
)

#option = st.selectbox(
#    "What is your favorite fruit ?",
#    ("Banana", "Strawberries", "Peaches"),)
#st.write("Your favorite fruit is :", option)
Customer = st.text_input('Your Name ?')
st.write("The name on yout smoothie will be :", Customer)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingrediants :', my_dataframe, max_selections=5)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        #st.subheader(each_fruit + ' Nutrition Information')
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+each_fruit )
        #fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=true)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','""" + Customer +  """');"""
    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=true)
