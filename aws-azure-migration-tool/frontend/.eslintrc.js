module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential', // Base rules for Vue 3
    'eslint:recommended', // Basic ESLint recommended rules
  ],
  parserOptions: {
    parser: '@babel/eslint-parser', // To parse modern JavaScript features
    requireConfigFile: false, // Added to prevent issues if babel.config.js is not in the same dir or project root
  },
  rules: {
    // Add any custom rules or overrides here
    // e.g., 'vue/multi-word-component-names': 'off' if you don't want to enforce multi-word component names
    'vue/multi-word-component-names': 'off',
  },
};
