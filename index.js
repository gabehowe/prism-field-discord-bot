const Discord = require('discord.js')
const fs = require('fs')
const {spawn} = require("child_process")
const client = new Discord.Client()
const config = JSON.parse(fs.readFileSync("config.json"))
const token = config['token']
const sammyGuildId = config['sammy_guild_id']
let language = JSON.parse(fs.readFileSync("language.json"))
let playlistItemsArray = []
let latestVids = []

const getApp = async (guildId) => {
    const app = client.api.applications(client.user.id)
    if (guildId) {
        app.guilds(guildId)
    }
    return app
}

client.on('ready', async () => {
    console.log('Ready!');
    updateJSON()
    // playlistItemsArray += JSON.parse(fs.readFileSync(""))
    // latestVids += playlistItemsArray["items"][0]
    // const sammyGuild = client.guilds.cache.get(sammyGuildId)

    function updateJSON() {
        spawn('python', ['youtube/updateJSON.py'])
    }

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
    const commands = await getApp(sammyGuildId).commands.get()
    if (!commands.toString().includes("ping")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'ping',
                description: 'you mums a guy',
            },
        })
    }
    if (!commands.toString().includes("purge")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'purge',
                description: 'removes messages (requires delete messages permission)',
                options: [{
                    name: 'amount',
                    description: 'the amount of messages to delete (0-99)',
                    required: true,
                    type: 4,
                },
                ]
            }
        })
    }
    if (!commands.toString().includes("sayas")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'sayas',
                description: 'sends a message "as" a user',
                options: [
                    {
                        name: 'user',
                        description: 'the user you want to impersonate',
                        required: true,
                        type: 6,
                    },
                    {
                        name: 'message',
                        description: 'what you want to say',
                        required: true,
                        type: 3,
                    }
                ]
            },
        })
    }
    if (!commands.toString().includes("vote")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'vote',
                description: 'vote for a candidate in the elections',
                options: [{
                    name: 'candidate',
                    description: 'person to vote for',
                    required: true,
                    type: 6,
                }]
            }
        })
    }
    if (!commands.toString().includes("startelection")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'startelection',
                description: 'starts the election'
            }
        })
    }
    if (!commands.toString().includes("endelection")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'endelection',
                description: 'ends the election'
            }
        })
    }
});

client.ws.on('INTERACTION_CREATE', async (interaction) => {
    let electionOver = Boolean.valueOf(fs.readFileSync("./elections/ended.txt"))
    const command = interaction.data.name.toLowerCase()
    const {name, options} = interaction.data
    const args = {}
    if (options) {
        for (const option of options) {
            const {name, value} = option
            args[name] = value
        }
    }
    if (command === 'ping') {
        await reply(interaction, language["pong"], 4)
    }
    else if (command === "sayas") {
        const guild = client.guilds.cache.get(sammyGuildId)
        let member = guild.members.cache.get(args['user'])
        if (member === undefined) {
            return
        }
        const embed = new Discord.MessageEmbed()
            .setAuthor(member.displayName, member.user.avatarURL(), 'https://www.youtube.com/watch?v=s-n9TaTdOjA')
            .setDescription(args['message'])
        const channel = guild.channels.cache.get(interaction.channel_id)
        await reply(interaction, embed, 4)

    }
    else if (command === "vote") {
        let candidate = client.guilds.cache.get(interaction.guild_id).members.cache.get(args['candidate'])
        if (electionOver) {
            await reply(interaction, language["no_election"], 4)
            return
        }
        if (fs.readFileSync("./elections/votes.txt").toString().includes(interaction.member.user.id)) {
            await reply(interaction, language["already_voted"], 4)
            return
        }
        fs.appendFile("./elections/votes.txt", interaction.member.user.id + "\n", () => {
        })
        const JSONfile = JSON.parse(fs.readFileSync("./elections/elections.json"))
        if (!JSON.stringify(JSONfile).includes(candidate.id)) {
            JSONfile[candidate.id] = {"name": candidate.displayName, "count": 1, "id": candidate.id}
        }
        else if (JSON.stringify(JSONfile).includes(candidate.id)) {
            JSONfile[candidate.id]["count"] += 1
        }
        fs.writeFileSync("./elections/elections.json", JSON.stringify(JSONfile))

        await reply(interaction, language["vote_submitted"], 4)
    }
    else if (command === "votecount") {
        if (electionOver) {
            await reply(interaction, language["no_election"], 4)
            return
        }
        await countVotesEmbed(interaction)
    }
    else if (command === "startelection") {
        if (!electionOver) {
            await reply(interaction, language["election_already_started"], 4)
            return
        }
        if (!interaction.member.roles.includes('703949595297972314')) {
            await reply(interaction, language["no_permission"], 4)
            return
        }
        electionOver = false
        fs.writeFileSync("./elections/elections.json", "{}")
        fs.truncateSync("./elections/votes.txt")
        fs.writeFileSync("./elections/ended.txt", "false")
        await reply(interaction, language["election_started"], 4)
    }
    else if (command === "endelection") {
        if (electionOver) {
            await reply(interaction, language["election_already_ended"], 4)
            return
        }
        if (!interaction.member.roles.includes('703949595297972314')) {
            await reply(interaction, language["no_permission"], 4)
        }
        electionOver = true
        const scores = countVotes()
        const channel = client.guilds.cache.get(interaction.guild_id).channels.cache.get(interaction.channel_id)
        if (scores[0] === undefined) {
            reply(interaction, language["no_votes"], 4)
            fs.writeFileSync("./elections/elections.json", "{}")
            fs.truncateSync("./elections/votes.txt")
            return
        }
        channel.send("Election ended.")
        countVotesEmbed(interaction)
        fs.writeFileSync("./elections/ended.txt", "true")
        if (scores[1]) {
            if (scores[0].count === scores[1].count) {
                channel.send("It was a tie!")
                fs.writeFileSync("./elections/elections.json", "{}")
                fs.truncateSync("./elections/votes.txt")
                return
            }
        }
        setTimeout(() => {
            channel.send("And the winner is...")
        }, 500)
        setTimeout(() => {
            channel.send("...")
        }, 1000)
        setTimeout(() => {
            channel.send("...")
        }, 1500)
        setTimeout(() => {
            channel.send("...")
        }, 2000)
        setTimeout(() => {
            channel.send("🎉 " + scores[0]['name'] + " 🎉")
        }, 3000)
        setTimeout(() => {
            channel.send(`${language['congratulations_to']} <@${scores[0]['id']}>`)
        }, 3250)
        fs.writeFileSync("./elections/elections.json", "{}")
        fs.truncateSync("./elections/votes.txt")
    }
    else if (command === "purge") {
        const channel = client.guilds.cache.get(interaction.guild_id).channels.cache.get(interaction.channel_id)
        const member = channel.guild.members.cache.get(interaction.member.user.id)
        if (!member.hasPermission("MANAGE_MESSAGES")) {
            reply(interaction, language["no_permission"], 4)
            return
        }
        if (args['amount'] > 99 || args['amount'] < 1) {
            reply(interaction, language["within_099"], 4)
            return
        }
        channel.messages.fetch({limit: (args['amount'])}).then(messages => {
            const unpinnedMessages = messages.filter(msg => !(msg.pinned)); //A collection of messages that aren't pinned
            channel.bulkDelete(unpinnedMessages, true);
            let msgsDeleted = unpinnedMessages.array().length; // number of messages deleted
            let e = language["messages_deleted"]
            if (msgsDeleted === 1) {
                e = language["message_deleted"]
            }
            reply(interaction, msgsDeleted + ` ${e}`, 4);
        }).catch(err => {
            reply(interaction, err, 4)
        });
    }
})

client.on('message', message => {
    handleMessage(message, language, Discord)
})

client.on('error', err => {
    console.warn(err);
});

client.on('messageReactionAdd', listener => {
})

client.login(token).then(r => {
})

function countVotesEmbed(interaction, language, client) {
    const scores = countVotes()
    const embed = new Discord.MessageEmbed()
        .setAuthor(language["current_votes"], client.user.avatarURL())
    let string = ""
    scores.forEach(function (key) {
        string += (key["name"] + ": " + key["count"] + "\n")
    })
    embed.setDescription(string)
    reply(interaction, embed, 4)
}

function countVotes() {
    const object = JSON.parse(fs.readFileSync("./elections/elections.json"))
    const scores = [];
    new Map(Object.entries(object)).forEach((value) => {
        if (value["count"]) {
            scores.push(value)
        }
    })
    scores.sort(function (a, b) {
        return b.count - a.count;
    });
    return scores
}


const createAPIMessage = async (interaction, content, client) => {
    const {data, files} = await Discord.APIMessage.create(
        client.channels.resolve(interaction.channel_id),
        content
    )
        .resolveData()
        .resolveFiles()

    return {...data, files}
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}
