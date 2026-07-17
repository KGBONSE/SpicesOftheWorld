# n8n Local Install & Credential Setup (Free, Self-Hosted)

*Zero-cost-to-start path. n8n Cloud no longer has a permanent free tier (as of 2026 it's $24+/month) — self-hosting via Docker on your own computer is free and sufficient for building and testing.*

---

## Step 1 — Install n8n locally

1. Install **Docker Desktop** from docker.com if you don't already have it (free, Mac/Windows/Linux).
2. Open a terminal and run:
   ```
   docker volume create n8n_data
   docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
   ```
3. Open `http://localhost:5678` in your browser. n8n will prompt you to create an owner account (just you — this is local and free).

*Note: this runs n8n only while the container is running / your terminal is open. That's fine for building and testing manually. If you later want it running unattended on a schedule, you'd move to a small VPS ($4–7/month) — not needed yet.*

## Step 2 — Add your Anthropic API credential

1. In n8n: **Credentials** → **New**
2. Search for "Anthropic" → select it
3. Paste in your Anthropic API key (from console.anthropic.com — separate from claude.ai, this is pay-as-you-go per token rather than a subscription; you'll need to create an account there and add billing if you haven't)

## Step 3 — Connect Google Drive

1. **Credentials** → **New** → search "Google Drive"
2. n8n walks you through Google OAuth — sign in with your Google account and grant access. No manual API console setup needed for basic use.

## Step 4 — Build the workflow

Once both credentials exist, follow `05-n8n-setup-guide.md` for the exact node-by-node build (Manual Trigger → Google Drive → Data Loader → Text Splitter → Embeddings → Vector Store → AI Agent → output), pasting in the system prompts from files 03 and 04.

## Status as of this export

- n8n instance: **not yet set up**
- Model choice: **Claude (Anthropic API)** — confirmed
- Google Drive: **not yet connected**
