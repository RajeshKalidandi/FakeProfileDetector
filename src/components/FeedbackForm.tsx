import React, { useState } from 'react';
import { submitFeedback } from '../services/api';

interface FeedbackFormProps {
  analysisId: string;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ analysisId }) => {
  const [feedback, setFeedback] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await submitFeedback(analysisId, feedback);
      alert('Feedback submitted successfully!');
      setFeedback('');
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <h3 className="text-lg font-semibold mb-2">Provide Feedback</h3>
      <select
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        className="w-full p-2 border rounded mb-2"
        required
      >
        <option value="">Select feedback</option>
        <option value="correct">Correct analysis</option>
        <option value="fake">Actually fake</option>
        <option value="genuine">Actually genuine</option>
      </select>
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Submit Feedback
      </button>
    </form>
  );
};

export default FeedbackForm;
