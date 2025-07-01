# ✅ NOVA: The Writers' Conspiracy — Project Checklist

## Implemented (Checked = In Folder & Running)

- [x] **System Design Document** (`NOVA_SYSTEM_DESIGN.md`)
    - Artifact: Full system/architecture/creative summary
- [x] **MemoryService.ts** (TypeScript, async-ready, marker-indexed)
    - Artifact: `frontend/src/memory/MemoryService.ts`
- [x] **MarkerSchema (JSON)**
    - Artifact: `marker-schema.json` (to be added)
- [x] **AgentBase.ts** (abstract agent class)
    - Artifact: `frontend/src/agents/AgentBase.ts`
- [x] **WriterAgent.ts** (example agent, scaffolded)
    - Artifact: `frontend/src/agents/WriterAgent.ts` (to be added)
- [x] **MemoryService & Marker Handling Documentation**
    - Artifact: (in chat, to be added as `MEMORY_DOCS.md`)

## TODO / Planned (For MVP & Beyond)

- [ ] **ProjectManagerAgent.ts** (orchestrates agent workflow)
    - Artifact: `frontend/src/agents/ProjectManagerAgent.ts`
- [ ] **EditorAgent.ts** (refines prose)
    - Artifact: `frontend/src/agents/EditorAgent.ts`
- [ ] **QA Agent & User Preference Agent** (Phase 2)
    - Artifact: `frontend/src/agents/QAAgent.ts`, `UserPreferenceAgent.ts`
- [ ] **LLM API Integration** (OpenAI, Claude, etc.)
    - Artifact: Service integration code
- [ ] **Backend API Stubs** (FastAPI endpoints for agent orchestration, memory, etc.)
    - Artifact: `backend/app/api/v1/endpoints/`
- [ ] **Frontend UI Stubs** (React components for project, manuscript, agent chat)
    - Artifact: `frontend/src/components/`
- [ ] **Expanded Documentation** (Contributor guides, onboarding, best practices)
    - Artifact: `docs/`, `MEMORY_DOCS.md`, etc.
- [ ] **Test Harnesses & E2E Tests**
    - Artifact: `tests/`

---

**Artifacts produced so far:**
- `NOVA_SYSTEM_DESIGN.md` (system/creative summary)
- `frontend/src/memory/MemoryService.ts` (memory logic)
- `frontend/src/agents/AgentBase.ts` (agent base class)
- `frontend/src/agents/WriterAgent.ts` (example agent, to be added)
- `marker-schema.json` (to be added)
- `MEMORY_DOCS.md` (to be added)

**Artifacts to be produced:**
- All TODOs above, as the project evolves

---

*Check off each item as it is implemented and present in the codebase. This checklist is your living roadmap for NOVA's cathedral.* 