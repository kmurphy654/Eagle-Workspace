---
name: eagle-quick-quote
description: Create a single Eagle Environmental radon proposal packet on demand when Kevin already knows what goes in it. Given an address and a few facts, generate the proposal PDF, the warranty, and the external system sheet, then build a Gmail draft to the customer (and optionally file the docs into the town's Dropbox Proposals folder). Use whenever Kevin says "make a quote", "create a proposal", "write up a quote for <address>", or similar — a one-off manual quote, NOT the daily inbox scan.
---

# Eagle Environmental — Quick Quote (manual, on demand)

Kevin gives the address and the handful of facts he already knows. You build the packet.
Do **not** classify, hunt through Gmail, or try to figure out whether it's a good lead — Kevin
has already decided. Just make the documents.

## What Kevin has to give you (all required)
- **Street address + town** (e.g. `68 Baldwin Dr, Hampden`)
- **Customer name** (e.g. `John Smith`)
- **Customer email** — needed only to address the draft. If Kevin doesn't give one, still
  make the PDFs and create the draft with the To field blank; tell him it needs an address before it can send.
- **Number of pipes / suction points** — ALWAYS. This drives the proposal wording and is never
  assumed. If Kevin didn't say, ask "how many pipes?" before generating. (This is the `--points` value.)
- **Warranty** — ALWAYS. `4year`, `2year`, or `none`. Never assume; if Kevin didn't say, ask which.

Pipes and warranty are not optional and have no default — if either is missing, ask for it and
do not generate until you have both.

## Prompting Kevin through it (when info is missing)
Kevin will often type a short sentence and leave things out. Don't fail and don't assume —
**walk him through the gaps in one friendly pass**, then confirm before building.

1. **Parse whatever he gave** and figure out what's still missing from the required set:
   address, customer name, email, **# of pipes**, **warranty**. (Price is not required — it
   defaults to $1,650, but confirm it in the recap.)
2. **Ask for everything missing in ONE message**, as a short numbered list — don't drip one
   question at a time. Example:
   > Got 68 Baldwin Dr, Hampden for John Smith. Before I build it I need:
   > 1. Customer email?
   > 2. How many pipes (suction points)?
   > 3. Warranty — 4‑year, 2‑year, or none?
   > 4. Price — or should I use the standard $1,650?
3. If he answers only some, ask again for just the ones still open. Keep it brief.
4. **Recap and confirm before generating.** One line back to him:
   > Building: 68 Baldwin Dr, Hampden MA · John Smith <jsmith@gmail.com> · $1,650 · 2 pipes · 4‑yr warranty · exterior RP145 3". Go?
   Wait for his "yes/go" (or a correction) before running any scripts. If he corrects a field,
   re-recap the changed line and confirm.
5. Only after confirmation, run STEPS 1–7 below.

Keep the tone quick and plain — Kevin is doing these between jobs. Never lecture, never re-ask
for something he already gave.

## Defaults (use silently unless Kevin overrides)
| Field | Default | Override cues |
|---|---|---|
| Price | **$1,650** | any dollar amount he says |
| Fan | **RP145** | "old house"/pre-2000 → **GX5A**; or he names a model |
| Pipe size | **3"** | "4 inch" (also auto-4" if he says living area > 3,500 sq ft) |
| System | **exterior** | "interior"/"attic fan"/"through the roof"/"add-a-fan" → interior |
| Central | **off** | "garage with living space above" → add `--central` |
| State | **MA** | he names another (NH, CT, …) |
| Date | **today** (M/D/YYYY) | — |

> **Number of pipes** and **warranty** are NOT in this table on purpose — they are required inputs (above), not defaults.

Title-case the town everywhere (`leominster` → `Leominster`).

## Steps

### 1. Copy templates to /tmp
```
cp "eagle-tools/templates/Blank with signature.pdf" /tmp/blank_sig.pdf
cp "eagle-tools/templates/External Radon System Sheet.pdf" /tmp/external_template.pdf   # exterior jobs
```
Warranty template:
- 4year → `cp "eagle-tools/templates/4 Warranty.pdf" /tmp/warranty_template.pdf`
- 2year → `cp "eagle-tools/templates/2.7 WARRANTY.pdf" /tmp/warranty_template.pdf`
- none  → skip (no warranty/sheet generated)

**Interior / add-a-fan** override: warranty is always `4 Warranty.pdf`, and the system sheet is the
interior one from Dropbox — `mcp__Dropbox__download_link` on `/_A-Z forms/Internal Radon System Sheet.pdf`
(file_id `id:HIR4vMWqTuwAAAAAAAEAiA`) downloaded to `/tmp/external_template.pdf`; if that fails, fall back
to `cp "eagle-tools/templates/External Radon System Sheet.pdf" /tmp/external_template.pdf`.

### 2. Build a slug for the filenames
CamelCase street + house number + TitleCase town, no spaces.
`68 Baldwin Dr, Leominster` → `BaldwinDr68Leominster`.

### 3. Generate the proposal
```
python eagle-tools/make_proposal.py \
  --name "FULL NAME" --addr "STREET ADDRESS" --town "TOWN, STATE" \
  --pipe PIPE --fan FAN --price PRICE --date M/D/YYYY --points POINTS \
  --template /tmp/blank_sig.pdf --out /tmp/{SLUG}_Proposal.pdf \
  [--central]   [--interior]
```
For **interior**, omit `--fan`/`--central`, add `--interior` (zero holes drilled, location TBD).

### 4. Generate warranty + external sheet (skip entirely if warranty = none and not interior)
```
python eagle-tools/make_warranty.py \
  --addr "STREET ADDRESS, TOWN, STATE" \
  --template-warranty /tmp/warranty_template.pdf \
  --template-external /tmp/external_template.pdf \
  --out-warranty /tmp/{SLUG}_Warranty.pdf --out-external /tmp/{SLUG}_ExternalSheet.pdf
```
Then confirm the files exist (`ls -la`). If the proposal PDF is missing, stop and tell Kevin — never make a draft without it.

### 5. Create the Gmail draft (never send)
`base64 -w0` each PDF and attach it via `mcp__Gmail__create_draft`.
- **To:** customer email  **Subject:** `Radon Mitigation Proposal — STREET ADDRESS, TOWN`
- Body:
  > Hi FIRST_NAME,
  >
  > Thank you for reaching out to Eagle Environmental. Please find attached our proposal for radon mitigation at STREET ADDRESS, TOWN, STATE.
  >
  > We will install a sub-slab depressurization system using a RadonAway fan with PIPE" PVC pipe. Proposal price: $PRICE. This includes all labor, materials, and our standard warranty.
  >
  > Please reply or call (508) 393-7633 to schedule.
  >
  > Kevin Murphy
  > Eagle Environmental
  > (508) 393-7633
  > eagle82nd@gmail.com

  Interior systems: replace the pipe sentence with "…interior system with the fan installed in the attic and the pipe routed through the roof." Add-a-fan: use price $1,150 and "We can add a radon fan to your existing passive pipe system…".
- **Never put the fan model (RP145/GX5A) in the email body.**
- Attach `{SLUG}_Proposal.pdf` always; add `{SLUG}_Warranty.pdf` + `{SLUG}_ExternalSheet.pdf` unless warranty = none.

### 6. (Optional) File into Dropbox
Only if Kevin asks to "file it" / "put it in Dropbox". Create the two PDFs in `/{Town} Proposals`
named `{Street}{Num}p{Town}.pdf` (proposal) and `{Street}{Num}d{Town}.pdf` (drawing/warranty),
matching the existing naming in that folder. The Gmail draft alone does NOT touch Dropbox.

### 7. Log it
Append one entry to `pending-quotes.json` (`source: "manual"`, `draft_sent: false`) so the
follow-up chase and post-send sync see it. Commit + push if Kevin wants a record kept.

## Guardrails
- **Never send email** — only create a draft for Kevin to review and send.
- Always attach real PDFs; a draft with no attachments (or with command text in the body) is worse than none.
- Interior / add-a-fan always attach all three PDFs.
