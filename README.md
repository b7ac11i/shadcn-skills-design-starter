# 🎨 shadcn/ui + Tailwind CSS v4 + Next.js 15 Design System Starter

โปรเจกต์เริ่มต้น (Starter Template) สำหรับการพัฒนาเว็บแอปพลิเคชันด้วย **Next.js 15 (App Router)** ร่วมกับ **Tailwind CSS v4** และชุดระบบการออกแบบ **shadcn/ui** ที่ทำงานประสานร่วมกับโทเค็นดีไซน์ (Design Tokens) ที่ถูกส่งออกมาจาก Figma (`variables-export.json`) โดยตรง

---

## ⚡ คุณสมบัติหลัก (Key Features)

* **Next.js 15 & React 19** — สถาปัตยกรรมแบบ App Router ล่าสุด ปลอดภัย รวดเร็ว และรองรับ Server Components เป็นหลัก
* **Tailwind CSS v4** — การตั้งค่าคอนฟิกด้วย CSS-first รูปแบบใหม่ ทำงานร่วมกับ `@theme` ได้สะดวกรวดเร็ว
* **Figma Bridge & Tokens** — ระบบคัดลอกและแมปโทเค็นตัวแปรดีไซน์จำนวน 35 ตัวแปร (Light / Dark / Primary) ที่ผ่านการแปลงรูปแบบสี RGB เป็น HSL เพื่อการแสดงผลที่ลื่นไหล
* **3 Theme Modes Support** — รองรับสไตล์ถึง 3 โหมด: Light Mode ☀️, Dark Mode 🌙 และ Primary Theme (ธีมเฉพาะตัวโปรเจกต์) 🔵
* **Next-Themes Integration** — ควบคุมระบบ Dark Mode ด้วย `next-themes` หุ้มด้วยโครงสร้าง `ThemeProvider` ทั่วทั้งแอปพลิเคชัน
* **TypeScript Strict Mode** — กำหนดการพิมพ์ข้อมูลอย่างเข้มงวด ป้องกันข้อผิดพลาดล่วงหน้า
* **Modern Typography & Spacing** — ฟอนต์ระบบ Inter (Sans) และ Geist Mono (Mono) กำหนดระยะห่างระยะช่องไฟ (gap) อิงจากระบบ Base Unit 4px (Figma Space Variables)

---

## 📁 โครงสร้างโปรเจกต์ (Project Directory Structure)

```
├── .claude/
│   └── skills/
│       └── shadcn-ui-design/
│           ├── SKILL.md                 # Component-generation workflow (ระบบแนะนำคำสั่ง)
│           ├── assets/
│           │   └── globals.css          # ไฟล์โทเค็นตั้งต้นที่แปลงมาจาก Figma
│           ├── references/
│           │   ├── DESIGN.md            # ดีไซน์สเปก, API คอมโพเนนต์ และคลาสจำกัดการใช้งาน
│           │   └── TOKENS.md            # บันทึกประวัติตัวแปร Figma ทั้งหมด 1,806 ตัวแปร
│           └── scripts/
│               └── figma-tokens-to-css.py  # สคริปต์ Python สำหรับแปลง RGB float เป็น HSL
├── app/
│   ├── globals.css                      # โทเค็นดีไซน์และ Tailwind v4 Layer สไตล์หลัก
│   ├── layout.tsx                       # หน้า Layout หลัก (หุ้มด้วย ThemeProvider และตั้งค่าฟอนต์)
│   └── page.tsx                         # หน้าแรกตัวอย่างแอปพลิเคชัน
├── components/
│   ├── ui/                              # โฟลเดอร์สำหรับติดตั้งคอมโพเนนต์ของ shadcn/ui (ห้ามแก้ไขมือ)
│   └── theme-provider.tsx               # ตัวควบคุมธีม Light/Dark/Primary
├── lib/
│   └── utils.ts                         # ยูทิลิตี้ฟังก์ชัน cn สำหรับการรวมคลาส CSS ที่ซับซ้อน
├── package.json                         # ดีเพนเดนซีและคำสั่งการรันโปรเจกต์
└── tsconfig.json                        # ตัวกำหนดสเปกของ TypeScript
```

---

## 🛠️ ขั้นตอนการเริ่มทำงาน (Getting Started)

### 1. การติดตั้งไลบรารีที่จำเป็น (Dependencies Installation)
หากต้องการรันโปรเจกต์ในเครื่องของคุณ ให้ใช้คำสั่งดังนี้เพื่อติดตั้งดีเพนเดนซีทั้งหมด:
```bash
npm install
```

### 2. การรันระบบในโหมดนักพัฒนา (Development Server)
รันคำสั่งด้านล่างนี้เพื่อสตาร์ทเครื่องเซิร์ฟเวอร์จำลองเพื่อทดสอบระบบ:
```bash
npm run dev
```
จากนั้นเปิดบราวเซอร์แล้วเข้าไปที่ [http://localhost:3000](http://localhost:3000)

### 3. การรันคำสั่งตรวจสอบความถูกต้อง (Build Project)
เพื่อทดสอบว่าหน้าเว็บไซต์ หน้าคอมโพเนนต์ และฟังก์ชัน TypeScript ทั้งหมดทำงานได้อย่างถูกต้องสำหรับการส่งมอบขึ้น Production ให้ใช้คำสั่ง:
```bash
npm run build
```

---

## 🔄 ขั้นตอนการแปลงและอัปเดต โทเค็นดีไซน์จาก Figma (Figma Token Workflow)

เมื่อทีมออกแบบมีการอัปเดตสีหรือดีไซน์ตัวแปรบน Figma ให้ทำตามขั้นตอนการซิงก์ข้อมูลดังนี้:

1. ทำการส่งออกข้อมูลตัวแปรจาก Figma ผ่านปลั๊กอิน `lazyyysync` จะได้ไฟล์ `variables-export.json`
2. นำไปบันทึกไว้ภายนอกโฟลเดอร์หลัก หรือรันสคริปต์ Python ในโฟลเดอร์สคริปต์เพื่อแปลงค่า RGB float เป็น HSL:
   ```bash
   python3 .claude/skills/shadcn-ui-design/scripts/figma-tokens-to-css.py ../variables-export.json > .claude/skills/shadcn-ui-design/assets/globals.css
   ```
3. นำบล็อกสไตล์ที่ได้ในโฟลเดอร์ `assets/globals.css` มารวมเข้ากับส่วน `@layer base` ในไฟล์ [app/globals.css](file:///Users/admin/Design%20Lazyyy/create-skill-design/app/globals.css)
4. ตรวจสอบรายละเอียดความสอดคล้องของสีใน Dark Mode ว่า `--card` และ `--background` แยกโทนความเข้มแตกต่างกันอย่างถูกต้อง

---

## 🛡️ กฎเหล็กของนักพัฒนาโปรเจกต์นี้ (Development Guidelines)

* **Server Components by default** — พยายามสร้าง Component เป็น Server Component เสมอ ใส่ `"use client"` เฉพาะเวลาจำเป็นต้องใช้ Event listener หรือ Hooks ของ React เท่านั้น
* **Semantic Colors Only** — ห้ามกำหนดสีตรงๆ เช่น `bg-white` หรือ `bg-neutral-900` ให้ระบุผ่านสีเชิงสัญลักษณ์ดีไซน์ เช่น `bg-background`, `text-foreground`, `bg-primary` เสมอ
* **No Violet/Purple Colors** — ห้ามนำเข้าหรือประกาศใช้งานสีโทนสีม่วง/น้ำเงินม่วงเป็นอันขาด สีหลัก (Primary) ของโปรเจกต์นี้คือสีโทนกลางกลุ่ม Neutral
* **cn Helper Utility** — รวมและลบคลาสทับซ้อนด้วยฟังก์ชัน `cn(...)` เสมอ ห้ามบวก String หรือใช้ Template Literals ตรงๆ ในตัวเลือกคลาสสไตล์
