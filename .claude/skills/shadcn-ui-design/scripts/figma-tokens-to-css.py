#!/usr/bin/env python3
"""
figma-tokens-to-css.py — regenerate the shadcn/ui CSS token block from a Figma export.

Reads the `shadcn/ui` collection from a lazyyysync `variables-export.json`, converts each
color (RGB 0–1 float) to shadcn's HSL channel format, and prints a globals.css `@layer base`
block with :root (light), .dark, and [data-theme="primary"] selectors.

Usage:
    python3 figma-tokens-to-css.py ../../../../variables-export.json
    python3 figma-tokens-to-css.py /abs/path/variables-export.json > ../assets/globals.css

Note: only emits tokens that differ from base for the dark/primary selectors is NOT done —
it emits the full set per mode so output matches assets/globals.css. Verify dark `--card`
(#171717) != `--background` (#0a0a0a) after regenerating.
"""
import json
import sys

# shadcn/ui semantic tokens in the order they should appear in :root
ORDER = [
    "background", "foreground", "card", "card-foreground", "popover",
    "popover-foreground", "primary", "primary-foreground", "secondary",
    "secondary-foreground", "muted", "muted-foreground", "accent",
    "accent-foreground", "destructive", "border", "input", "ring",
    "chart-1", "chart-2", "chart-3", "chart-4", "chart-5",
    "sidebar", "sidebar-foreground", "sidebar-primary", "sidebar-primary-foreground",
    "sidebar-accent", "sidebar-accent-foreground", "sidebar-border", "sidebar-ring",
    "background-color", "semantic-background", "semantic-border", "semantic-foreground",
]

# Figma mode name -> CSS selector
MODE_SELECTOR = {
    "light mode": ":root",
    "dark mode": ".dark",
    "primary": '[data-theme="primary"]',
}


def rgb_to_hsl_channels(r, g, b):
    """RGB floats (0–1) -> shadcn HSL channel string 'H S% L%'."""
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    H = round(h * 360, 1)
    S = round(s * 100, 1)
    L = round(l * 100, 1)
    fmt = lambda x: str(int(x)) if x == int(x) else str(x)
    return f"{fmt(H)} {fmt(S)}% {fmt(L)}%"


def value_for(var, mode_name):
    mv = var["valuesByMode"].get(mode_name)
    if mv is None:
        return None
    val = mv["value"]
    if not (isinstance(val, dict) and "r" in val):
        return None
    base = rgb_to_hsl_channels(val["r"], val["g"], val["b"])
    a = val.get("a", 1)
    return f"{base} / {round(a * 100)}%".replace(".0 ", " ") if a < 0.999 else base


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: figma-tokens-to-css.py <variables-export.json>")
    with open(sys.argv[1]) as f:
        data = json.load(f)

    shadcn = {v["name"]: v for v in data["variables"]
              if v["collectionName"] == "shadcn/ui"}

    print("@layer base {")
    for mode_name, selector in MODE_SELECTOR.items():
        print(f"  {selector} {{")
        for name in ORDER:
            var = shadcn.get(name)
            if not var:
                continue
            css = value_for(var, mode_name)
            if css:
                print(f"    --{name}: {css};")
        print("  }")
        print()
    print("}")


if __name__ == "__main__":
    main()
