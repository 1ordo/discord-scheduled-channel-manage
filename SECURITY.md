# Security Policy

## Supported Versions

We actively support the following versions of Discord Scheduled Channel Manager Bot:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Create a Public Issue

Please **do not** create a public GitHub issue for security vulnerabilities. This could put users at risk.

### 2. Contact Us Privately

Send an email to [security@yourdomain.com] with the following information:

- A detailed description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any suggested fixes or mitigations

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 1 week
- **Fix Development**: Timeline depends on severity
- **Public Disclosure**: After fix is released and users have time to update

### 4. Responsible Disclosure

We follow responsible disclosure practices:

1. We will acknowledge your report within 48 hours
2. We will provide regular updates on our progress
3. We will notify you when the vulnerability is fixed
4. We will publicly credit you for the discovery (unless you prefer to remain anonymous)

## Security Best Practices for Users

### Bot Token Security

- **Never** commit your bot token to version control
- Store your bot token in the `configuration.env` file (which should be in `.gitignore`)
- Regenerate your bot token if you suspect it has been compromised
- Use environment variables in production deployments

### Server Permissions

- Grant the bot only the minimum permissions required
- Regularly review bot permissions in your Discord server
- Use role-based permissions to limit access to sensitive channels

### Database Security

- The bot uses SQLite by default, which stores data locally
- Ensure proper file permissions on your server
- Consider regular backups of your database file
- In production, consider using a more robust database system

### Updates

- Keep your bot updated to the latest version
- Subscribe to security notifications for dependencies
- Regularly update Python and system packages

## Common Security Considerations

### Input Validation

The bot includes input validation for:
- Time formats
- Channel names
- Role assignments
- Database queries

### Error Handling

- Errors are logged but sensitive information is not exposed
- Database errors are handled gracefully
- Network errors are properly caught and logged

### Logging

- Logs contain operational information
- Sensitive information (like tokens) is never logged
- Log files should be secured in production environments

## Dependencies

We regularly monitor our dependencies for security vulnerabilities:

- `discord.py` - Official Discord API library
- `python-dotenv` - Environment variable loading
- `pytz` - Timezone handling

Keep these dependencies updated by running:
```bash
pip install -r requirements.txt --upgrade
```

## Contact Information

For security-related questions or concerns:

- Security Email: [security@yourdomain.com]
- General Support: [GitHub Issues](https://github.com/yourusername/discord-scheduled-channel-manager/issues)
- Discord Server: [Your Discord Server Link]

Thank you for helping keep Discord Scheduled Channel Manager Bot secure!
