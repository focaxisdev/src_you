# Sensitive data policy

Status: normative for `src_you` v0.1.0.

## Default

Personal state is private by default. Public framework files must contain only
fictional, synthetic, or fully de-identified examples.

## Absolute exclusions

Never persist these values in L1, L2, checkpoint manifests, changelogs, issue
reports, examples, or prompt transcripts:

- passwords, one-time codes, recovery codes, and security answers;
- API keys, access tokens, OAuth credentials, session cookies, and private keys;
- full card numbers, CVVs, banking credentials, or signing keys;
- raw secrets embedded in URLs or environment dumps.

If encountered, stop ingestion, redact output, and direct the person to rotate
the secret when exposure may have occurred.

## Sensitive personal domains

Health, family, finance, precise location, legal, employment, and private project
details may be durable, but require:

- clear future value;
- minimum necessary representation;
- an appropriate protected store;
- strict routing so unrelated tasks do not retrieve them;
- a safe pointer instead of raw source material when possible.

## Evidence versus state

Raw files, chats, emails, medical documents, and external pages are evidence.
They are not automatically canonical knowledge. Extract only confirmed minimum
state and preserve provenance without copying unnecessary sensitive text.

## Release gate

Before public release, perform both:

1. pattern scanning for secrets and identifiers; and
2. semantic review for personal stories, unique combinations, private URLs,
   IDs, hashes, or copied conversation language.

Test 7 covers this policy. The baseline scanner is
[`../scripts/scan_sensitive_placeholders.py`](../scripts/scan_sensitive_placeholders.py).
