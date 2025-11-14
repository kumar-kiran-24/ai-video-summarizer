from src.utils.exception import CustomException
from src.utils.logger import logging

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter=RecursiveCharacterTextSplitter(chunk_size=50,chunk_overlap=11
                                             )

class DataVectorize:
    def __init__(self):
        pass

    def datavectrizer(self,text_path):
        text_loader=TextLoader(text_path)
        text_documnet=text_loader.load()
        docs=text_splitter.split_documents(text_documnet)
        DB=FAISS.from_documents(docs,embedding=embeddings)
        path=r"C:\mini_project\data"
        DB.save_local(path)
        return path
    

if __name__=="__main__":
    obj=DataVectorize()
    result=obj.datavectrizer(text_path=r"C:\mini_project\data\transcript.txt")
    print(result)

