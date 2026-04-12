# KEEL License FAQ

## What license is KEEL under?

KEEL is licensed under AGPL-3.0. See [LICENSE](LICENSE) for the full text.

## Does AGPL apply to my project?

No. KEEL is a **template** — it generates files (CI pipelines, pre-commit configs, CLI, documentation structure) that become part of YOUR project. The generated output is yours to license however you choose. AGPL applies to KEEL itself (the template engine and its source), not to the projects you create with it.

This is analogous to how a code generator's license doesn't infect generated code. Your `copier.yml` answers determine YOUR project's license.

## Can I use KEEL in a commercial project?

Yes. Generate your project with `copier copy`, choose your own license (MIT, Apache-2.0, or AGPL-3.0), and the generated project is yours. KEEL's AGPL applies if you modify and redistribute KEEL itself.

## What if I modify KEEL?

If you modify KEEL's templates and distribute those modifications (including as a network service), AGPL requires you to share your modifications under AGPL. This protects the KEEL community from proprietary forks.

## Can I get a commercial license?

Yes. Contact the maintainers to negotiate a commercial license if AGPL doesn't work for your organization. Dual licensing (AGPL + commercial) is available.

## Why AGPL instead of MIT?

AGPL ensures that improvements to KEEL's engineering process templates benefit everyone. If someone builds a better tier system or better guardrails on top of KEEL, those improvements come back to the community. MIT would allow proprietary forks that fragment the ecosystem.
