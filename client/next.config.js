/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "export",
    trailingSlash: true,
    images: {
        unoptimized: true,
        domains: ["s3.amazonaws.com"],
    },
    webpack: (config, { isServer, nextRuntime, webpack }) => {
        // Avoid AWS SDK issue "Critical dependency: the request of a dependency is an expression"
        if (isServer && nextRuntime === "nodejs")
            config.plugins.push(
                new webpack.IgnorePlugin({ resourceRegExp: /^aws-crt$/ })
            );
        return config;
    },
};

module.exports = nextConfig;
