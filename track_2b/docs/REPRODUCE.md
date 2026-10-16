# Reproduce SafeRouter ReplayLab

Python 3.12+, Docker and a locally administered Apertus endpoint. Code: Apache-2.0; authored synthetic task data: CDLA-Permissive-2.0; documentation/report: CC-BY-4.0. Template copyright and LICENSE retained.

From repository root:

```
make run
```

Opens http://127.0.0.1:19564 . Default is evidence inspection and deterministic replay, explicitly using recorded model output. Click Live Generate only with your local Apertus configured. An unavailable endpoint produces an error; it never substitutes a fixture.

`LLM_NAME`, `LLM_BASE_URL`, `LLM_API_KEY` are exposed as required by the template. A nonempty LLM_API_KEY is sent as an Authorization Bearer header; an empty key omits authentication. LLM_NAME is sent as the model selector, not only a display label. It refuses external model hosts. Only local hosts are allowed; other server implementations need explicit wire-contract validation.

For native local development:

```
python -m venv .venv
.venv/bin/pip install -r track_2b/requirements.txt
.venv/bin/python track_2b/src/server.py
.venv/bin/python -m unittest discover -s track_2b/tests -v
```

Downloaded counterexamples replay without a model, network, Hypothesis, or model weights:

```
python track_2b/src/replay.py replaylab-counterexample.json
```

Live model, supplied separately under its own licence:

```
llama-server -m /models/apertus-v1.5-q4.gguf --host 127.0.0.1 --port 19464 -t 2 -tb 2 -np 1 -c 4096 -ngl 0 --jinja --alias Apertus-v1.5-8B-Q4_K_M
```

This exact model was already available locally. Weights SHA256: a037df8d87ff6caacee794ee85f55342f2152e0d359b7389033300c3bee5f299. Runtime: llama.cpp b11429, d81235049. CPU 2 threads, GPU disabled, one parallel slot. Do not distribute the model in this repository. Official upstream: https://huggingface.co/swiss-ai/Apertus-v1.5-8B . The exact local quantization origin is not independently certified; the digest fixes the tested file. It is not a fine-tuned model.

The selected adapter uses `/v1/chat/completions`, fixed JSON schema, `enable_thinking=false`, temperature0, seed42 and max_tokens450. Two fixed synthetic teaching examples distinguish retry/key identity and total counts. A complete stop response is JSON-parsed and passed to an independent validator. No thinking-token markers are required. Full request, raw response and timings are retained; gold and target labels are never sent. See REVIEW_GATE.md for mandatory explicit review before replay and the unchanged 6/8 new-task outcome.

The historical thinking-v1 comparison consumed all schema-valid model seeds, including contract-inexact ones. The correct/clean controls are always included. A and B share reference, targets, DSL and a deletion shrinker. Hypothesis stateful is used with generate phase, database disabled, 12 steps, and fixed seeds. This is one bounded stateful configuration, not the strongest possible Hypothesis campaign; Hypothesis native failure shrinking is replaced by the same explicit shrinker in both arms.

Call view: 800 target operation calls per target/seed/arm, including candidate execution and shrinking. Time view: 10 seconds per target/seed/arm, including amortized model startup and generation. Model output is shared across targets; the full measured cost is divided equally across all eight targets in each independent replicate. It is not charged once per target and not silently omitted. Preparation/specification authoring is separate and was not timed. No monetary model fee, production API use, human productivity measure, or statistical superiority is claimed.

Current records are results/v3-teaching; the server intentionally reads that cohort. Root results are historical evidence and do not measure v3. Earlier report/video are retained in history/thinking-v1; current root report/video are v3.

To rerun inference/comparison, create a fresh output directory or preserve the old results first: runners intentionally refuse overwriting evidence. Read the experiment amendment before interpreting repaired adapter repetitions as independent tests.

## Deployment boundary

On-premise is the target. Download model and Python/Docker dependencies during preparation, then use local inference. Deterministic recorded replay works with Docker `--network none`. Live local inference needs the explicitly configured local model host. Strict air-gapped live inference is a deployment option only after all model/runtime assets are provisioned inside the same disconnected environment; no Swiss cloud deployment is claimed.

This is a deliberately synchronous router simulation. It does not call an actual provider, test real transport streaming, execute generated code, or operate production funds. A fixed reference may itself be wrong; canaries establish the narrow test chain, not the specification's correctness.

See CONFIGURATION_AMENDMENT.md for the post-freeze transport repair,26 stub-inclusive tests, local-host policy and the unchanged historical6/8 accuracy result. Choose the endpoint's advertised model alias; the variable cannot change weights in a single-model server.
