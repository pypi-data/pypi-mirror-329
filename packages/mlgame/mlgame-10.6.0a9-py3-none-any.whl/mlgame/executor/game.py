import time
import traceback

import pandas as pd
import pygame
from markdown.util import deprecated

from mlgame.core.communication import GameCommManager
from mlgame.core.exceptions import ErrorEnum, GameError, GameProcessError, MLProcessError
from mlgame.core.model import GameErrorSchema, MLGameDataType, MLGameEntityWrapperSchema, SystemMsgSchema, \
    GameProgressSchema
from mlgame.executor.interface import ExecutorInterface
from mlgame.game.generic import quit_or_esc
from mlgame.game.paia_game import PaiaGame
from mlgame.utils.io import save_json
from mlgame.utils.logger import logger
from mlgame.view.sound_controller import SoundController
from mlgame.view.view import PygameViewInterface


class GameExecutor(ExecutorInterface):
    def __init__(
            self,
            game: PaiaGame,
            game_comm: GameCommManager,
            game_view: PygameViewInterface,
            sound_controller:SoundController,
            fps=30, one_shot_mode=False, no_display=False, output_folder=None):
        self._view_data = None
        self._last_pause_btn_clicked_time = 0
        self._pause_state = False
        self.no_display = no_display
        self.game_view = game_view
        self.sound_controller = sound_controller
        self.frame_count = 0
        self.game_comm = game_comm
        self.game = game
        self._active_ml_names = []
        self._ml_delayed_frames = {}
        self._active_ml_names = list(self.game_comm.get_ml_names())
        self._dead_ml_names = []
        self._ml_execution_time = 1 / fps
        self._fps = fps
        self._ml_delayed_frames = {}
        self._output_folder = output_folder
        for name in self._active_ml_names:
            self._ml_delayed_frames[name] = 0
        # self._recorder = get_recorder(self._execution_cmd, self._ml_names)
        self._frame_count = 0
        self.one_shot_mode = one_shot_mode
        self._proc_name = str(self.game)
        self._clock = pygame.time.Clock()
        self._last_m_key_pressed = time.time()

    def run(self):
        game = self.game
        game_view = self.game_view
        try:
            self._send_system_message("AI準備中")

            self._send_game_info(game.get_scene_init_data())

            self._wait_all_ml_ready()
            self._send_system_message("遊戲啟動")
            while not self._quit_or_esc():
                if game_view.is_paused():
                    # 這裡的寫法不太好，但是可以讓遊戲暫停時，可以調整畫面。因為game_view裡面有調整畫面的程式。
                    self._clock.tick(self._fps)
                    game_view.draw(self._view_data)
                    # time.sleep(0.05)
                    self.sound_controller.pause()
                    continue

                scene_info_dict = game.get_data_from_game_to_player()
                keyboard_info = game_view.get_keyboard_info()

                self._send_data_to_ai_clients(scene_info_dict, keyboard_info)
                self._clock.tick(self._fps)
                cmd_dict = self._receive_cmd_from_ai_clients()

                # self._recorder.record(scene_info_dict, cmd_dict)
                logger.debug(f"update game state at {self._frame_count}")
                result = game.update(cmd_dict)
                self._frame_count += 1
                logger.debug(f"get_scene_progress_data at {self._frame_count}")

                self._view_data = game.get_scene_progress_data()

                logger.debug(f"game_view.draw at {self._frame_count}")
                game_view.draw(self._view_data)

                logger.debug(f"_play_audio at {self._frame_count}")

                self._play_audio(self._view_data)

                # save image
                if self._output_folder:
                    game_view.save_image(f"{self._output_folder}/{self._frame_count:05d}.jpg")
                self._send_game_progress(self._view_data)

                # Do reset stuff
                logger.debug(f"reset or quit by {result} at {self._frame_count}")

                if result == "RESET" or result == "QUIT":
                    scene_info_dict = game.get_data_from_game_to_player()
                    # send to ml_clients and don't parse any command , while client reset ,
                    # self._wait_all_ml_ready() will works and not blocks the process
                    for ml_name in self._active_ml_names:
                        self.game_comm.send_to_ml((scene_info_dict[ml_name], [],True), ml_name)
                    # TODO check what happen when bigfile is saved
                    time.sleep(0.1)
                    game_result = game.get_game_result()

                    attachments = game_result['attachment']
                    print(pd.DataFrame(attachments).to_string())

                    if self.one_shot_mode or result == "QUIT":
                        self._send_system_message("遊戲結束")
                        self._send_game_result(game_result)
                        if self._output_folder:
                            save_json(self._output_folder, game_result)
                        self._send_system_message("關閉遊戲")
                        self._send_end_message()
                        time.sleep(1)

                        break
                    game.reset()
                    game_view.reset()

                    self._frame_count = 0
                    # TODO think more
                    for name in self._active_ml_names:
                        self._ml_delayed_frames[name] = 0
                    logger.debug(f"_wait_all_ml_ready at {self._frame_count}")

                    self._wait_all_ml_ready()
        except Exception:
            # handle unknown exception
            # send to es
            e = GameProcessError(self._proc_name, traceback.format_exc())
            logger.exception(e)
            self._send_game_error_with_obj(GameError(
                error_type=ErrorEnum.GAME_EXEC_ERROR,
                message=e.__str__(),
                frame=self._frame_count,

            ))

        pass

    def _wait_all_ml_ready(self):
        """
        Wait until receiving "READY" commands from all ml processes
        """
        # Wait the ready command one by one
        for ml_name in self._active_ml_names:
            recv = ""
            while recv != "READY":
                try:
                    recv = self.game_comm.recv_from_ml(ml_name)
                    if isinstance(recv, GameError):
                        # handle error when ai_client couldn't be ready state.
                        # logger.info(recv.message)
                        self._dead_ml_names.append(ml_name)
                        self._active_ml_names.remove(ml_name)
                        self._send_game_error_with_obj(recv)
                        break
                except Exception as e:
                    logger.exception(e)
                    self._dead_ml_names.append(ml_name)
                    self._active_ml_names.remove(ml_name)
                    # self._send_game_error(f"AI of {ml_name} has error at initial stage.")
                    ai_error = GameError(
                        error_type=ErrorEnum.AI_INIT_ERROR, frame=0,
                        message=f"AI of {ml_name} has error at initial stage. {e.__str__()}")

                    self._send_game_error_with_obj(ai_error)
                    traceback.print_exc()

                    break
    def _send_data_to_ai_clients(self,scene_info_dict, keyboard_info):
        try:
            # TODO add schema

            for ml_name in self._active_ml_names:
                logger.debug(f"send_to_ml to {ml_name} at {self._frame_count}")
                self.game_comm.send_to_ml((scene_info_dict[ml_name], keyboard_info,self.game.ai_enabled), ml_name)
        except KeyError:
            raise KeyError(
                "The game doesn't provide scene information "
                f"for the client '{ml_name}'")
        pass
    def _receive_cmd_from_ai_clients(self) -> dict:
        logger.debug(f"recv_from_all_ml at {self._frame_count}")
        response_dict = self.game_comm.recv_from_all_ml()

        # logger.info(f"check command of {response_dict} from ml at {self._frame_count}")
        cmd_dict = {}
        for ml_name in self._active_ml_names[:]:
            cmd_received = response_dict[ml_name]
            if isinstance(cmd_received, MLProcessError):
                # print(cmd_received.message)
                # handle error from ai clients
                self._send_game_error_with_obj(GameError(
                    error_type=ErrorEnum.AI_EXEC_ERROR,
                    message=str(cmd_received),
                    frame=self._frame_count
                ))
                self._dead_ml_names.append(ml_name)
                self._active_ml_names.remove(ml_name)
            elif isinstance(cmd_received, GameError):
                self._send_game_error_with_obj(cmd_received)
                self._dead_ml_names.append(ml_name)
                self._active_ml_names.remove(ml_name)
            elif isinstance(cmd_received, dict):
                self._check_delay(ml_name, cmd_received["frame"])
                cmd_dict[ml_name] = cmd_received["command"]
            else:
                cmd_dict[ml_name] = None

        for ml_name in self._dead_ml_names:
            cmd_dict[ml_name] = None

        if len(self._active_ml_names) == 0:
            error = MLProcessError(
                self._proc_name,
                f"The process {self._proc_name} exit because all ml processes has exited.")
            game_error = GameError(
                error_type=ErrorEnum.GAME_EXEC_ERROR, frame=self._frame_count,
                message="All ml clients has been terminated")

            self._send_game_error_with_obj(game_error)
            self._send_game_result(self.game.get_game_result())
            self._send_end_message()

            raise error
        return cmd_dict

        pass

    @deprecated
    def _make_ml_execute(self, scene_info_dict, keyboard_info) -> dict:
        # TODO deprecated
        """
        Send the scene information to all ml processes and wait for commands

        @return A dict of the recevied command from the ml clients
                If the client didn't send the command, it will be `None`.
        """
        try:
            # TODO add schema

            for ml_name in self._active_ml_names:
                logger.debug(f"send_to_ml to {ml_name} at {self._frame_count}")
                self.game_comm.send_to_ml((scene_info_dict[ml_name], keyboard_info), ml_name)
        except KeyError:
            raise KeyError(
                "The game doesn't provide scene information "
                f"for the client '{ml_name}'")

        time.sleep(self._ml_execution_time)
        # self._clock.tick(self._fps)

        logger.debug(f"recv_from_all_ml at {self._frame_count}")

        response_dict = self.game_comm.recv_from_all_ml()

        # logger.info(f"check command of {response_dict} from ml at {self._frame_count}")
        cmd_dict = {}
        for ml_name in self._active_ml_names[:]:
            cmd_received = response_dict[ml_name]
            if isinstance(cmd_received, MLProcessError):
                # print(cmd_received.message)
                # handle error from ai clients
                self._send_game_error_with_obj(GameError(
                    error_type=ErrorEnum.AI_EXEC_ERROR,
                    message=str(cmd_received),
                    frame=self._frame_count
                ))
                self._dead_ml_names.append(ml_name)
                self._active_ml_names.remove(ml_name)
            elif isinstance(cmd_received, GameError):
                self._send_game_error_with_obj(cmd_received)
                self._dead_ml_names.append(ml_name)
                self._active_ml_names.remove(ml_name)
            elif isinstance(cmd_received, dict):
                self._check_delay(ml_name, cmd_received["frame"])
                cmd_dict[ml_name] = cmd_received["command"]
            else:
                cmd_dict[ml_name] = None

        for ml_name in self._dead_ml_names:
            cmd_dict[ml_name] = None

        if len(self._active_ml_names) == 0:
            error = MLProcessError(
                self._proc_name,
                f"The process {self._proc_name} exit because all ml processes has exited.")
            game_error = GameError(
                error_type=ErrorEnum.GAME_EXEC_ERROR, frame=self._frame_count,
                message="All ml clients has been terminated")

            self._send_game_error_with_obj(game_error)
            self._send_game_result(self.game.get_game_result())
            self._send_end_message()

            raise error
        return cmd_dict

    def _check_delay(self, ml_name, cmd_frame):
        """
        Check if the timestamp of the received command is delayed
        """
        delayed_frame = self._frame_count - cmd_frame
        if delayed_frame > self._ml_delayed_frames[ml_name]:
            self._ml_delayed_frames[ml_name] = delayed_frame
            logger.warning(f"The client '{ml_name}' delayed {delayed_frame} frame at frame({self._frame_count})")


    def _quit_or_esc(self) -> bool:
        if self.no_display:
            return self._frame_count > 30000
        else:
            return quit_or_esc()

    def _send_game_result(self, game_result_dict):
        # TO be deprecated("_send_game_error_with_obj")
        obj = MLGameEntityWrapperSchema(
                type=MLGameDataType.GAME_RESULT,data=game_result_dict)
        self.game_comm.send_to_others(
            obj
        )

    def _send_system_message(self, msg: str):

        self.game_comm.send_to_others(
            MLGameEntityWrapperSchema(
                type=MLGameDataType.SYSTEM_MSG,data=SystemMsgSchema(message= msg))
        )

    def _send_game_info(self, game_info_dict):

        self.game_comm.send_to_others(
            MLGameEntityWrapperSchema(
                type=MLGameDataType.GAME_INFO,data=game_info_dict
            )
        )

    def _send_game_progress(self, game_progress_dict:GameProgressSchema):
        """
        Send the game progress to the transition server
        """
        if not isinstance(game_progress_dict, GameProgressSchema):
            game_progress_dict = GameProgressSchema.model_validate(game_progress_dict)
        game_progress_dict.frame = self._frame_count
        #
        # data_dict = {
        #     "type": "game_progress",
        #     "data": game_progress_dict
        # }


        # use wrapper
        logger.debug(game_progress_dict)
        self.game_comm.send_to_others(
            MLGameEntityWrapperSchema(
            data=game_progress_dict
        ))


    def _send_game_error_with_obj(self, error: GameError):
        # print(error)

        self.game_comm.send_to_others( MLGameEntityWrapperSchema(
                type=MLGameDataType.GAME_ERROR,
                data=GameErrorSchema(
                    message=error.message,
                    error_type=error.error_type,
                    frame=error.frame),
            ))


    def _send_end_message(self):
        self.game_comm.send_to_others(MLGameEntityWrapperSchema(type=MLGameDataType.END))

    def _play_audio(self, progress_data:GameProgressSchema):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m] and  (time.time() - self._last_m_key_pressed) > 0.3:
            self.sound_controller.toggle_sound()
            self._last_m_key_pressed = time.time()
        
        if not isinstance(progress_data, GameProgressSchema):
            progress_data =GameProgressSchema.model_validate(progress_data)
        music_objs = progress_data.musics
        sound_objs = progress_data.sounds
        logger.debug("unpause")
        self.sound_controller.unpause()
        logger.debug("play music")

        for music_obj in music_objs :
            self.sound_controller.play_music(music_obj['music_id'])
        logger.debug("play sound")
        for sound_obj in sound_objs:
            self.sound_controller.play_sound(sound_obj['sound_id'])

        pass