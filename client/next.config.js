/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "export",
    images: {
        unoptimized: true,
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
