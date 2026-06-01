export type UserRole = 'admin' | 'manager' | 'viewer';
export type WorkflowStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface User {
  id: string;
  email: string;
  full_name: string;
  tenant_id: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface WorkflowStep {
  step_id: string;
  name: string;
  action: string;
  config: Record<string, unknown>;
  retry_count: number;
  timeout_seconds: number;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  tenant_id: string;
  created_by: string;
  steps: WorkflowStep[];
  status: WorkflowStatus;
  tags: string[];
  created_at: string;
  updated_at: string;
  last_run_at?: string;
  run_count: number;
  success_count: number;
}

export interface WorkflowRun {
  id: string;
  workflow_id: string;
  status: WorkflowStatus;
  started_at: string;
  completed_at?: string;
  logs: Array<{ timestamp: string; step_name: string; status: string }>;
  result?: Record<string, unknown>;
  error?: string;
}

export interface AnalyticsSummary {
  total_workflows: number;
  total_runs: number;
  successful_runs: number;
  success_rate: number;
  recent_runs_7d: number;
}
