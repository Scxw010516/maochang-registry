module.exports = {
  root: true,
  globals: {
    defineProps: "readonly",
    withDefaults: "readonly",
  },
  env: {
    node: true,
    // es2022: true,
  },

  parserOptions: {
    parser: "@typescript-eslint/parser",
  },

  rules: {
    // 关闭组件名称必须是多个单词的形式的检查
    "vue/multi-word-component-names": "off",
    // 关闭未使用的变量检查
    "no-unused-vars": "off",
  },

  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    // "@vue/typescript",
  ],
};
