# Historical thinking-v1 evaluation

This document describes the preserved earlier experiment, not the current v3 protocol or review workflow. See REVIEW_GATE.md and results/v3-teaching for current outcomes.

# Interpretation and pre-registration deviations

Tasks and six exact defect implementations were frozen before the first new Apertus call (Git 976c383). The initial protocol is unchanged. A correct target and a separately labelled clean-control instance share correct behavior.

Initial adapter run: all 12 task outputs were rejected because disabled-thinking completions do not emit mandatory thinking boundaries. Raw rows remain intact. The original scorer incorrectly compared missing rejection to a null gold reason; `attempt1-rescore.json` corrects this explicitly to 0/12 exact outcomes. No candidate or execution success is inferred from these rows.

The amendment enables thinking mode and adds one fixed teaching example and explicit operation field values. These are repaired repetitions of the same task set, not new independent heldout tasks. All model candidates, invalid responses, unknown-key mistakes, errors, elapsed time, original token IDs and final answer text remain available. The simple adapter canary is separate from task accuracy, but included in repair cost. Final task responses have one attempt each after this amendment; no selection of successful retries.

Hypothesis is a real RuleBasedStateMachine generator with rule parameters drawn from the same bounded DSL. For a transparent shared shrink budget, native Hypothesis failure shrinking is disabled and both arms use the same single-deletion shrinker. This is a bounded configuration, not exhaustive tuning of mature testing tools. Stateful examples reset both reference and target. Unknown operations are allowed negative tests; malformed operations are not.

The time-budget analysis charges the complete initial failed cohort, adapter canary, repaired cohort and model startup. Those costs are amortized across all eight targets within every replicate. The same fixed model response set is reused across the five Hypothesis seeds; those are five test-generator seeds, not five independent model replications. If model overhead exhausts the 10-second target share, B executes no target calls. This time view applies predetermined availability cutoffs to measured startup/generation latency, then runs remaining target time. It is not five new cold model launches or five independently clocked generation deadline trials. In this configuration even the first valid candidate becomes available after the total80-second campaign allowance, including repair overhead. The call-budget view separately caps target calls at 800 and includes shrinking.

The protocol itself was authored with a coding assistant; independent human validation of its exact semantics has not been recorded. Canaries prove that the implemented checker detects these injected faults and that a deliberately disabled oracle fails them. They do not prove that the reference is the right real-world billing contract. A negative result checks this sequence only.

Network scope: local adapter rejects non-local model hosts. Runtime process sockets were sampled three times during actual inference and showed loopback only. This is not a full packet/syscall audit. A Docker --network none run proves deterministic replay requires no network. Live model generation inside a fully disconnected deployment must be provisioned and separately tested; no untested air-gap claim is made.

The first full comparison aborted after one clean A row because aborting Hypothesis from a rule at an external cumulative quota can trigger FlakyStrategyDefinition. The failed row is retained separately in comparison-attempt1.jsonl and excluded from final statistics. Budget enforcement now runs in the parent; a private spawned Hypothesis worker sends bounded operations over a pipe and is stopped/reaped at the quota or first divergence. Hypothesis itself receives no budget exception. An800-call clean B-arm regression with a nonzero seed offset covers this failure. No task, target, oracle or budget was changed.
