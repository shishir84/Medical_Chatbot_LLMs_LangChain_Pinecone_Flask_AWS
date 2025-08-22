from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()   

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")  

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_embeddings()

index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,   
    index_name=index_name
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chatModel = ChatOpenAI(model_name="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "Answer the following question: {input}") 
])

question_answering_chain = create_stuff_documents_chain(
    llm=chatModel,  
    prompt=prompt
    )
rag_chain = create_retrieval_chain(
    retriever,
    question_answering_chain
    )


@app.route('/') 
def index():
    return render_template('chat.html')

@app.route('/get', methods=['POST', 'GET'])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)
    response = rag_chain.invoke({"input": input})
    print(response["answer"])
    return str(response["answer"])

  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




