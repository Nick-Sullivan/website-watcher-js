class Scrape {
    constructor(id, scrapedAt) {
        this.id = id;
        this.scrapedAt = scrapedAt;
    }

    getDate() {
        return (
            this.scrapedAt.getFullYear() +
            "-" +
            (this.scrapedAt.getMonth() + 1).toString().padStart(2, "0") +
            "-" +
            this.scrapedAt.getDate().toString().padStart(2, "0")
        );
    }

    getTime() {
        return (
            this.scrapedAt.getHours().toString().padStart(2, "0") +
            ":" +
            this.scrapedAt.getMinutes().toString().padStart(2, "0") +
            ":" +
            this.scrapedAt.getSeconds().toString().padStart(2, "0")
        );
    }
}

export { Scrape };
