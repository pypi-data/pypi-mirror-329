from deepanything.Server.Server import DeepAnythingServer
import json

with open("test/config.json", encoding="utf-8") as f:
    conf = json.load(f)

server = DeepAnythingServer(config=conf)
server.run()