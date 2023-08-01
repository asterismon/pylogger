class Logger_InternalError(SyntaxError):pass
loggers:dict[str,dict] = {
    "message": {
        "fore_color": "rgb(0, 255, 255)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "info": {
        "fore_color": "rgb(0, 255, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "warning": {
        "fore_color": "rgb(255, 255, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "error": {
        "fore_color": "rgb(255, 0, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "final": {
        "fore_color": "rgb(255, 0, 0)",
        "back_color": "rgb(255, 255, 0)",
        "extend_settings": "bold",
        "available": True,
    },
    "off": {
        "fore_color": "rgb(100, 100, 100)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
}
def message(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def info(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def warning(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def error(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def final(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def off(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
