# Live source map

Use structured and primary sources first. Aggregators discover candidates; original repositories and official documentation establish facts.

| Layer | Discovery sources | Primary verification |
| --- | --- | --- |
| Agents | LobeHub Agent Market, framework directories, GitHub topics and search | Agent source repository, provider documentation, model/tool configuration |
| Agent skills | skills.sh, `npx skills find`, Codex Plugins, GitHub search | `SKILL.md`, bundled scripts/references, source history, security reports |
| MCP servers | Official/community MCP registries, LobeHub MCP, GitHub | Server repository, tool schemas, transport/auth documentation, releases |
| Tools/APIs/CLIs | GitHub, Awesome lists, package registries, vendor directories | Official docs, source, API/CLI reference, release and security history |
| Libraries | npm, PyPI, crates.io, Maven Central, pkg.go.dev, GitHub | Package metadata, source, maintainers, releases, CI, advisories, license |
| Products | GitHub topics, awesome-selfhosted, Docker Hub, product directories | Official site/docs, deployment source, container provenance, license, releases |

## Query strategy

Build queries from:

`outcome + object + platform + deployment + constraint + open-source synonym`

Try synonyms such as `self-hosted`, `FOSS`, `source available`, `library`, `SDK`, `CLI`, `MCP server`, `agent skill`, and the domain's established technical terms. Use negative terms to remove irrelevant industries or proprietary-only offerings.

## Evidence priority

1. License text, source repository, official documentation, signed releases, security advisories.
2. Package registries, foundation registries, vendor-maintained catalogs.
3. Independent benchmarks and reproducible technical reviews.
4. Community directories, blog posts, discussions, and popularity metrics.

Record an as-of date. Prefer evidence updated within the decision horizon. When sources conflict, report the conflict and prefer the primary source for project-owned facts.
