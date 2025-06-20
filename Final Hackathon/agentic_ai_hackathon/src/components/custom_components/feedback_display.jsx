import React from 'react';

const FeedbackDisplay = ({ data }) => {
  if (!data || !data.result) return null;

  // If result is a string (old case), try to parse it
  const result = typeof data.result === 'string' ? {} : data.result;

  // Also check if data.result might be a stringified object
  const fallbackResult =
    typeof data.result === 'string' && data.result.includes('{')
      ? JSON.parse(data.result.replace(/'/g, '"'))
      : {};

  // Check depth/originality and relevance inside fallbackResult if result is empty
  const relevanceOutput =
    result?.output ||
    fallbackResult?.output ||
    'Relevance feedback not available';
  const depthOutput = data?.depth || 'Depth feedback not available';
  const socialImpactMatch =
    typeof data.result === 'string'
      ? data.result.match(/Social Impact Score:\s*(\d+)\/100/)
      : null;
  const socialImpact = socialImpactMatch?.[1] || '0';

  return (
    <div className="mx-auto max-w-xl space-y-6 rounded-xl bg-white p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800">
        🧠 AI Feedback Summary
      </h2>

      <div className="space-y-2 text-gray-700">
        <p>
          <strong>🔍 Relevance:</strong> {relevanceOutput}
        </p>
        <p>
          <strong>📚 Depth Evaluation:</strong> {depthOutput}
        </p>
        <p>
          <strong>📢 Social Impact Score:</strong> {socialImpact}/100
        </p>
      </div>
    </div>
  );
};

export default FeedbackDisplay;
