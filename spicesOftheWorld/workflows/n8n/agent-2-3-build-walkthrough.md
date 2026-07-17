# Agent 2 & 3 — Build Walkthrough (n8n)

Detailed, click-by-click version of `setup-guide.md`. Follow top to bottom
and tick each box as you go. Assumes you've already completed:
- [x] n8n installed and running locally (`local-install-steps.md`)
- [x] Anthropic API credential added in n8n
- [x] Google Drive connected, with `knowledge-base/` uploaded to a Drive folder

---

## Part A — Agent 2 (Knowledge & Brand Voice)

### A1. Create the workflow
Open `http://localhost:5678` → **+ Add workflow** → rename it
"Agent 2 — Knowledge & Brand Voice".

### A2. Add a Manual Trigger
This is the default starting node in a new workflow — leave it, it's for
testing this branch directly.

### A3. Pull the knowledge base in
Add a **Google Drive** node → operation **Search Files** (or **Download**)
→ point it at the Drive folder you uploaded `knowledge-base/` into →
select your Google Drive credential.

### A4. Load + chunk the documents
- Add **Default Data Loader** (search "Data Loader" — under the
  LangChain/AI node category) → feeds the file contents in as documents
- Add **Recursive Character Text Splitter** right after it → chunk size
  **1000**, chunk overlap **200** (good default for markdown)

### A5. Embeddings — pick one (Anthropic has no embeddings API)
Claude/Anthropic can't do this step — it only offers chat models, not
embeddings. Two options:
- [ ] **Free/local**: install Ollama, pull `nomic-embed-text`, use the
      **Embeddings Ollama** node pointed at it. Zero-cost, matches the
      blueprint's philosophy.
- [ ] **Cheap and simpler to wire up**: **Embeddings OpenAI** node with
      `text-embedding-3-small`. Needs an OpenAI API key; costs fractions
      of a cent for this knowledge base's size.

Circle whichever you pick — the Vector Store node needs this feeding it.

### A6. Build the index
Add **Simple Vector Store** node, set mode to **Insert**. Wire up:

```
Manual Trigger → Google Drive → Default Data Loader → Text Splitter → Embeddings → Vector Store (Insert)
```

Click **Execute workflow** once. This builds the index — Insert mode is
only needed for this one run.

### A7. Switch to Retrieve mode
Change the Simple Vector Store node's mode to **Retrieve**. Leave it here
for normal use — only switch back to Insert if you change the knowledge
base files and need to rebuild the index.

### A8. Build the agent itself
- Add a **Chat Trigger** node ("When chat message received") — gives you
  a chat box to test with
- Add an **Execute Workflow Trigger** node ("When Executed by Another
  Workflow") alongside it, with one expected input field: `topic` (text).
  Both triggers can feed the same downstream nodes — Chat Trigger is for
  you testing manually now, Execute Workflow Trigger is for Agent 3 to
  call this workflow later (Part B).
- Add an **AI Agent** node connected from both triggers:
  - Chat Model: your Anthropic/Claude credential
  - Connect the Vector Store (now in Retrieve mode) as a **Tool** input
  - Paste everything below the `---` divider in
    `agents/agent-2-knowledge-voice.md` into the **System Message** field

### A9. Test it
- [ ] Open the chat panel, ask *"Tell me about Grains of Paradise"*
- [ ] Ask *"What's the West Africa spice story?"*
- [ ] Ask 1–2 more spice questions of your choice
- [ ] Run each 3–4 times if the first answer feels off

**Check for:** does it sound like you — memory-first, comma-chained,
adjective-stacked — or like a textbook? If facts are right but voice is
off, fix the system prompt, not the retrieval setup.

**Don't move to Part B until this feels right.**

---

## Part B — Agent 3 (Script Writer), chained on top

### B1. Create the workflow
New workflow → rename "Agent 3 — Script Writer".

### B2. Add the input trigger
Add a **Chat Trigger** (or Manual Trigger with a fixed test value while
building) — this is where you type the episode topic, e.g. *"Grains of
Paradise, Ghana episode"*.

### B3. Call Agent 2
Add an **Execute Workflow** node → select the Agent 2 workflow from the
dropdown → map the incoming topic to the `topic` field on Agent 2's
Execute Workflow Trigger (from A8). This runs Agent 2's retrieval +
voice-writing on that topic and returns researched, voice-written facts.

### B4. Add the Script Writer AI Agent
Add an **AI Agent** node after the Execute Workflow node:
- Chat Model: your Anthropic/Claude credential
- Paste everything below the `---` divider in
  `agents/agent-3-script-writer.md` into the **System Message** field
- Confirm Agent 2's output is landing in this node's input as the
  research context (n8n passes the previous node's output through
  automatically — double-check the mapping)

### B5. Set up the Google Sheet review log
- [ ] Create a Google Sheet with 4 column headers: **Date | Topic |
      Script Text | Status**
- [ ] Copy its sheet ID/URL
- Add a **Google Sheets** node after the AI Agent → operation
  **Append Row** → point it at that sheet → map:
  - Date → current timestamp
  - Topic → the input topic
  - Script Text → the AI Agent's output
  - Status → fixed value `"Needs review"`
- If you don't already have a Google Sheets credential, n8n usually lets
  you reuse your Google Drive OAuth connection — add the Sheets scope if
  prompted.

### B6. Test end to end
- [ ] Trigger with *"Grains of Paradise, Ghana episode"* (or your own
      topic) — confirm the Sheet gets a new row with a full six-part
      script, including two Hook/Close variants
- [ ] Check: Hook/Close sound like you, not generic narration?
- [ ] Check: geography/history/blend/dish sections factually grounded —
      any `[NEEDS VERIFICATION]` flags mean the knowledge base didn't
      have that fact (expected, not a bug)

### B7. Keep the manual review habit
Nothing moves past this Sheet without your eyes on it first, especially
the Hook/Close — this stays true even once you automate further
(per `setup-guide.md` Step 4).

---

## Next milestone

Once you're happy with a full script for one real topic, that's the
signal to move on to Agent 4 (Thumbnail) — which still needs a market
photo and a solo farm-work-clothes shot of you first (see
`docs/open-tasks.md`).
