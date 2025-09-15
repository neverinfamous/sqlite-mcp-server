# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2025.x  | :white_check_mark: |
| < 2025  | :x:                |

## Reporting a Vulnerability

We take the security of the SQLite MCP Server seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to writenotenow@gmail.com with the following information:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

## Response Timeline

We will acknowledge receipt of your vulnerability report within 48 hours and will send a more detailed response within 72 hours indicating the next steps in handling your report.

After the initial reply to your report, we will keep you informed of the progress towards a fix and may ask for additional information or guidance.

## Security Best Practices

When using the SQLite MCP Server:

1. **Database Security**: Ensure your SQLite database files have appropriate file permissions
2. **Input Validation**: Always validate and sanitize input data before database operations
3. **Connection Security**: Use secure connections when accessing databases over networks
4. **Access Control**: Implement proper authentication and authorization mechanisms
5. **Regular Updates**: Keep the MCP server and its dependencies up to date

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all releases still under support
4. Release new versions as quickly as possible
5. Credit the reporter (unless they prefer to remain anonymous)

Thank you for helping keep the SQLite MCP Server and its users safe!
