# randpass 🎲
![CI](https://github.com/realMNohgee/randpass/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Secure password and passphrase generator.** Zero dependencies, pure Python stdlib.

> Part of the **Trust & Reliability Layer for Agentic AI** — provenance, economics, truth, and interop tools for people building on agentic models.

## Why it exists
Strong credentials shouldn't require an internet connection or a password manager. randpass uses Python's `secrets` module for cryptographically secure random generation — xkcd-style passphrases, classic passwords, and entropy estimation in one tool.

## One tool, many domains
| Domain | What randpass does |
|---|---|
| **Security** | Generate strong passwords for services, APIs, tokens |
| **DevOps** | Script credential rotation in CI/CD pipelines |
| **User Onboarding** | Generate memorable passphrases for new users |
| **Agentic AI** | Create secure API keys, agent secrets, sandbox tokens |

## Install
```bash
git clone git@github.com:realMNohgee/randpass.git
cd randpass
python3 randpass.py --help
```

## Quick start
```bash
python3 randpass.py password --length 20
python3 randpass.py passphrase --words 5 --separator "."
python3 randpass.py entropy "myP@ssw0rd!"
python3 randpass.py password --count 3 --format json
```

## License
MIT — see [LICENSE](LICENSE).

---
🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)**
