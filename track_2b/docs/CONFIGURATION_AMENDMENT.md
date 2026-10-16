# Configuration repair after frozen v3 evaluation

The original release 11db4649, model protocol 7122674 and review workflow 27d62cc remain preserved. The new8 result is still 6/8. No model inference batch was rerun and no accuracy result is transferred to an untested model/service. The original model.py bytes are archived in history/v3-model-frozen.py; audit_v3.py verifies their original frozen hash and the unchanged core/scorer/gold hashes. The original freeze JSON is unchanged.

Preflight found that LLM_NAME was only metadata and LLM_API_KEY was passed into Docker but unused. The repaired adapter sends LLM_NAME in the Chat Completions `model` field, consistently records it, and sends a nonempty LLM_API_KEY only as an `Authorization: Bearer` header. Empty key means an unauthenticated local server. The key is never put in request JSON, evidence, UI output or errors. Make exports all three variables and forwards their names, avoiding value interpolation into a shell command.

LLM_BASE_URL accepts local HTTP endpoints only:127.0.0.1, localhost, host.docker.internal or apertus. Both server base and a trailing /v1 base are accepted. URL credentials, query and fragment are rejected. Redirects are refused and environment HTTP proxies are disabled for model traffic. This keeps a key from following a redirect or local request through an unrelated proxy. External cloud URLs remain intentionally unsupported; this is an on-premise prototype.

Use the model id/alias advertised by the endpoint. A llama.cpp single-model server may ignore the request model field; setting LLM_NAME does not switch its loaded weights. To expose a stable advertised id, launch the separately provisioned server with `--alias Apertus-v1.5-8B-Q4_K_M`. Router mode uses the model field for routing. Operators must still verify the actual weights/digest, not infer them from a label.

Verification: 26 native tests, including 9 real local HTTP-stub/make-launch tests. They verify selected model/base/Bearer arrival, wrong key 401, wrong model 404, missing/invalid keys, blocked redirects, direct local traffic with deliberately broken proxy settings, URL credential/external-host rejection, exact frozen prompt/schema/sampling equality apart from the model selector, and make environment forwarding. The minimal application image passes 25 tests and explicitly skips the one host-only make test; the actual root make→Docker→host-stub positive and 401 paths were separately verified. The initial host-test-in-image failure is retained in private evidence. The stub does not prove compatibility with every LLM implementation or new model accuracy.

The five-page report and 90-second video document the original real model/UI run and retained failures. This configuration amendment changes transport support only; it does not replace that evidence. No new model runtime, terms acceptance, publication or official submission was performed.

Sources:
- https://github.com/HackApertus/project-template (the three required environment variables and Docker make run)
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (model alias, Bearer authentication and single-model/router behavior)
