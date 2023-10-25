const { test } = require("@playwright/test");
const fs = require("fs");
const path = require("path");

export const AuthenticatedSessionFixture = {
    storageState: async ({ browser, parameterStore }, use) => {
        const outputDir = test.info().project.outputDir;
        const fileName = path.resolve(outputDir, ".auth.json");
        // Authenticate the first time, then re-use the session state
        if (!fs.existsSync(fileName)) {
            const page = await browser.newPage({ storageState: undefined });
            const session = new AuthenticatedSession(page, parameterStore);
            await session.login();
            await page.context().storageState({ path: fileName });
            await page.close();
        }
        await use(fileName);
    },
};

class AuthenticatedSession {
    constructor(page, parameterStore) {
        this.page = page;
        this.parameterStore = parameterStore;
        this.userLogin = page.getByPlaceholder("name@flowbite.com");
        this.passwordLogin = page.getByLabel("Your password");
        this.submitButton = page.getByRole("button", { name: "Submit" });
        this.notification = page.getByRole("status");
    }

    async login() {
        const env = process.env.ENVIRONMENT.toLowerCase();
        await this.page.goto(
            `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/login/`
        );
        const username = this.parameterStore.automatedTesterUsername;
        const password = this.parameterStore.automatedTesterPassword;
        await this.userLogin.fill(username);
        await this.passwordLogin.fill(password);
        await this.submitButton.click();
        await this.page.waitForURL("**/watchers/");
    }
}
