import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import supabase from '../config/supabaseClient';
import supabase from '../../config/supabaseClient';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailvalid, setEmailvalid] = useState(false);
  
  const displayNone = { display: 'none' };
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoading(true);

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      console.error('Error logging in:', error.message);
      document.getElementById('EmailAbsentError').style.display = 'block';
      setLoading(false);
    } else {
      console.log('User logged in successfully!');
      document.getElementById('loginSuccess').style.display = 'block';

      // Save user data to localStorage
      localStorage.setItem('userDetails', JSON.stringify({
        email: data.user.email,
        id: data.user.id
      }));

      setTimeout(() => {
        navigate('/'); // Redirect to the homepage
      }, 1000);
    }
  };

  const handleChange = (event) => {
    if (event.target.name === "email") {
      validateEmail(event.target.value);
    } else if (event.target.name === "password") {
      validatePassword(event.target.value);
    }
  };

  const validateEmail = (value) => {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$/.test(value)) {
      setEmail(value);
      setEmailvalid(true);
      document.getElementById('EmailInvalidError').style.display = 'none';
    } else {
      document.getElementById('EmailInvalidError').style.display = 'block';
    }
  };

  const validatePassword = (value) => {
    setPassword(value);
  };

  return (
    <div className="authincation mt-5 mb-5 h-100">
      <div className="container pb-5 login-container h-100">
        <div className="row pt-5 justify-content-center h-100 align-items-center">
          <div className="col-md-10 pt-5 background-white col-sm-12">
            <div className="authincation-content">
              <div className="row no-gutters">
                <div className="col-xl-12">
                  <div className="auth-form">
                    <h3 className="text-center mb-4 text-primary">
                      <strong>Login</strong>
                      <p className="text-black mb-0 p-0 fs-16">(Existing User)</p>
                    </h3>
                    <form onSubmit={handleLogin}>
                      <div className="form-group">
                        <label className="mb-1 text-primary"><strong>Email</strong></label>
                        <input onChange={handleChange} type="email" name="email" className="form-control" placeholder="hello@example.com" />
                      </div>
                      <div className="alert alert-danger mt-2" id='EmailInvalidError' style={displayNone} role="alert">
                        This Email is Invalid.
                      </div>
                      <div className="form-group">
                        <label className="mb-1 text-primary"><strong>Password</strong></label>
                        <input value={password} type="password" onChange={handleChange} name="password" className="form-control" placeholder="Password" />
                      </div>
                      <div className="alert alert-danger" id='EmailAbsentError' style={displayNone} role="alert">
                        Invalid Credentials. Check and try again
                      </div>
                      <div id='loginSuccess' className="alert alert-success" style={displayNone} role="alert">
                        <strong>Success!</strong> Logging you in.
                      </div>
                      <div className="text-center mt-4">
                        <button type="submit" className="btn bg-primary text-white btn-block">
                          {loading ? <span>Loading...</span> : <span>Sign Me In</span>}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
