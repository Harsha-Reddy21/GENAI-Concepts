import React, { useState } from 'react';
import TaskForm from './components/TaskForm';
import RecommendationList from './components/RecommendationList';
import './styles.css';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (taskData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      setError('Error getting recommendations. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>AI Coding Agent Recommender</h1>
        <p>Find the perfect AI coding assistant for your development task</p>
        <div className="powered-by">Powered by Google Gemini</div>
      </header>
      
      <main>
        <TaskForm onSubmit={handleSubmit} loading={loading} />
        
        {error && <div className="error-message">{error}</div>}
        
        <RecommendationList recommendations={recommendations} />
      </main>
      
      <footer>
        <p>&copy; 2023 AI Coding Agent Recommender</p>
      </footer>
    </div>
  );
}

export default App; 