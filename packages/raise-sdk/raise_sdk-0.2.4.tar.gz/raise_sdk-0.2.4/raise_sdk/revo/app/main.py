# -*- coding: utf-8 -*-
"""
    RAISE - RAI Synthetic Data Generator

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os
import time

# Third-party app imports
from celery import Celery
from celery.utils.log import get_task_logger
import requests
import docker

# import docker

# Imports from your apps
from code_runner_files.Config import CeleryConfigProcessingScripts
from CodeRunner import CodeRunner

# from code_runner_files.LogClass import LogClass
from code_runner_files.custom_exceptions import MinioConnectionError, DockerConnectionError

celery_app = Celery()
celery_app.config_from_object(CeleryConfigProcessingScripts)

logger = get_task_logger(__name__)

TIME_OUT_ERROR = 2
SYNTAX_ERROR = 1


@celery_app.task(name=os.environ.get("PROCESSING_SCRIPTS_TOPIC", "processing-scripts"), max_retries=2)
def processing_script_execution(experiment_id,dataset_id):

    logger.info("⌛ Processing script execution task received with experiment_id = " + experiment_id)

    try:
        # Create the CodeRunner class
        code_runner = CodeRunner(experiment_id=experiment_id, logger=logger)
        logger.info("- Experiment path: " + code_runner.experiment_path)
        logger.info("- Root path: " + code_runner.root_path)
        logger.info("- Experiment id: " + code_runner.experiment_id)

        # Prepare the experiment path that contains the files needed for running the code
        code_runner.prepare_experiment_path()
        logger.info("🥳 Experiment path prepared for running the code.")
        
        try:
            code_runner.prepare_data_from_minio(dataset_id=dataset_id)
            logger.info("🥳 Data retrieved from minio correctly")
        except MinioConnectionError:
            logger.exception("There has been an error retrieving the data from minio")

        try:
            # Build docker image for experiment
            logger.info("⌛ Building docker image for experiment")
            code_runner.build_docker_image()
            logger.info(
                f"🥳 Docker image generated for experiment_id = {experiment_id}. ⌛ Running the code for the"
                " experiment..."
            )
        except docker.errors.BuildError as exception:
            logger.error(f"Cannot build image img_raise_{experiment_id}. BuildError: {exception}")
            # Notify the RCN that the experiment execution has not been done
            url = os.environ.get("RCN_EXPERIMENT_REGISTRATION_ENDPOINT")
            params = {"experiment_id": experiment_id, "status_code": TIME_OUT_ERROR}
            try:
                rcn_response = requests.post(url, params=params)
                logger.info(
                    f"""RCN API experiment registration request:{params},
                        status_code {rcn_response.status_code},
                        response_request: {rcn_response.text}"""
                )
                return False
            except Exception:
                logger.exception("Cannot connect to RCN API")
            for line in exception.build_log:
                if 'error' in line:
                    logger.error("Build log error:", line['error'])
                elif 'stream' in line:
                    logger.info(line['stream'].strip())
            return False

        # Execute the processing script
        start_time = time.time()
        logger.info("⌛ Running docker container for experiment")
        code_runner.run_docker_container()
        if code_runner.status_code == TIME_OUT_ERROR:
            logger.exception("Timeout error")
        else:
            logger.info(
                f"🥳 Code successfully runned for experiment_id = {experiment_id}. ⌛ Checking the results of the"
                " experiment..."
            )
        logger.info(f"Elapsed time: {time.time()-start_time}")

        # upload data to minio
        try:
            code_runner.upload_results_to_minio_and_execution_logs()
        except Exception:
            logger.exception("Could not upload data to minio")
            #TODO: make a real exception

        # Save the obtained results and logs
        logger.info("⌛ Checking results existence for experiment")
        code_runner.check_results()
        if code_runner.status_code == TIME_OUT_ERROR:
            logger.exception("⏲️ Timeout error")
        # elif code_runner.status_code == SYNTAX_ERROR:
        #     logger.exception(f"There are no results for experiment_id = {experiment_id}. ⌛ Saving log file...")
        #     code_runner.save_logfile()
        # else:
        #     logger.info(f"🥳 Results correctly stored for experiment_id = {experiment_id}. ⌛ Saving log file...")
        #     code_runner.save_logfile()
        try:
            # Notify the RCN that the experiment execution has been finished
            url = os.environ.get("RCN_EXPERIMENT_REGISTRATION_ENDPOINT")
            params = {"experiment_id": experiment_id, "status_code": code_runner.status_code}
            rcn_response = requests.post(url, params=params)
            logger.info(
                f"""RCN API experiment registration request:{params},
                        status_code {rcn_response.status_code},
                        response_request: {rcn_response.text}"""
            )
        except Exception:
            logger.exception("Cannot connect to RCN API")

        # Remove docker image
        logger.info("Removing docker image after execution...")
        removed = code_runner.remove_image()
        if removed:
            logger.info(f"Image removed for experiment_id = {experiment_id}")
        else:
            logger.exception("Exception occured when trying to remove the docker image")

    except MinioConnectionError:
        logger.exception("There has been an error while preparing the experiment path for running the code.")
        # Notify the RCN that the experiment execution has not been done
        url = os.environ.get("RCN_EXPERIMENT_REGISTRATION_ENDPOINT")
        params = {"experiment_id": experiment_id, "status_code": TIME_OUT_ERROR}
        rcn_response = requests.post(url, params=params)
        logger.info(
            f"""RCN API experiment registration request:{params},
                    status_code {rcn_response.status_code},
                    response_request: {rcn_response.text}"""
        )
        return False

    except DockerConnectionError:
        logger.exception("There has been an error with the docker connection")
        # Notify the RCN that the experiment execution has not been done
        url = os.environ.get("RCN_EXPERIMENT_REGISTRATION_ENDPOINT")
        params = {"experiment_id": experiment_id, "status_code": TIME_OUT_ERROR}
        rcn_response = requests.post(url, params=params)
        logger.info(
            f"""RCN API experiment registration request:{params},
                    status_code {rcn_response.status_code},
                    response_request: {rcn_response.text}"""
        )

        return False


if __name__ == "__main__":
    worker = celery_app.Worker()
    worker.start()
