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
        this.addButton = page.getByTestId("new-watcher");
        this.watcherModal = new NewWatcherModal(page);
        this.watcherDetail = new WatcherDetail(page);
        this.watcherList = page.getByTestId("flowbite-card");
    }

    async goto() {
        const env = process.env.ENVIRONMENT.toLowerCase();
        await this.page.goto(
            `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/watchers/`
        );
    }

    async waitForListToLoad() {
        await this.addButton.click();
        await this.watcherModal.cancelButton.click();
    }
    async countWatchers() {
        return await this.watcherList.count();
    }

    async selectCardWithName(name) {
        const count = await this.countWatchers();
        for (let i = 0; i < count; i++) {
            const card = await this.watcherList.nth(i);
            const cardName = await card.getByTestId("name");
            const text = await cardName.innerText();
            if (text == name) {
                await card.click();
                return;
            }
        }
    }
}

class NewWatcherModal {
    constructor(page) {
        this.page = page;
        this.name = page.getByPlaceholder("My New Watcher");
        this.url = page.getByPlaceholder("https://google.com");
        this.createButton = page.getByRole("button", { name: "Create" });
        this.cancelButton = page.getByRole("button", { name: "Cancel" });
    }
}

class DeleteWatcherModal {
    constructor(page) {
        this.page = page;
        this.deleteButton = page.getByRole("button", { name: "Delete" });
    }
}
class WatcherDetail {
    constructor(page) {
        this.page = page;
        this.dropdownButton = page.locator("svg").nth(1);
        this.editButton = page.getByRole("button", { name: "Edit" });
        this.deleteButton = page.getByRole("button", { name: "Delete" });
        this.deleteModal = new DeleteWatcherModal(page);
    }
}
