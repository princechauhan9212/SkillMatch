import streamlit as st
from Pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os 


# First Lets configure 

gemini_api_key = os.getenv('Google_API_Key2')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key=gemini_api_key,
    temperature = 0.9)

# Lets create the side bar to upload the resume 
st.sidebar.title('UPLOAD YOUR RESUME (Only PDF  )')
file =st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    file_text=text_extractor(file)
    st.sidebar.success('File uploaded Sucessfully')

# Create the mian od the application 

st.title(':orange[SKILLMATCH:-] :blue[AI Assisted Skill Match]')
st.markdown('#### This application will match and analyzeyour resume and the the jo description providede')
tips='''
1. Upload your resume(PDF only) in side bar.
2. copy and paste the job description below.
3. click on submit the run the appliction.'''
st.write(tips)

job_desc=st.text_area(':red[copy and paste your job description over here:] ',max_chars= 50000)
if st.button('SUBMIT'):
    with st.spinner('Processing....'):
        prompt =f'''
        <Role> You are an expeert in analyzing resume and matching in 
        <Goal> Match the resume and the job description provided below
        <context> The following cintent has been provided by the applicant and create 
        *Resume :{file_text}
        *job Description:{job_desc}
        <format> report should follow this steps:
        * Give a brief Description of the applicant  in 3 to 5 lines.
        * Describe in percentage what are the chances of this resume getting selected.
        * Need to be the exact percentage, you can give interval of percentage. 
        * Give the expected ATS score along with matching and non matching keywords.
        * Perform a SWOT analysis and explian each parameter ie strength , weakness, opportunity and threat
        * Give what all sections in the current resume thath are required to be changed in order to Improve the ATS score and selection percentage 
        * Show both current version and impproved version of the section in resume .
        * create two sample resume whcih can maximize the ATS score. 


        <Instruction>
        * Use bullet points for explanation where ver possible.
        *create tables for description where ever required.
        *stricl do not add any new skill in sample resume.
        *The fromat of sample resumes should be in such a way that they can be coppied and pasted in word file.
        '''


        response = model.invoke(prompt)
        st.write(response.content)
