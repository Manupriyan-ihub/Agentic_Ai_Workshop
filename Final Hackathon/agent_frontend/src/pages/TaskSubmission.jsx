import { useState } from "react";

function TaskSubmission() {
  const [formData, setFormData] = useState({
    linkedinUrl: "",
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [articleTitle, setArticleTitle] = useState("");
  const [verificationResult, setVerificationResult] = useState(null);
  const [showReportModal, setShowReportModal] = useState(false);

  // LinkedIn URL validation
  const validateLinkedInUrl = (url) => {
    const linkedinRegex =
      /^https?:\/\/(www\.)?linkedin\.com\/(pulse\/|in\/|company\/|feed\/update\/|posts\/)/i;
    return linkedinRegex.test(url);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.linkedinUrl.trim()) {
      newErrors.linkedinUrl = "LinkedIn URL is required";
    } else if (!validateLinkedInUrl(formData.linkedinUrl)) {
      newErrors.linkedinUrl = "Please enter a valid LinkedIn article URL";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setSubmitStatus(null);
    setCurrentStep(1);

    try {
      // Step 1: Fetch article title
      setCurrentStep(1);
      const titleResponse = await fetch("http://127.0.0.1:8000/get-title", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: formData.linkedinUrl,
        }),
      });

      if (!titleResponse.ok) {
        throw new Error("Failed to fetch article title");
      }

      const titleData = await titleResponse.json();
      setArticleTitle(titleData.title);

      // Step 2: Submit for verification
      setCurrentStep(2);
      const verifyResponse = await fetch("http://127.0.0.1:8000/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: formData.linkedinUrl,
          article_title: titleData.title,
          user_id: "1",
        }),
      });

      if (verifyResponse.ok) {
        const verifyData = await verifyResponse.json();
        setVerificationResult(verifyData);
        setSubmitStatus({
          type: "success",
          message: `Task submitted successfully! Article: "${titleData.title}"`,
        });
        setFormData({ linkedinUrl: "" });
        setArticleTitle("");
        setCurrentStep(0);
      } else {
        throw new Error("Failed to submit task for verification");
      }
    } catch (error) {
      setSubmitStatus({
        type: "error",
        message:
          error.message || "An error occurred while processing your request",
      });
      setCurrentStep(0);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-full">
      {/* Header Section */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl">📝</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Task Submission
            </h1>
            <p className="text-slate-600 mt-1">
              Submit your LinkedIn article for review
            </p>
          </div>
        </div>

        {/* Progress indicator */}
        <div className="bg-gradient-to-r from-purple-100 to-indigo-100 rounded-xl p-4 border border-purple-200/50">
          <div className="flex items-center gap-2 text-sm text-slate-700">
            <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
            <span>Step 1: Submit your LinkedIn article URL</span>
          </div>
        </div>
      </div>

      {/* Report Modal */}
      {showReportModal && verificationResult && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => setShowReportModal(false)}
          ></div>

          {/* Modal */}
          <div className="relative bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="sticky top-0 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-t-3xl p-6 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">📊</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">
                      Article Analysis Report
                    </h2>
                    <p className="text-purple-100">
                      Detailed insights and recommendations
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setShowReportModal(false)}
                  className="w-10 h-10 bg-white/20 hover:bg-white/30 rounded-xl flex items-center justify-center transition-all duration-200"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <div className="p-8 space-y-8">
              {/* Overall Score */}
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-full border-8 border-white shadow-lg mb-4">
                  <div className="text-center">
                    <div className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                      {verificationResult.score_feedback.final_score}
                    </div>
                    <div className="text-sm text-slate-600 font-medium">
                      Final Score
                    </div>
                  </div>
                </div>
                <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-4 border border-purple-200/30">
                  <p className="text-slate-700 font-medium">
                    {verificationResult.score_feedback.summary_feedback}
                  </p>
                </div>
              </div>

              {/* Score Breakdown */}
              <div className="bg-white/80 rounded-2xl p-6 shadow-lg border border-white/50">
                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                  <span className="text-purple-600">📈</span>
                  Score Breakdown
                </h3>
                <div className="grid md:grid-cols-3 gap-6">
                  {Object.entries(
                    verificationResult.score_feedback.breakdown
                  ).map(([category, score]) => {
                    const getScoreColor = (score) => {
                      if (score >= 80) return "from-green-500 to-emerald-500";
                      if (score >= 60) return "from-yellow-500 to-orange-500";
                      return "from-red-500 to-pink-500";
                    };

                    const getScoreIcon = (category) => {
                      switch (category) {
                        case "relevance":
                          return "🎯";
                        case "insight":
                          return "💡";
                        case "engagement":
                          return "❤️";
                        default:
                          return "📊";
                      }
                    };

                    return (
                      <div key={category} className="text-center">
                        <div className="mb-3">
                          <div className="text-2xl mb-2">
                            {getScoreIcon(category)}
                          </div>
                          <div className="text-lg font-semibold text-slate-800 capitalize">
                            {category}
                          </div>
                        </div>
                        <div className="relative">
                          <div className="w-full bg-slate-200 rounded-full h-3 mb-2">
                            <div
                              className={`bg-gradient-to-r ${getScoreColor(
                                score
                              )} h-3 rounded-full transition-all duration-1000 ease-out`}
                              style={{ width: `${score}%` }}
                            ></div>
                          </div>
                          <div
                            className={`text-2xl font-bold bg-gradient-to-r ${getScoreColor(
                              score
                            )} bg-clip-text text-transparent`}
                          >
                            {score}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Improvement Suggestions */}
              <div className="bg-white/80 rounded-2xl p-6 shadow-lg border border-white/50">
                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                  <span className="text-indigo-600">🚀</span>
                  Improvement Suggestions
                </h3>
                <div className="space-y-4">
                  {verificationResult.score_feedback.improvement_suggestions.map(
                    (suggestion, index) => (
                      <div
                        key={index}
                        className="flex gap-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200/30"
                      >
                        <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                          {index + 1}
                        </div>
                        <p className="text-slate-700 leading-relaxed">
                          {suggestion}
                        </p>
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Reflection Prompt */}
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-200/30">
                <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                  <span className="text-purple-600">🤔</span>
                  Reflection Prompt
                </h3>
                <div className="bg-white/60 rounded-xl p-6 border border-white/50">
                  <p className="text-slate-700 leading-relaxed font-medium italic">
                    "{verificationResult.score_feedback.reflection_prompt}"
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-center gap-4 pt-4">
                <button
                  onClick={() => setShowReportModal(false)}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl"
                >
                  Close Report
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stepper Loader */}
      {isLoading && (
        <div className="mb-8">
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4 text-center">
              Processing Your Submission
            </h3>
            <div className="flex items-center justify-between max-w-md mx-auto">
              {/* Step 1 */}
              <div className="flex flex-col items-center flex-1">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 ${
                    currentStep >= 1
                      ? "bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg"
                      : "bg-slate-200 text-slate-400"
                  }`}
                >
                  {currentStep > 1 ? (
                    <span className="text-lg">✓</span>
                  ) : currentStep === 1 ? (
                    <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : (
                    <span className="text-lg">📄</span>
                  )}
                </div>
                <div className="mt-2 text-xs text-center">
                  <div className="font-semibold text-slate-700">
                    Fetching Title
                  </div>
                  <div className="text-slate-500">Getting article info</div>
                </div>
              </div>

              {/* Connector */}
              <div
                className={`flex-1 h-1 mx-4 rounded-full transition-all duration-500 ${
                  currentStep >= 2
                    ? "bg-gradient-to-r from-purple-600 to-indigo-600"
                    : "bg-slate-200"
                }`}
              >
                <div
                  className={`h-full rounded-full transition-all duration-1000 ${
                    currentStep >= 2
                      ? "w-full bg-gradient-to-r from-purple-600 to-indigo-600"
                      : "w-0"
                  }`}
                ></div>
              </div>

              {/* Step 2 */}
              <div className="flex flex-col items-center flex-1">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 ${
                    currentStep >= 2
                      ? "bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg"
                      : "bg-slate-200 text-slate-400"
                  }`}
                >
                  {currentStep === 2 ? (
                    <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : (
                    <span className="text-lg">🚀</span>
                  )}
                </div>
                <div className="mt-2 text-xs text-center">
                  <div className="font-semibold text-slate-700">Verifying</div>
                  <div className="text-slate-500">Submitting task</div>
                </div>
              </div>
            </div>

            {/* Current Step Info */}
            <div className="mt-6 text-center">
              {currentStep === 1 && (
                <div className="bg-blue-50 rounded-lg p-3 border border-blue-200/50">
                  <p className="text-sm text-blue-800">
                    <span className="font-semibold">Step 1:</span> Fetching
                    article title from LinkedIn...
                  </p>
                </div>
              )}
              {currentStep === 2 && (
                <div className="bg-purple-50 rounded-lg p-3 border border-purple-200/50">
                  <p className="text-sm text-purple-800">
                    <span className="font-semibold">Step 2:</span> Submitting "
                    {articleTitle}" for verification...
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Main Form Card */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-200/20 to-indigo-200/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-cyan-200/20 to-purple-200/20 rounded-full blur-3xl"></div>

        <div className="relative z-10">
          {/* Instructions */}
          <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200/30">
            <h3 className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
              <span className="text-blue-600">ℹ️</span>
              Instructions
            </h3>
            <ul className="text-sm text-slate-600 space-y-1">
              <li>• Paste the complete URL of your LinkedIn article</li>
              <li>• Make sure the article is publicly accessible</li>
              <li>• URL should start with https://linkedin.com/</li>
            </ul>
          </div>

          {/* Form */}
          <div className="space-y-6">
            <div className="space-y-2">
              <label
                htmlFor="linkedinUrl"
                className="block text-sm font-semibold text-slate-700"
              >
                LinkedIn Article URL *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg
                    className="w-5 h-5 text-slate-400"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                  </svg>
                </div>
                <input
                  type="url"
                  id="linkedinUrl"
                  name="linkedinUrl"
                  value={formData.linkedinUrl}
                  onChange={handleInputChange}
                  placeholder="https://linkedin.com/pulse/your-article-title"
                  className={`w-full pl-12 pr-4 py-4 rounded-xl border-2 transition-all duration-300 focus:outline-none focus:ring-0 ${
                    errors.linkedinUrl
                      ? "border-red-300 bg-red-50 focus:border-red-500"
                      : "border-slate-200 bg-white/50 focus:border-purple-500 focus:bg-white/80"
                  }`}
                  disabled={isLoading}
                />
              </div>
              {errors.linkedinUrl && (
                <p className="text-red-600 text-sm flex items-center gap-1 mt-1">
                  <span>⚠️</span>
                  {errors.linkedinUrl}
                </p>
              )}
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <button
                onClick={handleSubmit}
                disabled={isLoading}
                className={`w-full py-4 px-8 rounded-xl font-semibold text-white transition-all duration-300 transform ${
                  isLoading
                    ? "bg-slate-400 cursor-not-allowed"
                    : "bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 hover:scale-105 hover:shadow-lg hover:shadow-purple-500/25"
                }`}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>
                      {currentStep === 1
                        ? "Fetching Article Title..."
                        : currentStep === 2
                        ? "Submitting for Verification..."
                        : "Processing..."}
                    </span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <span>🚀</span>
                    <span>Submit Task</span>
                  </div>
                )}
              </button>
            </div>
          </div>

          {/* Status Messages */}
          {submitStatus && (
            <div
              className={`mt-6 p-4 rounded-xl border-2 ${
                submitStatus.type === "success"
                  ? "bg-green-50 border-green-200 text-green-800"
                  : "bg-red-50 border-red-200 text-red-800"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-lg">
                    {submitStatus.type === "success" ? "✅" : "❌"}
                  </span>
                  <span className="font-semibold">{submitStatus.message}</span>
                </div>
                {submitStatus.type === "success" && verificationResult && (
                  <button
                    onClick={() => setShowReportModal(true)}
                    className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-2 rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 font-semibold text-sm"
                  >
                    📊 View Report
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Additional Info Card */}
      <div className="mt-8 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-200/30">
        <h3 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
          <span className="text-purple-600">💡</span>
          Tips for Success
        </h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-600">
          <div className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span>Ensure your article is published and public</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span>Double-check the URL format</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span>Make sure the content is original</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span>Article should be relevant to GenAI</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TaskSubmission;
