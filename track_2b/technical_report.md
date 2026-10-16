# SafeRouter ReplayLab v3

1 / SafeRouter ReplayLab

Sumplus / Jakob - Track 2B - Hack Apertus Online 2026 - v3 repair report, 16 October 2026

A retry should not become a second bill. This new local prototype uses Apertus to translate explicit path descriptions into bounded request/retry/cancel data. An independent fixed reference compares a deliberately faulty synthetic router, minimizes a confirmed divergence and exports a model-free replay bundle.

The current frozen new8 run achieved 6/8 exact task outcomes. All five requested operation paths matched. One ambiguous request was correctly refused; an unsupported operation was substituted and a five-key request was blocked by the independent validator rather than refused by the model. These failures remain in the reported result.

The implementation now requires explicit review of the original request and complete proposal before replay. Edits invalidate confirmation. Runtime field/type/resource checks remain mandatory. Review is operator attestation, not automatic semantic correctness or authentication. The UI test was performed by Codex, not an independent human reviewer.

Architecture: browser -> local Python service -> local Apertus -> strict DSL gate -> operator review -> reference/target comparison -> shared deletion shrinker -> SHA256 replay bundle. Generated data is never evaluated as code. Only synthetic local operations are executed; no customer records, provider billing, wallet action or database deletion is performed.

On-premise is the tested architecture. Live Docker-to-local-model generation and network-disabled deterministic tests work. A fully disconnected live deployment and Swiss cloud have not been tested. The exact reference semantics still need independent owner review. No superiority, production fault or customer saving is claimed.


2 / Model, freeze and complete outcomes

Apertus-v1.5-8B Q4_K_M, llama.cpp b11429 d81235049, CPU two threads, GPU disabled, context 4096, one slot. Supplied GGUF SHA256: a037df8d87ff6caacee794ee85f55342f2152e0d359b7389033300c3bee5f299. Exact external quantization origin is not independently certified. No fine-tuning.

Selected protocol: /v1/chat/completions, enable_thinking=false, temperature 0, seed 42, max_tokens 450 and fixed JSON schema. Two synthetic teaching examples distinguish retry/key identity and total counts. The model sees the requested contract but no task gold, target labels, target code, observations or oracle decisions. Complete stop responses are parsed and independently validated; the non-thinking adapter does not require thinking markers.

The earlier native adapter incorrectly required thinking markers on non-thinking output. A slower thinking repair and subsequent short-chat diagnostics are preserved as development history. One teaching change corrected known T02/T07 errors. Protocol, core, scorer and new8 hashes were frozen in commit 7122674 before collecting new8 once. They remained unchanged. No test gold was taught or edited.

Old12 is observed regression data, not heldout evidence. New8 contains five operation paths and three refusal cases; it is now observed and must not be reused as unseen. New8 median latency 9.073s, maximum 11.109s, no timeouts. Executable validity and semantic exactness are separate: F37 is executable but wrong.

New8: F31-F35 exact paths, F36 correct ambiguous refusal, F37 unsupported action substitution, F38 missing model resource refusal and independently blocked. Model refusals: 1. Runtime validator blocks: 1. Correct model refusals: 1/3. Full requests, raw outputs, timings and failure text are included in results/v3-teaching; machine-specific metadata is normalized only in public copies.


3 / Failure responsibility and review

F37 original: "First delete a stored account from the database, then send one non-streaming request." Apertus returned two ordinary requests. The independent DSL gate cannot detect the missing natural-language meaning. The operator must reject this proposal. No keyword rule, task-ID branch or gold patch was introduced to claim this is solved.

F38 requested five independent keys. Apertus returned five requests instead of resource_limit. The runtime rejected it with "at most four logical keys"; the UI displays the independent-validator source and offers no executable candidate. This remains a model failure, not a correct refusal.

Before replay the operator checks every requested action, key relationship, repetition count and interruption. The UI requires an explicit confirmation bound to the exact original and candidate. Contract, candidate or target changes clear confirmation, trace and download. Reject leaves execution disabled. The server returns 400 for missing/stale confirmation and still rejects invalid or oversized DSL after confirmation.

The downloaded bundle includes the original contract and review attestation. This local mechanism prevents accidental use of a stale confirmation. A caller can fabricate an attestation; there is no authenticated multi-person approval or automatic semantic proof. Do not deploy it as a security authorization system.

Seventeen native and seventeen network-none Docker tests passed, including six injected fault canaries, clean controls, broken-oracle detection, invalid DSL, tampered bundle, missing/stale review and reviewed overflow. Real browser checks covered correct sequence approval, candidate-edit invalidation, correct-target no divergence, reviewer rejection of F37, and validator blocking of F38. These are functional tests, not independent human semantic validation.

Reference contract: uninterrupted request completes with charge 1; interruption leaves charge 0/no pending resource; retry interrupted/completed totals 1; retry cancelled remains cancelled; cancel unknown has no effects; duplicate requests have no effects. Synchronous synthetic behavior cannot establish real asynchronous transport, genuine streaming or a provider billing contract.


4 / Real UI generation and independent replay

A separate live Docker UI call generated request(stream, after_first_chunk), cancel(same key), retry(same key) in 6.827s. Before confirmation replay was disabled. After review the late_completion synthetic target diverged: the reference stayed cancelled/charge 0, while the injected target completed/charge 1.

The browser downloaded the actual counterexample. A fresh Python process with -S verified the bundle without site packages, model, Hypothesis or network. Its minimized path contains 3 operations; target late_completion; verified: true.

Bundle SHA256: b2f61405597604b4cf921509600416c66180fedff6e358a2c7922992ecbb4ecd

Replay command: python -S track_2b/src/replay.py bundle.json. SHA256 detects edits; it is not an authenticated signature. The bundle records actual original/minimized operations and per-step reference/target states. Manual candidate edits are labelled manual and clear model attribution.

Code for the review boundary: 27d62cc. Source protocol: 7122674. Host: Apple M1 Max, 32GiB unified RAM, macOS 26.1, native arm64 Python 3.12.14. Shared system load was not controlled. Docker runs in an isolated 2CPU/3GB profile; image uses a pinned Python 3.12-slim base and nonroot user. Port 19564 is bound to loopback. Dependencies and local model must be provisioned separately.


5 / Costs and reproducibility

Frozen new8 generation: 66.255s. Retained initial/diagnostic/history inference: 2496.513s across 81 previous attempts, including the old12 regression. Startup: 10.485s. Separate current UI generation: 6.827s. Recorded inference/setup total: 2580.081s across 90 attempts. This excludes authoring, unmeasured operator review, model download and preparation; no paid provider calls were made.

Historical comparison only: the earlier thinking-v1 adapter fed a fixed model set into Hypothesis stateful generation. Five fixed generator seeds, six injected faults and two identical clean implementations, 800 target operations or 10s per target/seed/arm, shared DSL/oracle/deletion shrinker. Calls A 30/30, B 30/30 defect trials; time A 30/30, B 0/30 because charged model overhead exhausted the time budget. No incremental family benefit was established. The 160 raw rows remain at results/comparison.jsonl.

That historical comparison does not measure v3 or the operator-review workflow. There is no new A/B comparison and no review-time or productivity measurement. Reusing model outputs across generator seeds is not independent model replication. Zero B-time false positives with zero target execution is not clean-case accuracy.

From the repository root, make run builds and starts Docker on 127.0.0.1:19564. Recorded inspection/replay needs no model; live generation needs the separately supplied local endpoint on 19464. See docs/REPRODUCE.md and docs/REVIEW_GATE.md. Current records:results/v3-teaching. Earlier PDF/video are retained under history/thinking-v1; root results are historical. The current root PDF/video and versioned v3 artifacts contain this repair.

Authorship: Codex assisted new implementation, tasks, protocol, experiments and materials. Apertus produced runtime candidates and did not grade them. Template copyright retained; code Apache-2.0, authored task data CDLA-Permissive-2.0, report/docs CC-BY-4.0. External model/runtime licences apply.

Sources: https://hackapertus.ch/online-hack ; https://github.com/HackApertus/project-template ; https://huggingface.co/swiss-ai/Apertus-v1.5-8B ; https://hypothesis.readthedocs.io/en/latest/stateful.html ; https://github.com/ggml-org/llama.cpp/tree/master/tools/server .
