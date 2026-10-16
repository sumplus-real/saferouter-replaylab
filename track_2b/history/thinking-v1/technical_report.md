# SafeRouter ReplayLab

Track 2B - Hack Apertus Online 2026
Team Sumplus - Jakob

## 1. Summary

SafeRouter ReplayLab converts explicit retry/cancel path descriptions into bounded test candidates with a locally served Apertus 1.5 model. A predefined protocol compares a separate reference and six deliberately faulty synthetic routers. Confirmed counterexamples can be minimized, downloaded and replayed without a model or network. This is a new local prototype started on 15 October 2026; no real provider calls, customer records or production billing are used. The comparison does not establish superiority over Hypothesis.

## 2. Architecture and target deployment

On-premise: browser -> local Python service -> local Apertus -> strict DSL validation -> fixed reference and synthetic target -> shared deletion shrinker -> JSON replay bundle. Generated data is never evaluated as code. Only request, retry and cancel are allowed, with 1-12 operations and at most four keys. JSON fields, types, resource bounds and cross-field consistency are validated.

The browser supports explicit recorded-response inspection and local live generation; an unavailable or invalid model answer is an error, never a hidden fixture. Target selection is not sent to the model. Correct/clean targets, six fault canaries, a disabled-oracle canary and tampered bundles exercise the verification chain. Runtime inference is local; socket observations cover only sampled instants, not a complete egress audit. Docker network-none replay was tested. Disconnected live deployment and Swiss cloud were not tested.

## 3. Use of Apertus

Apertus-v1.5-8B Q4_K_M, external pre-existing GGUF SHA256 a037df8d87ff6caacee794ee85f55342f2152e0d359b7389033300c3bee5f299. llama.cpp b11429 d81235049, CPU two threads, GPU off, context 4096, one slot, temperature 0 seed 42. No fine-tuning. Native apply-template/completion/detokenize adapter requires exact ordered token32/33 thinking boundaries and parses only the final tail. Missing/duplicate boundaries and truncated/invalid output fail closed. Model raw responses and timings are preserved. Exact quantization origin beyond the recorded file digest is not independently certified.

Apertus sees DSL instructions, one teaching example and the task contract. It never sees mutant labels, source, gold paths, expected observations or acceptance decisions. The coding assistant helped author the fixed protocol and code; independent human validation of exact oracle semantics has not been recorded.

## 4. Data, development and sources

Twelve new synthetic tasks (ten executable paths, two rejection cases), six injected fault families and two clean labels were frozen before inference (976c383). English and German task text contains no personal data. Initial disabled-thinking adapter: all 12 outputs rejected. The original missing-rejection/null scorer bug is explicitly corrected in attempt1-rescore.json; original raw rows are retained. An adapter amendment enables thinking and clarifies operation fields using one teaching example; the same 12 tasks are repeated once. These repetitions are not independent heldout evidence.

The repaired set yielded 4/12 executable candidates and 3/12 exact task outcomes including rejection cases. All invalid responses count. Initial cohort and one diagnostic canary add 328.54s; repaired generation 1781.52s; startup 10.49s. Measured comparison-pipeline inference/setup time 2120.54s across 25 model attempts. No customer usage or human productivity claim.

## 5. Evaluation

A: Hypothesis 6.151.9 RuleBasedStateMachine. B: same generator after all schema-valid model seeds, including contract-inexact seeds. Same DSL, reference, targets and deletion shrinker. Five fixed generator seeds 17,29,43,71,101. Native Hypothesis shrinking disabled to share explicit budget accounting; this is one bounded tool configuration, not exhaustive baseline tuning.

A failed initial comparison row is retained separately; parent-process budget enforcement fixes the observed Hypothesis interruption conflict. Each target/seed/arm has either 800 target-operation calls or 10 seconds. Candidate execution and shrinking count. The time view includes full startup and all failed/repaired generation cost amortized across eight targets in every replicate. The time view applies fixed availability cutoffs to measured inference latency, not five fresh cold model deadline launches. Same saved model responses are reused for the five generator seeds, not five independent model draws.

| Budget | Arm | Fault trials found | Clean false positives |
|---|---|---|---|
| calls | A | 30/30 | 0 |
| calls | B | 30/30 | 0 |
| time | A | 30/30 | 0 |
| time | B | 0/30 | 0 |

Median time to first counterexample: call view A 0.199s, B 265.068s, including model cost. Time view A 0.178s; B has no observation because its budget expires before any target call. The zero B-time false-positive count is not a tested clean-case accuracy rate. Extra discovered families in B:0. Total target operations in the call view: A 11690, B 9014; these are local synthetic operations, not paid provider calls.

All 160 expected trial rows are present; 90 discovered minimized traces independently replay. Family-level counts and every undiscovered run remain in comparison.jsonl and summary.json. This small synthetic campaign supports no statistical or production superiority claim.

## 6. Limitations

No true asynchronous transport, real streaming, provider integration, concurrent race coverage, security audit, production billing verification, participant study or customer use. A late retry is a synchronous late-completion proxy. Reference agreement does not prove natural language correctness. The protocol is assistant-authored and requires owner review. Schema-valid candidates can violate a requested path. Tokenizer IDs and native adapter are model-specific. Startup uses pre-existing weights and excludes download; specification authoring/preparation were not timed. Model repair repetitions weaken independent generalization evidence. SHA256 detects accidental changes but is not an authenticated signature.

## 7. Reproducibility

Code version: fb782abe4bd18cb996a9de816aff6abc125b4ddc. Root make run builds a Docker image and starts port19564. Recorded evidence inspection/replay needs no model; live generation requires separately provisioned local Apertus. See docs/REPRODUCE.md for exact runtime and environment variables LLM_NAME, LLM_BASE_URL, LLM_API_KEY. Download a bundle and run python track_2b/src/replay.py bundle.json. The full original candidates and seed-by-target raw results are included.

A separate post-evaluation live UI functional check generated a valid one-request sequence in 27.37s. The correct target stayed clean, the injected legal-rejection target diverged, and the downloaded bundle replayed in a fresh Python process. This 26th model attempt and its time are separate from the 25-attempt comparison pipeline, not another independent performance trial.

## 8. Next steps

Independently review the protocol, add a real asynchronous adapter, preregister new untouched task families and compare stronger Hypothesis configurations before assessing practical incremental value.

## Licence and assistance

Template and code Apache-2.0; report/documentation CC-BY-4.0; newly authored synthetic task data CDLA-Permissive-2.0. External model/runtime/dependency licences apply. Codex assisted code, protocol, experiments and local material creation; Apertus alone generated runtime candidates. No additional paid inference or provider calls. See docs/SOURCES.md.

## References

https://github.com/HackApertus/project-template
https://hackapertus.ch/online-hack
https://huggingface.co/swiss-ai/Apertus-v1.5-8B
https://hypothesis.readthedocs.io/en/latest/stateful.html
https://github.com/ggml-org/llama.cpp/tree/master/tools/server
