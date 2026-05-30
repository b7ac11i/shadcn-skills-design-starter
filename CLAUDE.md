# design-system — Claude Code Package

A portable **shadcn/ui + Tailwind CSS v4 + Next.js 15** design-system package. All UI rules,
component patterns, and design tokens are sourced from a **Figma export** (`variables-export.json`).
This folder is the design-system *package* — drop it into a Next.js project to drive consistent UI.

<!-- This is not a Next.js app root. It carries the skill + token spec to consume elsewhere. -->

## Package contents

```
.claude/skills/shadcn-ui-design/
├── SKILL.md                       # component-generation workflow (auto-loads when relevant)
├── references/
│   ├── DESIGN.md                  # tokens, component APIs, layout & form patterns — the spec
│   └── TOKENS.md                  # full Figma export: 1,806 variables across 17 collections
├── assets/
│   └── globals.css                # ready-to-paste token block (light / dark / primary)
└── scripts/
    └── figma-tokens-to-css.py     # regenerate the token block from variables-export.json
```

## Read first

1. **`.claude/skills/shadcn-ui-design/SKILL.md`** — the workflow (Server/Client decisions, patterns, verify checklist). Auto-discovered; full instructions load only when needed.
2. **`.claude/skills/shadcn-ui-design/references/DESIGN.md`** — single source of truth for tokens, component usage, forms, layout.
3. **`.claude/skills/shadcn-ui-design/references/TOKENS.md`** — consult only for an exact variable value.

## Stack

Next.js 15 (App Router) · React 19 · TypeScript (strict) · Tailwind CSS v4 · shadcn/ui (new-york) · next-themes · react-hook-form + zod · lucide-react.

## Using this package in a Next.js project

1. Copy `.claude/skills/shadcn-ui-design/` into the target app's `.claude/skills/`.
2. `npx shadcn@latest init` — choose **cssVariables: true**, **baseColor: neutral**.
3. Copy `assets/globals.css` into `app/globals.css` (light / `.dark` / `[data-theme="primary"]`).
4. Wrap `app/layout.tsx` with the `ThemeProvider` from `references/DESIGN.md` (Dark Mode section).
5. Generate UI via the skill — invoke `/shadcn-ui-design` or let it auto-trigger.

## Core conventions (always)

- **Server Components by default** — add `"use client"` only for hooks / events / browser APIs.
- **Semantic tokens only** — `bg-primary`, `text-muted-foreground`. Never raw colors (`bg-neutral-900`, `bg-blue-500`) and **never violet/purple** — the primary palette is neutral.
- **`cn()`** from `@/lib/utils` for every conditional class. No template-string class concatenation.
- **`gap-*` not `space-x-*`/`space-y-*`. `size-10` not `w-10 h-10`.**
- **Forms** — always `react-hook-form + zod` together, with `<FormField>` / `<FormMessage>`.
- **Edit `app/globals.css`** for token changes — never create a new CSS file.
- **CLI for components** — `npx shadcn@latest add <name>`. Never hand-write `components/ui/*`.
- **Fonts** — `font-sans` (Inter), `font-mono` (Geist Mono). Never hardcode font names.

## Figma token workflow (static export)

Tokens come from a **static export**, not live Figma.

- **Source of truth:** `../variables-export.json` (lazyyysync export — 17 collections, 1,806 variables).
- **In-package snapshot:** `references/TOKENS.md` documents every variable; `references/DESIGN.md` maps them to CSS variables.
- **Theme modes (3):** the `shadcn/ui` collection drives `:root` (light) · `.dark` · `[data-theme="primary"]`.
- **To update tokens:**
  1. Re-export `variables-export.json` from Figma (lazyyysync plugin).
  2. Run `python3 scripts/figma-tokens-to-css.py ../variables-export.json > assets/globals.css` (RGB→HSL).
  3. Sync the same block into `references/DESIGN.md` and the `references/TOKENS.md` snapshot.
  4. Verify dark mode: `--card` (#171717) ≠ `--background` (#0a0a0a) — they differ by one shade.

See **`references/DESIGN.md` → "Figma Bridge"** for the alias → CSS-variable → Tailwind mapping table.

## Commands

```bash
npx shadcn@latest init                 # scaffold tokens + config (cssVariables, neutral)
npx shadcn@latest add <component>      # install a component
npx shadcn@latest add <a> <b> <c>      # install several at once
npx shadcn@latest search <query>       # find a component

npm run dev                            # Next.js dev server (in the consuming app)
npm run build
npm run lint
```
