// assistantSlice.js

import { createSlice } from '@reduxjs/toolkit';

const storedAssistant = localStorage.getItem('assistant');

const assistantSlice = createSlice({
  name: 'assistant',
  initialState: storedAssistant || '',
  reducers: {
    updateAssistant: (state, action) => {
      const newAssistant = action.payload;
      localStorage.setItem('assistant', newAssistant);
      return newAssistant;
    },
  },
});

export const { updateAssistant } = assistantSlice.actions;
export const selectAssistant = (state) => state.assistant;
export default assistantSlice.reducer;
