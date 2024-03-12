// store.js

import { configureStore } from '@reduxjs/toolkit';
import assistantReducer from './assistantSlice';

export const store = configureStore({
  reducer: {
    assistant: assistantReducer,
    // Add other reducers if needed
  },
});
