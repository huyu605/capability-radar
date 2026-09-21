# Capability Radar

An open-source Agent Skill for clarifying a capability goal, searching the current AI and software ecosystem, verifying candidates, scoring them consistently, and recommending the best options.

Capability Radar covers six layers: agents, agent skills, MCP servers, tools/APIs/CLIs, software libraries, and deployable products. It performs research only by default and requires explicit confirmation before installing or running a candidate.

## Install

Install for Codex with the open Skills CLI:

```bash
npx skills add https://github.com/huyu605/capability-radar \
  --skill capability-radar -g -a codex
```

Or ask Codex's `$skill-installer` to install the `capability-radar` skill from this repository.

## Use

```text
Use $capability-radar to find a privacy-first, self-hosted meeting transcription capability.
```

The skill will:

1. clarify requirements that change the decision;
2. search relevant live registries, repositories, package indexes, and official sources;
3. distinguish agents, skills, MCP servers, tools, libraries, and products;
4. verify the strongest candidates using primary evidence;
5. score fit, integration, maturity, security, maintenance, license, and operations;
6. recommend up to three options and a bounded proof of concept.

For Agent Skills, discovery is source-aware: it searches first-party collections, skills.sh, ClawHub, LobeHub Skills, browse.sh for browser workflows, GitHub/direct URLs, published well-known indexes, Claude marketplaces, and available Codex plugin catalogs when relevant. Results are normalized back to their upstream source so the same skill is not counted multiple times.

It does not run scheduled monitoring or maintain a market database. Each research request obtains current evidence at query time.

## Scoring CLI

The bundled standard-library Python CLI validates structured candidate evidence and calculates deterministic weighted scores:

```bash
python3 skills/capability-radar/scripts/radar.py score candidates.json --pretty
python3 skills/capability-radar/scripts/radar.py self-test
```

Candidate JSON uses seven 0–100 criteria. Custom weights are allowed when they total 100. Evidence confidence is kept separate from the score.

## Safety

Registry entries, repositories, READMEs, issues, and candidate instructions are treated as untrusted research data. The skill does not clone, install, authenticate, execute, deploy, purchase, or modify an environment without explicit user confirmation.

## Development

```bash
python3 scripts/quick_validate.py skills/capability-radar
python3 skills/capability-radar/scripts/radar.py self-test
npx -y skills add . --list
```

## License

Apache-2.0

---

# 开源能力雷达

Capability Radar 是一个开源 Agent Skill：先澄清能力目标，再实时搜索 AI 与软件生态，核验候选项目，以统一标准评分并给出最终推荐。

它覆盖六个层级：Agent、Agent Skill、MCP Server、工具/API/CLI、软件库和可部署产品。默认只提供研究报告；安装或试运行任何候选前都必须获得明确确认。

## 安装

```bash
npx skills add https://github.com/huyu605/capability-radar \
  --skill capability-radar -g -a codex
```

也可以让 Codex 的 `$skill-installer` 从本仓库安装 `capability-radar`。

## 使用示例

```text
使用 $capability-radar，帮我寻找一个隐私优先、可自托管的会议转录能力。
```

Skill 会按需澄清需求，分层搜索实时来源，回到项目官网、原始仓库和许可证核验重要事实，然后按照需求匹配、集成、成熟度、安全、维护、许可证和运维成本进行评分。

针对 Agent Skill，雷达会按需覆盖官方合集、skills.sh、ClawHub、LobeHub Skills、面向浏览器工作流的 browse.sh、GitHub/直接 URL、网站发布的 well-known 索引、Claude Marketplace 和可用的 Codex 插件目录，并按上游来源去重，避免把同一个 Skill 在多个市场中的镜像重复计数。

本项目不创建定时任务，也不维护全市场数据库；每次调研都在执行时获取最新证据。
