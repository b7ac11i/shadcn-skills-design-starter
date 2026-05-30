---
name: shadcn-ui-design
description: "Generate and maintain shadcn/ui components for a Next.js 15 App Router project. Use when the user wants to create a component, build UI, generate a form, implement a design, add a page layout, or translate a Figma design to code. Handles Server vs Client Component decisions, file placement, react-hook-form + zod forms, dark mode, and Figma-to-code token mapping."
disable-model-invocation: false
---

# Design System

Generates and maintains UI for a **Next.js 15 App Router + shadcn/ui + Tailwind v4** project.

**Step 0 — Always read `references/DESIGN.md`** before writing code. It is the single source of truth for design tokens, component APIs, and patterns. For the full list of 1,806 Figma variables, consult `references/TOKENS.md` only when you need an exact value.

Skill layout:
- `references/DESIGN.md` · `references/TOKENS.md` — spec + full token export
- `assets/globals.css` — ready-to-paste token block for a Next.js app
- `scripts/figma-tokens-to-css.py` — regenerate the token block from `variables-export.json`

Then follow the workflow below for every request.

---

## Decision: Server vs Client Component

```
Does the component use any of these?
  ├── useState / useEffect / useRef / other React hooks  → "use client"
  ├── Event handlers (onClick, onChange, onSubmit)       → "use client"
  ├── Browser APIs (localStorage, window, document)      → "use client"
  ├── next-themes (useTheme)                             → "use client"
  ├── react-hook-form (useForm)                          → "use client"
  └── None of the above                                  → Server Component (no directive)
```

**Default: Server Component.** Only add `"use client"` when the checklist above applies.

---

## Workflow

### Phase 1 — Plan (before writing code)

1. What type of component is this?
   - **Display** → Card, list item, stat block → likely Server Component
   - **Interactive** → Form, dialog, dropdown, toggle → needs `"use client"`
   - **Page** → Route in `app/` → Server Component, compose from smaller components
   - **Layout** → Wraps children → usually Server Component

2. What data does it need? → Define TypeScript interface first, no `any`

3. Where does the file go?
   - Page: `app/(group)/page-name/page.tsx`
   - Reusable component: `components/[feature]/component-name.tsx`
   - Form schema: `lib/validations/name.ts`
   - Server action: `app/actions/name.ts`

4. Which shadcn components are needed? → Check `references/DESIGN.md` Component Catalog

### Phase 2 — Build

Write in this order:
1. Imports (shadcn → `@/components/ui/`, utilities → `@/lib/utils`, icons → `lucide-react`)
2. Zod schema (if form)
3. TypeScript interface
4. Component function
5. JSX — use semantic tokens only

### Phase 3 — Verify

Before finishing, confirm:
- [ ] TypeScript interface defined — no `any`
- [ ] `"use client"` added only if hooks/events present
- [ ] All colors use semantic tokens (`bg-primary`, not `bg-neutral-900`)
- [ ] No violet/purple classes anywhere
- [ ] `cn()` used for all conditional class merging
- [ ] `font-sans` / `font-mono` used — not hardcoded font names
- [ ] Icon-only buttons have `<span className="sr-only">`
- [ ] Forms use `react-hook-form + zod` with `<FormField>` / `<FormMessage>`
- [ ] Dialog/Sheet have `DialogTitle` / `SheetTitle`
- [ ] `suppressHydrationWarning` on `<html>` if dark mode is involved

---

## Patterns

### Display Component (Server)

```tsx
// components/[feature]/item-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface ItemCardProps {
  title: string
  description: string
  status: "active" | "inactive" | "pending"
  className?: string
}

export function ItemCard({ title, description, status, className }: ItemCardProps) {
  const variant = { active: "default", inactive: "secondary", pending: "outline" } as const

  return (
    <Card className={cn(className)}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">{title}</CardTitle>
          <Badge variant={variant[status]}>{status}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  )
}
```

### Form Component (Client)

```tsx
// components/[feature]/create-form.tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  name: z.string().min(1, "Required"),
  email: z.string().email("Invalid email"),
})

type FormValues = z.infer<typeof schema>

interface CreateFormProps {
  onSubmit: (values: FormValues) => Promise<void>
}

export function CreateForm({ onSubmit }: CreateFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: "", email: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl><Input type="email" {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving..." : "Save"}
        </Button>
      </form>
    </Form>
  )
}
```

### Dialog with Form (Client)

```tsx
"use client"
import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { CreateForm } from "./create-form"

export function CreateDialog() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>New Item</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create Item</DialogTitle>
        </DialogHeader>
        <CreateForm
          onSubmit={async (values) => {
            // call server action
            setOpen(false)
          }}
        />
      </DialogContent>
    </Dialog>
  )
}
```

### Page (Server Component)

```tsx
// app/(dashboard)/items/page.tsx
import { ItemCard } from "@/components/items/item-card"
import { CreateDialog } from "@/components/items/create-dialog"

export default async function ItemsPage() {
  // fetch data server-side
  const items = await getItems()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Items</h1>
          <p className="text-sm text-muted-foreground">Manage your items</p>
        </div>
        <CreateDialog />
      </div>

      {items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <p className="text-sm text-muted-foreground">No items yet.</p>
          <CreateDialog />
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => (
            <ItemCard key={item.id} {...item} />
          ))}
        </div>
      )}
    </div>
  )
}
```

### Loading State

```tsx
// app/(dashboard)/items/loading.tsx  ← Next.js Suspense
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

export default function Loading() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-5 w-1/2" />
            <Skeleton className="h-4 w-3/4" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-16 w-full" />
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

### Server Action

```tsx
// app/actions/items.ts
"use server"
import { z } from "zod"
import { revalidatePath } from "next/cache"

const createSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
})

export async function createItem(data: z.infer<typeof createSchema>) {
  const result = createSchema.safeParse(data)
  if (!result.success) return { error: result.error.flatten().fieldErrors }
  // await db.insert(...)
  revalidatePath("/items")
  return { success: true }
}
```

---

## Figma to Code

1. **Colors** — find the Figma alias (e.g. `tw/neutral/900`) → map to CSS token → use Tailwind class
2. **Spacing** — Figma variable name maps directly (`gap-4` = 16px → `gap-4`, `p-14` = 56px → `p-14`)
3. **Radius** — `rounded-md`=6px, `rounded-xl`=12px, `rounded-3xl`=24px, `rounded-full`=9999px
4. **Typography** — `size/sm`=14px → `text-sm`, `weight/semibold`=600 → `font-semibold`, `leading/5`=20px → `leading-5`
5. **Font** — `family/sans` = Inter → `font-sans`, `family/mono` = Geist Mono → `font-mono`

| Figma Alias | Tailwind |
|---|---|
| `tw/neutral/900` (primary light) | `bg-primary` |
| `tw/neutral/100` (muted/secondary) | `bg-muted` / `bg-secondary` |
| `tw/neutral/500` | `text-muted-foreground` |
| `tw/red/600` (destructive light) | `bg-destructive` |
| `tw/neutral/200` (border light) | `border-border` |

---

## Quick Install

```bash
pnpm dlx shadcn@latest add button card input label form \
  select dialog sheet badge alert separator tabs \
  table avatar skeleton tooltip dropdown-menu \
  checkbox radio-group switch textarea \
  breadcrumb pagination progress
```
