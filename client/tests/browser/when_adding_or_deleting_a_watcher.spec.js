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
test("the new watcher should be shown on the screen", async ({
    watcherScreen,
}) => {
    await watcherScreen.waitForListToLoad();
    await watcherScreen.addButton.click();
    const numStartingWatchers = await watcherScreen.countWatchers();
    await watcherScreen.watcherModal.name.fill("a new name");
    await watcherScreen.watcherModal.url.fill("https://google.com/");
    await watcherScreen.watcherModal.createButton.click();
    await watcherScreen.waitForListToLoad();
    const numWatchers = await watcherScreen.countWatchers();
    expect.soft(numWatchers).toBe(numStartingWatchers + 1);
});

test("the deleted watcher should be removed on the screen", async ({
    watcherScreen,
}) => {
    await watcherScreen.waitForListToLoad();
    const numStartingWatchers = await watcherScreen.countWatchers();
    await watcherScreen.selectCardWithName("a new name");
    await watcherScreen.watcherDetail.dropdownButton.click();
    await watcherScreen.watcherDetail.deleteButton.click();
    await watcherScreen.watcherDetail.deleteModal.deleteButton.click();
    await watcherScreen.waitForListToLoad();
    const numWatchers = await watcherScreen.countWatchers();
    expect.soft(numWatchers).toBe(numStartingWatchers - 1);
});
