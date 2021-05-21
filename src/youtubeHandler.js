const fs = require("fs");
const {spawn} = require("child_process")
let playlistItemsArray = []
let latestVids = []


function runYoutubeChecker(client, sammyGuild, language) {
    function updateJSON() {
        spawn('python', ['youtube/updateJSON.py'])
    }

    updateJSON()
    playlistItemsArray += JSON.parse(fs.readFileSync(""))
    latestVids += playlistItemsArray["items"][0]
    setInterval(() => {
        updateJSON()
        fs.readFile("youtube.json", {encoding: "utf-8"}, (err, data) => {
            playlistItemsArray = JSON.parse(data)
            if (playlistItemsArray["items"][0]['snippet']['resourceId']["videoId"] !== latestVids['snippet']['resourceId']["videoId"]) {
                if (sammyGuild === undefined) {
                    return
                }
                client.channels.cache.get('703951319538335775').send(
                    language['new_video'] + `\n https://youtu.be/${playlistItemsArray["items"][0]['snippet']["resourceId"]["videoId"]}
                `).catch(err => {
                    console.log("Error sending the message")
                })
            }
            latestVids += playlistItemsArray["items"][0]
        })

    }, 15 * 1000)
}

module.exports = {runYoutubeChecker}