const Discord = require('discord.js')
const fs = require('fs')
const {countVotesEmbed} = require("./util");
const {reply} = require("./util");
const getApp = (guildId, client) => {
    const app = client.api.applications(client.user.id)
    if (guildId) {
        app.guilds(guildId)
    }
    return app
}
async function loadInteraction(sammyGuildId, name, description, options, commands,client) {
    if (!commands.toString().includes(name)) {
        await getApp(sammyGuildId,client).commands.post({
            data: {
                name: name,
                description: description,
                options: options
            }
        })
    }
}

async function handleInteraction(interaction, sammyGuildId, language, client) {
}

module.exports = {handleInteraction, loadInteraction}