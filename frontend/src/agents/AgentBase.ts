// Remove the import for MemoryService and related types
// import { MemoryService, MemoryEntry, MemoryMarker } from '../memory/MemoryService';

export interface AgentConfig {
  id: string;
  name: string;
  persona: string;
  contextWindow: number; // Max number of memory entries to use
  shard?: string; // Optional: agent-specific memory shard
}

export interface AgentTask {
  id: string;
  type: string;
  input: any;
  markers?: Partial<MemoryMarker>[];
  userId?: string;
}

// Local placeholder for MemoryService and related types
export interface MemoryMarker {
  id: string;
  type: string;
  value: string;
  agent?: string;
  timestamp: string;
  version?: number;
}

export interface MemoryEntry {
  id: string;
  content: string;
  markers: MemoryMarker[];
  createdAt: string;
  updatedAt?: string;
  version?: number;
}

export class MemoryService {
  async queryMemory(params: { markers: Partial<MemoryMarker>[]; agent?: string }): Promise<MemoryEntry[]> {
    return [];
  }
  async writeMemory(entry: Omit<MemoryEntry, 'id' | 'createdAt'>): Promise<MemoryEntry> {
    return {
      id: 'placeholder',
      content: entry.content,
      markers: entry.markers,
      createdAt: new Date().toISOString(),
      version: entry.version,
    };
  }
}

export abstract class AgentBase {
  protected config: AgentConfig;
  protected memoryService: MemoryService;

  constructor(config: AgentConfig, memoryService: MemoryService) {
    this.config = config;
    this.memoryService = memoryService;
  }

  // Main entry point for agent work
  async runTask(task: AgentTask): Promise<any> {
    const context = await this.getContext(task);
    return this.handleTask(task, context);
  }

  // Retrieve relevant context for this agent and task
  protected async getContext(task: AgentTask): Promise<MemoryEntry[]> {
    const markers = task.markers || [];
    const entries = await this.memoryService.queryMemory({
      markers,
      agent: this.config.shard,
    });
    // Limit to context window size
    return entries.slice(-this.config.contextWindow);
  }

  // Each agent must implement its own task handler
  protected abstract handleTask(task: AgentTask, context: MemoryEntry[]): Promise<any>;

  // Optional: hook for post-task memory write
  protected async writeMemory(entry: Omit<MemoryEntry, 'id' | 'createdAt'>) {
    return this.memoryService.writeMemory(entry);
  }

  // Optional: lifecycle hooks
  onStart?(task: AgentTask): void;
  onFinish?(task: AgentTask, result: any): void;
  onError?(task: AgentTask, error: Error): void;
} 