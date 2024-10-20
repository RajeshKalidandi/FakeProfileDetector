import React, { useState } from 'react';
import { createProfile } from '../services/api';

const ProfileForm: React.FC = () => {
  const [profileData, setProfileData] = useState({
    platform: '',
    profile_url: '',
    username: '',
    bio: '',
    post_count: 0,
    follower_count: 0,
    following_count: 0,
    profile_picture_url: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await createProfile(profileData);
      setSuccess('Profile created successfully!');
      setProfileData({
        platform: '',
        profile_url: '',
        username: '',
        bio: '',
        post_count: 0,
        follower_count: 0,
        following_count: 0,
        profile_picture_url: '',
      });
    } catch (error) {
      setError('Error creating profile. Please try again.');
      console.error('Error creating profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Add input fields for each profile property */}
      <input
        type="text"
        name="platform"
        value={profileData.platform}
        onChange={handleChange}
        placeholder="Platform"
        className="w-full p-2 border rounded"
        required
      />
      {/* Add more input fields for other properties */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
      >
        {isLoading ? 'Creating...' : 'Create Profile'}
      </button>
      {error && <p className="text-red-500">{error}</p>}
      {success && <p className="text-green-500">{success}</p>}
    </form>
  );
};

export default ProfileForm;
