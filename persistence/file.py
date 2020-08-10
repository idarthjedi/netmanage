from persistence.storage import Storage
from typing import List
from typing import Dict
from os import path
import pickle


class File(Storage):

    def save(self, location: str, found_machines: Dict) -> None:
        print("loading previous file")
        stored_machines = self.load(location)

        updated_machines = self.__merge(stored_machines, found_machines)

        print("saving to file")
        with open(location, mode="wb") as f:
            pickle.dump(updated_machines, f)

    def load(self, location: str) -> Dict:
        print("loading from file")
        loaddict = {}
        if path.exists(location):
            with open(location, mode="rb") as f:
                loaddict = pickle.load(f)

        return loaddict

    def __merge(self, oldlist: Dict, newlist: Dict) -> Dict:
        for key, value in newlist.items():
            if key in oldlist.keys():
                oldlist[key]["last_seen"] = newlist[key]["last_seen"]
            else:
                oldlist[key] = newlist[key]

        return oldlist
