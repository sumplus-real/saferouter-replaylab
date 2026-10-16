# Sources and assistance

Official HackApertus/project-template (Apache-2.0) was cloned to prepare this local prototype. The local working copy retains the official track_2b layout and template licence.

New code, task contracts, reference and synthetic defects were authored in this project on 15 October 2026. No old competition project code or private customer data were imported. The initial external research sequence-generation file was read as historical context; it is not counted in this evaluation.

Apertus 1.5 8B Q4_K_M performs runtime sequence proposal. It sees only the DSL and task contract. It does not see target implementations, mutant labels, gold paths, or expected observations. It does not grade results or approve actions. Model response failures are retained.

OpenAI Codex assisted implementation, experiment plumbing, documentation, and demo composition. It did not serve as the runtime model, replace Apertus responses, or grade counterexamples. The protocol and expected task paths were authored with Codex assistance and frozen before Apertus inference. Program code checks equivalence. An independent human review of the detailed oracle has not been recorded; this remains a limitation. No extra model provider calls or paid inference were purchased for the prototype.

Dependencies: Python standard library; Hypothesis 6.151.9 (MPL-2.0); sortedcontainers 2.4.0 (Apache-2.0); Docker python:3.12-slim base (its component licences apply). llama.cpp (MIT) and Apertus weights are external runtime assets, not checked into this project. Generated report uses standard local PDF tools; demo uses local rendering tooling. No third-party music/images/customer records.

References:
- https://github.com/HackApertus/project-template
- https://hackapertus.ch/online-hack
- https://hackapertus.ch/terms-and-conditions
- https://huggingface.co/swiss-ai/Apertus-v1.5-8B
- https://github.com/ggml-org/llama.cpp/tree/master/tools/server
- https://hypothesis.readthedocs.io/en/latest/stateful.html

Only machine-local model path metadata is normalized to a basename in publishable structured responses; answer text, token IDs and timings are unchanged. Raw structured responses are not HTTP byte captures. A separate post-evaluation live UI check is retained as ui-live-acceptance.json and is excluded from the12-task comparison; its additional model time is disclosed separately in the report.

Post-freeze configuration amendment:the repository remains a local clone, not a verified GitHub template-generated project. The new transport supports actual model selector and optional Bearer key. The report/video retain the original measured run; CONFIGURATION_AMENDMENT.md records stub-only validation. Root LICENSES.md and data/results licence metadata map the authored materials to official category licences.
