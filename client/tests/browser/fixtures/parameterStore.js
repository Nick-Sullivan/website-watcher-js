const aws = require("@aws-sdk/client-ssm");

export const ParameterStoreFixture = {
    parameterStore: async ({}, use) => {
        const client = new aws.SSMClient({ region: "ap-southeast-2" });
        const parameterStore = new ParameterStore(client);
        await parameterStore.load();
        await use(parameterStore);
    },
};

class ParameterStore {
    constructor(awsClient) {
        this.awsClient = awsClient;
        this.parameters = {};
        this.prefix = this.getPrefix();
    }

    getPrefix() {
        let env = process.env.ENVIRONMENT.toLowerCase();
        env = env.charAt(0).toUpperCase() + env.slice(1);
        return `/WebsiteWatcherJs/${env}`;
    }

    async load() {
        const names = {};
        names[`${this.prefix}/AutomatedTester/Username`] =
            "AUTOMATED_TESTER_USERNAME";
        names[`${this.prefix}/AutomatedTester/Password`] =
            "AUTOMATED_TESTER_PASSWORD";
        const input = {
            Names: Object.keys(names),
            WithDecryption: true,
        };
        const response = await this.awsClient.send(
            new aws.GetParametersCommand(input)
        );
        for (let parameter of response.Parameters) {
            const name = names[parameter["Name"]];
            const value = parameter["Value"];
            this.parameters[name] = value;
        }
    }

    get automatedTesterUsername() {
        return this.parameters["AUTOMATED_TESTER_USERNAME"];
    }

    get automatedTesterPassword() {
        return this.parameters["AUTOMATED_TESTER_PASSWORD"];
    }
}
