const Discord = require('discord.js')
const fs = require('fs')
const util = require("./src/util");
const {CommandInteraction} = require("discord.js");
const {loadInteraction} = require("./src/interactions");
const {handleMessage} = require("./src/messageHandler");
const client = new Discord.Client({
    intents: ['GUILD_MEMBERS', 'GUILD_MESSAGES', "GUILD_MESSAGE_TYPING", "GUILD_MESSAGE_REACTIONS",],
    fetchAllMembers: true,
    partials: ['MESSAGE', "CHANNEL", "GUILD_MEMBER", "REACTION", "USER"]
})
const config = JSON.parse(fs.readFileSync("config.json"))
const token = config['token']
const sammyGuildId = config['sammy_guild_id']
const childProcess = require("child_process")
const {v4: uuidv4} = require('uuid')
let languages = util.initLang()
JSON.parse(fs.readFileSync("./languages/english.json"))
const {runYoutubeChecker} = require("./src/youtubeHandler")


const getApp = (guildId) => {
    const app = client.api.applications(client.user.id)
    if (guildId) {
        app.guilds(guildId)
    }
    return app
}
const createAPIMessage = async (interaction, content) => {
    const {data, files} = await Discord.APIMessage.create(
        client.channels.resolve(interaction.channel_id),
        content
    )
                                       .resolveData()
                                       .resolveFiles()

    return {...data, files}
}

client.on('ready', async () => {
    const mazes = fs.readdirSync("C:\\Users\\gabri\\dev\\Discord\\pism-discorp-bot\\mazes\\")
    mazes.forEach(maze => {
        if (maze.endsWith("png")) {
            fs.unlinkSync(`C:\\Users\\gabri\\dev\\Discord\\pism-discorp-bot\\mazes\\${maze}`)
        }
    })
    console.log('Ready!');
    const commands = await getApp(sammyGuildId).commands.get()
    fs.writeFileSync("./commands.json", JSON.stringify(commands))
    if (!commands.toString().includes("ping")) {
        await getApp(sammyGuildId).commands.post({
            data: {
                name: 'ping',
                description: 'you mums a guy',
            },
        })
    }
    if (!getApp().commands.get().toString().includes("maze")) {
        await getApp().commands.post({
            data: {
                name: "maze",
                description: "creates a maze with the given proportions",
                options: [{
                    name: 'width',
                    description: 'the width of the maze',
                    required: true,
                    type: 4,
                },
                    {
                        name: 'height',
                        description: 'the height of the maze',
                        required: true,
                        type: 4,
                    }]
            }
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
                ],
                default_permission: true
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
    let map = {}
    let array = []
    Object.keys(languages).forEach(key => {
        if (key !== 'lang') {
            array.push({name: languages[key]["language_name"], value: key})
        }
    })
    await getApp(sammyGuildId).commands('845381288738816009').patch({
        data: {
            name: 'config',
            description: "changes some config options",
            options: [{
                name: "set",
                description: "add items to the config",
                type: 1,
                options: [{
                    name: "language",
                    description: "pick your language",
                    type: 3,
                    choices: array
                }]
            }, {
                name: "list",
                description: "list items in the config",
                type: 2,
                options: []
            }, {name: "remove", description: "remove items from the config", type: 2},]
        }
    })
    let animations = []
    JSON.parse(fs.readFileSync("./animations.json"))["owo_name_list"].forEach(val => {
        animations.push({name: val, value: val})
    })
    await getApp(sammyGuildId).commands('847274790360055808').patch({
        data: {
            name: 'animation',
            description: "try it to find out...",
            options: [
                {
                    type: 3,
                    name: "animation",
                    description: "animation to run",
                    required: true,
                    choices: animations
                }
            ]
        }
    })
    const sammyGuild = client.guilds.cache.get(sammyGuildId)
    await runYoutubeChecker(client, sammyGuild, languages["english"])
    fs.writeFileSync("./commands.json", JSON.stringify(commands))
    console.log("updating config")

});
client.on('interactionCreate', interaction => {

    if (interaction.isCommand()) {
        if (interaction.commandName === 'maze') {
            try {
                const uuid = uuidv4()
                const {value: width} = interaction.options.get('width')
                const {value: height} = interaction.options.get('height')
                if (width < 10 || height < 10) {
                    interaction.reply("dimensions must be >= 10")
                    return;
                }
                if (width > 501 || height > 501) {
                    interaction.reply("dimensions must be <= 500")
                    return
                }
                let timeout = (width * height > (250 * 250)) ? ((width * height)/45)*4 : 5000
                if (timeout < 5000) timeout = 5000
                console.log([height, width])
                childProcess.spawn('python', [`./mazes/maze-generation.py`, '--name', uuid, '--width', width, '--height', height])
                setTimeout(() => {
                    if (!fs.existsSync(`C:\\Users\\gabri\\dev\\Discord\\pism-discorp-bot\\mazes\\${uuid}.png`)) {
                        interaction.editReply("There was an error creating your maze. (Probably took too long)")
                        return
                    }
                    interaction.editReply({
                        files: [{
                            attachment: `C:\\Users\\gabri\\dev\\Discord\\pism-discorp-bot\\mazes\\${uuid}.png`,
                            name: 'maze.png',
                        }]
                    }).catch()
                }, timeout)
            } catch (e) {
                interaction.editReply(interaction, "There was an error creating your maze.")
            }
            interaction.defer()
        }
    }
})
client.ws.on('INTERACTION_CREATE', async (interaction) => {
    const isElection = JSON.parse(fs.readFileSync("./elections/isElection.json"))
    const channel = client.channels.cache.get(interaction.channel_id)
    const command = interaction.data.name.toLowerCase()
    const {name, options} = interaction.data
    const args = {}
    let userLanguageName = ''
    const parsedFile = JSON.parse(fs.readFileSync("./user_data/user_data.json"))
    if (interaction.member === undefined) {
        return
    }
    if (parsedFile[interaction.member.user.id] === undefined) {
        userLanguageName = "english"
    }
    else if (parsedFile[interaction.member.user.id]["language"] === undefined) {
        userLanguageName = "english"
    }
    else {
        userLanguageName = parsedFile[interaction.member.user.id]["language"]
    }
    const userLanguage = languages[userLanguageName]
    if (options) {
        for (const option of options) {
            const {name, value} = option
            args[name] = value
        }
    }

    if (command === 'ping') {
        await reply(interaction, userLanguage["pong"], 4)
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
        await reply(interaction, embed, 4)

    }
    else if (command === "config") {
        if (options[0]["name"] === "set") {
            if (options[0]["options"][0]["name"] === "language") {
                const choice = options[0]["options"][0]["value"]
                const userData = JSON.parse(fs.readFileSync("./user_data/user_data.json"))
                if (userData[interaction.member.user.id] === undefined) {
                    userData[interaction.member.user.id] = {}
                }
                userData[interaction.member.user.id]["language"] = choice
                fs.writeFileSync("./user_data/user_data.json", JSON.stringify(userData))
                reply(interaction, "Set language to " + languages[choice]["language_name"])
            }
        }
    }
    else if (command === "vote") {
        let candidate = client.guilds.cache.get(interaction.guild_id).members.cache.get(args['candidate'])
        if (!isElection) {
            await reply(interaction, userLanguage["no_election"], 4)
            return
        }
        if (fs.readFileSync("./elections/votes.txt").toString().includes(interaction.member.user.id)) {
            await reply(interaction, userLanguage["already_voted"], 4)
            return
        }
        if (candidate.id === interaction.member.user.id) {
            await reply(interaction, userLanguage["no_self_vote"], 4)
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

        await reply(interaction, userLanguage["vote_submitted"], 4)
    }
    else if (command === "votecount") {
        if (!isElection) {
            await reply(interaction, userLanguage["no_election"], 4)
            return
        }
        await countVotesEmbed(interaction, channel, userLanguageName)
    }
    else if (command === "startelection") {
        if (isElection) {
            await reply(interaction, userLanguage["election_already_started"], 4)
            return
        }
        if (!interaction.member.roles.includes('845357914176225300')) {
            await reply(interaction, userLanguage["no_permission"], 4)
            return
        }
        fs.writeFileSync("./elections/elections.json", "{}")
        fs.truncateSync("./elections/votes.txt")
        fs.writeFileSync("./elections/isElection.json", "true")
        await reply(interaction, userLanguage["election_started"], 4)
    }
    else if (command === "endelection") {
        if (!isElection) {
            console.log(userLanguage["election_already_ended"])
            await reply(interaction, userLanguage["election_already_ended"], 4)
            return
        }
        if (!interaction.member.roles.includes('845357914176225300')) {
            await reply(interaction, userLanguage["no_permission"], 4)
        }
        const scores = countVotes()
        await reply(interaction, "Election ended.", 4)
        if (scores[0] === undefined) {
            channel.send(userLanguage["no_votes"])
            fs.writeFileSync("./elections/elections.json", "{}")
            fs.truncateSync("./elections/votes.txt")
            fs.writeFileSync("./elections/isElection.json", "false")
            return
        }
        countVotesEmbed(interaction, channel, userLanguageName)
        fs.writeFileSync("./elections/isElection.json", "false")
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
            channel.send(`${userLanguage['congratulations_to']} <@${scores[0]['id']}>`)
        }, 3250)
        fs.writeFileSync("./elections/elections.json", "{}")
        fs.truncateSync("./elections/votes.txt")
    }
    else if (command === "purge") {
        const channel = client.guilds.cache.get(interaction.guild_id).channels.cache.get(interaction.channel_id)
        const member = channel.guild.members.cache.get(interaction.member.user.id)
        if (!member.hasPermission("MANAGE_MESSAGES")) {
            reply(interaction, userLanguage["no_permission"], 4)
            return
        }
        if (args['amount'] > 99 || args['amount'] < 1) {
            reply(interaction, userLanguage["within_099"], 4)
            return
        }
        channel.messages.fetch({limit: (args['amount'])}).then(messages => {
            const unpinnedMessages = messages.filter(msg => !(msg.pinned)); //A collection of messages that aren't pinned
            channel.bulkDelete(unpinnedMessages, true);
            let msgsDeleted = unpinnedMessages.array().length; // number of messages deleted
            let e = userLanguage["messages_deleted"]
            if (msgsDeleted === 1) {
                e = userLanguage["message_deleted"]
            }
            reply(interaction, msgsDeleted + ` ${e}`, 4);
        }).catch(err => {
            reply(interaction, err, 4)
        });
    }
    else if (command === "animation") {
        const owoJson = JSON.parse(fs.readFileSync("./animations.json"))
        const message = reply(interaction, owoJson["owo_frames"][options[0]["value"]][0])
        let blinkSpeed = 100
        let blinkInterval = 1000
        let chance = 35
        let currentFrame = 0
        let doBlink = true
        if (options[0]["value"] === "o_o") {
            chance = 0
            blinkSpeed = 10
            blinkInterval = 100
        }
        if (options[0]["value"] === "moon") {
            chance = 0
            blinkInterval = 500
            doBlink = false
        }
        const interval = await setInterval(() => {
            const rand = util.getRandomInt(0, chance)
            if (currentFrame > owoJson["owo_frames"][options[0]["value"]].length) {
                currentFrame = 0
            }
            if (rand <= 10) {
                editInteraction(interaction, owoJson["owo_frames"][options[0]["value"]][currentFrame])
                currentFrame++
                setTimeout(() => {
                    if (doBlink) {
                        if (currentFrame > owoJson["owo_frames"][options[0]["value"]].length) {
                            currentFrame = 0
                        }
                        editInteraction(interaction, owoJson["owo_frames"][options[0]["value"]][currentFrame])
                    }
                }, blinkSpeed)
            }

        }, blinkInterval)
        await setTimeout(() => {
            clearInterval(interval)
            client.api.webhooks(interaction.application_id, interaction.token).messages("@original").delete()
        }, 60 * 1000)
    }
})

client.on('message', message => {
    handleMessage(message, languages, Discord)
})

client.on('error', err => {
    console.warn(err);
});

client.on('messageReactionAdd', listener => {
})

client.login(token).then(() => {
})

function countVotesEmbed(interaction, channel, userLanguage) {
    const scores = countVotes()
    const embed = new Discord.MessageEmbed()
        .setAuthor(languages[userLanguage]["current_votes"], client.user.avatarURL())
    let string = ""
    scores.forEach(function (key) {
        string += (key["name"] + ": " + key["count"] + "\n")
    })
    embed.setDescription(string)
    channel.send(embed)
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

const reply = async (interaction, response) => {
    let data = {
        content: response,
    }

    // Check for embeds
    if (typeof response === 'object') {
        data = await createAPIMessage(interaction, response)
    }

    client.api.interactions(interaction.id, interaction.token).callback.post({
        data: {
            type: 4,
            data,
        },
    })
}
const editInteraction = async (interaction, response) => {
    // Set the data as embed if reponse is an embed object else as content
    const data = typeof response === 'object' ? {embeds: [response]} : {content: response};
    // Get the channel object by channel id:
    const channel = await client.channels.resolve(interaction.channel_id);
    // Edit the original interaction response:
    client.api.webhooks(interaction.application_id, interaction.token).messages("@original").patch({
        data
    })
};
process.on('uncaughtException', function (err) {
    console.log(err)
})