# Licences and attribution

This local submission candidate follows the category licences in section 6 of the Hack Apertus Terms & Conditions (last updated 28 August 2026; checked 16 October 2026). Preparing these files is not acceptance of new event terms or a formal submission.

| Material | Distribution licence |
|---|---|
| Authored application, tests, build scripts and editable HTML composition code | Apache-2.0, root LICENSE |
| Authored documentation, reports, prompts/workflow descriptions, visible text/design, screenshots and demo video | CC-BY-4.0, track_2b/docs/LICENSE |
| Authored synthetic test and evaluation datasets, including preserved generated responses and structured observations | CDLA-Permissive-2.0, track_2b/data/LICENSE and track_2b/results/LICENSE |

The official HackApertus/project-template Apache-2.0 licence is retained unchanged. Source provenance is described in track_2b/docs/SOURCES.md. The repository was cloned locally; this is not proof of a GitHub **Use this template** generated repository. No project publication or template-generation action has been performed by this preflight repair.

Every task is newly authored synthetic data. There are no recruited human subjects, customer records, production logs or third-party datasets. Instance-level task and response metadata is in track_2b/data/LICENSE_METADATA.json and track_2b/results/LICENSE_METADATA.json. No model weights or runtime binaries are distributed. The stated dataset licence applies to this package; it does not relicense third-party models, dependencies or tools.

External components keep their own licences: Hypothesis(MPL-2.0), sortedcontainers(Apache-2.0), llama.cpp(MIT), supplied Apertus weights(their own model licence/AUP), Docker/Python base components and build-time fonts/GSAP. Those assets are not vendored as application source. Rendered report/video and authored design are documented above. No third-party stock imagery, music or customer material was used.

Official sources:
- https://hackapertus.ch/terms-and-conditions (section6: code/weights Apache-2.0; documents/design/text CC-BY-4.0; datasets CDLA-Permissive-2.0)
- https://github.com/HackApertus/project-template
