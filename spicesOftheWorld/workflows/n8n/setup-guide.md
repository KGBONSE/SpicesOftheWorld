# Fudi People — n8n Setup Guide: Agents 2 & 3

*For a detailed, click-by-click, checkbox version of everything below
(including the embeddings-provider gotcha and Sheet setup), see
`agent-2-3-build-walkthrough.md`.*

## Goal for this build
Get Agent 2 (Knowledge & Brand Voice) working standalone and testable, then chain Agent 3 (Script Writer) on top. Don't build Trends Scout, Thumbnail, Editing, or Publishing yet — prove this loop works first.

---

## Step 1 — Get your files into Google Drive

Put these in one Drive folder (e.g. "Fudi People Knowledge Base"):
- The 7 regional spice markdown files (Africa, Middle East, South Asia, SE Asia, East Asia, Americas, Europe)
- Spice science profiles file
- World of spice recipes file
- The pairing spreadsheet
- fudi-people-voice-profile.md (the refined version)

## Step 2 — Build Agent 2 (Knowledge & Brand Voice)

In a new n8n workflow:

1. **Manual Trigger** node (for testing) — later you'll swap this for a Form Trigger or Google Sheets trigger
2. **Google Drive** node → "Download" or "List Files" pointed at your Knowledge Base folder
3. **Default Data Loader** node → feeds the file contents in
4. **Recursive Character Text Splitter** node → chunk size ~1000 characters, overlap ~200 (good default for markdown)
5. **Embeddings** node → use a free embedding model (n8n has free/local options — check the Embeddings node dropdown for what's available without a paid API key)
6. **Simple Vector Store** node → set to "Insert" mode the first time you run it (this builds the index), then switch to "Retrieve" mode for normal use
7. **AI Agent** node:
   - Connect the Vector Store as a **Tool** (this lets the agent search your knowledge base on demand instead of you pasting everything in every time)
   - Paste the Agent 2 system prompt (from `agent2-knowledge-brand-voice-system-prompt.md`) into the System Message field
   - Connect your chat model (whichever LLM you're using)
8. **Chat Trigger** or simple input field → type a test question like "Tell me about Grains of Paradise" and check the output sounds like you, not a textbook

**Test before moving on.** Run it 3-4 times with different spice questions. If the voice doesn't feel right, that's the system prompt to adjust — not the retrieval.

## Step 3 — Build Agent 3 (Script Writer) on top

1. New workflow (or new branch in the same one)
2. **Input**: episode topic (e.g. "Grains of Paradise, Ghana episode")
3. Call Agent 2's workflow as a sub-workflow (n8n supports this via the "Execute Workflow" node) to pull the researched, voice-written facts
4. **AI Agent** node with the Agent 3 system prompt (`agent3-script-writer-system-prompt.md`) pasted in
5. Output → **Google Sheets** node (one row per script draft, with columns: Date, Topic, Script Text, Status) so you have a running log to review

## Step 4 — Manual review loop (keep this even after automating)

Every script drafted should land in a Google Sheet or get emailed to you before anything moves further down the pipeline (thumbnail, editing, publishing). Don't let any agent post or finalize without your eyes on it first — this matters most for the voice-driven sections (Hook and Close) where a wrong note is most noticeable.

---

## What NOT to build yet

- Agent 1 (Trends Scout) — separate system, no dependency on voice profile/knowledge base
- Agent 4 (Thumbnail) — needs your photo library properly organized first
- Agent 5 (Editing) — later phase per the original blueprint
- Agent 6 (Publishing) — only once you're confident in script quality

## Next milestone

Once Agent 2 + 3 produce a script you're happy with for one spice/episode, that's the signal to move on to Thumbnail (Agent 4) using your photo reference library.
