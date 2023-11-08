from io import BytesIO
import base64
from PIL import Image
import streamlit as st
from datetime import date
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os
import pdfkit
# comment this line when deploying in streamlit
# path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# comment this line when deploying in streamlit
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

st.set_page_config(layout="centered", page_icon="", page_title="Exam 2")
st.title("Exam 2 test corrections ")


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
    # st.button("Click me")
    # Load HTML template
    env = Environment(loader=FileSystemLoader(
        "."), autoescape=select_autoescape())

    template = env.get_template("template_test_corrections.html")
    st.write("Please check the version of the exam 2 you had and then for each question you missed, state the correct answer followed by explanation of why that is the answer. As an example, check the explanations the instructor gave for each questions of the the sample exam.")
    st.write(" ")
    st.write("The purpose of the this assignments is to understand what you missed by any means necessary; so you can ask help from me, the tutoring service or your classmates but submit your own work with your own words. You can get a maximum of .4*(100- your current Exam grade) as a bonus. For example, if you have 60% now, you can get .4*40=16 additional points")
    st.write("No extra point will be given for doing extra question other than what you missed")

    form = st.form("template_form")

    username = form.text_input(
        label="Full NAME: Last, first", placeholder="Doe, John")
    ver = form.text_input(label="Exam version you had",
                          placeholder="Version A, B, or C", key="ver")
    form.markdown(" ")

    q_list = []
    for i in range(42):
        quest = form.text_area(
            label=f"question #{i + 1}",  placeholder="I got it correct", height=100, max_chars=500, key=f"q{i + 1}")
        q_list.append(quest)

    # st.text_area(label, value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible")
    form.markdown(
        "End of Questions. Congratulations! Now generate a pdf of this page by clicking the below button below and then follow the lead.")
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
            # q01=q01,
            ver=ver,
            q_list=q_list,

        )

        # generation of the pdf using local library, top config uncomment
        #pdf = pdfkit.from_string(html, configuration=config)
        # use this one when deploying in streamlit
        pdf = pdfkit.from_string(html, False)
        st.balloons()

        st.success(
            "🎉 Your PDF file has been generated! please click the below to download it to your machine and then submit it in gradescope assignment under the same name!")
        st.download_button(
            "⬇️ Download pdf",
            data=pdf,
            file_name="Test_corrections_Assgn.pdf",
            mime="application/octet-stream",
        )

# location of this file: cd "C:\Users\aembaye\OneDrive - University of Arkansas\C2-embaye\Teaching\00_AllCourses\Ec_2013\Assessments\NewAnalysis_HW\Exam2_Corrections"
# streamlit run local_app2.py
