export const WatcherScreenFixture = {
    watcherScreen: async ({ page }, use) => {
        const watcherScreen = new WatcherScreen(page);
        await watcherScreen.goto();
        await use(watcherScreen);
    },
};

class WatcherScreen {
    constructor(page) {
        this.page = page;
        this.logo = page.getByRole("link", {
            name: "Flowbite logo Website Watcher",
        });
    }

    async goto() {
        const env = process.env.ENVIRONMENT.toLowerCase();
        await this.page.goto(
            `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/watchers/`
        );
    }
}
