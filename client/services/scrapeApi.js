import { getCookie } from "cookies-next";
import { COOKIE_KEY_ID_TOKEN } from "@/services/constants";
import { Scrape } from "@/models/Scrape";

export const getScrapes = async (websiteId) => {
    const url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/websites/${websiteId}/scrapes`;
    const idToken = getCookie(COOKIE_KEY_ID_TOKEN);
    const headers = { Authorization: `Bearer ${idToken}` };

    const rawResponse = await fetch(url, {
        method: "GET",
        headers: headers,
        credentials: "include",
    });

    const response = await rawResponse.json();
    console.log(response);

    const scrapes = response["scrapes"].map((item) => {
        const dt = new Date(item.scraped_at);
        return new Scrape(item.scrape_id, dt);
    });

    scrapes.sort((a, b) => b.scrapedAt - a.scrapedAt);

    return scrapes;
};

export const getScreenshot = async (websiteId, scrapeId) => {
    const url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/websites/${websiteId}/scrapes/${scrapeId}/screenshot`;
    const idToken = getCookie(COOKIE_KEY_ID_TOKEN);
    const headers = { Authorization: `Bearer ${idToken}` };

    const rawResponse = await fetch(url, {
        method: "GET",
        headers: headers,
        credentials: "include",
    });

    const response = await rawResponse.json();
    console.log(response);

    const screenshotUrl = response["screenshot_url"];
    return screenshotUrl;
};
