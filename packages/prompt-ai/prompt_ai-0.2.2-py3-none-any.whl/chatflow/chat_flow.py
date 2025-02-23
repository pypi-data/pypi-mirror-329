import textwrap
import numpy as np
import pandas as pd
from pymongo import MongoClient
import google.generativeai as genai


def configure(mongo_uri, database, collec, gen_API, column ):
    uri = mongo_uri
    client = MongoClient(uri)
    db = client[database]
    collection = db[collec]
    doc = collection.find()
    data = list()

    # Fetching each document from a collection and appending it into a variable 'data' of list data_type
    for document in doc:
        data.append(document)

    # Created dataframes of by fetching datasets from mongoDb
    df = pd.DataFrame(data)
    df.columns = column

    # API key for using gemini api model
    # API_KEY = gen_API
    genai.configure(api_key=gen_API)

    return df


# Fetching stored datasets from MongoDB database
# uri = 'mongodb+srv://robertjr:pg123456@cluster0.ljveogm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
# client = MongoClient(uri)
# db = client['knowledge_base.csv']
# collection = db['articles']
# doc = collection.find()
# data = list()
#
# # Fetching each document from a collection and appending it into a variable 'data' of list data_type
# for document in doc:
#     data.append(document)
#
# # Created dataframes of by fetching datasets from mongoDb
# df = pd.DataFrame(data)
# df.columns = ['id', 'title', 'text', 'Embeddings']
#
# #API key for using gemini api model
# API_KEY = 'AIzaSyAIQv1OLwiQTn623OduzpZNkMJkv3rCdQ4'
# genai.configure(api_key=API_KEY)

# query = "What is multivibrator please explain in simple language?"


def find_best_passage(query, dataframe):
  """
  Compute the distances between the query and each document in the dataframe
  using the dot product.
  """
  model = 'models/embedding-001'
  query_embedding = genai.embed_content(model=model,
                                        content=query,
                                        task_type="retrieval_query")
  dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding["embedding"])
  idx = np.argmax(dot_products)
  return dataframe.iloc[idx]['text'] # Return text from index with max value


def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a technical audience, so there is no need to break down complicated concepts but when asked to break down complicated concepts then only break it and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, just write not applicable to answer this question.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)

  return prompt

def generate(query, df):
    # df = init()
    passage = find_best_passage(query, df)
    prompt = make_prompt(query, passage)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    answer = model.generate_content(prompt)
    response = answer.text
    print(response)
    # add_convo_rec(query, response)
    return response