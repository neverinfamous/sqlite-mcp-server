// ESLint configuration for SQLite MCP Server JavaScript utilities
// This helps address CodeQL security warnings
// Using .eslintrc.js format for maximum compatibility

module.exports = {
  env: {
    node: true,
    es2022: true
  },
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: "commonjs"
  },
  rules: {
    // Security-related rules to address CodeQL warnings
    "no-eval": "error",
    "no-implied-eval": "error",
    "no-new-func": "error",
    "no-unsafe-finally": "error",
    "no-unsafe-negation": "error",
    
    // Prevent potential injection vulnerabilities
    "no-template-curly-in-string": "error",
    
    // Best practices
    "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "no-console": "warn",
    "prefer-const": "error",
    "no-var": "error",
    
    // Error handling
    "no-empty": "error",
    "no-throw-literal": "error",
    
    // Code quality
    "eqeqeq": "error",
    "no-unreachable": "error",
    "valid-typeof": "error"
  }
};