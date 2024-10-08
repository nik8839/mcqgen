import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

load_dotenv()

KEY=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=KEY,model_name="gpt-3.5-turbo",temperature=0.5)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker . Given the above data,it is ypur job to\
    to creaate  aquiz of {number} mutliple choice questions for {subject}\
        in {tone} tone.\
Make sure the question are not repeated and check all the questions\
    to be conforming the text . Make sure to format your responses\
like respons like json below and use it as a guide.\
    Ensure to make {number} MCQs.
### RESPONSE_JSON
{response_json}                        


"""


quiz_geneartion_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)


quiz_chain=LLMChain(llm=llm,prompt=quiz_geneartion_prompt,output_key="quiz",verbose=True)




TEMPLATE2="""
You are an expert english grammer and writer . Given a Multiple choice\
    quiz for {subject}
    students. You need to evaluate the complexity of thr question and give a complete analysis of the quiz .\
        If the quiz is not at par with cognnitive and analytical abilities \
update the quiz question that needs to be changed and change the tone so that it perfectlt matches\
with student abilities 
QUIZ_MCQ:
{quiz}            

Check from an expert English writer of the above quiz

"""


quiz_evaluation_prompt=PromptTemplate(
    input_variables=[
    "subject","quiz"],
    template=TEMPLATE2)


review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True)


generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain,review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=[
        "quiz","review"
    ], verbose=True
)



