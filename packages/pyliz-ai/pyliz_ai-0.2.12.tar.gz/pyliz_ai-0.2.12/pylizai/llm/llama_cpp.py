import os
import subprocess
from git import Repo
from pylizlib.config.pylizdir import PylizDir, PylizDirFoldersTemplate
from pylizlib.data import datautils
from pylizlib.model.operation import Operation
from pylizlib.os import pathutils, osutils, fileutils

from pylizai.core.ai_setting import AiQuery, AiSetting

from pylizai.core.ai_source import AiSource
from loguru import logger
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_model_list import AiModelList


class LlamaCppController:

    def __init__(self, pyliz_dir: PylizDir):
        self.pyliz_dir = pyliz_dir

    @staticmethod
    def __run_with_lib(query: AiQuery):
        # llm = Llama(
        #     model_path=query.setting.get_model_local_path(),
        #     n_gpu_layers=1,
        #     max_tokens=9072,
        #     temperature=0.7,
        #     n_ctx=1024,
        # )
        # response = llm(prompt=query.prompt, max_tokens=4096)
        # print(response)
        # result = response['choices'][0]
        # result_text = result['text']
        # return Operation(status=True, payload=result_text)
        pass

    def run(self, query: AiQuery):
        try:
            dw_type = query.setting.download_type
            if dw_type == AiDownloadType.HG_FILES or dw_type == AiDownloadType.DEFAULT:
                return LlamaCppController.__run_with_lib(query)
            elif dw_type == AiDownloadType.WEB_FILES:
                return LlamaCppController.LlamaCppGit(
                    path_install=os.path.join(self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.AI), "llama.cpp"),
                    path_models=self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.MODELS),
                    path_logs=os.path.join(self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.LOGS), "llama.cpp"),
                ).run(query)
            else:
                raise ValueError(f"Download type not supported in LlamaCpp: {dw_type}")
        except Exception as e:
            return Operation(status=False, error=str(e))


    # noinspection PyMethodMayBeStatic
    class LlamaCppGit:

        GITHUB_URL = "https://github.com/ggerganov/llama.cpp.git"

        def __init__(
                self,
                path_install: str,
                path_models: str,
                path_logs: str
        ):
            # Init paths
            self.path_install = path_install
            self.path_models = path_models
            self.path_logs = path_logs
            self.log_build_folder = os.path.join(self.path_logs, "build")
            pathutils.check_path(self.log_build_folder, True)


        def __clone_repo(self):
            logger.debug("Cloning LlamaCpp...")
            # check if the folder already exists
            if os.path.exists(self.path_install):
                logger.debug("LlamaCpp already installed.")
                return
            else:
                logger.debug(f"LlamaCpp not installed. Proceeding installing in {self.path_install}...")
                pathutils.check_path(self.path_install, True)
            # checking folder
            pathutils.check_path_dir(self.path_install)
            # Cloning github repo
            Repo.clone_from(LlamaCppController.LlamaCppGit.GITHUB_URL, self.path_install)
            logger.debug("Clone successful.")


        def __check_requirements(self):
            logger.debug("Checking requirements...")
            make_ok = osutils.is_command_available("cmake")
            is_os_unix = osutils.is_os_unix()
            if not make_ok:
                raise Exception("Make command not available. Please install make.")
            if not is_os_unix:
                raise Exception("This component (LlamaCPP) is only available on Unix systems.")


        def __build_sources(self):
            bin_folder = os.path.join(self.path_install, "build", "bin")
            if os.path.exists(bin_folder):
                logger.debug("LLamaCPP already built.")
                return
            logger.debug("Building sources...")
            risultato = subprocess.run(["cmake", "-B", "build", "-DBUILD_SHARED_LIBS=OFF"], check=True, cwd=self.path_install, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            risultato_2 = subprocess.run(["cmake", "--build",  "build",  "--config", "Release"], check=True, cwd=self.path_install, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logger.debug("LLamaCPP build successful.")
            self.__crete_build_log(risultato, risultato_2)


        def __crete_build_log(self, risultato, risultato2):
            log_build_name = datautils.gen_timestamp_log_name("llamacpp-", ".txt")
            log_build_path = os.path.join(self.log_build_folder, log_build_name)
            with open(log_build_path, "w") as f:
                f.write("[BUILD 1]**************************\n")
                f.write(risultato.stdout)
                f.write("--------------------\n")
                f.write(risultato.stderr)
                f.write("[BUILD 2]**************************\n")
                f.write(risultato2.stdout)
                f.write("--------------------\n")
                f.write(risultato2.stderr)

        def run_llava(
                self,
                setting: AiSetting,
                image_path: str,
                prompt: str,
        ) -> str:
            try:
                # Creating variables and checking requirements
                source = setting.source
                folder = os.path.join(self.path_models, source.model_name)
                if not os.path.exists(folder):
                    raise Exception("LLava model not installed.")
                # Run the model
                path_model_file = os.path.join(self.path_models, source.model_name, source.get_ggml_file().file_name)
                path_mmproj_file = os.path.join(self.path_models, source.model_name, source.get_mmproj_file().file_name)
                path_exe = os.path.join(self.path_install, "build", "bin")
                command = ["./llama-llava-cli", "-m", path_model_file, "--mmproj", path_mmproj_file, "--image", image_path, "-p", prompt ]
                # saving and extracting the result
                log_file = os.path.join(self.path_logs, datautils.gen_timestamp_log_name("llava-result", ".txt"))
                with open(log_file, 'w') as file:
                    result = subprocess.run(command, cwd=path_exe, stdout=file, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise Exception("Error running LLava: " + result.stderr.decode())
                with open(log_file, 'r') as file:
                    return file.read()
            except Exception as e:
                raise Exception("Error running LLava from llamaCPP (local git): " + str(e))


        def __run_model(self, query):
            if query.setting.model == AiModelList.LLAVA:
                return self.run_llava(query.setting, query.payload_path, query.prompt)
            else:
                raise ValueError(f"Model not supported in this type of LLamaCPP: {query.setting.model}")


        def run(self, query: AiQuery):
            self.__clone_repo()
            self.__check_requirements()
            self.__build_sources()
            return self.__run_model(query)


