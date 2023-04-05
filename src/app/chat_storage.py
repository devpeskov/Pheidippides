import json
from pathlib import Path


class ChatStorage:
    __jsonfile = Path(__file__).resolve().parent / "chat_storage.json"

    def __init__(self):
        self.__init_storage()
        self.__chats: list = self.__get_chats()

    def add_chat(self, chat_id: str) -> bool:
        if chat_id not in self.__chats:
            self.__chats.append(chat_id)
            self.__save()
            return True
        return False

    def remove_chat(self, chat_id: str) -> bool:
        if chat_id in self.__chats:
            self.__chats.remove(chat_id)
            self.__save()
            return True
        return False

    def get_list_of_chats(self) -> list[str]:
        return self.__chats

    def __init_storage(self) -> None:
        if not self.__jsonfile.exists():
            self.__jsonfile.write_text("[]")

    def __get_chats(self):
        with open(self.__jsonfile, "r") as file:
            return json.load(file)

    def __save(self) -> None:
        with open(self.__jsonfile, "w") as file:
            json.dump(self.__chats, file)
