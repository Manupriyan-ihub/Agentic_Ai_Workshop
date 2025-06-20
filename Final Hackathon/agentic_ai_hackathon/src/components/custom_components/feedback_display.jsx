import React from 'react';

const FeedbackDisplay = ({ data }) => {
  if (!data || !data.result) return null;

  const resultText = typeof data.result === 'string' ? data.result : '';

  // 1. Extract and parse Relevance block
  const relevanceMatch = resultText.match(/🧠 Relevance:\s*({[\s\S]*?})/);
  const relevance = relevanceMatch
    ? JSON.parse(relevanceMatch[1].replace(/'/g, '"'))
    : null;

  // 2. Extract and parse Depth Evaluation block
  const depthMatch = resultText.match(/📚 Depth Evaluation:\s*({[\s\S]*?})/);
  const depth = depthMatch
    ? JSON.parse(depthMatch[1].replace(/'/g, '"'))
    : null;

  // 3. Extract Social Impact Score
  const socialImpactMatch = resultText.match(
    /📢 Social Impact Score:\s*(\d+)\/100/,
  );
  const socialImpact = socialImpactMatch?.[1] || 'N/A';

  return (
    <div className="mx-auto max-w-xl space-y-6 rounded-xl bg-white p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800">
        🧠 AI Feedback Summary
      </h2>

      <div className="space-y-2 text-gray-700">
        {relevance?.output && (
          <p>
            <strong>🔍 Relevance:</strong> {relevance.output}
          </p>
        )}
        {depth?.output && (
          <p>
            <strong>📚 Depth Evaluation:</strong> {depth.output}
          </p>
        )}
        <p>
          <strong>📢 Social Impact Score:</strong> {socialImpact}/100
        </p>
      </div>
    </div>
  );
};

export default FeedbackDisplay;
