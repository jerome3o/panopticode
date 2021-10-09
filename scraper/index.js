const puppeteer = require('puppeteer');
const dotenv = require('dotenv');
const axios = require('axios');
const fs = require('fs');

dotenv.config();

async function scrape() {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        // headless: false,
    });

    const dataFolder = `./data/${new Date().toISOString().replace(/:/gi, "_")}`;

    const page = await browser.newPage();
    await page._client.send(
        'Page.setDownloadBehavior', {
            behavior: 'allow',
            downloadPath: dataFolder,
        }
    );

    // log in
    await page.goto('https://online.asb.co.nz/auth/?fm=header:login');

    await page.waitForSelector('input[id="dUsername"]');
    await page.type('input[id="dUsername"]', process.env.LOGIN);

    await page.waitForSelector('input[id="password"]');
    await page.type('input[id="password"]', process.env.PASSWORD);

    await page.keyboard.press('Enter');

    async function getHubFrame(page) {
        const frameHandle = await page.waitForSelector("#everyday-banking-hub")
        const frame = await frameHandle.contentFrame();
        await frame.waitForSelector("#account-list>div");
        return frame
    }

    let frame = await getHubFrame(page);
    const allAccounts = await frame.$$eval("#account-list>div>div button", divs => divs.map(d => d.id));
    const accounts = allAccounts.filter(a => !a.includes("ASBKS") & a != "");

    const mainUrl = page.url();

    for (let index = 0; index < accounts.length; index++) {
        frame = await getHubFrame(page);
        const a = accounts[index];

        console.log(`scraping ${a}`);
        await frame.click(`#${a}`)
        await page.waitForSelector("#ExportFormatDropdown_input");
        await page.click("#ExportFormatDropdown_input")
        await page.waitForTimeout(50);
        await page.select("#ExportFormatDropdown", "CSV - Generic")
        await page.waitForTimeout(5000);
        await page.goto(mainUrl);
    }

    await browser.close();
    return dataFolder;
};


async function upload(dataFolder) {
    fs.readdir(
        dataFolder,
        (err, files) => {
            if (err) {
                console.error("Could not list the directory.", err);
                process.exit(1);
            }
            files.forEach(file => {
                const text = fs.readFileSync(`${dataFolder}/${file}`).toString("utf-8");
                axios({
                    method: 'post',
                    url: process.env.INGESTION_SERVICE,
                    data: { text },
                })
            });
        }
    )
}


async function main() {
    const dataFolder = await scrape();
    upload(dataFolder);
}


main()
setInterval(
        main,
        1000 * 60 * 60 * 24
    )
    // <input title="" autocomplete="off" name="username" type="text" 
    // placeholder="" spellcheck="false" class="cf-input-field" data-testid="username" 
    // value = "" > < /input>