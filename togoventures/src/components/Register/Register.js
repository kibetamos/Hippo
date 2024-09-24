import { useState } from 'react';
// import supabase from "../../config/supabaseClient";// Import your Supabase client
// import supabase from '../config/supabaseClient';
import supabase from '../../config/supabaseClient';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async () => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });
    if (error) console.error('Error signing up:', error.message);
    else console.log('User signed up successfully!');
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignup}>Sign Up</button>
    </div>
  );
}

export default Register;
