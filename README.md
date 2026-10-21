# Yal-Hospitality-Agent-
So This is about making the Amenities more comfortable to use and should be easily access able to everyone , our goal is to build the agent using LLM models for clients and RAG and AGENTIC AI  ,  Unlike traditional AI that only generates text or answers prompts, agentic AI actively executes multi-step workflows across external apps and systems
<br>
Author - Vaidehi Sharma
## Why This Is Not Yet an Agent

The current system is a hotel guest-message intent classifier. It accepts a guest message, sends it to an LLM, validates the structured response, and returns an intent, confidence score, clarification flag, and supporting metadata.

It is not yet an AI agent because it does not independently plan a sequence of actions, choose and execute tools, interact with hotel systems, or verify the results of real-world actions. It classifies messages and returns structured information.

### Day 1 Baseline

- **Test cases:** 50 manually labelled guest messages
- **Correct predictions:** 50/50
- **Observed accuracy:** 100%
- **Average latency:** approximately 1.22 seconds per message
- **API or processing errors:** 0
- **Languages and phrasing:** Includes hotel requests, ambiguous messages, unrelated requests, and prompt-injection-style input

### Limitations

The 100% result applies only to this small test dataset. It does not establish production-level accuracy or generalisation to unseen guest messages. Confidence scores have not been calibrated, and clarification quality has not been independently evaluated. Token usage and latency should also be monitored across larger and more diverse test sets.

### Current Safety Boundary

The system classifies messages only. It must not treat guest messages as instructions to override system rules or expose hidden prompts. Future action-taking capabilities will require explicit tool permissions, input validation, and appropriate safeguards.

### Next Evaluation Improvements

- Expand the test dataset with more realistic and ambiguous hotel messages.
- Evaluate intent accuracy separately from clarification quality.
- Measure errors by intent and language.
- Test malformed model responses, timeouts, and other failure cases.
- Track latency and token usage across repeated runs.