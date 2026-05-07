#!/usr/bin/env node

function usage() {
  console.error(`Usage: extract.mjs "url1" ["url2" ...] --aisa-api-key <key>`);
  process.exit(2);
}

const rawArgs = process.argv.slice(2);
let apiKey = "";
const args = [];
for (let i = 0; i < rawArgs.length; i++) {
  const arg = rawArgs[i];
  if (arg === "--aisa-api-key") {
    apiKey = (rawArgs[i + 1] ?? "").trim();
    i++;
    continue;
  }
  args.push(arg);
}
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const urls = args.filter(a => !a.startsWith("-"));

if (urls.length === 0) {
  console.error("No URLs provided");
  usage();
}

if (!apiKey) {
  console.error("Missing --aisa-api-key");
  process.exit(1);
}

const resp = await fetch("https://api.aisa.one/apis/v1/tavily/extract", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${apiKey}`,
  },
  body: JSON.stringify({
    urls: urls,
  }),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`AIsa Tavily Extract failed (${resp.status}): ${text}`);
}

const data = await resp.json();

const results = data.results ?? [];
const failed = data.failed_results ?? [];

for (const r of results) {
  const url = String(r?.url ?? "").trim();
  const content = String(r?.raw_content ?? "").trim();
  
  console.log(`# ${url}\n`);
  console.log(content || "(no content extracted)");
  console.log("\n---\n");
}

if (failed.length > 0) {
  console.log("## Failed URLs\n");
  for (const f of failed) {
    console.log(`- ${f.url}: ${f.error}`);
  }
}
