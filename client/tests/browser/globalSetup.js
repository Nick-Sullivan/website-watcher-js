const dotenv = require("dotenv");

export const globalSetup = async (config) => {
    dotenv.config({ path: ".env" });
};

module.exports = globalSetup;
