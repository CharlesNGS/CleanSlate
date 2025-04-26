import React, { useState } from 'react';
import 'D:\CleanSlate\_AppBuild\Style CSS\CSS Files';

function Signin() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    
    const handleSubmit = async (e) => {


    };
    return (
      <form onSubmit={handleSubmit}>
        <div1>
            <div2>
                <label>
                    Username:
                    <input 
                    type="text" 
                    value={username}
                    />
                </label>
                <label>
                    Password:
                    <input 
                    type="password"
                    value={password}
                    />
                </label>
            </div2>
            <div2>
                <button 
                type="submit"
                onPress={handleSubmit}
                >
                    Sign In
                </button>
            </div2>
        </div1>
      </form>
    )
  }

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Signin />);