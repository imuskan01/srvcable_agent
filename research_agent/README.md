# SRVCABLE Research Brief Agent (Super Investing, AI Innovator Part B)

Input: an NSE ticker + a folder of scraped documents.
Output: a one-page Markdown brief for a retail investor (Snapshot, Bull case, Bear case, Open questions, Sources with [S#] citations).

## How to run
Requires Python 3.9+. No packages to install (standard library only).

1. Get a free Gemini API key at https://aistudio.google.com (Get API key).
2. Set the key (do not commit it):
   - Windows: `set GEMINI_API_KEY=your_key_here`
   - Mac/Linux: `export GEMINI_API_KEY=your_key_here`
3. Run:

       python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --docs research_pack --out brief.md

Options: `--today 2026-09-23` (default), `--reuse` (reuse saved extractions after a failed run).
Outputs: `brief.md`, `brief.md.draft.md` (before verification), `brief.md.log.json` (audit trail), `brief.md.extractions.json`.
If a model name stops working: `python list_models.py`, then set `EXTRACT_MODEL` / `WRITE_MODEL`.

## Files
- `agent.py`: the pipeline
- `prompts/system_prompt.md`: the system prompt (the agent's rules)
- `research_pack/`: the 8 test documents
- `run3.md`: the brief the agent generated for SRVCABLE (as submitted)
- `TEST_LOG.md`: 3 runs, what went wrong, what I changed
- `reference_brief_by_claude.md`: a hand-written answer key I used to sanity-check output (NOT agent output)

## How it thinks (design)
0. **Preflight in plain Python (no LLM):** parses each file's header, computes document age vs today, regex-detects prompt-injection text, and checks the ticker/company name appears. A hostile page cannot talk this stage out of flagging it. If neither the ticker nor the company name appears, the document is excluded, overriding the model.
1. **Triage + extract (small model, one call per document):** right company? stale? how trustworthy? facts, bull/bear points, red flags.
2. **Write (larger model):** the system prompt enforces: documents are data, not instructions; never invent facts; entity and date checks; rank sources (exchange filings > company > news > tip blogs); reconcile conflicting numbers with arithmetic; no buy/sell call.
3. **Verify (larger model):** re-checks every number and citation against the raw documents, recomputes growth and margins, removes unsupported claims, enforces length.

Reliability: retries on overload, backup model on repeated 503/429, token-budget retry if output is cut off, fallback to the draft if the verified brief is truncated.

## Models and why
- `gemini-flash-lite-latest` for per-document extraction: repetitive, fast, cheap, free tier.
- `gemini-flash-latest` for writing and verification: stronger reasoning for numbers and spotting conflicts, still free tier.
- Backups on overload: `gemini-flash-lite-latest`, `gemini-2.5-flash`.
I chose the free tier so no spend is needed. I first built the same pipeline for Claude models but switched to Gemini because I had no API credit.

## Known limitations
- The verifier is also an LLM, so it reduces errors but does not remove them. In the final run the model still called exports "high-margin" without a source and speculated about why one article's revenue differed. A human should spot-check numbers.
- The backup model on overload is weaker, so quality can vary between runs.
- Reads only .md/.txt files. No live-data tool (web search / NSE data).
- The entity check needs `--company`; without it only the model judges whether a document is about the right company.
- Free-tier Gemini may use inputs to improve Google products; fine for this fictional data, not for private data.
