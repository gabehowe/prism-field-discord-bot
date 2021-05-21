const fs = require("fs");
const {spawn} = require("child_process")
let playlistItemsArray = {}
let latestVids = {}


function runYoutubeChecker(client, sammyGuild, language) {
    function updateJSON() {
        spawn('python', ['youtube/updateJSON.py'])
    }

    updateJSON()
    fs.readdir("./youtube/", (err, files) => {
        files.forEach(file => {
            if (!file.endsWith(".json")) return;
            fs.readFile(`./youtube/${file}`, {encoding: 'utf-8'}, (err, data) => {
                playlistItemsArray[file] = JSON.parse(data)
                latestVids[file] = JSON.parse(data)["items"][0]
            })
        })
    })
    setInterval(() => {
        updateJSON()
        fs.readdir("./youtube/", (err, files) => {
            files.forEach(file => {
                if (!file.endsWith(".json")) return;
                fs.readFile(`./youtube/${file}`, {encoding: 'utf-8'}, (err, data) => {
                    playlistItemsArray[file] = JSON.parse(data)
                    if (playlistItemsArray["file"]["items"][0]['snippet']['resourceId']["videoId"] !== latestVids[file]['snippet']['resourceId']["videoId"]) {
                        if (sammyGuild === undefined) {
                            return
                        }
                        client.channels.cache.get('703951319538335775').send(
                            language['new_video'] + `\n https://youtu.be/${playlistItemsArray["items"][0]['snippet']["resourceId"]["videoId"]}
                `).catch(err => {
                            console.log("Error sending the message")
                        })
                    }
                    latestVids[file] = playlistItemsArray[file]["items"][0]
                })
            })
        })
    }, 15 * 1000)
}

module.exports = {runYoutubeChecker}