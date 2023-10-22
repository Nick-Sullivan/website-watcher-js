#!/usr/bin/node
let aws = require("@aws-sdk/client-ssm");
let dotenv = require("dotenv");
let fs = require("fs");

dotenv.config({ path: "../.env" });

let isLocal =
    (process.env.USE_LOCAL_SERVER ?? "false").toLowerCase() === "true";
let env = process.env.ENVIRONMENT.toLowerCase();
env = env.charAt(0).toUpperCase() + env.slice(1);

const prefix = `/WebsiteWatcherJs/${env}`;
const names = {};
names[`${prefix}/ApiGateway/Url`] = "NEXT_PUBLIC_API_GATEWAY_URL";
names[`${prefix}/Cognito/Region`] = "NEXT_PUBLIC_COGNITO_REGION";
names[`${prefix}/Cognito/ClientId`] = "NEXT_PUBLIC_COGNITO_CLIENT_ID";

const input = {
    Names: Object.keys(names),
    WithDecryption: true,
};
const client = new aws.SSMClient({ region: "ap-southeast-2" });
client.send(new aws.GetParametersCommand(input)).then((response) => {
    let content = "";
    for (let parameter of response.Parameters) {
        const name = names[parameter["Name"]];
        let value = parameter["Value"];
        if (name === "NEXT_PUBLIC_API_GATEWAY_URL" && isLocal) {
            value = "http://127.0.0.1:8000";
        }
        content += `${name}=${value}\r\n`;
    }
    fs.writeFileSync(".env", content);
});
