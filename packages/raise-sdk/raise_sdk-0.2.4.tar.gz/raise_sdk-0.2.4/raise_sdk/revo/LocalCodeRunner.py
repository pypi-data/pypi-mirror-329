# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:28:20 2024

@author: anappa
"""

# Stdlib imports
import os
import sys
import time
import shutil
import logging
import datetime
import subprocess
from pathlib import Path

# Third-party app imports
import docker
import docker.errors

# Imports from your apps
from .app.CodeRunner import CodeRunner, connect_with_docker
from templates import PYTHON_3_8_DOCKERFILE_TEMPLATE
from raise_sdk.utils.file_utils import find_local_paths, clean_folder


#%%
# ================================= PARAMETERS ================================
TIMEOUT_CONTAINER = os.environ.get("TIMEOUT_CONTAINER", 300)
COMPATIBLE_PROGRAMMING_LANGUAGES = ["Python 3.8"]
DOCKERFILE_TEMPLATES             = {"Python 3.8": PYTHON_3_8_DOCKERFILE_TEMPLATE}
# =============================================================================

#%%
# ================================== CLASSES ==================================
class LocalCodeRunner(CodeRunner):
    def __init__(
                  self,
                  script       : str,
                  requirements : str,
                  dataset      : str,
                 ):
        
        self.script_path       = script
        self.requirements_path = requirements
        self.dataset_path      = dataset
        self.data_format   = None
        self.experiment_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.status_code   = 0
        
        self.root_path       = os.getcwd()
        self.experiment_path = os.path.join(self.root_path,".myexperiments",self.experiment_id)
        self.logs_path       = os.path.join(self.experiment_path,"logs")
        self.results_path    = os.path.join(self.experiment_path,"results")
        os.makedirs(self.experiment_path, exist_ok=True)
        os.makedirs(self.logs_path, exist_ok=True)
        os.makedirs(self.results_path, exist_ok=True)
        
        self.logfile         = os.path.join(self.logs_path,"rai-psm.log")
        self.logger          = self.create_logger()
        self.logger.info("- Experiment path: " + self.experiment_path)
        self.logger.info("- Root path: " + self.root_path)
        self.logger.info("- Experiment id: " + self.experiment_id)
        
        self.docker_client   = connect_with_docker(self.logger)
    
    def create_logger(self):
        # Create a logger object
        logger = logging.getLogger(__name__)
        # Remove all handlers associated with the logger (if any)
        if logger.hasHandlers():
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        # Basic configuration
        logging.basicConfig(
                             level    = logging.DEBUG,  # Set the logging level
                             format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format for log messages
                             datefmt  = '%Y-%m-%d %H:%M:%S',  # Format for timestamps
                             handlers = [
                                          logging.FileHandler(self.logfile),  # Log to a file
                                          logging.StreamHandler()  # Log to the console
                                         ]
                            )
        return logger
    
    def prepare_experiment_path(self):
        dst = self.experiment_path
        # main.py and any other scripts (or folders)
        try:
            local_paths = find_local_paths(self.script_path)
        except ValueError as exc:
            self.logger.exception(f"Exception occurred while preparing the experiment path: {str(exc)}")
            self.status_code = 2
        for src in self.script_path:
            src_path = Path(src)
            dst_path = os.path.join(dst, local_paths.get(src_path, src_path.name))
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)  # Ensure parent directory exists
                shutil.copy(src_path, dst_path)
        # requirements.txt
        for src in self.requirements_path:
            shutil.copy(src, os.path.join(dst, os.path.basename(src)))
        # dataset file(s)
        for src in self.dataset_path:
            src_path = Path(src)
            dst_path = os.path.join(dst, src_path.name)
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)
        # "Dockerfile"
        if self.docker_client is not None:
            dockerfile_path = os.path.join(self.experiment_path,'Dockerfile')
            with open(dockerfile_path, 'w') as f:
                f.write(PYTHON_3_8_DOCKERFILE_TEMPLATE)
        self.logger.info(" Experiment path prepared for running the code.")
        return
    
    def build_docker_image(self):
        try:
            super().build_docker_image()
        except docker.errors.BuildError:
            self.logger.exception(f"Cannot build image img_raise_{self.experiment_id}")
        else:
            self.logger.info(
                    f" Docker image generated for experiment_id = {self.experiment_id}."
                    )
        return
    
    # run_docker_container()  --> environment_variables() has to be adapted,
    #                             volumes paths have to be adapted
    def run_docker_container(self):
        self.logger.info(" Running the container for the experiment...")
        try:
            self.docker_client.containers.run(
                image=f"img_raise_{self.experiment_id}",
                environment=self.environment_variables(),
                auto_remove=True,
                remove=True,
                name=f"container_raise_{self.experiment_id}",
                detach=True,
                volumes=[f"{self.logs_path}:/tmp/logs",
                         f"{self.results_path}:/tmp/results"],
            ).wait(timeout=TIMEOUT_CONTAINER)
            self.status_code = 0
            self.logger.info(" Execution ended successfully.")
        except Exception as exc:
            self.logger.exception(f"Exception occurred while running the docker container: {str(exc)}")
            self.status_code = 2
        return
    
    def run_python(self):
        self.logger.info(" Running the experiment without docker...")
        try:
            os.chdir(self.experiment_path)
            # Install dependencies from requirements
            self.logger.info("Installing requirements...")
            for file in self.requirements_path:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file])
            # Execute the main.py script
            self.logger.info("Executing main.py...")
            subprocess.check_call([sys.executable, 'main.py'])
            self.status_code = 0
            self.logger.info(" Execution ended successfully.")
        except Exception as exc:
            self.logger.exception(f"Exception occurred while running the experiment: {str(exc)}")
            self.status_code = 2
        finally:
            os.chdir(self.root_path)
        return

    # save_logfile()          --> not necessary
    ...
    
    # check_results()         --> override and adapt it
    def check_results(self):
        try:
            if len(os.listdir(self.results_path)) == 0:
                self.logger.info(" Results folder is empty.")
                self.status_code = 1
            else:
                self.status_code = 0
                for file in os.listdir(self.results_path):
                    if os.path.getsize(os.path.join(self.results_path,file)) == 0:
                        self.logger.info(f" File {file} is empty.")
                        self.status_code = 1
        except Exception as exc:
            self.logger.exception(f"Exception occurred while checking the results: {str(exc)}")
            self.status_code = 2
        return
    
    # remove_image()          --> override and adapt it
    def remove_image(self):
        self.logger.info(" Removing docker image after execution...")
        time.sleep(5)
        try:
            image = f"img_raise_{self.experiment_id}"
            self.docker_client.images.remove(image)
            self.logger.info(f"Image removed for experiment_id = {self.experiment_id}")
            return True
        except Exception as exc:
            self.logger.exception(f"Exception occurred while removing the docker image: {str(exc)}")
            return False
        
    def clean_experiment_path(self):
        clean_folder(self.experiment_path, items_to_keep=["logs", "results"])
        return
    
    # environment_variables() --> override and adapt it
    def environment_variables(self):
        return {
            "EXPERIMENT_ID"    : self.experiment_id,
        }
# =============================================================================

#%%
# ================================= FUNCTIONS =================================

# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================