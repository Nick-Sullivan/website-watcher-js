const { test, expect } = require("@playwright/test");
let dotenv = require("dotenv");

test.beforeAll(async ({}) => {
    let isCicd = (process.env.IS_CICD ?? "false").toLowerCase() === "true";
    if (!isCicd) {
        dotenv.config({ path: ".env" });
    }
});

test.beforeEach(async ({ page }) => {
    const env = process.env.ENVIRONMENT.toLowerCase();
    await page.goto(
        `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/`
    );
});

test("page should have correct title", async ({ page }) => {
    await expect(page).toHaveTitle("Create Next App");
});

test("main button should go to login", async ({ page }) => {
    const button = page.getByRole("link", {
        name: "List watchers -> This is a test.",
    });
    await button.click();

    await page.waitForURL("**/login/");
});
