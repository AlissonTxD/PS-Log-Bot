import json
import os

JSON_DATABASE = "config.json"

class JsonModel:

    def open_json(self) -> dict:
        if not os.path.exists(JSON_DATABASE):
            raise FileNotFoundError("config file no found")
        with open(JSON_DATABASE, "r") as fp:
            var = json.load(fp)
            return var


if __name__ == "__main__":
    json_model = JsonModel()
    config = json_model.open_json()
    print(config)