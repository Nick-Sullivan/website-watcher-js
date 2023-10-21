#!/usr/bin/node
let aws = require("@aws-sdk/client-ssm");
let dotenv = require("dotenv");
let fs = require("fs");

dotenv.config({ path: "../.env" });
let env = process.env.ENVIRONMENT.toLowerCase();
env = env.charAt(0).toUpperCase() + env.slice(1);

const prefix = `/WebsiteWatcherJs/${env}`;
const names = {};
names[`${prefix}/ApiGateway/Url`] = "API_GATEWAY_URL";
names[`${prefix}/AutomatedTester/Username`] = "AUTOMATED_TESTER_USERNAME";
names[`${prefix}/AutomatedTester/Password`] = "AUTOMATED_TESTER_PASSWORD";
names[`${prefix}/Cognito/ClientId`] = "COGNITO_CLIENT_ID";
names[`${prefix}/Cognito/UserPool/Id`] = "COGNITO_USER_POOL_ID";

const input = {
    Names: Object.keys(names),
    WithDecryption: true,
};
const client = new aws.SSMClient({ region: "ap-southeast-2" });
client.send(new aws.GetParametersCommand(input)).then((response) => {
    let content = "";
    for (let parameter of response.Parameters) {
        const name = names[parameter["Name"]];
        const value = parameter["Value"];
        content += `${name}=${value}\r\n`;
    }
    fs.writeFileSync(".env", content);
});
