---
name: eagle-todo-list
description: Refresh and show Kevin's Eagle Environmental to-do list, the printable Claude Doc "Eagle To-Do List", grouped into the same sections every time and brought up to date from Gmail, Google Calendar, Dropbox and Kevin's own checkmarks in the doc. Use whenever the user says "to-do list", "todo list", "show me the list", "update the list", or asks what Kevin needs to work on. Always show the WHOLE list, never just what changed.
---

# Eagle Environmental: To-Do List

Kevin is old school and prints this list. When the user says **"to-do list"** (or anything
like it), bring the list up to date, open it, and show the whole thing. Don't ask what
they want first. Don't ask permission for the routine steps below.

## Where the list lives

- Claude Doc: **"Eagle To-Do List"**, https://claude.ai/code/artifact/0326c027-d84f-42bb-b27c-44f0b928fe35
  (a viewer link is https://claude.ai/artifact/1Pa5mjC5RtfDToe8eahrCc).
- Update this one doc in place. Don't make a new doc each day. If it has been deleted or
  can't be reached, create a new one with the same sections and tell the user the new link.
- Change the title's "Week of …" to the Monday of the current week, and the "Prepared"
  date to today.

## The sections (always these, in this order)

Every section is a table whose first column is **Done** with `[ ]`, so Kevin can tick
items by hand.

1. **Call first: customers waiting on us.** They said yes or asked a question, and the
   next move is ours: book a visit or install, answer a question, send a revised quote.
   Columns: Done | Customer | Address | Contact | What they need.
2. **Toll Brothers and service calls.** Fan noise, fan swaps and Toll work orders not yet
   on the calendar. Columns: Done | Who | Address | Contact | What they need.
3. **Office items.** Invoices to send, bills to pay, payments to watch for, W9s, test
   kits, Dropbox filing, calendar fixes (for example, an install with no installer
   named). Columns: Done | Who | What is needed.
4. **Waiting on the customer.** Kevin already replied or offered dates, so the next move
   is theirs. Say what was offered and when. Columns: Done | Customer | Address | Phone | Status.
5. **New web quote requests, no reply yet.** Oldest first. Columns:
   Done | Date | Name | Town | Address | Phone. Keep the count line above the table
   ("N requests came in <first date>–<last date>") correct. Point out towns that could
   share a trip.
6. **Estimates to check.** Past estimate visits with no install booked and no answer.
   Keep the three existing sub-tables (proposal never emailed / no proposal file /
   other) and their notes.
7. **Already done.** A short running log of what got booked, sent, or closed out, plus
   people who said no. It is a record, not a to-do, so keep it brief.

Only open items appear in sections 1–6. When something is booked, finished, or the
customer says no, take its row off and add one line about it to section 7.

## How to refresh it

Do these in order. Keep each tool result small: use `PLAIN_TEXT` or `MINIMAL` message
formats, never `RAW`. When a result is too big it is saved to a file; pull out what you
need from that file with python or jq.

### 1. Read the doc first and respect Kevin's marks
Read the doc body (it is large, so it gets saved to a file; parse the XML with python).
Kevin ticks items **in the doc** as he works (`[x]`, `[ x ]`, `x`, or a stray `x` left on
its own line). Any ticked row is done: delete it and log it in section 7. Delete stray
`x` paragraphs too. Also note any text Kevin typed; never overwrite his wording without
reason.

### 2. Gmail (eagle82nd@gmail.com)
Look at everything since the list was last prepared. **Include Trash**
(`includeTrash: true`): Kevin's working conversations often end up in Trash, sent
replies included.
- `after:<last prepared date> -from:webadmin@radonremover.com -in:sent`: customer
  replies, Toll Brothers, vendors, bank alerts.
- `in:sent after:<date>`: what Kevin already answered. A customer thread whose newest
  message is Kevin's belongs in **Waiting on the customer** (or is done if it confirms a
  booking). A customer message with no reply from Kevin belongs in **Call first**.
- `from:webadmin@radonremover.com after:<date>`: new web quote requests (subject
  "New Request For Quote! <Name>"). Get the name, town, address and phone from the
  snippet or the plain-text body. If the form has no address, write
  "(no address given)" plus the useful facts: level, square feet, sump.
- Replies to the "Still interested in a radon quote…" and "Checking in on your radon
  proposal…" follow-ups: a yes goes in Call first, a no or "all set" goes in section 7.
- Payments: TD Bank "We deposited your payment" alerts and Zelle notices clear
  payment-watch rows.
- Skip newsletters, Toll "Tailgate Talk", QuickBooks receipts and AccuStar lab reports.
  The lab reports go to a label automatically and the client is copied on them.

### 3. Google Calendar (primary)
List about the next three weeks. Event titles follow
`<Tech> <D|J|S> <Town> <Street> … HO <name> <phone> … $<price> confirmed with check`,
where D is an estimate, J an install and S a service call. Estimators are Bryan and
Vince; installers are Bob, Abijai and Vince.
- A customer on the list who now has a matching event is booked: take them off and log it.
- A "J …" event with no tech name at the start goes in **Office items** as "put an
  installer name on it".
- Events that start with "Hold" or say "off schedule for now" aren't bookings. Brenda
  (405 Browning Ln, Worcester) is off the schedule until she calls back, so keep her off
  the list.
- When suggesting a date for a Call first item, check who is free that day. Treat
  "<Tech> off", "Bob Marlborough by 2:25" and "Bob Bolton for 3" as time off.

### 4. Dropbox
For filing rows ("put the proposal in /<Town> Proposals"), search by file name, for
example `SouthSt596` in title-only mode. When the file is there, the row is done.

### 5. Write the changes
- Use `mcp__Claude_Docs__update` with `engine: "prose"`. Whole-block replaces and
  deletes need a guard: put `"ifRev": <rev from your latest read>` on the payload, or
  `ifHash` on the op.
- On `guard_mismatch`, Kevin edited the doc while you worked. Read it again, take in his
  change, and resend. Never use `force`.
- `find` targets must be unique. Use `nth` or a block id when the same text appears
  twice.
- Insert rows as `{"type":"row","content":[{"type":"cell","content":[{"type":"paragraph","content":[{"type":"text","text":"…"}]}]}, …]}`
  after an existing row id. To move a row between sections, delete it and insert it in
  the new table.

### 6. Show it
- Open the doc with the Artifact tool (`action: "open"`) and give the viewer link.
- The link only opens for the claude.ai account that owns the doc, so Kevin can't open it
  signed in with his own account. Every time, also export the tab as a letter-size PDF
  (`mcp__Claude_Docs__export`, `format: "pdf"`), decode `data.bytes_b64` into
  `printouts/Eagle To-Do List <YYYY-MM-DD>.pdf`, and send that file to the user so Kevin can
  print it.
- In chat, list **every open item in every section**: one short line per person or task,
  grouped under the section names. The web quote section can be a compact
  "Name (Town)" list. Always show the whole list, not just the changes. After that, add
  a short "Changed since last time" note.

## "Still interested?" emails for old web requests
When asked, go through the **Inbox** web quote requests (subject "New Request For Quote!")
that are more than 14 days old. Skip anyone Kevin has already emailed or who has a visit on
the calendar. **Never include fan replacement requests** ("New Fan Replacement Request");
those belong in section 2. Draft one email per person with the subject
"Still interested in a radon quote for <address>, <town>?", using the same wording as the
9/27 batch. Leave them as drafts until the user says to send. Once they are sent, file the
sent emails in the "A REQUEST FOR QUOTE" label, **and also move each person's original
web-form email ("New Request For Quote!") out of the Inbox into that same label** (add the
label, remove INBOX). Anyone Kevin has emailed should no longer sit in the Inbox.

## Standing rules from Kevin
- Customer emails are **drafts first**. Never send a customer email unless told to.
- Don't archive or clear the Inbox wholesale; it upsets Kevin. Only obvious junk such as
  FedEx notices can be archived.
- Don't ask permission for routine reads and doc updates. Just do them.
- Contacts: Kevin's cell is 508-868-2974, the office is 508-393-7633. Toll Brothers
  invoices now go to Todd Cusson (tcusson@tollbrothers.com); Karen Davis has moved on.
