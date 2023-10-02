import pdfkit
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' #comment this line when deploying in streamlit
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) #comment this line when deploying in streamlit
import os
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(layout="centered", page_icon="", page_title=" NHW02")
st.title("Econ 2013 News Analysis Homework 02: EV Market ")
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
#   st.button("Click me")
# Load HTML template
    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())

    template = env.get_template("template.html")
    st.write("The purpose of this page is to answer questions and generate a pdf file to be submitted in gradescope under the submission portal "
             "corresponding to the assignment name. You are not submitting in streamlit anything-- you are just generating a pdf file")
    form = st.form("template_form")

    username = form.text_input("Full NAME: Last, first", placeholder="Doe, John")
    form.markdown("***The questions:***")
    form.markdown("Please read the following article from Wall Stree Journal (WSJ) titled “TSMC to Boost Chip Production With Up to \$44 Billion Investment, " 
             " by Yang Jie, January 13, 2022 issue.")
    form.markdown("[Link to the Article](https://www.proquest.com/docview/2619154138/123B20B55928445DPQ/1?accountid=8361)")

    form.markdown("Question 1. From the article: “Taiwan Semiconductor Manufacturing Co., the world’s largest contract chip "
                    "maker, said it would increase its investment to boost production capacity by up to 47\% this year "
                    "from a year earlier as demand continues to surge amid a global chip crunch.” Firms make short-run "
                    "and long-run production decisions. Is TSMC’s decision to increase production capacity a short-run "
                    "or a long run-decision? Briefly explain your answer.")
    q01 = form.text_input("Answer Question 1 below", placeholder="one line answer", key=1)
    form.markdown("To answer the questions below use the grapher app linked here [Grapher app](https://xlitemprod.pearsoncmg.com/Grapher/Grapher.aspx?productid=ccng&appproductid=4&handler_urn=pearson%2Fccng_econ_xl%2Fslink%2Fx-pearson-ccng_econ_xl&learningproduct=VL) .")
    form.markdown("There is a video on how to draw on Bb if you haven't seen it. Once you draw your graph, please save the graph in your machine for future use. Use the simple segment to draw supply and demand curves and the two head arrows to indicate surplus or shortage when applicable")
    form.markdown("draw and label a graph that depicts a downward-sloping demand curve and an "
                    "upward-sloping supply curve in the market for semiconductor chips. Assume that the " 
                    "market price and quantity of semiconductor chips are equal to the equilibrium price and quantity. "
                    "The article states: 'As a pandemic-fueled surge in demand for various devices requiring semiconductors "
                    "has created widespread shortages, major chip makers have been on an investment spree to raise production capacity.' ")
    form.markdown("Question 2. Use your graph to depict how an increase in demand could result in a shortage of chips and upload the graph below:")

    #q02 = form.text_area("write one paragraph about the current situation of the economy", height=200, max_chars=200, placeholder="many line answer", key=2)
    # Handle multiple image uploads
    image_base64_list = []
    for i in range(1):  # Change '2' to the number of images you want the user to upload
        uploaded_file = form.file_uploader(f" Upload Graph {i + 2} graph below", type=["png", "jpg", "jpeg"], key=f"q{i + 2}")
        if uploaded_file is not None:
            # Read the image
            image = Image.open(uploaded_file)
            # Convert image to base64 string
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_base64_list.append(image_base64)

    form.markdown("Question 3. Use another graph to show how an increase in investment in production capacity could eliminate"
                    "the shortage you show in questions 2. Start with a graph that you have drawn in question 2 and upload the new one here")

    for i in range(1):
        uploaded_file = form.file_uploader(f" Upload Graph {i + 3} graph below", type=["png" , "jpg" , "jpeg"] ,
                                           key=f"q{i + 3}")
        if uploaded_file is not None:
            # Read the image
            image = Image.open(uploaded_file)
            # Convert image to base64 string
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_base64_list.append(image_base64)
    form.markdown("End of Questions. Congratulations!")
    form.markdown(" ")
    form.markdown(" ")
    submit = form.form_submit_button("Generate PDF")

    if submit:
        # Render the HTML template
        html = template.render(
            username=username,
            # course="Report Generation in Streamlit",  # You can update the course name here
            # date=date.today().strftime("%B %d, %Y"),
            # grade="97",  # You can update the grade here
            q01=q01,
            #q02=q02,
            image_base64_list=image_base64_list,

        )

        pdf = pdfkit.from_string(html, configuration=config) #generation of the pdf using local library, top config uncomment
    #pdf = pdfkit.from_string(html, False)  # use this one when deploying in streamlit
        st.balloons()

        st.success(
            "🎉 Your PDF file has been generated! you can  download it by clicking the below button to save it and submit it in gradescope assignment!")
        st.download_button(
            "⬇️ Download pdf",
            data=pdf,
            file_name="AssignX.pdf",
            mime="application/octet-stream",
        )


#This file uses the virt env at
#secret: Econ2013
# conda deactivate
# ..\..\..\..\..\..\Rh\Learn\_Python\myProjects\Streamlit_apps\venv4pdfgen\Scripts\activate.ps1
#C:\Users\aembaye\OneDrive - University of Arkansas\C2-embaye\Rh\Learn\_Python\myProjects\Streamlit_apps\venv4pdfgen\Scripts
# streamlit run ./main.py

