import base64
from typing import Callable, Any
import ollama
from ollama import Client
from pydantic import BaseModel
from pylizlib.model.operation import Operation
from pylizlib.network.netres import NetResponse
from pylizlib.network.netutils import exec_get, exec_post
from loguru import logger
from pylizai.log.pylizAiLogging import format_log_result


# https://github.com/ollama/ollama-python
# https://github.com/ollama/ollama/blob/main/docs/api.md


class Ollamaliz:

    OLLAMA_PORT = "11434"
    OLLAMA_HTTP_LOCALHOST_URL = "http://localhost:" + OLLAMA_PORT


    def __init__(self, url: str, enable_download: bool = False):
        self.url = url
        self.enable_dw = enable_download
        self.client = ollama.client = Client(host=url)

    @staticmethod
    def __get_query_format_from_params(json_format: bool | None, class_model: Any | None):
        try:
            if json_format:
                return "json"
            elif class_model is not None:
                return class_model.model_json_schema()
            else:
                return ""
        except Exception as e:
            raise Exception(f"Error while getting query format: {e}")

    def check_ollama(self) -> NetResponse:
        return exec_get(self.url)

    def get_model_list_with_get(self) -> NetResponse:
        api_url = self.url + "/api/tags"
        return exec_get(api_url)

    def get_models_list(self) -> list[str]:
        mappings = self.client.list()
        models = []
        for item in mappings.models:
            models.append(item.model)
        return models

    def has_model(self, name: str):
        models = self.get_models_list()
        for model in models:
            if model == name:
                return True
        return False

    def download_model(self, name: str, en_stream: bool, callback: Callable[[str], None] | None = None):
        try:
            # Richiesta al server per scaricare il modello
            stream = self.client.pull(
                model=name,
                insecure=False,
                stream=en_stream,
            )

            # Gestione dello streaming dei progressi
            if en_stream:
                total_size = None
                downloaded = 0

                for data in stream:
                    status = data.get("status", "Aggiornamento non disponibile")
                    current_size = data.get("current_size")
                    total_size = data.get("total_size", total_size)

                    if current_size is not None and total_size:
                        downloaded = current_size
                        percentage = (downloaded / total_size) * 100
                        progress_message = f"Download progress: {percentage:.2f}%"
                    else:
                        progress_message = status

                    logger.trace("Ollama download: " + progress_message)
            else:
                # Se lo streaming è disabilitato, consuma i dati normalmente
                result = list(stream)  # Consuma tutto lo stream per completare l'operazione
            return Operation(status=True)

        except Exception as e:
            return Operation(status=False, error=str(e))


    def check_model(self, model_name: str):
        if self.has_model(model_name):
            logger.debug(f"Model {model_name} found in ollama server.")
            return
        else:
            if self.enable_dw:
                logger.debug(f"Model {model_name} not found in ollama server. Downloading...")
                status = self.download_model(model_name, True)
                logger.info(f"Model {model_name} downloaded.")
                if not status:
                    raise Exception(f"Error downloading model {model_name} from ollama server: {status.error}")
            else:
                raise Exception(f"Model {model_name} not found in ollama server. Please download the model first.")

    def send_post_query(self, prompt: str, model_name: str) -> NetResponse:
        api_url = self.url + "/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        return exec_post(api_url, payload, False)

    def send_post_llava_query(self, prompt: str, image_base_64: str, model_name: str) -> NetResponse:
        api_url = self.url + "/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "images": [image_base_64],
            "format": "json",
            "stream": False
        }
        return exec_post(api_url, payload, False)

    def send_query(
            self,
            prompt: str,
            model_name: str,
            json_format: bool = False,
            image_path: str | None = None,
            custom_format: BaseModel | None = None,
    ) -> str:
        # handle query format
        query_format = Ollamaliz.__get_query_format_from_params(json_format, custom_format)

        # logs
        logger.trace(f"About to run ollama query with format: {format_log_result(query_format)}...")
        logger.debug(f"Running ollama query with model {model_name}...")

        # Check images if needed
        image_base64 = None
        if image_path is not None:
            with open(image_path, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        # Run query
        response = self.client.generate(
            model=model_name,
            prompt=prompt,
            stream=False,
            format=query_format,
            images=[image_base64] if image_base64 is not None else None,
        )

        # Check response
        if response.done:
            logger.info(f"Ollama query succeeded!")
            logger.trace(f"Ollama statistics: TK/S={(response.eval_count / response.eval_duration) * (10**9)}. TK={response.eval_count}.")
            logger.trace(f"Ollama query response: {format_log_result(response.response)}")
            return response.response
        else:
            raise Exception(f"Error while running ollama query: {response.error}")










#
#
# def check_ollama():
#     url_set = read_config(CfgSection.AI.value, CfgList.OLLAMA_URL_SET.value, True)
#     if url_set is False:
#         print("Ollama url was not set. Please re-run the application with init command.")
#         raise typer.Exit()
#     print("Checking ollama server status...")
#     url = read_config(CfgSection.AI.value, CfgList.OLLAMA_URL.value)
#     response = check_ollama_status(url)
#     if response.is_successful():
#         print("Ollama server is running.")
#     else:
#         error = response.get_error()
#         rich.print("Ollama server is not running or some error occurred: " + "[red]" + error + "[/red]")
#         print("Please check the server and try again.")
#         raise typer.Exit()
#
#
# def download_models_list(ollama_url: str) -> list[OllamaModel]:
#     net_res = get_installed_models(ollama_url)
#     if net_res.is_successful():
#         data = json.loads(net_res.response.text)
#         models = [OllamaModel(**model) for model in data['models']]
#         return models
#     else:
#         error = net_res.get_error()
#         print("Error while fetching models: " + "[red]" + error + "[/red]")
#         raise typer.Exit()
#
#
# def is_model_installed(model_name: str, actual_list: list[OllamaModel]) -> bool:
#     for model in actual_list:
#         if model.name == model_name:
#             return True
#     return False
#
#
# def check_required_model(name: str):
#     pass
#
#
# def get_ai_power_model_list(ai_power: AiPower) -> list[str]:
#     if ai_power == AiPower.HIGH.value:
#         return ['llava:13b', 'llava:13b']
#     elif ai_power == AiPower.MEDIUM.value:
#         return ['llava:13b', 'llama3:latest']
#     else:
#         return ["llava:7b"]
#
#
# def download_required_models(ai_power: AiPower, actual_list: list[OllamaModel]):
#     required_models = get_ai_power_model_list(ai_power)
#     for model in required_models:
#         print("Checking if model " + model + " is installed in ollama...")
#         if not is_model_installed(model, actual_list):
#             print("Downloading model: ", model)
#             # download_model(model)
#         else:
#             rich.print("Model [bold blue]" + model + "[/bold blue] is already installed.")
#
#
# def download_model(ollama_url: str, model_name: str):
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "name": model_name,
#         "stream": True
#     }
#
#     response = requests.post(ollama_url, headers=headers, data=json.dumps(data), stream=True)
#
#     total = None
#     completed = 0
#
#     for line in response.iter_lines():
#         if line:
#             status = json.loads(line.decode('utf-8'))
#             if 'total' in status and 'completed' in status:
#                 total = status['total']
#                 completed = status['completed']
#                 percentage = (completed / total) * 100
#                 print(f"Downloading: {percentage:.2f}% complete")
#             elif status.get("status") == "success":
#                 print("Download complete!")
#                 break
#             else:
#                 print(f"Status: {status.get('status')}")
#
#
# def scan_image_with_llava(
#         file_path: str,
# ) -> AilizImage | None:
#
#     # Converting image to base64
#     with open(file_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#
#     # Reading prompt from resources
#     with open("./resources/llava_prompt3.txt", "r") as file:
#         prompt = file.read()
#
#     # Reading ollama/ai config
#     ollama_url = read_config(CfgSection.AI.value, CfgList.OLLAMA_URL.value)
#     power = ai_power = read_config(CfgSection.AI.value, CfgList.AI_POWER.value)
#     model_name = AiPower.get_llava_from_power(power)
#
#     # Getting response from ollama
#     response = send_llava_query(ollama_url, prompt, encoded_string, model_name)
#
#     if response.is_successful():
#         resp_text = response.text
#         resp_text_json = json.loads(resp_text)
#         resp_obj = OllamaResponse.from_json(resp_text_json)
#         print(resp_obj.response)
#         info_json = json.loads(resp_obj.response)
#         output_image = AilizImage(file_path)
#         output_image.set_ai_filename(info_json.get("filename"))
#         output_image.set_ai_description(info_json.get("description"))
#         output_image.set_ai_tags(info_json.get("tags"))
#         output_image.set_ai_text(info_json.get("text"))
#         output_image.set_ai_scanned(True)
#         return output_image
#     else:
#         error = response.get_error()
#         rich.print("Error while connecting to ollama: " + "[red]" + error + "[/red]")
#         return None


# def get_tags_from_llava_result(llava_result:str):
#     try:
#         # Getting response from ollama
#         response = send_llava_query(ollama_url, prompt, encoded_string, model_name)
#
#         # Checking ollama response and extracting data
#         if response.is_successful():
#             resp_text = response.text
#             resp_text_json = json.loads(resp_text)
#             resp_obj = OllamaResponse.from_json(resp_text_json)
#             return resp_obj.response
#         else:
#             error = response.get_error()
#             rich.print("Error while connecting to ollama: " + "[red]" + error + "[/red]")
#             return None
#     except Exception as e:
#         rich.print("Error while analyzing current image: " + "[red]" + e + "[/red]")
#         return None



