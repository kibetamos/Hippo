import React, { useState, useEffect } from 'react';
import Header from '../_layouts/Headers/Headers';
import Sidebar from '../_layouts/Sidebar/Sidebar';
import Footers from '../_layouts/Footers/Footers';
import supabase from '../config/supabaseClient';

const Profile = () => {
  const [userDetails, setUserDetails] = useState(null);
  const [name, setName] = useState("");
  const [userId, setUserId] = useState("");
  const [email, setEmail] = useState("");  // Added state for email
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getUserDetails = async () => {
    setLoading(true);
    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) {
        const id = session.user.id;
        setUserId(id);

        const { data, error } = await supabase
          .from('profiles')
          .select('first_name, last_name, email')  // Fetching email
          .eq('id', id)
          .single();

        if (error) throw error;

        setUserDetails(data);
        setName(`${data.first_name} ${data.last_name}`);
        setEmail(data.email);  // Set the email state
      }
    } catch (error) {
      console.error('Error fetching user details:', error.message);
      setError('Failed to load user details.');
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const [firstName, lastName] = name.split(' ', 2);
      const { error } = await supabase
        .from('profiles')
        .update({ first_name: firstName, last_name: lastName, updated_at: new Date() })
        .eq('id', userId);

      if (error) throw error;

      alert('Profile updated successfully!');
      getUserDetails(); // Refresh user details
    } catch (error) {
      console.error('Error updating profile:', error.message);
      setError('Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getUserDetails();
  }, []);

  return (
    <div>
      <Header title="Profile" />
      <Sidebar />
      <div className="content-body">
        <div className="container-fluid">
          <div className="row">
            <div className="col-lg-12">
              <div className="profile card card-body px-3 pt-3 pb-0">
                <div className="profile-head">
                  <h4 className="text-primary pl-4 mb-5">User Information</h4>
                  <div className="profile-info">
                    <div className="profile-photo">
                      <img src="images/profile/profile.png" className="img-fluid rounded-circle" alt="Profile" />
                    </div>
                    <div className="profile-details">
                      <div className="px-2 mr-2">
                        <p className="mb-1">Name</p>
                        <h4 className="text-muted mb-0">
                          {userDetails ? name : 'Loading...'}
                        </h4>
                      </div>
                      <div className="px-2 mr-2">
                        <p className="mb-1">ID</p>
                        <h4 className="text-muted mb-0">
                          {userId || 'Loading...'}
                        </h4>
                      </div>
                      <div className="px-2 mr-2">
                        <p className="mb-1">Email</p>
                        <h4 className="text-muted mb-0">
                          {email || 'Loading...'}
                        </h4>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-lg-12">
              <div className="profile card card-body px-3 pt-3 pb-0">
                <div className="profile-head">
                  <h4 className="text-primary pl-3 mb-3">Update Profile</h4>
                  <div className="profile-details">
                    <form onSubmit={updateProfile} className="full-width">
                      <div className="form-group col-md-12">
                        <label>Name</label>
                        <input
                          type="text"
                          value={name}
                          className="form-control"
                          placeholder="Full Name"
                          onChange={(e) => setName(e.target.value)}
                        />
                      </div>

                      {error && (
                        <div className="alert alert-danger mt-2">
                          <strong>Error: </strong>{error}
                        </div>
                      )}

                      <button type="submit" className="btn btn-primary" disabled={loading}>
                        {loading ? 'Loading...' : 'Update Profile'}
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footers />
    </div>
  );
};

export default Profile;
