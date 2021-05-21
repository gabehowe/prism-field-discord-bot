const {getRandomInt} = require("./util");

function handleMessage(message, language, Discord) {
    if (message.author.bot) {
        return;
    }
    const rand = getRandomInt(0, 1000)
    if (rand === 1) {
        message.channel.send(language["ew"] + message.member.displayName)
    }
    const args = message.content.toString().slice(0).trim().split(' ');
    const command = args.shift().toLowerCase();
    if (command === '02999ae6-5782-4bd5-a78b-7d25b87fe14c ' && message.member.hasPermission("ADMINISTRATOR")) {
        const embed = new Discord.MessageEmbed()
        embed.setTitle(language["react_for_roles"])
        embed.addField("🌎",)

    }
    if (command === 'b8f6c917-ee4f-4ddc-93b1-94d36388e5b6f' && message.member.hasPermission("ADMINISTRATOR")) {
        const Channel = message.channel
        message.delete().then(() => {
        });
        Channel.send(
            "https://media.discordapp.net/attachments/822900347810873405/822923932406382653/rules.png?width=877&height=304",)
            .then()
        Channel.send(
            "** **\n" +
            "**1.** Respect other's opinions, even if they do not agree with your own (This includes things such as the furry fandom).\n" +
            "** **\n" +
            "**2.** Inappropriate images/links are not allowed, and will be taken down.\n" +
            "** **\n" +
            "**3.** Excessive profanity is discouraged, as it makes many people uncomfortable.\n" +
            "** **\n" +
            "**4.** Keep subjects in their respective channels\n" +
            "** **\n" +
            "**5.** As long as it pertains to the current discussion, gifs/memes in <#470999786703552514> are okay. (Note: you have to have the <@&718097534710710428> role or higher to post media in general)\n" +
            "** **\n" +
            "**6.** \"Ghost Chatting\" (saying something and then deleting it repeatedly) is prohibited, as it's very annoying and puts people out of the conversation.\n" +
            "** **\n" +
            "**7.** If people wish to keep their real names private, respect their decision and refer to them by their username instead.\n" +
            "** **\n" +
            "**8.** \"Chainposting\" (sending multiple messages that may be considered spam) is ok, just know where to end it.\n" +
            "** **\n" +
            "**9.** Getting warned/muted 3 times results in a ban.\n" +
            "** **\n" +
            "**10.** Bot commands are only for <#765209868805472256>")
            .then(() => {
            })
    }
    if (command === 'af380375-a4fb-4ed6-9a85-87e878726baa' && message.member.hasPermission("ADMINISTRATOR")) {
        message.delete().then()
        message.channel.send(
            "https://media.discordapp.net/attachments/822900347810873405/822925547101093928/helpful_hints.png?width=877&height=292")
        message.channel.send("** **\n" +
            "The <#739922571671240725> channel is for memes. Just type \"pls meme\" for a new image meme. (can contain profanity)\n" +
            "** **\n" +
            "<#703951319538335775> is where new videos and livestreams are posted.\n" +
            "** **\n" +
            "<#703951289205260409> is for little snippets and pics of WIP videos.\n" +
            "** **\n" +
            "If you just want to chat with everyone, <#470999786703552514> is the place for you.\n" +
            "** **\n" +
            "For all artists out there, we have a <#712748629366145030> channel just for you! Please remember to keep it appropriate!\n" +
            "** **\n" +
            "Self-nicknaming has been disabled for privacy reasons. If you want a nickname, Ping/DM a staff member.\n" +
            "** **\n" +
            "As long as you have subscribed to one of the prism channels, you are eligible for the <@&718097534710710428> role. Just ask a staff member for verification, and we can get it to you ASAP\n" +
            "** **\n" +
            "For any questions or concerns, go to <#719895040767295559>")
    }
}
module.exports = {handleMessage}