// ESLint configuration for SQLite MCP Server JavaScript utilities
// This helps address CodeQL security warnings

module.exports = [
  {
    files: ["*.js", "utils/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "commonjs",
      globals: {
        console: "readonly",
        process: "readonly",
        Buffer: "readonly",
        __dirname: "readonly",
        __filename: "readonly",
        module: "readonly",
        require: "readonly",
        exports: "readonly"
      }
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
      
      // Error handling - use no-empty instead of no-empty-catch for ESLint 8.x
      "no-empty": "error",
      "no-throw-literal": "error",
      
      // Code quality
      "eqeqeq": "error",
      "no-unreachable": "error",
      "valid-typeof": "error"
    }
  }
];
