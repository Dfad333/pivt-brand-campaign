---
name: feedback-preflight-cost
description: "Always quote the credit cost before running any paid generation — Tarek asked for cost up front, not after"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 41a85166-e466-460f-bbaa-9a42e25beb05
  modified: 2026-08-15T13:53:21.832Z
---

Before creating anything with a paid generation tool (Higgsfield images, video, audio), **tell
Tarek the cost first and let him decide** — do not submit and report the spend afterwards.

**Why:** he asked for this directly on 2026-08-15, after a motion-piece build spent 50 credits
across 4 stills and 2 video takes without him seeing a number beforehand. He phrased it as
"tokens" but the billable unit is Higgsfield credits.

**How to apply:**
- Higgsfield `generate_image` / `generate_video` accept `get_cost: true`, which returns the
  credit cost **without submitting a job**. Run that first, quote it, then generate.
- `get_cost` is NOT supported inside `generate_image_batch` / `generate_video_batch` — preflight
  a single representative request, multiply by the number of items, and say so.
- Quote the round total, not per-item, since rounds are usually 2 images or 2 video takes.
- Be explicit that Claude **token** usage is not something I can measure — no tool reports it.
  Only quote credits, and say that's what's being quoted.
- Rerolls to fix a defect still cost credits: flag the cost of a reroll before firing it.
- `balance` gives credits + plan; `transactions` gives spend history for reconciling.

Baseline observed 2026-08-15: Nano Banana Pro still (4:5, 4k) = **4 credits**;
Minimax Hailuo 2.3 video ~6s = **10**; MiniMax H3 video ~6.6s = **24**.

Related: [[project-brand-campaign]]
