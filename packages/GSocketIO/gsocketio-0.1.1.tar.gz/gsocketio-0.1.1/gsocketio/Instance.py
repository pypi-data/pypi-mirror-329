from logging import WARNING, Logger
from threading import Lock
from typing import Any, Callable, Dict, Iterator, Optional, Tuple

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

from .Utils.LogManager import get_logger
from .Utils.Payload import EmitData
from .Utils.Typing import LogMessage, Payload
from .Utils.Wrapper import broadcast_wrapper, emit_wrapper, on_wrapper


class SocketBase:
    _lock = Lock()
    _events: Dict[str, Callable] = dict()

    _app: Optional[Flask] = None
    _logger: Optional[Logger] = None
    _socketio: Optional[SocketIO] = None
    _instance: Optional["SocketBase"] = None

    def __init__(self, app: Optional[Flask] = None, log_level: int = WARNING) -> None:
        if self._logger is None:
            self._logger = get_logger("GSocketIO", log_level)
        else:
            if log_level != WARNING:
                self._logger.setLevel(log_level)

        if app is None and self._socketio is None:
            self._logger.warning(LogMessage.Instance.value)

        if app is not None and self._socketio is None:
            self._app = app
            self._socketio = SocketIO(app)

    def __new__(cls, *args, **kwargs) -> "SocketBase":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def __str__(self) -> str:
        if not self._events:
            return LogMessage.NoEvent.value
        max_key_len = max(len(k) for k in self._events)
        return "\n".join(
            f"{k.ljust(max_key_len)} : {v}" for k, v in self._events.items()
        )

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for k, v in self._events.items():
            yield k, v

    def __getitem__(self, item: str) -> Callable:
        if item not in self._events:
            raise KeyError(LogMessage.AttrErr.value.format(item))

        return self._events[item]

    def __len__(self) -> int:
        return len(self._events)

    @property
    def socketio(self) -> SocketIO:
        return self._socketio

    def _register(
        self,
        func: Callable,
        wrap: Callable,
        namespace: str = "/",
        dtype: Optional[Payload] = None,
    ) -> None:

        name = func.__name__
        if name in self._events:
            self._logger.warning(LogMessage.Mounted.value.format(name))
            return

        kwargs = {
            "func": func,
            "namespace": namespace,
            "dtype": dtype,
            "app": self._app,
            "socketio": self._socketio,
        }

        self._events[name] = wrap(**kwargs)
        setattr(self, name, self._events[name])
        self.socketio.on_event(name, self._events[name], namespace=namespace)
        self._logger.info(LogMessage.Register.value.format(name))

    @staticmethod
    def _join(data: Dict[str, Any]) -> None:
        data = {"username": data["username"], "room": data["room"]}
        data = EmitData(data)

        if hasattr(data, "username") and hasattr(data, "room"):
            join_room(data.room)
            emit("join", data.json, to=data.room)
            print(data.username, data.room)

    @staticmethod
    def _leave(data: Dict[str, Any]) -> None:
        data = {"username": data["username"], "room": data["room"]}
        data = EmitData(data)

        if hasattr(data, "username") and hasattr(data, "room"):
            leave_room(data.room)
            emit("leave", data.json, to=data.room)
            print(data.username, data.room)

    @staticmethod
    def _connect(_) -> None:
        print(f"Connected!")

    @staticmethod
    def _disconnect(_) -> None:
        print(f"disconnected!")


class Socket(SocketBase):
    def init(
        self,
        connect_func: Optional[Callable] = None,
        disconnect_func: Optional[Callable] = None,
        join_func: Optional[Callable] = None,
        leave_func: Optional[Callable] = None,
    ) -> None:
        self.connection_enable(
            connect_func=connect_func, disconnect_func=disconnect_func
        )
        self.room_enable(join_func=join_func, leave_func=leave_func)

    def run(self, **kwargs):
        self.socketio.run(self._app, **kwargs)

    def set_on(
        self, func: Callable, namespace: str = "/", dtype: Payload = Payload.OnData
    ) -> None:
        self._register(func, on_wrapper, namespace, dtype)

    def set_emit(self, func: Callable, namespace: str = "/") -> None:
        self._register(func, emit_wrapper, namespace)

    def set_broadcast(self, func: Callable) -> None:
        self._register(func, broadcast_wrapper)

    def start_background_task(self, target: Callable, *args, **kwargs) -> None:
        self.socketio.start_background_task(target=target, *args, **kwargs)

    def connection_enable(
        self,
        connect_func: Optional[Callable] = None,
        disconnect_func: Optional[Callable] = None,
    ) -> None:
        self.connect_enable(connect_func)
        self.disconnect_enable(disconnect_func)

    def room_enable(
        self,
        join_func: Optional[Callable] = None,
        leave_func: Optional[Callable] = None,
    ) -> None:
        self.join_enable(join_func)
        self.leave_enable(leave_func)

    def connect_enable(self, func: Optional[Callable] = None) -> None:
        if func is None:
            func = self._connect
        self.socketio.on_event("connect", func)
        self._logger.info(LogMessage.Activate.value.format(func.__name__, "connect"))

    def disconnect_enable(self, func: Optional[Callable] = None) -> None:
        if func is None:
            func = self._disconnect
        self.socketio.on_event("disconnect", func)
        self._logger.info(LogMessage.Activate.value.format(func.__name__, "disconnect"))

    def join_enable(self, func: Optional[Callable] = None) -> None:
        if func is None:
            func = self._join
        self.socketio.on_event("join", func)
        self._logger.info(LogMessage.Activate.value.format(func.__name__, "join"))

    def leave_enable(self, func: Optional[Callable] = None) -> None:
        if func is None:
            func = self._leave
        self.socketio.on_event("leave", func)
        self._logger.info(LogMessage.Activate.value.format(func.__name__, "leave"))
