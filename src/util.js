const fs = require("fs");
const {spawn} = require("child_process")

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

function initLang() {
    spawn('python',['../languages/updateLang.py'])
    return JSON.parse(fs.readFileSync("./languages/lang.json"))
}

module.exports = {getRandomInt, initLang}