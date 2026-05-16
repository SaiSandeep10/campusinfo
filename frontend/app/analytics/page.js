// frontend/app/analytics/page.js
'use client'
import { useState, useEffect } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/api/analytics`)
      const data = await response.json()
      setAnalytics(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-screen bg-gray-950">
      <div className="text-center">
        <div className="flex gap-2 justify-center mb-4">
          <span className="w-3 h-3 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-3 h-3 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-3 h-3 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
        <p className="text-gray-400">Loading Analytics...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="flex items-center justify-center h-screen bg-gray-950">
      <p className="text-red-400">Error: {error}</p>
    </div>
  )

  const stats = analytics?.overall_stats || {}
  const popular = analytics?.popular_queries || []
  const categories = analytics?.category_distribution || {}
  const activity = analytics?.daily_activity || []
  const gaps = analytics?.information_gaps || []

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">

      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">📊 Analytics Dashboard</h1>
            <p className="text-gray-400 mt-1">ANITS Campus Assistant Usage Insights</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={fetchAnalytics}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm transition"
            >
              🔄 Refresh
            </button>
            <a
              href="/"
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition"
            >
              ← Back to Chat
            </a>
          </div>
        </div>

        {/* Overall Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total Messages", value: stats.total_messages || 0, icon: "💬", color: "blue" },
            { label: "Total Sessions", value: stats.total_sessions || 0, icon: "👥", color: "green" },
            { label: "Today", value: stats.messages_today || 0, icon: "📅", color: "purple" },
            { label: "This Week", value: stats.messages_this_week || 0, icon: "📈", color: "orange" },
          ].map((stat, i) => (
            <div key={i} className="bg-gray-900 rounded-xl p-5 border border-gray-700">
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className="text-2xl font-bold text-white">{stat.value}</div>
              <div className="text-gray-400 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

          {/* Popular Queries */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold mb-4">🔥 Popular Questions</h2>
            {popular.length === 0 ? (
              <p className="text-gray-500 text-sm">No data yet. Start asking questions!</p>
            ) : (
              <div className="space-y-3">
                {popular.map((q, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1 min-w-0">
                      <span className="text-blue-400 font-bold text-sm w-6">
                        #{i + 1}
                      </span>
                      <span className="text-gray-300 text-sm truncate">
                        {q.question}
                      </span>
                    </div>
                    <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full ml-2 shrink-0">
                      {q.count}x
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Category Distribution */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold mb-4">📂 Category Usage</h2>
            {Object.keys(categories).length === 0 ? (
              <p className="text-gray-500 text-sm">No data yet!</p>
            ) : (
              <div className="space-y-3">
                {Object.entries(categories).map(([cat, data], i) => (
                  <div key={i}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-300 capitalize">{cat}</span>
                      <span className="text-gray-400">{data.count} ({data.percentage}%)</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full transition-all"
                        style={{ width: `${data.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Daily Activity */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold mb-4">📅 Daily Activity (Last 7 Days)</h2>
            {activity.length === 0 ? (
              <p className="text-gray-500 text-sm">No data yet!</p>
            ) : (
              <div className="space-y-2">
                {activity.map((day, i) => {
                  const maxCount = Math.max(...activity.map(d => d.count)) || 1
                  const width = Math.max((day.count / maxCount) * 100, 2)
                  return (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-gray-400 text-xs w-12 shrink-0">{day.date}</span>
                      <div className="flex-1 bg-gray-700 rounded-full h-4 relative">
                        <div
                          className="bg-green-500 h-4 rounded-full transition-all"
                          style={{ width: `${width}%` }}
                        />
                      </div>
                      <span className="text-gray-300 text-xs w-6 text-right">{day.count}</span>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          {/* Information Gaps */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold mb-2">⚠️ Information Gaps</h2>
            <p className="text-gray-500 text-xs mb-4">
              Questions where chatbot gave fallback responses
            </p>
            {gaps.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-green-400 text-sm">✅ No gaps detected!</p>
                <p className="text-gray-500 text-xs mt-1">Chatbot is answering all questions!</p>
              </div>
            ) : (
              <div className="space-y-2">
                {gaps.map((gap, i) => (
                  <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800 rounded-lg p-3">
                    <span className="text-red-400 text-sm shrink-0">⚠️</span>
                    <span className="text-gray-300 text-sm">{gap}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-gray-600 text-xs">
          Last updated: {analytics?.generated_at ? new Date(analytics.generated_at).toLocaleString() : 'N/A'}
        </div>

      </div>
    </div>
  )
}