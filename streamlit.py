# import streamlit as st
# import streamlit.components.v1 as components
# import os
# #################################
# car_types = ['Toyota','Mitsubishi','Ford','Fiat']
# car = st.text_input("Type a car")
# button = st.button("Check availability")

# if button == True:
#     have_it = car.lower() in [c.lower() for c in car_types]
#     if have_it:
#         st.write("We have that car")
#     else:
#         st.write("We dont have that car")
# #################################
# file_name = st.text_input("Enter File name")
# with open('image.jpg',"rb") as file:
#     btn = st.download_button(
#         label="Download Image",
#         data=file,
#         file_name=file_name,
#         mime="image/png"
#     )




# st.title("Display Local HTML File")

# # Read local HTML file
# with open("./virtual-tour/VT04.html", "r", encoding="utf-8") as f:
#     html_content = f.read()

# components.html(html_content, height=600)