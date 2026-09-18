# Security Policy

## Reporting a security issue

Please do not publish exploit details, secrets, access tokens, or private project data in a public issue.

For ordinary bugs that do not expose sensitive data, use the repository's bug-report issue template.

For a potential security issue, contact the repository owner privately through an appropriate GitHub contact method when available and include only the minimum information needed to reproduce the problem.

## Scope

Security-sensitive areas include:

- ZIP extraction and path traversal
- plugin installation and replacement behavior
- project backup handling
- execution of local tools such as Python or Git
- resource downloads and repository synchronization
- malformed or hostile plugin/resource metadata
- accidental overwrite of GB Studio project files
- secret/token leakage into logs or generated reports

## Design principles

GptBC aims to:

- keep project changes non-destructive by default
- back up plugin directories before replacement
- validate archive extraction paths
- avoid bundling or silently executing third-party plugin code
- keep resource caches separate from project assets until explicitly used
- surface compatibility uncertainty instead of silently forcing installation

## Supported versions

Security fixes are expected to target the latest version on the `main` branch first. Stable release/version policy will become stricter as GptBC matures.
