export const HomeScreenFixture = {
    homeScreen: async ({ page }, use) => {
        const homeScreen = new HomeScreen(page);
        await homeScreen.goto();
        await use(homeScreen);
    },
};

class HomeScreen {
    constructor(page) {
        this.page = page;
        this.button = page.getByRole("link", {
            name: "List watchers -> This is a test.",
        });
    }

    async goto() {
        const env = process.env.ENVIRONMENT.toLowerCase();
        await this.page.goto(
            `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/`
        );
    }
}
