import logging

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    # def create_user(self, email, password, first_name="", last_name=""):
    #     register_endpoint = self.base_url + "/user/register/"
    #
    #     payload = {
    #         "email": email,
    #         "password": password,
    #         "verify_password": password,
    #         "first_name": first_name,
    #         "last_name": last_name,
    #     }
    #
    #     try:
    #         response = requests.post(register_endpoint, json=payload)
    #
    #         if response.status_code == 201:
    #             response_data = response.json()
    #             token = response_data.get("token")
    #             return token
    #         else:
    #             print(f"Error {response.status_code}: {response.text}")
    #     except requests.RequestException as e:
    #         print("An error occurred while retrieving token:", str(e))

    def get_user_token(self, username, password):
        login_endpoint = self.base_url + "/user/login/"

        payload = {
            "username": username,
            "password": password,
        }

        try:
            response = requests.post(login_endpoint, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                token = response_data.get("token", None)
                return token
            else:
                print(f"Error {response.status_code}: {response.text}")
        except requests.RequestException as e:
            print("An error occurred while retrieving token:", str(e))

    def create_model(self, name: str, system_prompt: str):
        logger.info(f"Creating model with name: {name}")
        response = requests.post(
            f"{self.base_url}/core/models/create/",
            json={"name": name, "system_prompt": system_prompt},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 201:
            logger.error(f"Failed to create model: {response.text}")
        else:
            logger.info("Model created successfully")
        return response.json()

    def get_model_id_by_name(self, name: str):
        logger.info(f"Retreiving model id with name: {name}")
        response = requests.post(
            f"{self.base_url}/core/models/get-model-id/",
            json={"model_name": name},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to retrieve model: {response.text}")
        else:
            logger.info("Model retrieve successfully")
        return response.json().get("model_id", None)

    def index_files(self, file_objects, index_uuid: str = "", name: str = ""):
        files_info = []
        for file_name, file_object in file_objects.items():
            files_info.append({"name": file_name, "type": file_name.split(".")[-1]})

        upload_urls = self._get_upload_urls(files_info)
        keys = []
        for upload_url in upload_urls:
            file_name = upload_url.get("name")
            if file_name in file_objects:
                s3_data = upload_url.get("url")
                keys.append(s3_data.get("fields").get("key"))
                logger.info(f"Uploading {file_name} to S3 at URL: {s3_data.get('url')}")
                upload_res = requests.post(
                    s3_data.get("url"),
                    data=s3_data.get("fields"),
                    files={"file": file_objects[file_name]},
                )
                if upload_res.status_code == 204:
                    logger.info(f"{file_name} successfully uploaded to S3")
                else:
                    logger.error(
                        f"Failed to upload {file_name} to S3: {upload_res.text}"
                    )
                    raise Exception(f"Failed to upload {file_name} to S3")

        res = self._index_data(keys, index_uuid, name=name)
        return res.get("uuid")

    def get_index_uuid_by_name(self, name: str):
        logger.info(f"Retrieving index uuid with name: {name}")
        response = requests.post(
            f"{self.base_url}/core/indexes/get-index-uuid/",
            json={"index_name": name},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to retrieve index: {response.text}")
        else:
            logger.info("Index retrieved successfully")
        return response.json().get("uuid", None)

    def _get_upload_urls(self, files):
        logger.info(f"Requesting upload URLs for files: {files}")
        req = {
            "files": files,
        }
        response = requests.post(
            f"{self.base_url}/core/data-files/get-upload-urls/",
            json=req,
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to get upload URLs: {response.text}")
        else:
            logger.info("Successfully retrieved upload URLs")
        return response.json()

    def _index_data(self, s3_keys, index_uuid: str = "", name: str = ""):
        logger.info(f"Indexing data for s3_keys: {s3_keys}")

        req = {"name": name, "s3_keys": s3_keys}

        if index_uuid:
            req["index_uuid"] = index_uuid
        response = requests.post(
            f"{self.base_url}/core/indexes/",
            json=req,
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to index data: {response.text}")
        else:
            logger.info("Data indexed successfully")
        return response.json()

    def chat(
        self,
        model_id: int,
        index_uuid: str,
        query: str,
    ):
        logger.info(
            f"Chatting with model_id: {model_id}, index: {index_uuid} and query: {query}"
        )
        response = requests.post(
            f"{self.base_url}/core/models/{model_id}/chat/",
            json={"query": query, "index_uuid": index_uuid},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to chat: {response.text}")
        return response.json()

    def basic_chat(self, prompt: str, gpt_model="gpt-4o"):
        logger.info(f"Initializing a basic chat")
        response = requests.post(
            f"{self.base_url}/core/chat/",
            json={"prompt": prompt},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to chat: {response.text}")
        return response.json()

    def retrieve(self,
        model_id: int,
        index_uuid: str,
        query: str,):

        logger.info(
            f"Retrieving with model_id: {model_id}, index: {index_uuid} and query: {query}"
        )
        response = requests.post(
            f"{self.base_url}/core/models/{model_id}/retrieve/",
            json={"query": query, "index_uuid": index_uuid},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to retrieve: {response.text}")
        else:
            logger.info("Retrieve successful")
        return response.json()