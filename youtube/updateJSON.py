import http.client
import json

with open("../config.json", "r+", encoding="utf-8") as jsonFile:
    config = json.load(jsonFile)
connection = http.client.HTTPSConnection("youtube.googleapis.com")
for i in config["tracked_playlists"]:
    connection.request("GET",
                       "/youtube/v3/playlistItems?part=snippet&playlistId=%s&key=AIzaSyCuLx74MKSILujTHrxvauZP6ih4N"
                       "-Jg4gM" % i)
    response = connection.getresponse().read()
    with open("./youtube/%s.json" % i, "w+", encoding="utf-8") as file:
        file.write(response.decode())
