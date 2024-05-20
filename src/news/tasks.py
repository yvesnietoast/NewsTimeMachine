from celery import shared_task
from .models import newsBit
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama  # Make sure to properly handle API credentials and initialization
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

@shared_task
def request_summary(newsbit_id):
    newsbit = newsBit.objects.get(id=newsbit_id)
    
    llm = ChatOpenAI(api_key="") #INSERT API KEY
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class Summerizer."),
    ("user", "{input}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    print("testing")
    response=chain.invoke({"input": f"Can you give me a summary of this following transcript: {newsbit.transcript} This is the title:{newsbit.title}" })

    print("Response from OpenAI:", response)
    newsbit.summary=response

    newsbit.save()