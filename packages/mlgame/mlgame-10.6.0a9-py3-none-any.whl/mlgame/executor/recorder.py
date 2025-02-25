from mlgame.core.communication import TransitionCommManager
from mlgame.executor.interface import ExecutorInterface
from mlgame.utils.logger import logger


from orjson import orjson


import os


class ProgressLogExecutor(ExecutorInterface):
    def __init__(self, progress_folder, progress_frame_frequency, pl_comm: TransitionCommManager):
        # super().__init__(name="ws")
        self._proc_name = f"progress_log({progress_folder}"
        self._progress_folder = progress_folder
        self._progress_frame_frequency = progress_frame_frequency
        self._comm_manager = pl_comm
        self._recv_data_func = self._comm_manager.recv_from_game
        self._filename = "{}.json"
        self._progress_data = []


    def save_json_and_init(self, path):

        with open(path, 'w') as f:
            # json.dump(self._progress_data, f)
            f.write(orjson.dumps(self._progress_data).decode())
        # Get the file size in kilobytes (1 KB = 1024 bytes)
        file_size_kb = os.path.getsize(path) / 1024
        # Print the file path and file size in KB
        print(f"File saved to: {path}, file size: {file_size_kb:.2f} KB")

        self._progress_data = []

    def run(self):
        self._comm_manager.start_recv_obj_thread()

        try:
            progress_count = -1
            while getattr(game_data := self._recv_data_func(),"type") != 'game_result':
                if getattr(game_data,'type') == 'game_progress':
                    # print(game_data)
                    if (game_data['data']['frame'] - 1) % self._progress_frame_frequency == 0 and game_data['data'][
                        'frame'] != 1:
                        self.save_json_and_init(os.path.join(
                            self._progress_folder, self._filename.format(progress_count := progress_count + 1)))
                    self._progress_data.append(game_data['data'])
            else:
                if self._progress_data:
                    self.save_json_and_init(os.path.join(
                        self._progress_folder,
                        self._filename.format(str(progress_count := progress_count + 1) + '-end')))
        except Exception as e:
            # exception = TransitionProcessError(self._proc_name, traceback.format_exc())
            self._comm_manager.send_exception(
                f"exception on {self._proc_name}")
            # catch connection error
            logger.exception(e)
        finally:
            logger.info("end pl")
