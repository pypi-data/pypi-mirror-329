from typing import Any, Callable, Dict, Optional

from flask import Flask
from flask_socketio import SocketIO

from GSocketIO.Utils.Payload import EmitData, OnData
from GSocketIO.Utils.Typing import Payload


def on_wrapper(func: Callable, dtype: Payload, **_) -> Callable:
    def wrapper(data: Dict[str, Any]) -> Optional[Any]:
        if dtype is Payload.OnData:
            data = OnData(data)
        return func(data)

    return wrapper


def emit_wrapper(
    app: Flask, socketio: SocketIO, func: Callable, namespace: str, **_
) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        data = func(*args, **kwargs)
        if isinstance(data, dict):
            data = EmitData(data)
        elif isinstance(data, OnData):
            data = EmitData(data.__dict__)
        with app.app_context():
            socketio.emit(func.__name__, data.json, namespace=namespace)

    return wrapper


def broadcast_wrapper(app: Flask, socketio: SocketIO, func: Callable, **_) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        data = func(*args, **kwargs)
        if isinstance(data, dict):
            data = EmitData(data)
        with app.app_context():
            socketio.emit(func.__name__, data.json)

    return wrapper
