# LangGraph Zero to Advanced — Roadmap Tracker

## Purpose

This document is the authoritative tracker for the 86-topic LangGraph curriculum.

- **Roadmap topic numbers** preserve the original learning sequence.
- **Repository lesson numbers** identify practical exercises and may differ from roadmap numbers.
- Supplementary deep dives do not replace or reorder roadmap topics.
- Passing tests proves implementation behavior, not necessarily conceptual mastery.

## Status definitions

- [ ] **Not started**
- [~] **In progress**
- [x] **Implemented and tested**
- [M] **Mastered** — implementation, explanation, edge cases, and review completed

A topic should only be marked mastered after its concepts have been explained, implemented where appropriate, tested, and reviewed.

---

## Phase 1 — Core Graph Model

| Topic | Concept | Status |
|---:|---|---|
| 05 | State | [x] Implemented; mastery to verify |
| 06 | Nodes | [x] Implemented; mastery to verify |
| 07 | Edges | [x] Implemented; mastery to verify |
| 08 | START / END | [x] Implemented; mastery to verify |
| 09 | State updates | [x] Implemented and tested |
| 10 | Reducers | [x] Implemented and tested |

**Existing work:** Python workflow foundations and repository lessons 11–17 cover state updates, reducers, custom reducers, parallel updates, and fan-in. Core graph concepts need a systematic review against the official LangGraph curriculum.

## Phase 2 — Messages & LLM State

| Topic | Concept | Status |
|---:|---|---|
| 11 | Messages | [ ] |
| 12 | MessagesState | [ ] |
| 13 | Message reducers | [ ] |
| 14 | HumanMessage / AIMessage / ToolMessage / SystemMessage | [ ] |
| 15 | Message history | [ ] |

## Phase 3 — Control Flow

| Topic | Concept | Status |
|---:|---|---|
| 16 | Conditional edges | [x] Implemented; mastery to verify |
| 17 | Routing | [x] Implemented; mastery to verify |
| 18 | Loops | [x] Implemented and tested |
| 19 | Recursion limits | [x] Implemented and tested |
| 20 | Command | [x] Implemented and tested |
| 21 | Send | [x] Implemented and tested |
| 22 | Map-reduce / fan-out / fan-in | [x] Implemented and tested |

**Existing work:** Repository lessons 18–25 include conditional routing, loops, `Command`, `Send`, and map-reduce. Some concepts will receive a structured review after Phase 2.

## Phase 4 — Persistence & Execution

| Topic | Concept | Status |
|---:|---|---|
| 23 | Checkpointers | [ ] |
| 24 | Threads | [ ] |
| 25 | Persistence model | [ ] |
| 26 | State snapshots | [ ] |
| 27 | Durable execution | [ ] |
| 28 | Fault recovery | [ ] |
| 29 | Retry semantics | [ ] |
| 30 | Time travel / replay | [ ] |

## Phase 5 — Memory

| Topic | Concept | Status |
|---:|---|---|
| 31 | Short-term memory | [ ] |
| 32 | Long-term memory | [ ] |
| 33 | Threads vs memory | [ ] |
| 34 | Memory stores | [ ] |
| 35 | Memory design patterns | [ ] |

## Phase 6 — Streaming

| Topic | Concept | Status |
|---:|---|---|
| 36 | Streaming | [ ] |
| 37 | Stream modes | [ ] |
| 38 | State streaming | [ ] |
| 39 | Message streaming | [ ] |
| 40 | Custom streaming | [ ] |
| 41 | Streaming events | [ ] |

## Phase 7 — Human-in-the-Loop

| Topic | Concept | Status |
|---:|---|---|
| 42 | Interrupts | [ ] |
| 43 | Human-in-the-loop | [ ] |
| 44 | Inspect state | [ ] |
| 45 | Modify state | [ ] |
| 46 | Resume execution | [ ] |

## Phase 8 — Subgraphs & Architecture

| Topic | Concept | Status |
|---:|---|---|
| 47 | Subgraphs | [ ] |
| 48 | Parent graph | [ ] |
| 49 | Child graph | [ ] |
| 50 | State boundaries | [ ] |
| 51 | Subgraph communication | [ ] |
| 52 | Multi-stage architecture | [ ] |

## Phase 9 — Runtime & Context

| Topic | Concept | Status |
|---:|---|---|
| 53 | Runtime | [ ] |
| 54 | Context | [ ] |
| 55 | Runtime configuration | [ ] |
| 56 | Dependency/context passing | [ ] |
| 57 | Execution metadata | [ ] |
| 58 | Store | [ ] |

## Phase 10 — Tools & Agents

| Topic | Concept | Status |
|---:|---|---|
| 59 | Tools | [ ] |
| 60 | Tool calling | [ ] |
| 61 | Tool execution | [ ] |
| 62 | Tool nodes | [ ] |
| 63 | Agent state | [ ] |
| 64 | Agent loops | [ ] |
| 65 | Model decisions | [ ] |
| 66 | Agent middleware | [ ] |
| 67 | Agent customization | [ ] |

## Phase 11 — Multi-Agent Systems

| Topic | Concept | Status |
|---:|---|---|
| 68 | Multi-agent architectures | [ ] |
| 69 | Agent state design | [ ] |
| 70 | Supervisor pattern | [ ] |
| 71 | Handoff pattern | [ ] |
| 72 | Network pattern | [ ] |
| 73 | Hierarchical agents | [ ] |
| 74 | Agent collaboration | [ ] |

## Phase 12 — Production Engineering

| Topic | Concept | Status |
|---:|---|---|
| 75 | Deployment | [ ] |
| 76 | Scaling | [ ] |
| 77 | Background execution | [ ] |
| 78 | Authentication | [ ] |
| 79 | Reliability | [ ] |
| 80 | Error handling | [ ] |
| 81 | Retries | [ ] |
| 82 | Idempotency | [ ] |
| 83 | Observability | [ ] |
| 84 | LangSmith | [ ] |
| 85 | Testing | [ ] |
| 86 | Production architecture | [ ] |

## Supplementary Track — Langfuse Observability

This is additional to the original 86 topics, not a replacement for any of them.

- [ ] Langfuse setup and configuration
- [ ] Trace and span fundamentals
- [ ] LangGraph tracing
- [ ] Run inspection and debugging
- [ ] Evaluation and observability practices

## Learning rules

1. Follow the original phase and topic order.
2. Explain the concept before introducing implementation.
3. Use runnable examples in the repository.
4. Test normal behavior, edge cases, and failure paths where relevant.
5. Include exercises and review questions.
6. Mark implemented topics separately from mastered topics.
7. Keep supplementary deep dives linked to the topic they reinforce.
8. Run the full regression suite before publishing meaningful changes.
9. Commit and push only after verifying the intended files and test results.

## Current checkpoint

- **Repository lessons completed:** through Lesson 25.
- **Last published commit:** `355bf8d`.
- **Next roadmap topic:** 11 — Messages.
- **Next action:** study and implement messages in LangGraph before advancing to MessagesState.
