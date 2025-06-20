import React from 'react';

const FeedbackDisplay = ({ data }) => {
  if (!data || !data.feedback || !data.result) {
    return null; // Or a fallback UI like <p>No feedback yet</p>
  }

  const { feedback } = data;

  // Extract scores from feedback
  const relevance = feedback.match(/Relevance: (\d+)/)?.[1];
  const insight = feedback.match(/Insight: (\d+)/)?.[1];
  const engagement = feedback.match(/Engagement: (\d+)/)?.[1];
  const average = feedback.match(/Average: ([\d.]+)/)?.[1];

  // Extract reflection prompt and improvement suggestions
  const reflectionPrompt = feedback.match(/Reflection Prompt:\n“([^”]+)”/)?.[1];
  const suggestions = feedback
    ?.match(/Improvement Suggestions:\n([\s\S]*)/)?.[1]
    ?.split(/\n\d\.\s+/)
    .filter(Boolean);

  return (
    <div className="mx-auto max-w-xl space-y-6 rounded-xl bg-white p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800">
        🧠 AI Feedback Summary
      </h2>

      <div className="space-y-1 text-gray-700">
        <p>
          <strong>Relevance:</strong> {relevance}/100
        </p>
        <p>
          <strong>Insight:</strong> {insight}/100
        </p>
        <p>
          <strong>Engagement:</strong> {engagement}/100
        </p>
        <p>
          <strong>Average Score:</strong> {average}/100
        </p>
      </div>

      {reflectionPrompt && (
        <div className="rounded border-l-4 border-yellow-400 bg-yellow-50 p-4">
          <p className="font-semibold">🪞 Reflection Prompt:</p>
          <p>{reflectionPrompt}</p>
        </div>
      )}

      {suggestions?.length > 0 && (
        <div>
          <p className="font-semibold text-gray-800">
            🔧 Improvement Suggestions:
          </p>
          <ul className="list-inside list-disc space-y-1 text-gray-700">
            {suggestions.map((tip, index) => (
              <li key={index}>{tip.trim()}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FeedbackDisplay;
