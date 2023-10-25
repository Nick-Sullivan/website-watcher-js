const { expect, test: testBase } = require("@playwright/test");
const { LoginScreenFixture } = require("./fixtures/loginScreen");
const { ParameterStoreFixture } = require("./fixtures/parameterStore");

const test = testBase.extend({
    ...LoginScreenFixture,
    ...ParameterStoreFixture,
});

test("page should have correct title", async ({ loginScreen }) => {
    await expect(loginScreen.page).toHaveTitle("Create Next App");
});

test("automated tester should be able to log in", async ({
    loginScreen,
    parameterStore,
}) => {
    const username = parameterStore.automatedTesterUsername;
    const password = parameterStore.automatedTesterPassword;
    await loginScreen.userLogin.fill(username);
    await loginScreen.passwordLogin.fill(password);
    await loginScreen.submitButton.click();
    await loginScreen.page.waitForURL("**/watchers/");
});

test("unauthorized users should get a warning", async ({ loginScreen }) => {
    await loginScreen.userLogin.fill("");
    await loginScreen.userLogin.type("fake@fake.com");
    await loginScreen.passwordLogin.fill("");
    await loginScreen.passwordLogin.type("password");
    await loginScreen.submitButton.click();
    await expect(loginScreen.notification).toBeVisible();
});
