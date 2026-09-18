# Public Release Checklist

Use this checklist before announcing a GptBC release publicly.

## Automated checks

- [ ] GitHub Actions `GptBC Validation` passes on `main`.
- [ ] `.agents/plugins/marketplace.json` resolves `./plugins/gptbc`.
- [ ] Root and installable plugin manifests report the same version.
- [ ] Python syntax checks and test suite pass.
- [ ] Plugin icon exists and is referenced by the installable manifest.
- [ ] Privacy, Terms, Security, License, and contribution documents are present.

## Installation check

Test from a clean Codex marketplace import:

```text
Source
https://github.com/scootieccc/GptBC

Git ref
main

Sparse paths
[leave blank]
```

Confirm that GptBC appears in the imported marketplace, installs successfully, shows the current icon, and exposes the expected skill prompts.

## GB Studio smoke test

Use a disposable GB Studio 4.3.x project and confirm:

1. `audit` runs without modifying project files.
2. `report` produces a build-readiness report.
3. official plugin search returns results.
4. resource catalog listing works.
5. resource inspection does not import files automatically.
6. an allowed test import records provenance.
7. overwrite protection and backups behave as documented.

## Public repository presentation

- [ ] README shows the current GptBC brand image.
- [ ] Repository description and topics match the current feature set.
- [ ] GitHub social preview uses the current GptBC artwork.
- [ ] Changelog contains the release changes.
- [ ] A version tag/release is created after final verification.

### GitHub social preview

GitHub's social-preview image is configured in the repository web UI. Upload the approved GptBC artwork under the repository's social-preview setting after the final brand image is selected.

## Third-party resource review

- [ ] Curated-source entries point to canonical upstream repositories where practical.
- [ ] Archived sources are not silently presented as current.
- [ ] License metadata is preserved.
- [ ] Unknown/NOASSERTION licenses remain blocked by default for automatic import.
- [ ] No third-party asset is represented as being relicensed by GptBC.

## Branding review

GptBC is an independent project. Before broad promotion, review release artwork and copy for third-party trademarks and avoid implying sponsorship, official status, or endorsement by Nintendo, GB Studio, OpenAI, or other rights holders.

## Release notes

Release notes should identify:

- GptBC version;
- supported/primary GB Studio version range;
- major new features;
- known limitations;
- security or compatibility changes;
- any migration steps;
- upstream resource-catalog changes that materially affect users.
