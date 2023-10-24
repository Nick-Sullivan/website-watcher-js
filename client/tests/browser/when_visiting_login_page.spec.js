const { test, expect } = require("@playwright/test");
let dotenv = require("dotenv");

test.beforeEach(async ({ page }) => {
    let isCicd = (process.env.IS_CICD ?? "false").toLowerCase() === "true";
    if (!isCicd) {
        dotenv.config({ path: ".env" });
    }

    const env = process.env.ENVIRONMENT.toLowerCase();
    await page.goto(
        `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/login/`
    );
});

test("page should have correct title", async ({ page }) => {
    await expect(page).toHaveTitle("Create Next App");
});

test("automated tester should be able to log in", async ({ page }) => {
    const userLogin = page.getByPlaceholder("name@flowbite.com");
    await userLogin.fill("nick.dave.sullivan+testing@gmail.com");

    const passwordLogin = page.getByLabel("Your password");
    await passwordLogin.fill("1GFbIcXMZ09mkBkY");

    const submitButton = page.getByRole("button", { name: "Submit" });
    await submitButton.click();

    await page.waitForURL("**/watchers/");
});

test("unauthorized users should get a warning message", async ({ page }) => {
    const userLogin = page.getByPlaceholder("name@flowbite.com");
    await userLogin.fill("");
    await userLogin.type("fake@fake.com");

    const passwordLogin = page.getByLabel("Your password");
    await passwordLogin.fill("");
    await passwordLogin.type("password");

    const submitButton = page.getByRole("button", { name: "Submit" });
    await submitButton.click();

    const notification = page.getByRole("status");
    await expect(notification).toBeVisible();
});
