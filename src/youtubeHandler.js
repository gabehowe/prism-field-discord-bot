const fs = require("fs");
const {spawn} = require("child_process")
let playlistItemsArray = {}
let latestVids = {}

function reloadYTDir() {
    fs.readdir("./youtube/", (err, files) => {
        files.forEach(file => {
            if (!file.endsWith(".json")) return;
            fs.readFile(`./youtube/${file}`, {encoding: 'utf-8'}, (err, data) => {
                playlistItemsArray[file] = JSON.parse(data)
                latestVids[file] = JSON.parse(data)["items"][0]
            })
        })
    })
}

async function runYoutubeChecker(client, sammyGuild, language) {
    function updateJSON() {
        spawn('python', ['youtube/updateJSON.py'])
    }

    updateJSON()
    reloadYTDir()
    setInterval(() => {
        updateJSON()
        fs.readdir("./youtube/", (err, files) => {
            files.forEach(file => {
                if (!file.endsWith(".json")) return;
                fs.readFile(`./youtube/${file}`, {encoding: 'utf-8'}, (err, data) => {
                        playlistItemsArray[file] = JSON.parse(data)
                        if (playlistItemsArray[file]["items"] === undefined) {
                            return;
                        }
                        if (playlistItemsArray[file]["items"][0]['snippet']['resourceId']["videoId"] !== latestVids[file]['snippet']['resourceId']["videoId"]) {
                            console.log("new vid")
                            if (sammyGuild === undefined) {
                                return
                            }
                            let alreadyPosted = false
                            client.channels.cache.get('703951319538335775').messages.fetch({limit: 10})
                                .then(messages => {
                                    messages.map((message) => {
                                        if (
                                            message.content.includes(
                                                playlistItemsArray[file]["items"][0]['snippet']["resourceId"]["videoId"])
                                        ) {
                                            alreadyPosted = true
                                        }
                                    })
                                })
                            if (alreadyPosted) {
                                return;
                            }
                            client.channels.cache.get('703951319538335775').send("<@&772453735108313088>" +
                                language['new_video'] + `\n https://youtu.be/${playlistItemsArray[file]["items"][0]['snippet']["resourceId"]["videoId"]}
                `).catch(() => {
                                console.log("Error sending the message")
                            })
                        }

                        latestVids[file] = playlistItemsArray[file]["items"][0]

                    }
                )
            })
        })
    }, 30 * 1000)
}

module.exports = {runYoutubeChecker, reloadYTDir}