import React from 'react';
import type { Workflow } from '../types';

interface Props { workflow: Workflow; onRun: (id: string) => void; }

const statusColors: Record<string, string> = {
  pending: '#f59e0b', running: '#3b82f6', completed: '#10b981', failed: '#ef4444',
};

export const WorkflowCard: React.FC<Props> = ({ workflow, onRun }) => {
  const successRate = workflow.run_count > 0 ? Math.round((workflow.success_count / workflow.run_count) * 100) : 0;
  return (
    <div style={{ border: '1px solid #e5e7eb', borderRadius: 12, padding: 20, background: '#fff', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>{workflow.name}</h3>
          <p style={{ margin: '4px 0 0', color: '#6b7280', fontSize: 14 }}>{workflow.description}</p>
        </div>
        <span style={{ background: statusColors[workflow.status] + '20', color: statusColors[workflow.status], padding: '2px 10px', borderRadius: 20, fontSize: 12, fontWeight: 500 }}>
          {workflow.status}
        </span>
      </div>
      <div style={{ display: 'flex', gap: 16, marginBottom: 12, fontSize: 13, color: '#6b7280' }}>
        <span>{workflow.steps.length} steps</span>
        <span>{workflow.run_count} runs</span>
        <span>{successRate}% success</span>
      </div>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 16 }}>
        {workflow.tags.map(tag => (
          <span key={tag} style={{ background: '#f3f4f6', color: '#374151', padding: '2px 8px', borderRadius: 6, fontSize: 12 }}>{tag}</span>
        ))}
      </div>
      <button onClick={() => onRun(workflow.id)}
        style={{ background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 16px', cursor: 'pointer', fontSize: 14, fontWeight: 500, width: '100%' }}>
        Run Workflow
      </button>
    </div>
  );
};
