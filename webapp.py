import pdfkit
#path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' #comment this line when deploying in streamlit
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) #comment this line when deploying in streamlit
import os
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(layout="centered" , page_icon="" , page_title=" HW00")
st.title("Econ 2013 HW00-- How to submit pdf file with grapher drawing and streamlit pdf generation")
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
    st.write("Here goes your normal Streamlit app...")
#    st.button("Click me")
# Load HTML template
    env = Environment(loader=FileSystemLoader(".") , autoescape=select_autoescape())

    # here the template is directly in the main .py file which is not ideal
    template = env.get_template("template2.html")
    st.write("Answer the following questions based on the assignment post on Blackboard:")
    form = st.form("template_form")

    student_name = form.text_input("Full NAME" , placeholder="John Doe")
    # q01 = form.text_area(label="questions 1 answered here:", height=200, max_chars=500, placeholder="No place like Economics!")
    q01 = form.text_input("What is your major/minor" , placeholder="one line answer", key=1)
    q02 = form.text_area("write one paragraph about the current situation of the economy" , height=200, max_chars=200, placeholder="many line answer", key=2)
    # Handle multiple image uploads
    image_base64_list = []
    for i in range(1):  # Change '2' to the number of images you want the user to upload
        uploaded_file = form.file_uploader(f"Q{i + 1}.1 Upload Graph {i + 1}" , type=["png" , "jpg" , "jpeg"] ,
                                           key=f"q{i + 1}")
        if uploaded_file is not None:
            # Read the image
            image = Image.open(uploaded_file)
            # Convert image to base64 string
            buffered = BytesIO()
            image.save(buffered , format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_base64_list.append(image_base64)

    submit = form.form_submit_button("Generate PDF")

    if submit:
        # Render the HTML template
        html = template.render(
            student_name=student_name ,
            # course="Report Generation in Streamlit",  # You can update the course name here
            # date=date.today().strftime("%B %d, %Y"),
            # grade="97",  # You can update the grade here
            q01=q01 ,
            q02=q02 ,
            image_base64_list=image_base64_list ,

        )

        #pdf = pdfkit.from_string(html, configuration=config) #generation of the pdf using local library, top config uncomment
        pdf = pdfkit.from_string(html , False)  # use this one when deploying in streamlit
        st.balloons()

        st.success(
            "🎉 Your PDF file has been generated! you can  download it by clicking the below button to save it and submit it in gradescope assignment!")
        st.download_button(
            "⬇️ Download pdf" ,
            data=pdf ,
            file_name="AssignX.pdf" ,
            mime="application/octet-stream" ,
        )


#This file uses the virt env at
#secret: streamlit123
# conda deactivate
# ../venv4pdfgen/Scripts/activate.ps1
# streamlit run ./webapp.py

