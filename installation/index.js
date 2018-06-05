let util = require('util');
let readLine = require('readline');
const exec = util.promisify(require('child_process').exec);
let Git = require("nodegit");
let fs = require('fs');

console.clear();
console.log(`Welkom to the Bartiméus sensors installation.`);

checkPython();

if (!fs.existsSync('./repo')) {
    console.log(`The application will now download the repository from git.`);
    downloadRepository();
}

async function downloadRepository() {
    await Git.Clone(`https://github.com/mikerovers/bartimeus-sensors.git`, `repo`).then((repository) => {
    
    }).catch((err) => {
        console.error(`Repository could not be downloaded:` , err);
    });
}

async function installDependencies() {
    const { stdout, stderr } = await exec(`pip install -r ./repo/requirements.txt`);
}

async function checkPython() {
    try {
        const { stdout, stderr } = await exec('which python');

        console.log('Python 3 found:', stdout);
    } catch(e) {
        console.error(`Python 3 not found.`);
        askInstallPython();
    }
}

async function installPythonDependencies() {
    const { sdout, stderr } = await exec(`pip install ./repo/requirements.txt`);
}

async function askInstallPython() {
    const rl = readLine.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question(`Do you want to install Python 3`, (answer) => {
        switch(answer.trim()) {
            case `y`:
                installPython();
                break;
            case 'n':
                process.exit();
                break;
            default:
                rl.close();
                askInstallPython()
                break;
        }

        rl.close();
    });
}

async function installPython() {
    console.log(`Installing Python...`);
    try {
        await exec('sudo apt-get update');
        await exec(`sudo apt-get install -y python3 python3-pip build-essential libssl-dev libffi-dev python-dev`);
        await exec(`sudo apt-get install -y python3-venv`);
    } catch(e) {
        console.error(err);   
    }
}