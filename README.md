# Raised & Rooted Academy — Website

A two-page conversion site for the micro school:

- **`index.html`** — main landing page (the pitch + the data + lead-magnet CTA)
- **`free-guide.html`** — lead-magnet opt-in page (captures **first name + email**)
- **`thank-you.html`** — post-signup confirmation / delivery page
- **`styles.css`** — shared warm & earthy styling
- **`vercel.json`** — clean-URL config for Vercel

Pure static HTML/CSS — no build step, no backend required. Deploys free on Vercel.

---

## 🚀 Deploy to a free Vercel link (2 minutes)

**Option A — drag & drop (fastest):**
1. Go to https://vercel.com/new
2. Drag this whole folder onto the page (or zip it and upload).
3. Vercel gives you a free `*.vercel.app` link instantly.

**Option B — CLI:**
```bash
npm i -g vercel
cd raised-and-rooted-academy
vercel        # follow prompts → free preview link
vercel --prod # promote to your production *.vercel.app link
```

**Option C — Git (recommended for ongoing edits):**
1. Push this folder to a GitHub repo.
2. In Vercel → "Add New Project" → import the repo → Deploy.
3. Every push auto-deploys.

---

## ✅ Before you go live — swap these placeholders

Search the project for `SWAP` and `REPLACE_WITH` to find each one.

| Where | What to change |
|-------|----------------|
| `free-guide.html` | **`action="REPLACE_WITH_YOUR_FORM_ENDPOINT"`** → your real form endpoint (see below). This is the only required change to start collecting emails. |
| `index.html` hero | `<!-- SWAP: location --> Your City` → your city/area |
| `index.html` FAQ | Real grade range, tuition info, contact email |
| `index.html` testimonials | Replace the 3 sample quotes with real family testimonials |
| `index.html` footer | `hello@raisedandrooted.example` → your real email |
| `thank-you.html` | Link the "Download the guide directly" `href` to your hosted PDF (optional) |
| Statistics everywhere | **Verify the figures** (NAEP/NCES numbers, ratios) against current sources before publishing — they're drawn from well-known education research but should be confirmed. |

---

## 📧 Wiring up email capture (pick one)

The form already POSTs name + email and redirects to `thank-you.html`. You just need an endpoint.

### Easiest — Formspree (free tier)
1. Sign up at https://formspree.io, create a form, copy your form ID.
2. In `free-guide.html`, set:
   ```html
   <form id="leadForm" action="https://formspree.io/f/YOUR_ID" method="POST" novalidate>
   ```
3. Done. Submissions land in your inbox + Formspree dashboard.

### Better long-term — MailerLite / Mailchimp
Use their embedded form or set the form `action` to their POST URL and field names. This lets you **auto-email the guide PDF** on signup and run follow-up sequences. (When you're ready for the full tripwire → upsell funnel, the `marketing-funnel` skill builds it out.)

> Until you set a real endpoint, the form still works for previewing — it skips the network call and goes straight to the thank-you page (no data stored).

---

## 🎨 Brand notes
- Palette + fonts live in `:root` at the top of `styles.css` — change once, updates everywhere.
- Display font: **Fraunces** · Body font: **Nunito Sans** (loaded from Google Fonts).
