import os
import chess
import backoff
import subprocess
from strategies import strategies

@backoff.on_exception(backoff.expo, BaseException, max_time=120)
def create_engine(config, board):
    cfg = config["engine"]
    engine_path = os.path.join(cfg["dir"], cfg["name"])
    engine_type = cfg.get("protocol")
    engine_options = cfg.get("engine_options")
    commands = [engine_path]
    if engine_options:
        for k, v in engine_options.items():
            commands.append("--{}={}".format(k, v))

    silence_stderr = cfg.get("silence_stderr", False)

    if engine_type == "strategy":
        return StrategyEngine(board, cfg["name"], cfg.get("strategy_options", {}) or {}, silence_stderr)

    return None


class EngineWrapper:

    def __init__(self, board, commands, options=None, silence_stderr=False):
        pass

    def set_time_control(self, game):
        pass

    def first_search(self, board, movetime):
        pass

    def search(self, board, wtime, btime, winc, binc):
        pass

    def print_stats(self):
        pass

    def name(self):
        return self.engine.name

    def quit(self):
        self.engine.quit()

    def print_handler_stats(self, info, stats):
        for stat in stats:
            if stat in info:
                print("    {}: {}".format(stat, info[stat]))

    def get_handler_stats(self, info, stats):
        stats_str = []
        for stat in stats:
            if stat in info:
                stats_str.append("{}: {}".format(stat, info[stat]))

        return stats_str


class StrategyEngine(EngineWrapper):

    def __init__(self, board, name, options=None, silence_stderr=False):
        self.strategy_name = name
        self.strategy_func = strategies[self.strategy_name]

    def set_time_control(self, game):
        pass

    def first_search(self, board, movetime):
        return self.strategy_func(board)

    def search(self, board, wtime, btime, winc, binc):
        return self.strategy_func(board)

    def print_stats(self):
        pass

    def name(self):
        return self.strategy_name

    def quit(self):
        pass
