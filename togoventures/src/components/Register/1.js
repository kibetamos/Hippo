import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styles from './Register.module.css';
import Headers from '../_layouts/Headers/Headers';
import Footers from '../_layouts/Footers/Footers';
import {
  Link, useNavigate
} from "react-router-dom";
import $ from 'jquery';
import { Variables } from '../_utils/GlobalVariables';

import axios from 'axios';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [first_name, setFirst_name] = useState('');
  const [last_name, setLast_name] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailvalid, setEmailvalid] = useState(false);

  // this.handleChange = this.handleChange.bind(this);

  const displayNone = { display: 'none' };

  const navigate = useNavigate();
  const submitForm = (e) => {
    e.preventDefault();
    // If fields are blank
    if (first_name == '') {
      $('#FirstNameInvalidError').show();
      return;
    }
    if (last_name == '') {
      $('#LastNameInvalidError').show();
      return;
    }
    if (email == '') {
      $('#EmailInvalidError').show();
      return;
    }
    if (password == '') {
      $('#ShortPasswordError').show();
      return;
    }
    if (password2 == '') {
      $('#UnmatchingPasswords').show();
      return;
    }
    if (password2 != password) {
      $('#UnmatchingPasswords').show();
      return;
    } else {
      $('#UnmatchingPasswords').hide();
    }
    if (!document.getElementById('TermsConfirm').checked) {
      $('#TermsError').show();
      return;
    } else {
      $('#TermsError').hide();
    }

    let submitPayload = {
      "password": password,
      "password2": password2,
      "email": email,
      "first_name": first_name,
      "last_name": last_name
    };
    const headers = {
      'Content-Type': 'application/json',
    }
    console.log('submitting');
    setLoading(true);
    console.log(submitPayload)
    axios.post('http://127.0.0.1:8000/registration/', submitPayload, { headers: headers })
      .then(response => {
        $('#EmailExistsError').hide();

        setLoading(false);
        console.log(response);

        if (response.status == 201) {
          $('#SubmitError').hide();
          $('.alert-success').show();

          localStorage.removeItem("gunduauser");
          let user = JSON.stringify(response);
          localStorage.setItem("gunduauser", user);
           console.log(JSON.stringify(response));
          setTimeout(function () {
            // navigate('/home');
            // $("#register-form").fadeOut();
            // $("#emailsent").removeClass("d-none");
            window.location.href = "/login";
          }, 2000);
        } else {
          $('.alert-success').hide();
          $('#SubmitError').show();
        }
      })
      .catch(error => {
        console.log('error');
        console.log(error);
        $('#EmailExistsError').hide();
        setLoading(false);
        if (error.response.data.email) {
          $('#EmailExistsError').show();
        } else {
          $('.alert-success').hide();
          $('#SubmitError').show();
        }
      })
  }

  const handleChange = (event) => {
    // this.setState({ [event.target.name]: event.target.value });
    if (event.target.name == "email") {
      validateEmail(event.target.value);
    } else if (event.target.name == "password") {
      validatePassword(event.target.value);
    } else if (event.target.name == "password2") {
      validatePassword2(event.target.value);
    } else if (event.target.name == "first_name") {
      validateFirstName(event.target.value);
    } else if (event.target.name == "last_name") {
      validateLastName(event.target.value);
    }
  }

  const validateFirstName = (value) => {
    $('#FirstNameInvalidError').hide();
    setFirst_name(value);
    // if (value.length < 2) {
    //   $('#FirstNameInvalidError').show();
    // }
  }

  const validateLastName = (value) => {
    $('#LastNameInvalidError').hide();
    setLast_name(value);
    // if (value.length < 2) {
    //   $('#FirstNameInvalidError').show();
    // }
  }


  const validateEmail = (value) => {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$/.test(value)) {
      $('#EmailInvalidError').hide();
      setEmail(value);
      setEmailvalid(true);
    } else {
      $('#EmailInvalidError').show();
    }
  }

  const validatePassword = (value) => {
    $('#IncorrectPasswordError').hide();
    if (value.length < 6) {
      // $('#IncorrectPasswordError').hide();
      $('#ShortPasswordError').show();
    } else {
      $('#ShortPasswordError').hide();
      if (/^(?=.*\d)(?=.*[a-z])(?=.*[a-zA-Z]).{6,}$/.test(value)) {
        // console.log('valid');
        setPassword(value);
        $('#IncorrectPasswordError').hide();
      } else {
        console.log('invalid');
        $('#IncorrectPasswordError').show();
      }
    }
  }

  const validatePassword2 = (value) => {
    if (value != password) {
      $('#UnmatchingPasswords').show();
    } else {
      setPassword2(value);
      $('#UnmatchingPasswords').hide();
    }
  }

  // const img = require('./loginbg.png');

  const bodyStyle = {
    // backgroundImage: `url(${img})`,
    backgroundSize: 'cover'
  }

  return (
    <div className={styles.Register} data-testid="Register">
      {/* <!-- dividers --> */}
      <div class="dividers">
        <div class="divider"></div>
        <div class="divider"></div>
        <div class="divider"></div>
        <div class="divider"></div>
      </div>
      <body style={bodyStyle} className="h-100 mt-5 pt-5">
        <div className="authincation mt-5 mb-5 h-100">
          <div className="container login-container h-100">
            <div className="row justify-content-center h-100 align-items-center">
              <div className="col-md-10 col-sm-12">
                <div id='register-form' className="authincation-content">
                  <div className="row no-gutters">
                    <div className="col-xl-12">
                      <div className="auth-form">
                        <h3 className="text-center mb-4 text-primary"><strong>Sign up</strong><p className='text-black mb-0 p-0 fs-16'>(New User)</p></h3>

                        <form id="registerAccountForm" onSubmit={submitForm}>
                          {/* <div className="form-group">
                              <label className="mb-1 text-primary"><strong>Username</strong></label>
                              <input type="text" className="form-control" name='username' onChange={this.handleChange} id='registerusername' placeholder="username" />
                            </div> */}
                          <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Full Name</strong></label>
                            <input type="text" className="form-control" onChange={handleChange} id='first_name' name="first_name" placeholder="FirstName" />
                            <div className="alert alert-danger mt-2" id='FirstNameInvalidError' style={displayNone} role="alert">
                              Please Input First Name
                            </div>
                          </div>

                          {/* <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Full Name</strong></label>
                            <input type="text" className="form-control" onChange={handleChange} id='last_name' name="last_name" placeholder="..." />
                            <div className="alert alert-danger mt-2" id='FirstNameInvalidError' style={displayNone} role="alert">
                              Please Input Last Name
                            </div>
                          </div> */}
                          <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Last Name</strong></label>
                            <input type="text" className="form-control" onChange={handleChange} id='last_name' name="last_name" placeholder="LastName" />
                            <div className="alert alert-danger mt-2" id='LastNameInvalidError' style={displayNone} role="alert">
                              Please Input a Name
                            </div>
                          </div>
                          <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Email</strong></label>
                            <input type="email" className="form-control" onChange={handleChange} id='registeremail' name="email" placeholder="hello@example.com" />
                            <div className="alert alert-danger mt-2" id='EmailInvalidError' style={displayNone} role="alert">
                              This Email is Invalid.
                            </div>
                          </div>
                          <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Password</strong></label>
                            <input type="password" className="form-control" onChange={handleChange} name='password' id="registerpassword" placeholder="Password" />
                          </div>
                          <div className="alert alert-danger mt-2" id='IncorrectPasswordError' style={displayNone} role="alert">
                            <strong>Invalid Password </strong>Your password should contain at least one number and a letter.
                          </div>
                          <div className="alert alert-danger mt-2" id='ShortPasswordError' style={displayNone} role="alert">
                            <strong>Too short </strong>Your password should be more than 6 characters
                          </div>
                          <div className="form-group">
                            <label className="mb-1 text-primary"><strong>Confirm Password</strong></label>
                            <input type="password" onChange={handleChange} className="form-control" name="password2" id='registercpassword' placeholder="Confirm Password" />
                          </div>

                          <div className="alert alert-danger" id='UnmatchingPasswords' style={displayNone} role="alert">
                            <strong>Error </strong>The two passwords do not match
                          </div>

                          <div class="custom-control custom-checkbox mb-3">
                            <input type="checkbox" class="" id="TermsConfirm" />
                            <label class="pl-1" for="TermsConfirm">I have read the <a className='text-blue'>terms and conditions</a> and I accept them.</label>
                          </div>

                          <div className="alert alert-danger" id='TermsError' style={displayNone} role="alert">
                            You have to accept our terms and conditions.
                          </div>

                          <div className="alert alert-danger" id='SubmitError' style={displayNone} role="alert">
                            <strong>Error </strong>Something went wrong. Confirm the email exists and try again.
                          </div>

                          <div id='loginSuccess' className="alert alert-success" style={displayNone} role="alert">
                            <strong>Account Created! Proceed to login</strong>
                          </div>

                          <div className="alert alert-danger" id='EmailExistsError' style={displayNone} role="alert">
                            This Email is Already Registered. Please Log In.
                          </div>

                          <div className="text-center mt-4">
                            <button type="submit" className="btn bg-primary text-white btn-block">
                              {loading ? <span>Loading...</span> : <span>Sign me up</span>}  </button>
                          </div>
                        </form>
                        <div className="new-account mt-3">
                          <p className="text-blackish">Already have an account?
                            <Link to="/login" class="text-primary" > Sign in</Link>
                            {/* <a className="text-primary" href="/login">Sign in</a> */}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div id='emailsent' className="authincation-content d-none mb-5">
                  <div className='p-5 mb-5  '>
                    <h4>We have sent an email to '<strong>{email}</strong>'<br /> Click the link in the email to complete your registration.</h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </body >
    </div>
  )
};

Register.propTypes = {};

Register.defaultProps = {};

export default Register;
