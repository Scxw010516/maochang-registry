module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],

  parserOptions: {
    parser: "@typescript-eslint/parser",
  },

  rules: {},

  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/typescript",
  ],
};
