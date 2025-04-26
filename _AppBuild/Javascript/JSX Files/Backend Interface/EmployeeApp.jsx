import React, { useState } from 'react';
import 'D:\CleanSlate\_AppBuild\Style CSS\CSS Files';

function Signin() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    
    const handleSubmit = async (e) => {


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
            <div>
                <button 
                className="font center"
                type="submit"
                onClick={handleSubmit}
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