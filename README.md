# SafeRouter ReplayLab

A retry or cancellation should not quietly change which logical request gets billed. SafeRouter ReplayLab uses local Apertus 1.5 to propose short request/retry/cancel paths, then checks them against a fixed synthetic protocol. Confirmed divergences become minimized, independently replayable JSON bundles.

Hack Apertus 2026, Track 2B. Team Sumplus, Jakob. New work started 15 October 2026. Based on the official HackApertus/project-template, preserving `track_2b/` and its challenge README.

```
make run
```

Open http://127.0.0.1:19564 . Docker starts the application from the repository root. Inspect clearly labelled saved model responses or configure your own on-premise Apertus for live generation. A missing/invalid model response is an explicit error; no fixture silently replaces live inference.

The complete prototype is in `track_2b/`:

- `src/`: model adapter, strict validator, reference/target simulator, shrinker, replay CLI, local UI.
- `data/`: frozen tasks, protocol, experiment plan and disclosed adapter amendment.
- `results/`: raw model attempts, corrected initial scoring, full seeded comparison, controls and counterexample evidence.
- `technical_report.md` and `Sumplus_Report.pdf`: measured results and limitations.
- `docs/REPRODUCE.md`: setup, model/runtime details, budgets and deployment boundary.
- `docs/SOURCES.md`: code, model, data and AI assistance disclosure.

Replay a downloaded bundle without Docker, a model, or any network:

```
python track_2b/src/replay.py replaylab-counterexample.json
```

All faults are deliberately injected into a local synchronous simulation. This is not a real provider integration, security audit, production billing check or proof of natural language contract correctness. The detailed protocol was assistant-authored and has no recorded independent human review. Repaired model repetitions are not independent heldout validation. Full comparison results do not establish superiority over mature testing tools.

On-premise deployment is the target. Recorded deterministic replay has no runtime network dependency; live inference needs separately provisioned local model/runtime assets. No Swiss cloud or fully disconnected live deployment is claimed.

Code/template: Apache-2.0. Authored report/documentation: CC-BY-4.0. Authored synthetic task data: CDLA-Permissive-2.0. External model/runtime/dependency licences apply. No customer data, credentials, model weights or private machine paths are included.

## Current repair status (16 October 2026)

The active application uses non-thinking Chat Completions and the frozen v3-teaching cohort. New8:6/8 exact, including failures; old12 regression:12/12, not unseen. Explicit review of the original and proposed sequence is required before replay. Independent resource validation remains mandatory. This is operator attestation, not automatic semantic correctness or authentication. See track_2b/docs/REVIEW_GATE.md. Root results are historical; earlier report/video are retained under history/thinking-v1. Current root report/video are v3; current evidence is results/v3-teaching and versioned v3 materials. No new comparison or superiority claim.

## Configuration preflight amendment

LLM_NAME, LLM_BASE_URL and optional LLM_API_KEY now reach the actual local Chat Completions transport.26 native tests include real HTTP stub and make-launch positive/negative checks. No model batch was rerun;6/8 remains the frozen historical outcome. See track_2b/docs/CONFIGURATION_AMENDMENT.md and LICENSES.md. The original11db4649 source ZIP is unchanged.
