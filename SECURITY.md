# Security Policy

## Supported Versions

The following table shows which versions of **MoleQL** and Python are currently
supported for security updates and bug fixes.

| MoleQL Version | Python Versions | Supported            |
|----------------|-----------------|----------------------|
| 0.x.x (latest) | ≥ 3.12          | ✅ Actively supported |
| < 0.x.x        | < 3.12          | ❌ Unsupported        |

MoleQL officially supports **Python 3.12 and newer**.
Security fixes are only applied to the latest MoleQL release that runs on
actively supported Python versions.

Older Python releases (≤ 3.11) or MoleQL versions are **not maintained** and
may contain unpatched vulnerabilities.

---

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** create a public
GitHub issue.
Instead, report it privately to the maintainers via email:

**📧 pedro@subvertic.com**

Please include:

1. A clear description of the issue and its potential impact.
2. Steps to reproduce, if applicable.
3. Any known workarounds or mitigations.

We’ll acknowledge receipt within **48 hours** and provide a status update
within **5 business days**, including a proposed remediation timeline.

---

## Responsible Disclosure

We kindly ask you to:

- Avoid publicly disclosing the vulnerability before a fix is released.
- Avoid exploiting or sharing the vulnerability beyond private reporting.
- Provide sufficient detail so the issue can be reproduced and verified.

Once the issue is fixed, a new release will be published, and the changelog will
include a reference like:

> *Security: Fixed unsafe pattern parsing in `FilterHandler`
> (reported by <researcher_name>)*

---

## Coordinated Disclosure with GitHub

This repository supports GitHub’s
**[Coordinated Disclosure](https://docs.github.com/en/code-security/security-advisories/about-coordinated-disclosure)**
process.
You may also report vulnerabilities through the “**Report a vulnerability**”
link in the GitHub repository’s **Security** tab.

---

## Encryption (Optional)

If you prefer to send encrypted reports, you can request a temporary GPG public
key from the maintainer via email before sharing sensitive data.

---

## Security Best Practices for Contributors

When contributing code, please:

- Validate and sanitize all user inputs.
- Avoid direct use of `eval`, `exec`, or unsafe regex patterns.
- Use parameterized queries or built-in MongoDB operators safely.
- Follow Python’s secure coding guidelines (see PEP 672).
- Run security checks before opening a PR:

  ```bash
  uv run pre-commit run --all-files
  uv run pytest
