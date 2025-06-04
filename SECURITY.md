# Security Policy

This policy outlines pyufunc's security commitments and practices for users across different licensing and deployment models.

To learn more about pyufunc's security service level agreements (SLAs) and processes, please [contact us](mailto:luoxiangyong01@gmail.com).

## Security is everyone's responsibility

It is important to remember that the security of the package is the result of the overall security of the framework foundation, the package itself, all python dependencies and your code. As such, it is your responsibility to follow a few important best practices:

- **Keep up-to-date with the latest package release**.
- **Evaluate your dependencies**. While Python provides many reusable packages, it is your responsibility to choose trusted 3rd-party libraries. If you use outdated libraries affected by known vulnerabilities or rely on poorly maintained code, your application security could be in jeopardy.
- **Adopt secure coding practices**. The first line of defense for your application is your own code. It is highly recommended to adopt secure software development best practices and perform security testing.

## Isolation for untrusted content

A security issue exists whenever you receive code from an untrusted source (e.g. a remote server) and execute it locally.

## Security recommendations

> - Only load secure content
> - Enable context isolation in all renderers
> - Use latest version of the package
> - Check which fuses you can change
> - Do not expose personal API keys to untrusted web content

## Reporting a Vulnerability

For details on how to report security vulnerabilities, please use the luoxiangyong01@gmail.com. The developer team will coordinate the fix and disclosure.

The developer team and community take security bugs in the package seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions. The team will send a response indicating the next steps in handling your report. After the initial reply to your report, the security team will keep you informed of the progress towards a fix and full announcement, and may ask for additional information or guidance.
