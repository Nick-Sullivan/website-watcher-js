import { getCookie, hasCookie, setCookie } from "cookies-next";
import { Watcher } from "@/models/Watcher";

import {
    CognitoIdentityProviderClient,
    InitiateAuthCommand,
} from "@aws-sdk/client-cognito-identity-provider";

export const isLoggedIn = () => {
    const hasIdToken = hasCookie(process.env.NEXT_PUBLIC_COOKIE_ID_TOKEN);
    return hasIdToken;
};

export const authenticate = async (username, password) => {
    const client = new CognitoIdentityProviderClient({
        region: process.env.NEXT_PUBLIC_COGNITO_REGION,
    });

    const command = new InitiateAuthCommand({
        AuthParameters: {
            USERNAME: username,
            PASSWORD: password,
        },
        AuthFlow: "USER_PASSWORD_AUTH",
        ClientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID,
    });
    try {
        const response = await client.send(command);
        const idToken = response.AuthenticationResult.IdToken;
        console.log("setting cookie");
        // TODO, make secure and HTTP only.
        setCookie(process.env.NEXT_PUBLIC_COOKIE_ID_TOKEN, idToken);
        console.log("getting cookie");
        const hasIdToken = getCookie(process.env.NEXT_PUBLIC_COOKIE_ID_TOKEN);
        console.log(hasIdToken);
        return true;
    } catch (e) {
        console.log(e);
        return false;
    }
};

export const authenticateBad = async (username, password) => {
    const body = {
        AuthParameters: {
            USERNAME: username,
            PASSWORD: password,
        },
        AuthFlow: "USER_PASSWORD_AUTH",
        ClientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID,
    };
    const headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
    };
    const rawResponse = await fetch(
        "https://cognito-idp.ap-southeast-2.amazonaws.com",
        {
            method: "POST",
            body: JSON.stringify(body),
            headers: headers,
        }
    );
    const response = await rawResponse.json();
    const idToken = response.AuthenticationResult.IdToken;
    return idToken;
};

export const getWatchers = async () => {
    const rawResponse = await fetch("https://cat-fact.herokuapp.com/facts");
    const response = await rawResponse.json();
    const watchers = response.map(
        (item, index) =>
            new Watcher(index.toString(), index.toString(), item.text)
    );
    return watchers;
};
