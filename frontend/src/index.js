import React from 'react';
import ReactDOM from 'react-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './App';
import './index.css'
ReactDOM.render(
  <GoogleOAuthProvider clientId="367909834885-lpljp3ptkm4eho6v93csibus76uq74lr.apps.googleusercontent.com">
      <React.StrictMode>
          <App />
      </React.StrictMode>
  </GoogleOAuthProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
