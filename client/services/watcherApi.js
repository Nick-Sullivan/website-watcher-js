import { Watcher } from "@/models/Watcher";
import { getCookie } from "cookies-next";
import { COOKIE_KEY_ID_TOKEN } from "@/services/constants";

export const getCatFacts = async () => {
    const rawResponse = await fetch("https://cat-fact.herokuapp.com/facts");
    const response = await rawResponse.json();
    const duplicatedResponse = [...response, ...response, ...response];
    const watchers = duplicatedResponse.map(
        (item, index) =>
            new Watcher(index.toString(), index.toString(), item.text)
    );
    return watchers;
};

export const getWatchers = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/websites`;
    const idToken = getCookie(COOKIE_KEY_ID_TOKEN);
    const headers = { Authorization: `Bearer ${idToken}` };

    const rawResponse = await fetch(url, {
        method: "GET",
        headers: headers,
        credentials: "include",
    });

    const response = await rawResponse.json();
    console.log(response);

    const watchers = response["websites"].map(
        (item, index) => new Watcher(item.website_id, item.name, item.url)
    );

    return watchers;
};
