# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os
import threading

# import time

# Third-party app imports


# Imports from your apps
from code_runner_files.LoadData import LoadData
from code_runner_files.ResultsObject import ResultsObject

from MyCode import MyCode
from code_runner_files.LogClass import LogClass


class Runner(LogClass):
    """
    Runs the code in the environment

    """

    def __init__(self, dataset_id: str, data_format: str) -> None:
        super().__init__()
        self.__dataset_id = dataset_id
        self.__data_format = data_format
        self.timeout_limit = 20 * 60

    def run(self):

        experiment_id = os.environ.get("EXPERIMENT_ID")
        self.log_info(f"Logs for experiment {experiment_id}")

        def run_thread():
            try:
                # dataset = LoadData(self.__dataset_id, self.__data_format)
                # self.log_info("Data loaded!! Running the code...")
                my_code = MyCode()
                results_list = my_code.run_code()
                self.log_info("Code runned!! Saving the results...")
                for results in results_list:
                    results_object = ResultsObject(
                        experiment_id=experiment_id,
                        results_data=results["data"],
                        filename=results["name"],
                        format=results["format"],
                    )
                    results_object.store_results_object()
                self.log_info("Results saved!!")

            except Exception as exc:
                self.log_exception(
                    f"EXECUTION FAILED FOR experiment_id = {experiment_id}. Following exception(s) occurred: {str(exc)}"
                )

        thread = threading.Thread(target=run_thread)
        thread.start()
        thread.join(timeout=self.timeout_limit)

        if thread.is_alive():
            thread.join()
            raise Exception(f"Remote execution time exceeded {self.timeout_limit} seconds.")
