#!/usr/bin/env node
/**
 * Generate site imagery with kie.ai "GPT Image 2" (gpt-image-2-text-to-image).
 *
 * Usage:
 *   KIE_API_KEY=sk-xxxx node scripts/generate-images.mjs
 *   # or generate a single one:  node scripts/generate-images.mjs hero
 *
 * Output: writes JPGs into ./assets/
 */

import { writeFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const API_KEY = process.env.KIE_API_KEY;
if (!API_KEY) {
  console.error("✗ Missing KIE_API_KEY env var.\n  Run:  KIE_API_KEY=sk-xxxx node scripts/generate-images.mjs");
  process.exit(1);
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = join(__dirname, "..", "assets");

const CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask";
const RECORD_URL = "https://api.kie.ai/api/v1/jobs/recordInfo";
const MODEL = "gpt-image-2-text-to-image";

// Shared style so every image feels like one brand: warm, earthy, real, hopeful.
const STYLE =
  "Photorealistic, warm natural lighting, earthy color palette of forest green, sage, " +
  "cream and warm terracotta. Authentic, candid, documentary feel — not stocky or staged. " +
  "Cozy modern micro-school / home-learning environment with wood textures, plants, and big " +
  "bright windows. Diverse, genuinely happy children. Suburban Katy, Texas warmth.";

const JOBS = [
  {
    key: "hero",
    aspect_ratio: "3:2",
    resolution: "2K",
    prompt:
      "A warm, inviting micro-school classroom scene: one friendly teacher sitting at a round " +
      "wooden table with a small group of about five elementary-age children (grades K-8), all " +
      "engaged and smiling, working together on a hands-on learning project. Potted plants on " +
      "the windowsill, soft morning light pouring through large windows, bookshelves in the " +
      "background. The mood is calm, personal, and joyful — every child is clearly seen and known. " +
      STYLE,
  },
  {
    key: "cover-bg",
    aspect_ratio: "3:4",
    resolution: "2K",
    prompt:
      "Premium portrait ebook / guide cover, 3:4 vertical, for a parenting guide published by a " +
      "small private microschool. Rich deep forest-green background (color #2f4a32) with a subtle " +
      "soft golden glow near the top, faint refined paper texture, and a thin elegant gold border " +
      "line inset from the edges. IMPORTANT: leave a generous CLEAN EMPTY area across the top third, " +
      "centered, reserved for a logo to be added later — do not draw any emblem, icon, tree, or " +
      "illustration in that top area. In the vertical center, a large centered book title set in a " +
      "classy high-contrast serif typeface, cream color (#f7f3ea), reading exactly: " +
      "\"The Real Numbers Behind Your Child's Future\". Directly beneath the title, a short thin " +
      "horizontal gold divider line, then a smaller centered sans-serif subtitle in soft cream " +
      "reading exactly: \"What the data really says about the school you choose, plus 10 simple " +
      "routines to raise a confident, capable child.\" Near the bottom center place a small cream " +
      "rounded-pill badge containing dark green uppercase text \"FREE DOWNLOAD\", and below it small " +
      "letter-spaced cream text reading \"RAISED & ROOTED ACADEMY\". Elegant, warm, trustworthy, " +
      "lots of negative space, beautiful professional typography, crisp vector-clean look, no " +
      "photographs and no people. Spell every word exactly as written.",
  },
  {
    key: "approach",
    aspect_ratio: "4:3",
    resolution: "2K",
    prompt:
      "A confident young elementary-age child standing and speaking, presenting an idea to a few " +
      "attentive classmates seated nearby in a cozy micro-school room. The child looks proud and " +
      "self-assured. Hands-on materials on the table, a small whiteboard with simple drawings " +
      "behind them. Captures real-world skills like communication and confidence being built. " +
      STYLE,
  },
  {
    key: "guide-cover",
    aspect_ratio: "3:4",
    resolution: "2K",
    prompt:
      "An elegant educational guide / ebook cover composition (no text), vertical. A warm, " +
      "hopeful image of a parent and child reading together at a sunlit wooden table at home, " +
      "viewed slightly from above, with cream and sage tones and a sprig of greenery. Clean, " +
      "premium, lots of soft negative space at the top and bottom for a title to be added later. " +
      STYLE,
  },
  {
    key: "og-image",
    aspect_ratio: "16:9",
    resolution: "2K",
    prompt:
      "A wide, welcoming banner image for a micro-school brand: a small group of happy, diverse " +
      "elementary children and a caring teacher learning together around a wooden table near a " +
      "big bright window with plants. Composed with open, uncluttered space on the left third " +
      "for a logo and headline to be overlaid later. Warm, trustworthy, family-oriented. " +
      STYLE,
  },
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function createTask(job) {
  const res = await fetch(CREATE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: MODEL,
      input: {
        prompt: job.prompt,
        aspect_ratio: job.aspect_ratio,
        resolution: job.resolution,
      },
    }),
  });
  const json = await res.json();
  if (json.code !== 200 || !json.data?.taskId) {
    throw new Error(`createTask failed for "${job.key}": ${JSON.stringify(json)}`);
  }
  return json.data.taskId;
}

// Pull the first image URL out of whatever shape recordInfo returns.
function extractUrls(data) {
  const candidates = [];
  const tryPush = (v) => {
    if (Array.isArray(v)) candidates.push(...v.filter((x) => typeof x === "string"));
    else if (typeof v === "string") candidates.push(v);
  };
  tryPush(data?.resultUrls);
  tryPush(data?.resultUrl);
  tryPush(data?.response?.resultUrls);
  if (typeof data?.resultJson === "string") {
    try {
      const parsed = JSON.parse(data.resultJson);
      tryPush(parsed.resultUrls);
      tryPush(parsed.result_urls);
      tryPush(parsed.urls);
    } catch {}
  }
  return candidates.filter((u) => /^https?:\/\//.test(u));
}

async function pollTask(taskId, key) {
  const deadline = Date.now() + 5 * 60 * 1000; // 5 min
  while (Date.now() < deadline) {
    const res = await fetch(`${RECORD_URL}?taskId=${encodeURIComponent(taskId)}`, {
      headers: { Authorization: `Bearer ${API_KEY}` },
    });
    const json = await res.json();
    const data = json.data || {};
    // kie.ai uses state: "waiting" | "queuing" | "generating" | "success" | "fail"
    const state = (data.state || data.status || "").toLowerCase();
    const urls = extractUrls(data);
    if (urls.length) return urls;
    if (state === "fail" || state === "failed" || data.failCode) {
      throw new Error(`Task ${key} failed: ${data.failMsg || JSON.stringify(json)}`);
    }
    process.stdout.write(`  · ${key}: ${state || "working"}…\r`);
    await sleep(4000);
  }
  throw new Error(`Task ${key} timed out`);
}

async function download(url, dest) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`download failed ${res.status} for ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  await writeFile(dest, buf);
  return buf.length;
}

async function run() {
  await mkdir(ASSETS_DIR, { recursive: true });
  const only = process.argv[2];
  const jobs = only ? JOBS.filter((j) => j.key === only) : JOBS;
  if (!jobs.length) {
    console.error(`No job named "${only}". Options: ${JOBS.map((j) => j.key).join(", ")}`);
    process.exit(1);
  }

  console.log(`Generating ${jobs.length} image(s) with ${MODEL}…\n`);
  for (const job of jobs) {
    try {
      console.log(`→ ${job.key} (${job.aspect_ratio}, ${job.resolution})`);
      const taskId = await createTask(job);
      const urls = await pollTask(taskId, job.key);
      const dest = join(ASSETS_DIR, `${job.key}.jpg`);
      const bytes = await download(urls[0], dest);
      console.log(`  ✓ saved assets/${job.key}.jpg (${(bytes / 1024).toFixed(0)} KB)\n`);
    } catch (err) {
      console.error(`  ✗ ${job.key}: ${err.message}\n`);
    }
  }
  console.log("Done.");
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
