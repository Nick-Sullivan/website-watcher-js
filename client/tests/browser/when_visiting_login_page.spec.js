const { test, expect } = require("@playwright/test");
let dotenv = require("dotenv");
let aws = require("@aws-sdk/client-ssm");

const loadParameterStoreVariables = async () => {
    let env = process.env.ENVIRONMENT.toLowerCase();
    env = env.charAt(0).toUpperCase() + env.slice(1);
    const prefix = `/WebsiteWatcherJs/${env}`;

    const names = {};
    names[`${prefix}/AutomatedTester/Username`] = "AUTOMATED_TESTER_USERNAME";
    names[`${prefix}/AutomatedTester/Password`] = "AUTOMATED_TESTER_PASSWORD";
    const input = {
        Names: Object.keys(names),
        WithDecryption: true,
    };
    const client = new aws.SSMClient({ region: "ap-southeast-2" });
    client.send(new aws.GetParametersCommand(input)).then((response) => {
        for (let parameter of response.Parameters) {
            const name = names[parameter["Name"]];
            let value = parameter["Value"];
            process.env[name] = value;
        }
    });
};

test.beforeAll(async ({}) => {
    let isCicd = (process.env.IS_CICD ?? "false").toLowerCase() === "true";
    if (!isCicd) {
        dotenv.config({ path: ".env" });
    }
    await loadParameterStoreVariables();
});

test.beforeEach(async ({ page }) => {
    const env = process.env.ENVIRONMENT.toLowerCase();
    await page.goto(
        `http://websitewatcherjs-${env}.com.s3-website-ap-southeast-2.amazonaws.com/login/`
    );
});

test("page should have correct title", async ({ page }) => {
    await expect(page).toHaveTitle("Create Next App");
});

test("automated tester should be able to log in", async ({ page }) => {
    const userLogin = page.getByPlaceholder("name@flowbite.com");
    await userLogin.fill(process.env["AUTOMATED_TESTER_USERNAME"]);

    const passwordLogin = page.getByLabel("Your password");
    await passwordLogin.fill(process.env["AUTOMATED_TESTER_PASSWORD"]);

    const submitButton = page.getByRole("button", { name: "Submit" });
    await submitButton.click();

    await page.waitForURL("**/watchers/");
});

test("unauthorized users should get a warning message", async ({ page }) => {
    const userLogin = page.getByPlaceholder("name@flowbite.com");
    await userLogin.fill("");
    await userLogin.type("fake@fake.com");

    const passwordLogin = page.getByLabel("Your password");
    await passwordLogin.fill("");
    await passwordLogin.type("password");

    const submitButton = page.getByRole("button", { name: "Submit" });
    await submitButton.click();

    const notification = page.getByRole("status");
    await expect(notification).toBeVisible();
});
