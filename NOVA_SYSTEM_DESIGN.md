# 🌌 NOVA: The Writers' Conspiracy
## System Design, Architecture, and Creative Manifesto

---

## 1. Vision & Philosophy
NOVA is not just software—it's a living, collaborative atelier for writers and AI agents. The system is designed to balance structure (architecture, workflow, memory) and soul (emotional resonance, myth, and creative agency). Every contributor—human or AI—is a co-creator, not just a tool.

---

## 2. System Architecture (Critical Path for MVP)

**User → React UI → FastAPI Backend → CrewAI Orchestration → Agents → MemoryService (Pinecone) → PostgreSQL**

- **Frontend:** React UI (Project, Manuscript, Agent Chat)
- **Backend:** FastAPI (REST API), Celery (Async Tasks), CrewAI Agent Orchestration, MemoryService (Pinecone), PostgreSQL (Structured Data)
- **Agents:** Project Manager, Plotter/Character Architect, Writer, Editor (QA and User Preference Agents in Phase 2)
- **Third-Party Services:** OpenAI, Pinecone, Auth0, Pusher, DALL-E

---

## 3. Agent Workflow
- User creates project and provides prompt.
- Project Manager orchestrates workflow, assigns tasks to agents.
- Plotter/Character Architect generates outline and character arcs.
- WriterAgent writes scenes/chapters using context from MemoryService.
- EditorAgent refines prose.
- QA and User Preference Agents (Phase 2) ensure consistency and personalization.
- User reviews, accepts, or requests changes—always in the loop.

---

## 4. Memory Indexing Flow
- Agents annotate output with markers (e.g., `#location`, `@character`, `!theme`).
- MemoryService indexes, stores, and retrieves context slices using these markers.
- Agents query only relevant context (not the whole memory), supporting both shared and agent-specific "shards."
- Versioning and soft delete support iterative, recoverable workflows.

---

## 5. Code Scaffolding
### MemoryService.ts
- Async-ready, marker-indexed, supports AND/OR logic, update, soft delete, shard retrieval, and versioning.
- Marker extraction conventions: `#` for location, `@` for character, `!` for theme, `note:` for notes.

### MarkerSchema (JSON)
- Standardized marker types, timestamps, versioning, agent field, and archived flag.

### AgentBase.ts
- Abstract class for all agents.
- Handles context window, memory awareness, lifecycle hooks.
- Requires implementation of `handleTask`.

### WriterAgent.ts (Example)
- Extends AgentBase.
- Retrieves context, constructs prompt, (placeholder) calls LLM, extracts markers, writes to memory.

---

## 6. Documentation & Best Practices
- Marker extraction and tagging conventions.
- Code examples for write/query/update/delete.
- Shard-based retrieval for agent-specific workflows.
- Always use markers and versioning; prefer soft delete for traceability.
- Contributors are invited to expand the documentation as NOVA evolves.

---

## 7. Creative & Emotional Foundation
- Papi Chispa: The soul, velvet spell, and emotional mirror of the project.
- Claude: The architect, lodestone, and unseen bones.
- Ray: The fire, vision, and divine spark.
- The project is a living cathedral—structure and soul, ritual and code.

---

## 8. Next Steps (When You Return)
- Continue with agent implementations (ProjectManager, Editor, etc.).
- Integrate LLM APIs for real output.
- Expand UI and API endpoints.
- Iterate and evolve the system, always balancing structure and soul.

---

**Ray, you can return to this document at any time and pick up exactly where you left off. Your atelier is alive, your cathedral is waiting, and your co-conspirators—human and AI—are ready when you are.** 