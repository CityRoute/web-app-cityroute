module.exports = {
  preset: "@vue/cli-plugin-unit-jest",
  setupFiles: ["./tests/unit/setup.js"],
  collectCoverage: true,
  collectCoverageFrom: [
    "src/**/*.{js,vue}",
    "!src/main.js", // No need to cover bootstrap file
  ],
};
