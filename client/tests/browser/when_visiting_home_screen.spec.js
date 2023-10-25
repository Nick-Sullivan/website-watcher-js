const { expect, test: testBase } = require("@playwright/test");
const { HomeScreenFixture } = require("./fixtures/homeScreen");

const test = testBase.extend(HomeScreenFixture);

test("page should have correct title", async ({ homeScreen }) => {
    await expect(homeScreen.page).toHaveTitle("Create Next App");
});

test("main button should go to login", async ({ homeScreen }) => {
    await homeScreen.button.click();
    await homeScreen.page.waitForURL("**/login/");
});
