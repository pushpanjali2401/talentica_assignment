import os
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

# class ReceiptInfo(BaseModel) :

def pdf_to_image_extractor(uploaded_file , temp_dir) : 
    import pdb; pdb.set_trace()
    reader = PdfReader(uploaded_file) # reading the file from streamlit
    all_pages = reader.pages
    pdf_name = reader.metadata['/Title'] 
    for i in range(len(all_pages)) :
        one_page = all_pages[i]
        for count , image_file in enumerate(one_page.images) :
            image_path = os.path.join(temp_dir.name , pdf_name + '_' + str(i) + '_' + image_file.name )
            with open(image_path , "wb") as f :
                f.write(image_file.data)
            return image_path

client = OpenAI()

prompt = """
You are a helpful AI assistant and your task is to extract below given information from receipts in JSON format.
Fields to extract according to given schema - 
{
    "invoice_number" : "string" ,
    "GST_number" : "string",
    "order_id" : "string" , 
    "order_date" : "string(dd-mm-yyyy)" ,
    "invoice_date" :"string(dd-mm-yyyy)",
    "billing_address" : {
        "name" : "string",
        "address" : "string"
    } ,
    "shipping_address" : {
        "name" : "string",
        "address" : "string"
    } ,
    "total_amount" : "float" ,
    "authorized_by" : "string" ,
    "product_name" : "string" ,
    "quantity" : "integer" ,
    "serial_number" : "string" ,
    "discount" : "string",
    "taxable_value" : "float",
    "IGST_percent" : "float",
    "IGST_amount" : "float" ,
    
}
Use only the values from the receipt image and format the output strictly according to the schema. Write "NA" for fields not available.
Do not include any extra explanation or commentary.
"""
def image_field_extractor(img_64_data) :
    response = client.responses.create(
        model = "gpt-4.1",
        input = [
            {
                "role" : "user",
                "content" : [
                    {"type" : "input_text" , "text" : prompt},
                    {"type" : "input_image" , "image_url" : f"data:image/jpeg;base64,{img_64_data}"}
                ]
            }
        ] ,
        # text_format = {"type" : "json"}
    )
    return response.output_text

def image_field_extractor_faster(img_64_data) :
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role" : "user" , 
                "content" : [
                    {"type" : "text" , "text" : prompt},
                    {"type" : "image_url" , "image_url" : {"url" : f"data:image/jpeg;base64,{img_64_data}"}}
                ]
            }
        ],
        response_format = {"type" : "json_object"}

    )
    return response.choices[0].message.content

def chat_llm(json_data , user_query) :
    response = client.responses.create(
        model = "gpt-4o-mini",
        # instructions = f"You are a helpful AI assistant. You task is to answer user query for  given bill details. Here is your bill details - {json_data}" ,
        instructions = f"""You are a helpful and friendly AI assistant. Your task is to assist the user by answering their queries based on the provided bill details. While staying informative and accurate, feel free to engage in light, polite chit-chat to make the conversation pleasant.

            Here are the bill details you’ll use to answer questions:
            {json_data}

            Be sure to keep your answers grounded in the bill data, but feel free to respond warmly—like a helpful customer support agent who's also approachable and easy to talk to.""",
        input = user_query
    )
    return response.output_text

def chat_llm_faster(json_data , user_query) :
    response = client.chat.completions.create(
        model = "gpt-4o-mini" ,
        messages = [
            {
                "role" : "developer" , "content" :f"""You are a helpful and friendly AI assistant. Your task is to assist the user by answering their queries based on the provided bill details. While staying informative and accurate, feel free to engage in light, polite chit-chat to make the conversation pleasant.

            Here are the bill details you’ll use to answer questions:
            {json_data}

            Be sure to keep your answers grounded in the bill data, but feel free to respond warmly—like a helpful customer support agent who's also approachable and easy to talk to.""",
            },
            {
                "role" : "user" , "content" : user_query

            }
        ]
    )
    return response.choices[0].message.content