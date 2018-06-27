const fs = require("fs");
const path = require("path");
const sluggr = require("sluggr");

const input = path.resolve(__dirname, "input.txt");
const output = path.resolve(__dirname, "sources/Notre_Dame_de_Paris_en_full.txt");

const file = fs.readFileSync(input);

const slugger = sluggr("\n", "àâçèéêëîïôöùûü", false);

const textWithoutNumbers = file.toString().replace(/[0-9]/g, " ");
const formattedText = slugger(textWithoutNumbers);

fs.writeFileSync(output, formattedText);
