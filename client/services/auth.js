import { getCookie, hasCookie, setCookie } from "cookies-next";
import { COOKIE_KEY_ID_TOKEN } from "@/services/constants";

import {
    CognitoIdentityProviderClient,
    InitiateAuthCommand,
} from "@aws-sdk/client-cognito-identity-provider";

export const isLoggedIn = () => {
    const hasIdToken = hasCookie(COOKIE_KEY_ID_TOKEN);
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
        setCookie(COOKIE_KEY_ID_TOKEN, idToken);
        // console.log("getting cookie");
        // const hasIdToken = getCookie(process.env.NEXT_PUBLIC_COOKIE_ID_TOKEN);
        // console.log(hasIdToken);
        return "";
    } catch (e) {
        console.log(e);
        return e.message;
    }
};
