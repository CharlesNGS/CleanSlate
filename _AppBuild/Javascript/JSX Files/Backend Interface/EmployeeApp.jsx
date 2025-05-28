import React, { useState } from 'react';
import 'D:\CleanSlate\_AppBuild\Style CSS\CSS Files\EmployeeApplicationStyle.css';

function Signin() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    
    const handleSubmit = async (e) => {
        e.preventDefault();

          const response = await fetch('/authentication', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
          });

          const result = await response.json();

          if (response.ok && result.redirect) {
            window.location.href = result.redirect;

          } else {
            alert('Authentication failed');
            console.log('Login failed:', result);
          }
    };

    return (
      <form onSubmit={handleSubmit}>
        <div>
            <div>
                <label
                className="font center">
                    Username:
                    <input 
                    title="Username"
                    type="text" 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <br />
                <label
                className="font center">
                    Password:
                    <input 
                    title="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
            </div>
            <br />
            <div>
                <button 
                className="font center"
                type="submit"
                >
                    Sign In:
                </button>
            </div>
        </div>
      </form>
    )
  }

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Signin />);