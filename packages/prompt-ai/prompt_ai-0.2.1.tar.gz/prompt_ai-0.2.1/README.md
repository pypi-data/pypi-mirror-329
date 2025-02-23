# Prompt-AI Library

**Prompt-AI** is a powerful library designed to optimize AI-driven prompt handling and response generation using the Gemini API. By introducing structured database management and efficient embedding retrieval, Prompt-AI significantly enhances performance, reduces response times, and provides a seamless solution for integrating AI models into various applications.

## Key Features

- **Efficient Embedding Management**: Prompt-AI stores pre-generated embeddings in a structured database, significantly reducing computational overhead and improving response times.
- **Real-Time Updates**: Manage datasets and dataframes efficiently, ensuring that embeddings are generated once and reused across multiple sessions.
- **Performance and Scalability**: The streamlined approach enhances performance and scalability, making Prompt-AI ideal for chatbots, recommendation systems, and other AI-powered tools.
- **Versatile Integration**: Seamlessly integrates with Node.js endpoint servers, bridging different technologies and workflows.

## Installation

To install Prompt-AI, use pip:

```bash
pip install prompt-ai
```
To upgrade to latest version: 
```bash
pip install prompt-ai --upgrade
```
---
## After Installation follow these steps to use promp-ai
### 1. Generate an API Key
To begin, you’ll need to generate an API key. Follow the link below to generate your API key:

[Generate API Key](https://aistudio.google.com/app/apikey?_gl=1*1ohn5hn*_ga*MTc3OTQxNzg5OC4xNzIyNDE2MDUx*_ga_P1DBVKWT6V*MTcyMzM3NTkzOS4xMi4xLjE3MjMzNzYxODUuNTYuMC4xMzQ0NjE1MTM2)

#### Brief Summary of Gemini Model
The Gemini model is a powerful AI-driven model designed for generating contextually relevant responses to user prompts. Unlike traditional approaches where embeddings are generated on each run, Prompt-AI integrates a more efficient workflow by storing pre-generated embeddings in a NoSQL database. This allows for faster response times and reduces computational overhead, making it ideal for applications like chatbots, recommendation systems, and other AI-powered tools.

### 3. Setting up MongoDB (In later versions: SQL and Cloud database will be added)
1. **Create a Database in Mongo Atlas or MongoDB Compass (Which you feel good).**
2. **Create collection and Documents.**
3. **Set the document in this structure:**
```doctest
{
"id": 1,
"title": "Gork vs Chat-gpt",
"text": "In the rapidly evolving landscape of artificial inte...",
}
```
### 4. Using Prompt-AI to manage prompts and generate response

**Prompt-AI** provides two core functions to help you manage prompts and generate responses:

#### 1) `configure(mongo_uri: string, db_name: string, collection_name: string, columns: array, API_KEY: string, embeddings: bool)`
```doctest
configure(mongo_uri, db_name, collection_name, columns, API_KEY, embeddings)
```
This function configures the connection to your MongoDB Atlas and sets up the necessary parameters for generating embeddings.

- **mongo_uri**: `string`  
  This should contain your MongoDB Atlas connection string.
```doctest
mongo_uri = 'mongoDB connection string'
```

- **db_name**: `string`  
  The name of your MongoDB database.
```doctest
db_name = 'Database Name'
```

- **collection_name**: `string`  
  The name of the collection in your database where the data is stored.
```doctest
collection_name = 'collection name'
```

- **columns**: `array`  
  An array of strings, each representing a field name present in each document of the collection. The field which contains <b>ANSWER</b> data must be named with ```'text'```.
```doctest
columns = ['id', 'title', 'text']
```
- **API_KEY**: `string`  
  The API key generated in the first step.
```doctest
API_KEY = 'key generated in first step'
```

- **embeddings**: `bool`  
  A boolean flag indicating whether embeddings need to be created (`true`) or if they already exist (`false`).
```doctest
embeddings = True or False
```
This function call will return datasets in form of tabular dataframe.
```doctest
id          title                    text                   embeddings
1       "chat-gpt features"    "chat-gpt has..."        [4.0322, 2.3344, 1.09...]
2       "Gork vs Chat-gpt"     "Gork have plenty..."    [1.1702, 0.4184, 5.19...]
```
overall <b>configure</b> function will look like this... 
```pycon
uri = 'your connection string' 
db = 'database_name'
col = 'collection_name'
API_KEY = 'api_key generated in first step'
column = ['id', 'title', 'text']
embeddings = True
dataframe = configure(uri, db, col, API_KEY, column, embeddings)
```
#### 2) `generate(user_prompt, dataframe)`
```doctest
generate(user_prompt, dataframe)
```
This function processes the user’s prompt, interacts with the database, and returns the AI-generated response.
<b>dataframe</b> will be used here inside generate() function.
```doctest
@app.post("/api")
async def generate_response(request: PromptRequest):
    # Extract the prompt from the request body
    user_prompt = request.prompt

    # calling generate() function with prompt and dataframe as parameter

    response = generate(user_prompt, df)

    return {"response": response}
```
Now on making post request to this endpoint keep `prompt: string` inside body of the post request in `JSON` format.
And for handling response you can have it in this way: 
```doctest
const response = await axios.post('endpoint_url/api', {prompt});
res = response.data.response;
```
Here I have used `axios`, but you can also use `fetch` api to make post request and fetch the response in the same way.

---

With **Prompt-AI**, you can efficiently manage AI-driven prompt handling, leveraging the Gemini model's capabilities with enhanced performance and scalability. Whether you’re building a chatbot, a recommendation system, or any other AI-powered application, Prompt-AI provides a streamlined and powerful solution.

## Happy Coding :)

---