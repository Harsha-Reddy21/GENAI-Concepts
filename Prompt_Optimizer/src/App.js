import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container, Box, Typography, TextField, Button, MenuItem,
  Paper, Grid, CircularProgress, Divider, Chip
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import './App.css';

// Create a theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  const [basePrompt, setBasePrompt] = useState('');
  const [selectedTool, setSelectedTool] = useState('');
  const [additionalContext, setAdditionalContext] = useState('');
  const [optimizedPrompt, setOptimizedPrompt] = useState('');
  const [explanation, setExplanation] = useState('');
  const [loading, setLoading] = useState(false);
  const [tools, setTools] = useState([]);
  const [error, setError] = useState('');

  // Fetch available tools on component mount
  useEffect(() => {
    const fetchTools = async () => {
      try {
        console.log('Fetching tools from backend...');
        const response = await axios.get('http://localhost:8000/tools');
        console.log('Tools response:', response.data);
        
        if (response.data.tools && response.data.tools.length > 0) {
          setTools(response.data.tools);
          setSelectedTool(response.data.tools[0]);
          console.log('Selected tool set to:', response.data.tools[0]);
        } else {
          console.warn('No tools found in response');
          // Set some default tools in case the backend fails
          const defaultTools = ["GitHub Copilot", "Cursor", "Replit", "Amazon CodeWhisperer", "Tabnine", "Codeium"];
          setTools(defaultTools);
          setSelectedTool(defaultTools[0]);
        }
      } catch (err) {
        console.error('Error fetching tools:', err);
        setError('Failed to load available tools. Please check if the backend is running.');
        
        // Set some default tools in case the backend fails
        const defaultTools = ["GitHub Copilot", "Cursor", "Replit", "Amazon CodeWhisperer", "Tabnine", "Codeium"];
        setTools(defaultTools);
        setSelectedTool(defaultTools[0]);
      }
    };

    fetchTools();
  }, []);

  const handleOptimize = async () => {
    if (!basePrompt.trim()) {
      setError('Please enter a prompt to optimize');
      return;
    }

    if (!selectedTool) {
      setError('Please select a target tool');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      console.log('Sending optimization request with tool:', selectedTool);
      const response = await axios.post('http://localhost:8000/optimize', {
        base_prompt: basePrompt,
        target_tool: selectedTool,
        additional_context: additionalContext || undefined
      });
      
      setOptimizedPrompt(response.data.optimized_prompt);
      setExplanation(response.data.explanation);
    } catch (err) {
      console.error('Error optimizing prompt:', err);
      setError(err.response?.data?.detail || 'Failed to optimize prompt. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Adaptive Prompt Optimizer
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Input
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  label="Base Prompt"
                  multiline
                  rows={6}
                  fullWidth
                  variant="outlined"
                  value={basePrompt}
                  onChange={(e) => setBasePrompt(e.target.value)}
                  placeholder="Enter your prompt here..."
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  label="Target Tool"
                  fullWidth
                  value={selectedTool}
                  onChange={(e) => {
                    console.log('Selected tool changed to:', e.target.value);
                    setSelectedTool(e.target.value);
                  }}
                  variant="outlined"
                  disabled={tools.length === 0}
                >
                  {tools.length > 0 ? (
                    tools.map((tool) => (
                      <MenuItem key={tool} value={tool}>
                        {tool}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem value="">No tools available</MenuItem>
                  )}
                </TextField>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  label="Additional Context (Optional)"
                  fullWidth
                  variant="outlined"
                  value={additionalContext}
                  onChange={(e) => setAdditionalContext(e.target.value)}
                  placeholder="Add any additional context about your task..."
                />
              </Grid>
              
              <Grid item xs={12}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  fullWidth 
                  onClick={handleOptimize}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Optimize Prompt'}
                </Button>
                {error && (
                  <Typography color="error" sx={{ mt: 2 }}>
                    {error}
                  </Typography>
                )}
              </Grid>
            </Grid>
          </Paper>
          
          {optimizedPrompt && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Results
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Optimized for <Chip label={selectedTool} color="primary" />
                </Typography>
                
                <SyntaxHighlighter 
                  language="markdown" 
                  style={docco}
                  customStyle={{ padding: '16px', borderRadius: '4px' }}
                >
                  {optimizedPrompt}
                </SyntaxHighlighter>
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Box>
                <Typography variant="h6" gutterBottom>
                  Optimization Explanation
                </Typography>
                <Typography variant="body1" component="div">
                  {explanation.split('\n').map((paragraph, index) => (
                    <p key={index}>{paragraph}</p>
                  ))}
                </Typography>
              </Box>
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 