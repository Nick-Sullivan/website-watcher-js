const { test: testBase } = require("@playwright/test");
const { WatcherScreenFixture } = require("./fixtures/watcherScreen");

const test = testBase.extend(WatcherScreenFixture);

test("it should redirect to the login page", async ({ watcherScreen }) => {
    await watcherScreen.page.waitForURL("**/login/");
});
