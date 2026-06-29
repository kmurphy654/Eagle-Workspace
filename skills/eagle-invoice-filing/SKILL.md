---
name: eagle-invoice-filing
description: Rename scanned Eagle Environmental invoices from generic scanner names to address-based names, then file each paid invoice (with its proposal, drawing, and warranty) into its town folder in Dropbox. Use whenever the user wants to rename, sort, or file scanned radon-mitigation invoices, or mentions the _Invoices folder, scanned invoices, or filing invoices into town folders.
---

# Eagle Environmental — Invoice renaming & filing

Renames freshly scanned handwritten invoices and files each paid one into the right Dropbox town folder, alongside that property’s proposal documents.

## Folders (in this Mac's Dropbox)
- Invoices to process: `$HOME/Library/CloudStorage/Dropbox/_Invoices` — the real synced folder. (Ignore any `~/Dropbox/_Invoices`; that’s a stale empty leftover.)
- Toll Brothers payments: `$HOME/Library/CloudStorage/Dropbox/_Toll Brothers payments` (note lowercase “payments”).
- Per-town folders at the Dropbox top level: `{Town}` (the final home) and `{Town} Proposals` (holds the proposal / drawing / warranty files).

## Step 1 — Read each scan, build an old→new rename table
- Scanner files look like `Receipt_YYYY-MM-DD_HHMMSS_<n>.jpg`.
- Open each image with the Read tool and read the handwritten **SOLD TO / ADDRESS / CITY** block (top-left). The “Per Proposal #” line in the body usually repeats the street and confirms the handwriting. If the address block and the proposal line disagree on the house number, prefer the **proposal line** and flag it.
- Target name: **`Street Name Number I Town.jpg`** — the letter **I** (Invoice) separates street+number from town. Include unit/lot if written.
  Examples: `Boutwell St 31 I Wilmington.jpg`, `Longley Rd 11 Unit 63 I Shirley.jpg`.
- Town spelled **formally** (Northborough, Tyngsborough, Marlborough, Foxborough, Newburyport). Keep the street-type abbreviation as written.
- For large batches, fan out to subagents to read the images in parallel.
- Before renaming, show the table and flag: ambiguous handwriting, house-number conflicts, and same-address repeats.

## Step 2 — Toll Brothers invoices
- If the invoice names “Toll Brothers” / “Toll Bros” anywhere (usually the SOLD TO / SHIP TO block, often with a Lot number), insert `Toll Bros` into the name right before the ` I `: e.g. `Shoreline Dr 1 Lot 16 Toll Bros I Hudson.jpg`. Match on the name actually being written, NOT just the presence of a Lot number.
- Then **move** those files out of `_Invoices` into `_Toll Brothers payments`. (That folder has inconsistent old naming — just keep the standard `... Toll Bros I Town` format.)

## Step 3 — Rename (non-Toll-Brothers)
- Rename with a script that **never overwrites** an existing file (skip + report collisions).
- Repeat visit to the same address (name already exists): keep both, append the invoice **date** as `M-D-YY` (e.g. `Walnut St 121 I Revere 4-30-26.jpg`).
- Invoices with no street number (e.g. `President Village I Fall River`) keep the name as-is.

## Step 4 — File each paid invoice into its Town folder
Every paid invoice (the `I` file) belongs in its `{Town}` folder, together with that property’s proposal docs. Document-type letters in filenames: **I**=Invoice, **P**=Proposal, **D**=Drawing, **W**=Warranty (also seen: DE, PM, S, Pic, G).
- For each `Street Number I Town.jpg`: look in `{Town} Proposals` for the same street+number, then **move both the matched proposal docs AND the invoice into `{Town}`**.
- **Matching / normalization:** strip spaces, case, and punctuation; canonicalize street-type words (drive→dr, road→rd, street→st, lane→ln, court→ct, circle→cir, terrace→terr, avenue→ave, place→pl); match `street+number` with a digit boundary so #1 ≠ #14.
- **Town-folder aliases** (invoice uses the formal spelling, folders use the short one): Foxborough→Foxboro, Marlborough→Marlboro, Northborough→Northboro, Tyngsborough→Tyngsboro, N Reading→North Reading, Marstons Mills→ folder `Marston Mills Proposals`. Some towns (e.g. Seekonk) have no Proposals folder.
- Many invoices have **no match** in `{Town} Proposals` because the proposal was already moved into `{Town}` in a prior cycle — in that case just move the invoice in to join it. Every paid invoice belongs in its town folder regardless.
- **Name collision in the town folder = a repeat service, not a duplicate:** file it anyway, appending **today's date** as `M-D-YY` (e.g. `Greenwich Ct 204 I Worcester 6-9-26.jpg`).

## Run it safely
1. Read the scans, build the old→new table, and show it for review (flag the ambiguous/conflict/repeat cases).
2. Rename with a `mv` script that refuses to overwrite.
3. Do a **dry-run match report** against the Proposals folders first.
4. Move with a script that **never overwrites** (skip + report collisions), then report what moved and any anomalies.

## Requirements
- Dropbox must be installed and fully synced on this Mac, so the folders above exist locally.
- Reading handwriting needs the Read tool (vision); for big batches, subagents speed it up.
