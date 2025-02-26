# Iden

## Introduction

**Iden** is an advanced framework designed to simplify the development and deployment of LLM-based (Large Language Model) applications. Whether you’re working on Retrieval-Augmented Generation (RAG), building sophisticated chatbots, or generating AI-driven insights, Iden streamlines the process with an intuitive and efficient pipeline.

Iden empowers users to define models enriched with system prompts and vector-based document indexes, seamlessly supporting formats like .txt and .json. These indexes and models can be quickly configured, enabling the rapid creation of AI applications, significantly reducing development time.

With features like token tracking for AI responses and support for dynamic prompts similar to OpenAI's chat completion—Iden provides robust tools for building scalable AI solutions tailored to diverse use cases.

**Identt** SDK allows you to interact with Iden thorough an easy to use client interface to implement your AI applications.
## Installation

**Identt** SDK is available on [PyPI](https://pypi.org/project/identt/) and can be installed using pip. To install the latest version of Iden, run the following command:

```
pip install identt
```

Also you can add Iden to your .pipfile under [packages] when deploying:

```
identt = "*" 
```

or

```
identt = "<version>" 
```

## Prerequisites

Before using the **Identt** SDK, ensure you have the following ready:

---

### 1. Backend Base URL
You need the base URL of the backend system that the Identt client will interact with. This URL will be provided by the admin.

---

### 2. User Token
A user token is required for authentication when interacting with the Identt backend. To obtain this token:
- **Request Admin**:
  - Contact your admin or project manager to create a user or a project-specific account for you.
  - The admin will provide an associated token upon creating the user.

---

### 3. Initiating the Client
Once you have the **Base URL** and **Token**, you can initialize the Identt client as follows:

```python
from identt import client

# Replace BASE_URL and TOKEN with your actual backend URL and user token
client = client.Client(base_url=BASE_URL, token=TOKEN)
```

## Examples

The following examples demonstrate the basic workflow and showcases sample use cases to help you get started quickly.

### Example 1: Simple RAG based Chatbot Application

#### 1. Read Constants from .env file:

It is a best practice to store `BASE_URL` and `TOKEN` values in a `.env` file and read them dynamically in your code.

```python
import os

BASE_URL = os.getenv("IDEN_BASE_URL")
TOKEN = os.getenv("IDEN_USER_TOKEN")
```

#### 2. Initialize the Client:

```python
from identt import client

client = client.Client(base_url=BASE_URL, token=TOKEN)
```

#### 3. Create the Model:

First you need to define a `SYSTEM_PROMPT` to create the model.

```python
SYSTEM_PROMPT = "You are a helpful assistant."
```

Then you can define a unique `model_name` and create the model as below.
```python
model_name = "chatbot_model"
model = client.create_model(name=model_name, system_prompt=SYSTEM_PROMPT)
model_id = client.get_model_id_by_name(name=model_name)
```

#### 4. Index Files:

First create a dictionary of file objects to be indexed in this RAG based chatbot application, as below.

```python
file_objects = {}

file_objects["data-1.json"] = open("data/data-1.json", "rb")
file_objects["data-2.json"] = open("data/data-2.json", "rb")
file_objects["data-3.txt"] = open("data/data-3.txt", "rb")
```

***
***Note:*** *Iden only supports `.json`, `.txt` and `.rtf` currently. You need to convert `.pdf`,`.doc` or any other format to one of the supported fromats above.*
***

Then pass this dictionary of file objects to a new index with unique name defined as below.

```python
index_name = "chatbot_index"
index = client.index_files(file_objects=file_objects, name=index_name)
index_uuid = client.get_index_uuid_by_name(name=index_name)
```
#### 5. Perform Chat:

Finally perform the chat by passing `model_id` and `index_uuid` along with a query/question of your choice.

```python
 response = client.chat(
        model_id=model_id,
        index_uuid=index_uuid,
        query="Tell me everything you know about Danu Kumanan",
    )
```

Response:
```
{
  'response': "Danu Kumanan is the CTO and Co-founder of 1 Club. He demonstrated entrepreneurial skills early on by selling his first website at the age of 13. He holds a Master's degree in AI & Mathematics and has developed his expertise as a blockchain engineer at prominent companies such as Dapper Labs, Flow, and Coinbase. His career highlights his dedication to advanced technology and leadership within the blockchain sector.", 
  'tokens': 390
}
```

#### 6. Further Usage

The created indexes and models are persistently stored in `Iden` backend. So no need to recreate or reindex files when using again. You can get the created `model_id` and `index_uuid` by its unique name as below for further use.

```python
model_id = client.get_model_id_by_name(name="chatbot_model")
index_uuid = client.get_index_uuid_by_name(name="chatbot_index")
```

You can add more files and update your created index as below.

```python
new_file_objects = {"data-4.txt": open("data/data-4.txt", "rb")}

index_uuid = client.get_index_uuid_by_name(name="chatbot_index")
index = client.index_files(file_objects=new_file_objects, index_uuid=index_uuid)
```

### Example 2: AI Application with Dynamic Prompts

One of the limitations of above example is that the `SYSTEM_PROMT` of the created model cannot be changed once created. Further some AI applications operate solely based on user prompts and do not require file indexing, providing responses directly from the input prompt which are subjected to change. For such use cases we can simply use `basic chat` functionality which works quite similar to chat completion API of `OpenAI`.

```python
DYNAMIC_PROMPT = f'dynamically changing prompt here: {prompt}'
PROMPT = DYNAMIC_PROMPT.fomrat(prompt=user_prompt)

response = client.basic_chat(prompt=PROMPT, gpt_model="gpt-4o-mini")
```

***
***Note:*** *If `gpt_model` parameter is not specified `Iden` will by default use `gpt-4o` model. The `gpt_model` parameter should be one of the below:*
- gpt-3
- gpt-3.5-turbo
- gpt-4
- gpt-4-turbo
- gpt-4-mini
- gpt-4o
- gpt-40-mini
- gpt-4o-2024-08-06
- o1-preview
- o1-mini

***