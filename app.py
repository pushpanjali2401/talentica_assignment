import base64
import streamlit as st
from pypdf import PdfReader
from io import StringIO , BytesIO
from modules import pdf_to_image_extractor , image_field_extractor , image_field_extractor_faster, chat_llm , chat_llm_faster
import tempfile
import os
import json

st.title("Talentic GenAI assistant")
# st.
uploaded_file = st.file_uploader("Upload a PDF" , type = ['pdf' , 'jpg' , 'jpeg' , 'png'])

if uploaded_file is not None :
    if uploaded_file.type == "application/pdf" :
        temp_dir = tempfile.TemporaryDirectory()
        img_path = pdf_to_image_extractor(uploaded_file , temp_dir) 
        with open(img_path , "rb") as image_file :
            img_data = base64.b64encode(image_file.read()).decode('utf-8') 
        if "json_data" not in st.session_state :
        
            # st.session_state.json_data = image_field_extractor(img_data)


            # st.session_state.json_data = image_field_extractor_faster(img_data) #openai here
            st.session_state.json_data = "----" # for trial
            
        try :
            json_data_formatted = json.loads(st.session_state.json_data) 
        except :
            json_data_formatted = st.session_state.json_data

        # st.write(json_data_formatted)

    else :
        img_data = base64.b64encode(uploaded_file.read()).decode('utf-8') 
        if "json_data" not in st.session_state :
            # st.session_state.json_data = image_field_extractor(img_data) 


            # st.session_state.json_data = image_field_extractor_faster(img_data)  #openai here
            st.session_state.json_data = "------" #for trial
        try :
            json_data_formatted = json.loads(st.session_state.json_data) 
        except :
            json_data_formatted = st.session_state.json_data
    with st.expander("Download bill details : ") :
        st.write(json_data_formatted)
        json_str = json.dumps(json_data_formatted , indent = 2)
        st.download_button(label = "download bill details" , data = json_str , file_name = f"{uploaded_file.name}.json" , icon=":material/download:")
    # query  = st.text_input("Ask bill related query")
    if "messages" not in st.session_state :
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query  = st.chat_input("Ask bill related query")
    if query :
        st.session_state.messages.append({"role" : "user" , "content" : query})
        with st.chat_message("user") :
            st.write(query)



        # resp = chat_llm_faster( st.session_state.json_data , query  ) # openai here
        resp = "test here" #for trial


        # c = st.container( border = True)
        # c.write(resp)

        with st.chat_message("ai") :
            st.write(resp)
        st.session_state.messages.append({"role" : "ai" , "content" : resp})

