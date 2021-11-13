from __future__ import annotations
from abc import abstractmethod
from json.decoder import JSONDecoder
from typing import Optional

class Handler:
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, command: str, chatid: str, json_telegram: any) -> Optional[str]:
        pass

class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def handle(self, command: str, chatid: str, json_telegram: any) -> str:
        if(self._next_handler != None):
            return self._next_handler.handle(command, chatid, json_telegram)
        
        return None