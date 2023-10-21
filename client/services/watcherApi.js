import { Watcher } from "@/models/Watcher";
import { getCookie } from "cookies-next";

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
    // return await getCatFacts();
    const url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/websites`;
    const idToken = getCookie(process.env.NEXT_PUBLIC_COOKIE_ID_TOKEN);
    console.log(idToken);
    const headers = { Authentication: `Bearer ${idToken}` };

    const rawResponse = await fetch(url, {
        method: "GET",
        headers: headers,
        credentials: "include",
    });

    const response = await rawResponse.json();
    console.log(response);

    return [];
};
