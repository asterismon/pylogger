import os
from inspect import currentframe
from queue import Queue

from threading import current_thread, Thread
from multiprocessing import current_process
from time import strftime
from types import FrameType
from typing import Callable
from rich.console import Console

__VERSION__ = "2.1.7"


class Logger:
    class mode:  # 调整日志级别
        ALL = -100
        DEBUG = -10
        NORMAL = 0
        INFO = 10
        WARNING = 20
        ERROR = 30
        FATAL = 40
        OFF = 100

    def __init__(
        self,
        process: bool = False,
        thread: bool = False,
        objID: bool = False,
        func_name: bool = True,
        filename: bool = True,
        line: bool = True,
        *,
        save: bool = True,
        quiet: bool = False,
        auto_highlight: bool = False,
        logfile_max: int = 30,
        kw_min: int = 9,
        mode: int = mode.NORMAL,
    ) -> None:
        """
        初始化Logger

        Args:
            process: 进程显示开关. 默认为False.
            thread: 线程显示开关. 默认为False.
            objID: 进程、线程和函数的ID开关,适合调试时打开. 默认为False.
            func_name: 显示函数名. 默认为True.
            filename: 显示文件名. 默认为True.
            line: 显示行数. 默认为True.
            save: 是否保存为文件. 默认为True.
            quiet: 控制台静默. 默认为False.
            auto_highlight: rich自动语法高亮开关. 默认为False.
            logfile_max: 保留的旧日志文件数目. 默认为30.
            kw_min: Logger类型关键字长度. 默认为7.
            level: Logger日志级别. 默认为level.NORMAL.
        """
        self.process = process
        self.thread = thread
        self.objID = objID
        self.func_name = func_name
        self.filename = filename
        self.line = line
        self.logfile_max = logfile_max
        self.kw_min = kw_min
        self.level = mode
        self.save = save
        self.quiet = quiet
        self.auto_highlight = auto_highlight
        self.queue: Queue = Queue()
        self.console = Console()
        self.logfileCleaner()
        Thread(target=self.__listener, name="logWriter", daemon=True).start()
        return

    def debug(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= -10:
            self.logger(
                mode="debug",
                _string=_string,
                fore_color="rgb(255,255,255)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def notice(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 0:
            self.logger(
                mode="notice",
                _string=_string,
                fore_color="rgb(0,255,255)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def info(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 10:
            self.logger(
                mode="info",
                _string=_string,
                fore_color="rgb(0,255,0)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def warning(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 20:
            self.logger(
                mode="warning",
                _string=_string,
                fore_color="rgb(255,255,0)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def error(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 30:
            self.logger(
                mode="error",
                _string=_string,
                fore_color="rgb(255,0,0)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def fatal(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 40:
            self.logger(
                mode="fatal",
                _string=_string,
                fore_color="rgb(255,0,0)",
                back_color="rgb(255,255,0)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def heartbeat(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 0:
            self.logger(
                mode="heartbeat",
                _string=_string,
                fore_color="rgb(150,150,150)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def panic(
        self,
        _string: str,
        callback: Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        if self.level <= 50:
            self.logger(
                mode="panic",
                _string=_string,
                fore_color="rgb(255,255,0)",
                back_color="rgb(200,0,0)",
                callback=callback,
                args=args,
                kwargs=kwargs,
            )

    def logger(
        self,
        mode: str,
        _string: str,
        fore_color: str,
        back_color: str = "",
        extend_settings: str = "",
        callback: Callable | None = None,
        *args,
        **kwargs,
    ):
        writeIn_log_mode = mode.upper() + " " * (self.kw_min - len(mode))
        time = strftime("%H:%M:%S")
        value = f"{time} [{writeIn_log_mode}]{self.__log()}: {_string}"
        self.queue.put(value + "\n")
        if self.quiet:
            pass
        self.console.print(
            value,
            highlight=self.auto_highlight,
            style=(
                f"{fore_color} on {back_color} {extend_settings}"
                if back_color
                else f"{fore_color} {extend_settings}"
            ),
        )
        if callback:
            callback(args, kwargs)

    def setLevel(self, level: int | mode):
        self.level = level

    def logfileCleaner(self):
        if not os.path.exists("logs"):
            os.mkdir("logs")
            return
        logs = os.listdir("./logs")[::-1]
        while len(logs) > self.logfile_max:
            os.remove(logs.pop())

    def __log(self):
        using: FrameType = currentframe().f_back.f_back.f_back
        filename = (
            f" in {os.path.basename(using.f_code.co_filename)}" if self.filename else ""
        )
        cur_process = current_process()
        process_id = f"(ID {id(cur_process)})" if self.objID else ""
        process = f" <Process {cur_process.name}{process_id}>" if self.process else ""
        cur_thread = current_thread()
        thread_id = f"(ID {id(cur_thread)})" if self.objID else ""
        thread = f" <Thread {cur_thread.name}{thread_id}>" if self.thread else ""
        objID = f" (ID {id(using.f_code)})" if self.objID else ""
        func_name = f" <{using.f_code.co_name}{objID}>" if self.func_name else ""
        line = f" ,line {using.f_lineno}" if self.line else ""
        return process + thread + func_name + filename + line

    def __listener(self):
        try:
            if self.save:
                with open(
                    "./logs/" + strftime("%Y-%m-%d") + ".log", "x", encoding="utf-8"
                ):
                    pass
        finally:
            while True:
                log = self.queue.get()
                if self.save:
                    with open(
                        "./logs/" + strftime("%Y-%m-%d") + ".log", "a", encoding="utf-8"
                    ) as f:
                        f.write(log)
                self.queue.task_done()
