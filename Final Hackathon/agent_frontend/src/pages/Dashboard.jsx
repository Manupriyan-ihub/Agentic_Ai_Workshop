import React, { useState, useEffect } from "react";
import { Eye, TrendingUp, FileText, BarChart3, X } from "lucide-react";

function Dashboard() {
  const [verifications, setVerifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReport, setSelectedReport] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // Fetch data from API
  useEffect(() => {
    const fetchVerifications = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/verifications");
        if (!response.ok) {
          throw new Error("Failed to fetch verifications");
        }
        const data = await response.json();
        setVerifications(data.verifications || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchVerifications();
  }, []);

  // Calculate statistics
  const stats = {
    totalArticles: verifications.length,
    averageScore:
      verifications.length > 0
        ? Math.round(
            verifications.reduce(
              (sum, v) => sum + v.score_feedback.final_score,
              0
            ) / verifications.length
          )
        : 0,
    highScoreArticles: verifications.filter(
      (v) => v.score_feedback.final_score >= 70
    ).length,
  };

  const handleViewReport = (verification) => {
    setSelectedReport(verification);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedReport(null);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getScoreBadgeColor = (score) => {
    if (score >= 80) return "bg-green-100 text-green-800";
    if (score >= 60) return "bg-yellow-100 text-yellow-800";
    return "bg-red-100 text-red-800";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg text-red-600">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">
            Overview of your article verifications and performance metrics
          </p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Total Articles */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  Total Articles
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.totalArticles}
                </p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Average Score */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  Average Score
                </p>
                <p
                  className={`text-2xl font-bold ${getScoreColor(
                    stats.averageScore
                  )}`}
                >
                  {stats.averageScore}
                </p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <BarChart3 className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>

          {/* High Score Articles */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  High Score Articles
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.highScoreArticles}
                </p>
                <p className="text-xs text-gray-500">Score ≥ 70</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Articles Table */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              Article Verifications
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Article Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {verifications.map((verification) => (
                  <tr key={verification._id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900 max-w-md truncate">
                        {verification.article_title}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getScoreBadgeColor(
                          verification.score_feedback.final_score
                        )}`}
                      >
                        {verification.score_feedback.final_score}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleViewReport(verification)}
                        className="flex items-center
                        bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-2 rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 font-semibold text-sm
                        "
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        View Report
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {verifications.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No articles found</p>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {showModal && selectedReport && (
        <div className="fixed inset-0 bg-white/30 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Article Report
              </h3>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-8 space-y-8">
              {/* Article Title */}
              <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-200/30">
                <h4 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <span className="text-purple-600">📝</span>
                  Article Title
                </h4>
                <p className="text-slate-700 font-medium leading-relaxed">
                  {selectedReport.article_title}
                </p>
              </div>

              {/* URL */}
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-2xl p-6 border border-blue-200/30">
                <h4 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <span className="text-blue-600">🔗</span>
                  Article URL
                </h4>
                <a
                  href={selectedReport.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 font-medium break-all hover:underline transition-all duration-300"
                >
                  {selectedReport.url}
                </a>
              </div>

              {/* Overall Score */}
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-full border-8 border-white shadow-lg mb-4">
                  <div className="text-center">
                    <div className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                      {selectedReport.score_feedback.final_score}
                    </div>
                    <div className="text-sm text-slate-600 font-medium">
                      Final Score
                    </div>
                  </div>
                </div>
                <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-4 border border-purple-200/30">
                  <p className="text-slate-700 font-medium">
                    {selectedReport.score_feedback.summary_feedback}
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
                  {Object.entries(selectedReport.score_feedback.breakdown).map(
                    ([category, score]) => {
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
                    }
                  )}
                </div>
              </div>

              {/* Improvement Suggestions */}
              <div className="bg-white/80 rounded-2xl p-6 shadow-lg border border-white/50">
                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                  <span className="text-indigo-600">🚀</span>
                  Improvement Suggestions
                </h3>
                <div className="space-y-4">
                  {selectedReport.score_feedback.improvement_suggestions.map(
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
                    "{selectedReport.score_feedback.reflection_prompt}"
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-center gap-4 pt-4">
                <button
                  onClick={closeModal}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl"
                >
                  Close Report
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
