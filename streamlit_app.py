# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: 24/7 Customize Smoothies")
st.write(
  """ Choose the fruit that you want for your smoothies!
  """
)
from snowflake.snowpark.functions import col

import streamlit as st

name_on_order = st.text_input("Name of Smoothies", )
st.write("The name of your smoothies will be:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
ingredients_string = ''

if ingredients_list:
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

 
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

#st.write(my_insert_stmt)
#st.stop()

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

cnx = st.connect("snowflake")
session = cnx.session();
