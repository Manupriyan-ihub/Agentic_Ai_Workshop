import React from 'react';

const EvaluationFeedback = ({ data }) => {
  const parsedResult = JSON.parse(data.result);

  return (
    <div className="mx-auto max-w-3xl space-y-6 rounded-xl bg-white p-6 text-gray-800 shadow-md">
      {/* Scores Section */}
      <div>
        <h2 className="text-xl font-bold text-blue-600">🧠 Relevance: 95</h2>
        <p className="text-md text-gray-700">
          📢 <strong>Social Impact Score:</strong> 75/100
        </p>
      </div>

      {/* Depth Evaluation */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800">
          📚 Depth Evaluation:
        </h3>
        <p className="rounded bg-gray-100 p-4 text-sm whitespace-pre-line">
          Summary: The article provides a basic overview of common Mongoose
          methods, lacking depth or originality. It&apos;s a simple tutorial
          suitable for beginners but offers no novel insights or advanced
          techniques. The "bonus tip" is helpful but not groundbreaking.
          {'\n\n'}Idea Density: 2{'\n'}Sentiment: Promotional, 3{'\n'}
          Application: 3
        </p>
      </div>

      {/* Score Breakdown */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800">
          📊 Score Breakdown:
        </h3>
        <ul className="ml-6 list-disc text-sm">
          <li>Relevance: 95/100</li>
          <li>Insight: 20/100</li>
          <li>Engagement: 75/100</li>
          <li>Average: 63.33/100</li>
        </ul>
      </div>

      {/* Reflection Prompt */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800">
          🪞 Reflection Prompt:
        </h3>
        <p className="text-sm text-gray-700 italic">
          “How could this post better showcase the unique aspects and
          contributions of your capstone project, going beyond a basic overview
          to highlight its originality, depth, and potential impact?”
        </p>
      </div>

      {/* Suggestions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800">
          🔧 Improvement Suggestions:
        </h3>
        <ol className="ml-6 list-decimal space-y-2 text-sm">
          <li>
            <strong>Deepen the analysis:</strong> Instead of simply listing
            Mongoose methods, delve into a specific problem your capstone
            project addressed using Mongoose. Show how you leveraged advanced
            features or overcame challenges using specific examples from your
            project.
          </li>
          <li>
            <strong>Showcase originality:</strong> If your capstone project
            involved a novel approach or solution, explicitly highlight it.
            Explain what makes your solution unique and why it's an improvement
            over existing methods. Consider adding visuals like charts or
            diagrams.
          </li>
          <li>
            <strong>Connect to a broader audience:</strong> Instead of focusing
            solely on technical details, relate your project to a larger
            context. How does your capstone project solve a real-world problem?
            Who benefits from your solution?
          </li>
        </ol>
      </div>
    </div>
  );
};

export default EvaluationFeedback;
