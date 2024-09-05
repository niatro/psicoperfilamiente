const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        headless: false,  // Para ver el navegador mientras se ejecuta
        executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', // Reemplaza esta ruta si Chrome está en otro lugar
        userDataDir: 'C:/TempChromeProfile',  // Reemplaza con la ruta al perfil de Chrome que estás utilizando
    });

    const urls = JSON.parse(fs.readFileSync('urls.json', 'utf8'));  // Cargar URLs desde un archivo JSON

    for (const {url, filePath} of urls) {
        const page = await browser.newPage();

        await page.setViewport({
            width: 1200,
            height: 1200,
            deviceScaleFactor: 1,
        });

        await page.goto(url, {
            waitUntil: "domcontentloaded",
            timeout: 60000,
        });

        await new Promise(resolve => setTimeout(resolve, 5000));  // Espera adicional para asegurarse de que todo esté cargado

        await page.screenshot({
            path: filePath,
            fullPage: true,
        });

        await page.close();
        console.log(`Captura de pantalla completa guardada en ${filePath}`);
    }

    await browser.close();
})();