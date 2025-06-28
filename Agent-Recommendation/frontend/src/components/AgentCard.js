import React from 'react';

function AgentCard({ agent, justification, score }) {
  return (
    <div className="agent-card">
      <div className="agent-header">
        <h3>{agent.name}</h3>
        <div className="agent-score">
          Match: {Math.round(score * 100)}%
        </div>
      </div>
      
      <p className="agent-description">{agent.description}</p>
      
      <div className="agent-details">
        <div className="strengths">
          <h4>Strengths</h4>
          <ul>
            {agent.strengths.map((strength, index) => (
              <li key={index}>{strength}</li>
            ))}
          </ul>
        </div>
        
        <div className="integration">
          <h4>Integrations</h4>
          <p>{agent.integration.join(', ')}</p>
        </div>
      </div>
      
      <div className="justification">
        <h4>Why this is recommended:</h4>
        <ul>
          {justification.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      </div>
      
      <div className="agent-footer">
        <p><strong>Learning curve:</strong> {agent.learning_curve}</p>
        <p><strong>Cost:</strong> {agent.cost}</p>
      </div>
    </div>
  );
}

export default AgentCard; 