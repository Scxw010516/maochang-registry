module.exports = {
  root: true,

  env: {
    node: true,
    es2022: true,
  },

  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],

  parserOptions: {
    parser: "@typescript-eslint/parser",
  },

  rules: {
    // 关闭未使用的变量检查
    "no-unused-vars": "off",
  },

  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/typescript",
  ],
};
