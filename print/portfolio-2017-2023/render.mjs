// Prints index.html to portfolio.pdf (1440×810 pages). Usage: node render.mjs [--shots dir]
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

// require() honours NODE_PATH, so a global Playwright install works too
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(new URL(import.meta.url).pathname);
const shots = process.argv.includes('--shots') ? process.argv[process.argv.indexOf('--shots') + 1] : null;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 810 } });
await page.goto(pathToFileURL(path.join(here, 'index.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
if (shots) {
  const pages = await page.$$('.page');
  for (let i = 0; i < pages.length; i++)
    await pages[i].screenshot({ path: path.join(shots, `s${String(i + 1).padStart(2, '0')}.png`) });
}
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: path.join(here, 'portfolio.pdf'), width: '1440px', height: '810px', printBackground: true });
await browser.close();
