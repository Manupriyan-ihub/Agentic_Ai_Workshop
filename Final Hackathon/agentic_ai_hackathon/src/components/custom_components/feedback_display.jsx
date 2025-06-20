import React from 'react';

const FeedbackDisplay = ({ data }) => {
  if (!data || !data.result) return <p>No feedback available.</p>;

  let relevance, depthFeedback, socialImpact;

  try {
    // Parse Relevance Section
    const relevanceMatch = data.result.match(/🧠 Relevance: (.*?)\n/);
    relevance = relevanceMatch ? relevanceMatch[1] : 'N/A';

    // Parse Depth Section
    const depthMatch = data.result.match(/📚 Depth Evaluation:\n(.*?)\n📢/s);
    depthFeedback = depthMatch
      ? depthMatch[1].trim()
      : 'No depth feedback found.';

    // Parse Social Impact Section
    const socialImpactMatch = data.result.match(
      /📢 Social Impact Score: (\d+)/,
    );
    socialImpact = socialImpactMatch ? socialImpactMatch[1] : 'N/A';
  } catch (error) {
    console.error('Error parsing result:', error);
  }

  return (
    <div className="mx-auto max-w-2xl space-y-4 rounded-lg bg-white p-4 shadow-lg">
      <h2 className="text-xl font-semibold text-gray-800">
        🔍 Article Evaluation Summary
      </h2>

      <div>
        <p className="font-medium text-gray-700">🧠 Relevance Score:</p>
        <p className="text-gray-900">{relevance}</p>
      </div>

      <div>
        <p className="font-medium text-gray-700">📚 Depth & Originality:</p>
        <pre className="rounded bg-gray-100 p-2 whitespace-pre-wrap text-gray-800">
          {depthFeedback}
        </pre>
      </div>

      <div>
        <p className="font-medium text-gray-700">📢 Social Impact Score:</p>
        <p className="text-gray-900">{socialImpact} / 100</p>
      </div>

      <div className="mt-4">
        <p className="font-medium text-gray-700">✅ Is Valid:</p>
        <p
          className={`font-semibold ${data.valid ? 'text-green-600' : 'text-red-600'}`}
        >
          {data.valid ? 'Valid' : 'Not Valid'}
        </p>
      </div>
    </div>
  );
};

export default FeedbackDisplay;
