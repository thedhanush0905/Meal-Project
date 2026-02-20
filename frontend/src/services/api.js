const API_URL = 'http://localhost:8080/api';

export const queryAI = async (query) => {
  try {
    const response = await fetch(`${API_URL}/ai/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error('AI service failed to respond');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
