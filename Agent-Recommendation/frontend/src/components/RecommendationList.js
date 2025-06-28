import React from 'react';
import AgentCard from './AgentCard';

function RecommendationList({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  return (
    <div className="recommendations">
      <h2>Top Recommended AI Coding Agents</h2>
      <div className="recommendation-list">
        {recommendations.map((rec, index) => (
          <AgentCard 
            key={index}
            agent={rec.agent}
            justification={rec.justification}
            score={rec.score}
          />
        ))}
      </div>
    </div>
  );
}

export default RecommendationList; 