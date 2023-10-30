const { test: testBase, expect } = require("@playwright/test");
const { WatcherScreenFixture } = require("./fixtures/watcherScreen");
const { ParameterStoreFixture } = require("./fixtures/parameterStore");
const {
    AuthenticatedSessionFixture,
} = require("./fixtures/authenticatedSession");

const test = testBase.extend({
    ...AuthenticatedSessionFixture,
    ...ParameterStoreFixture,
    ...WatcherScreenFixture,
});

test("clicking header should go to spaghetti", async ({ watcherScreen }) => {
    await watcherScreen.logo.click();
    await watcherScreen.page.waitForURL(
        "https://100percentofthetimehotspaghetti.com/"
    );
});
