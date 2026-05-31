# Contributing

Contributions are welcome, especially around marketplace importers, sample data, planning rules, documentation, and tests.

## Good First Contributions

- Add a normalized sample export for a marketplace.
- Improve box validation examples.
- Add tests for stockout and production shortfall scenarios.
- Improve documentation for sellers who are not developers.
- Add a marketplace adapter behind a clean normalization boundary.

## Data Safety

Do not commit:

- seller API tokens;
- spreadsheet IDs;
- service account files;
- real customer data;
- real prices or margin data;
- private marketplace reports;
- private Telegram, email, or CRM exports.

Use anonymized sample data instead.

## Adapter Rule

Adapters should translate marketplace-specific exports into generic `DemandSignal` rows. The planning core should stay marketplace-agnostic.

