import React, { useState } from 'react';
import { createFeedbackReport } from '../services/api';

interface FeedbackFormProps {
  analysisId: string;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ analysisId }) => {
  const [feedback, setFeedback] = useState('');
  const [additionalComments, setAdditionalComments] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await createFeedbackReport({
        analysis_id: analysisId,
        feedback,
        additional_comments: additionalComments,
      });
      setSuccess('Feedback submitted successfully!');
      setFeedback('');
      setAdditionalComments('');
    } catch (error) {
      setError('Failed to submit feedback. Please try again.');
      console.error('Error submitting feedback:', error);
    } finally {
      setIsLoading(false);
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
      <textarea
        value={additionalComments}
        onChange={(e) => setAdditionalComments(e.target.value)}
        placeholder="Additional comments"
        className="w-full p-2 border rounded mb-2"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
      >
        {isLoading ? 'Submitting...' : 'Submit Feedback'}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      {success && <p className="text-green-500 mt-2">{success}</p>}
    </form>
  );
};

export default FeedbackForm;
