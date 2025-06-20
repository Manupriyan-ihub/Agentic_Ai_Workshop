// import { configureStore } from "@reduxjs/toolkit";
// import loginReducer from "@/app/features/login/loginReducer";

// export const store = configureStore({
//   reducer: {
//     auth: loginReducer,
//   },
// });

import { configureStore } from '@reduxjs/toolkit';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web
import loginReducer from '@/app/features/login/loginReducer';

const persistConfig = {
  key: 'auth',
  storage,
  whitelist: ['isAuthenticated', 'user', 'token'], // only persist these fields
};

const persistedAuthReducer = persistReducer(persistConfig, loginReducer);

export const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore redux-persist actions
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(store);
