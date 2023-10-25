export const LoginScreenFixture = {
    loginScreen: async ({ page }, use) => {
        const loginScreen = new LoginScreen(page);
        await loginScreen.goto();
        await use(loginScreen);
    },
};

class LoginScreen {
    constructor(page) {
        this.page = page;
        this.userLogin = page.getByPlaceholder("name@flowbite.com");
        this.passwordLogin = page.getByLabel("Your password");
        this.submitButton = page.getByRole("button", { name: "Submit" });
        this.notification = page.getByRole("status");
    }

    async goto() {
        const env = process.env.ENVIRONMENT.toLowerCase();
        await this.page.goto(
            `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/login/`
        );
    }
}
