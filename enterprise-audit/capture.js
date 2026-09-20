const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'sites.json'), 'utf8'));
const outDir = path.join(process.cwd(), 'artifacts', 'enterprise-visual-audit');
fs.mkdirSync(outDir, { recursive: true });

const viewports = [
  { name: 'desktop', width: 1440, height: 1200 },
  { name: 'mobile', width: 390, height: 844 }
];

function safe(s) { return String(s).replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, ''); }
const results = [];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const site of manifest.sites) {
    for (const viewport of viewports) {
      const context = await browser.newContext({
        viewport: { width: viewport.width, height: viewport.height },
        userAgent: viewport.name === 'mobile'
          ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'
          : undefined
      });
      const page = await context.newPage();
      const consoleErrors = [];
      const pageErrors = [];
      page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text().slice(0, 1000)); });
      page.on('pageerror', err => pageErrors.push(String(err).slice(0, 1000)));

      let httpStatus = null, finalUrl = null, title = null, bodyTextLength = 0, error = null;
      const file = safe(site.entity_key) + '__' + viewport.name + '.png';
      const started = new Date().toISOString();
      try {
        const response = await page.goto(site.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        httpStatus = response ? response.status() : null;
        await page.waitForTimeout(2000);
        finalUrl = page.url();
        title = await page.title();
        bodyTextLength = (await page.locator('body').innerText({ timeout: 5000 }).catch(() => '')).trim().length;
        await page.screenshot({ path: path.join(outDir, file), fullPage: true });
      } catch (e) {
        error = String(e).slice(0, 2000);
        try { await page.screenshot({ path: path.join(outDir, file), fullPage: true }); } catch {}
        finalUrl = page.url();
      }

      results.push({
        ...site,
        viewport: viewport.name,
        width: viewport.width,
        height: viewport.height,
        screenshot: file,
        started_at: started,
        completed_at: new Date().toISOString(),
        http_status: httpStatus,
        final_url: finalUrl,
        title,
        body_text_length: bodyTextLength,
        console_errors: consoleErrors,
        page_errors: pageErrors,
        error,
        rendered: !error && bodyTextLength > 0 && (httpStatus === null || httpStatus < 400),
        review_status: 'needs_human_review'
      });
      await context.close();
    }
  }
  await browser.close();

  fs.writeFileSync(path.join(outDir, 'results.json'), JSON.stringify({
    generated_at: new Date().toISOString(),
    site_count: manifest.sites.length,
    screenshot_count: results.length,
    rendered_count: results.filter(x => x.rendered).length,
    failed_count: results.filter(x => !x.rendered).length,
    results
  }, null, 2));

  const failures = results.filter(x => !x.rendered);
  console.log(JSON.stringify({ sites: manifest.sites.length, screenshots: results.length, failures: failures.length }, null, 2));
})().catch(err => {
  console.error(err);
  process.exitCode = 1;
});
