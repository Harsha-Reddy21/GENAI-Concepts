import React, { useState } from 'react';

function TaskForm({ onSubmit, loading }) {
  const [taskDescription, setTaskDescription] = useState('');
  const [complexity, setComplexity] = useState('');
  const [taskType, setTaskType] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      description: taskDescription,
      complexity,
      task_type: taskType
    });
  };

  return (
    <div className="task-form">
      <h2>Describe Your Coding Task</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="taskDescription">Task Description:</label>
          <textarea
            id="taskDescription"
            value={taskDescription}
            onChange={(e) => setTaskDescription(e.target.value)}
            placeholder="Describe what you want to build or accomplish..."
            required
            rows={5}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="complexity">Task Complexity (optional):</label>
          <select
            id="complexity"
            value={complexity}
            onChange={(e) => setComplexity(e.target.value)}
          >
            <option value="">Select complexity</option>
            <option value="low">Low - Simple task</option>
            <option value="medium">Medium - Moderate complexity</option>
            <option value="high">High - Complex task</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="taskType">Task Type (optional):</label>
          <select
            id="taskType"
            value={taskType}
            onChange={(e) => setTaskType(e.target.value)}
          >
            <option value="">Select task type</option>
            <option value="web">Web Development</option>
            <option value="mobile">Mobile Development</option>
            <option value="data">Data Science/Analytics</option>
            <option value="backend">Backend/API</option>
            <option value="frontend">Frontend/UI</option>
            <option value="fullstack">Full Stack</option>
            <option value="devops">DevOps/Infrastructure</option>
            <option value="testing">Testing/QA</option>
          </select>
        </div>
        
        <button type="submit" disabled={loading || !taskDescription}>
          {loading ? 'Getting Recommendations...' : 'Get Recommendations'}
        </button>
      </form>
    </div>
  );
}

export default TaskForm; 