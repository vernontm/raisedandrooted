# Leads — storage & export

## Where leads are stored
Opt-ins from `free-guide.html` are written to **Supabase** → project *vernontm's Project*
(`ssllepovajmohdhvhzsa`) → table **`raised_rooted_leads`** (`name`, `email`, `source`, `created_at`).

The browser writes with the **publishable/anon key**, which has an **insert-only** row-level
policy: it can add a lead but cannot read, update, or delete the list. So the key being visible
in the page source is safe.

View leads anytime in the Supabase dashboard → Table Editor → `raised_rooted_leads`.

## Download all leads as a CSV (one click)
A secured Supabase **Edge Function** (`export-leads`) returns the full list as a CSV download.
It runs server-side with the service-role key (never exposed to the browser or this repo) and is
gated by a secret token.

**URL (token shared privately — not stored in this repo):**
```
https://ssllepovajmohdhvhzsa.supabase.co/functions/v1/export-leads?token=YOUR_SECRET_TOKEN
```
Just open that URL in a browser and the CSV downloads. Bookmark it for easy access.

- Correct token → `200` CSV download (`raised-rooted-leads-YYYY-MM-DD.csv`)
- Missing/wrong token → `401 Unauthorized`

### Rotating the token
The token is hard-coded in the deployed function (in Supabase, not in this repo). To change it,
redeploy `export-leads` with a new `EXPORT_TOKEN` value, or move it to a Supabase secret/env var
and read it via `Deno.env.get('EXPORT_TOKEN')`.

### Notes
- Free tier covers ~500 MB (hundreds of thousands of leads) at $0.
- When you're ready to email/nurture, the data is already in Supabase to sync to an ESP
  (MailerLite, etc.).
