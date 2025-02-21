from deepanything.Server.Server import DeepAnythingServer
import json

with open("test/config.json") as f:
    conf = json.load(f)

server = DeepAnythingServer(config_object=conf)
server.run()