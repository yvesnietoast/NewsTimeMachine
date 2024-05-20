from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader


llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Load, chunk and index the contents of text
loader = TextLoader("./transcripts.txt")
loader.load()
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
rag_chain.invoke("{input}")