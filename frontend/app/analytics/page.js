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
    <div className="flex items-center justify-center h-screen"
      style={{ background: 'var(--bg-primary)' }}>
      <div className="text-center">
        <div className="flex gap-2 justify-center mb-4">
          {[0, 150, 300].map((delay, i) => (
            <span key={i} className="w-3 h-3 rounded-full animate-bounce"
              style={{ background: '#3B82F6', animationDelay: `${delay}ms` }} />
          ))}
        </div>
        <p style={{ color: '#94A3B8' }}>Loading Analytics...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="flex items-center justify-center h-screen"
      style={{ background: 'var(--bg-primary)' }}>
      <p style={{ color: '#EF4444' }}>Error: {error}</p>
    </div>
  )

  const stats = analytics?.overall_stats || {}
  const popular = analytics?.popular_queries || []
  const categories = analytics?.category_distribution || {}
  const activity = analytics?.daily_activity || []
  const gaps = analytics?.information_gaps || []

  const categoryColors = {
    academics: '#3B82F6',
    facilities: '#10B981',
    placements: '#F59E0B',
    clubs: '#8B5CF6',
    contacts: '#06B6D4',
    locations: '#EF4444',
    general: '#94A3B8',
  }

  return (
    <div className="analytics-page" style={{
      background: 'var(--bg-primary)',
      minHeight: '100vh',
      overflowY: 'scroll',
      height: '100vh',
      color: 'var(--text-primary)',
      padding: '24px',
      fontFamily: 'Space Grotesk, sans-serif'
    }}>

      <div style={{ maxWidth: '1100px', margin: '0 auto' }}>

        {/* ── Header ── */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
              <div style={{
                width: '36px', height: '36px', borderRadius: '10px',
                background: 'linear-gradient(135deg, #3B82F6, #06B6D4)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 'bold', fontSize: '14px', color: 'white'
              }}>AN</div>
              <h1 style={{ fontSize: '24px', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                Analytics Dashboard
              </h1>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', margin: 0 }}>
              ANITS Campus Assistant — Usage Insights
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={fetchAnalytics}
              style={{
                padding: '8px 16px', borderRadius: '10px', fontSize: '13px',
                background: 'rgba(59,130,246,0.15)', color: '#3B82F6',
                border: '1px solid rgba(59,130,246,0.3)', cursor: 'pointer',
                fontFamily: 'Space Grotesk, sans-serif'
              }}>
              🔄 Refresh
            </button>
            <a href="/"
              style={{
                padding: '8px 16px', borderRadius: '10px', fontSize: '13px',
                background: 'var(--bg-card)', color: 'var(--text-secondary)',
                border: '1px solid var(--border-color)', textDecoration: 'none',
                display: 'inline-flex', alignItems: 'center'
              }}>
              ← Back to Chat
            </a>
          </div>
        </div>

        {/* ── Stats Cards ── */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
          {[
            { label: "Total Messages", value: stats.total_messages || 0, icon: "💬", color: '#3B82F6' },
            { label: "Total Sessions", value: stats.total_sessions || 0, icon: "👥", color: '#10B981' },
            { label: "Today", value: stats.messages_today || 0, icon: "📅", color: '#8B5CF6' },
            { label: "This Week", value: stats.messages_this_week || 0, icon: "📈", color: '#F59E0B' },
          ].map((stat, i) => (
            <div key={i} style={{
              background: 'var(--bg-card)',
              borderRadius: '16px',
              padding: '20px',
              border: '1px solid var(--border-color)',
            }}>
              <div style={{ fontSize: '28px', marginBottom: '8px' }}>{stat.icon}</div>
              <div style={{ fontSize: '28px', fontWeight: '700', color: stat.color, marginBottom: '4px' }}>
                {stat.value}
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* ── Popular + Category ── */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>

          {/* Popular Queries */}
          <div style={{
            background: 'var(--bg-card)', borderRadius: '16px',
            padding: '24px', border: '1px solid var(--border-color)'
          }}>
            <h2 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '16px', marginTop: 0 }}>
              🔥 Popular Questions
            </h2>
            {popular.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
                No data yet. Start asking questions!
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {popular.map((q, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: 1, minWidth: 0 }}>
                      <span style={{ color: '#3B82F6', fontWeight: '700', fontSize: '12px', width: '24px', flexShrink: 0 }}>
                        #{i + 1}
                      </span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '13px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {q.question}
                      </span>
                    </div>
                    <span style={{
                      background: '#3B82F6', color: 'white',
                      fontSize: '11px', padding: '2px 8px',
                      borderRadius: '999px', flexShrink: 0
                    }}>
                      {q.count}x
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Category Distribution */}
          <div style={{
            background: 'var(--bg-card)', borderRadius: '16px',
            padding: '24px', border: '1px solid var(--border-color)'
          }}>
            <h2 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '16px', marginTop: 0 }}>
              📂 Category Usage
            </h2>
            {Object.keys(categories).length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>No data yet!</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {Object.entries(categories).map(([cat, data], i) => {
                  const color = categoryColors[cat] || '#3B82F6'
                  return (
                    <div key={i}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span style={{ color: 'var(--text-secondary)', fontSize: '13px', textTransform: 'capitalize' }}>
                          {cat}
                        </span>
                        <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
                          {data.count} ({data.percentage}%)
                        </span>
                      </div>
                      <div style={{ background: 'var(--bg-hover)', borderRadius: '999px', height: '8px' }}>
                        <div style={{
                          background: color,
                          width: `${data.percentage}%`,
                          height: '8px',
                          borderRadius: '999px',
                          transition: 'width 0.5s ease'
                        }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

        </div>

        {/* ── Daily Activity + Info Gaps ── */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>

          {/* Daily Activity */}
          <div style={{
            background: 'var(--bg-card)', borderRadius: '16px',
            padding: '24px', border: '1px solid var(--border-color)'
          }}>
            <h2 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '16px', marginTop: 0 }}>
              📅 Daily Activity (Last 7 Days)
            </h2>
            {activity.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>No data yet!</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {activity.map((day, i) => {
                  const maxCount = Math.max(...activity.map(d => d.count)) || 1
                  const width = Math.max((day.count / maxCount) * 100, 2)
                  return (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span style={{ color: 'var(--text-muted)', fontSize: '11px', width: '44px', flexShrink: 0 }}>
                        {day.date}
                      </span>
                      <div style={{ flex: 1, background: 'var(--bg-hover)', borderRadius: '999px', height: '16px' }}>
                        <div style={{
                          background: 'linear-gradient(90deg, #10B981, #06B6D4)',
                          width: `${width}%`,
                          height: '16px',
                          borderRadius: '999px',
                          transition: 'width 0.5s ease'
                        }} />
                      </div>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '12px', width: '20px', textAlign: 'right' }}>
                        {day.count}
                      </span>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          {/* Information Gaps */}
          <div style={{
            background: 'var(--bg-card)', borderRadius: '16px',
            padding: '24px', border: '1px solid var(--border-color)'
          }}>
            <h2 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '4px', marginTop: 0 }}>
              ⚠️ Information Gaps
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '11px', marginBottom: '16px', marginTop: 0 }}>
              Questions where chatbot gave fallback responses
            </p>
            {gaps.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '20px 0' }}>
                <div style={{ fontSize: '32px', marginBottom: '8px' }}>✅</div>
                <p style={{ color: '#10B981', fontSize: '14px', fontWeight: '600', margin: 0 }}>
                  No gaps detected!
                </p>
                <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '4px' }}>
                  Chatbot is answering all questions correctly!
                </p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {gaps.map((gap, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'flex-start', gap: '8px',
                    background: 'rgba(239,68,68,0.08)',
                    border: '1px solid rgba(239,68,68,0.2)',
                    borderRadius: '10px', padding: '10px 12px'
                  }}>
                    <span style={{ color: '#EF4444', fontSize: '14px', flexShrink: 0 }}>⚠️</span>
                    <span style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>{gap}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* ── Cache Stats ── */}
        <CacheStats apiUrl={API_URL} />

        {/* ── Footer ── */}
        <div style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '11px', marginTop: '24px', paddingBottom: '24px' }}>
          Last updated: {analytics?.generated_at
            ? new Date(analytics.generated_at).toLocaleString()
            : 'N/A'}
        </div>

      </div>
    </div>
  )
}

// ── Cache Stats Component ──
function CacheStats({ apiUrl }) {
  const [cache, setCache] = useState(null)

  useEffect(() => {
    fetch(`${apiUrl}/api/cache/stats`)
      .then(r => r.json())
      .then(setCache)
      .catch(() => {})
  }, [])

  if (!cache) return null

  return (
    <div style={{
      background: 'var(--bg-card)', borderRadius: '16px',
      padding: '24px', border: '1px solid var(--border-color)',
      marginBottom: '20px'
    }}>
      <h2 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '16px', marginTop: 0 }}>
        ⚡ Cache Performance
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
        {[
          { label: "Cached Entries", value: cache.total_entries || 0, color: '#3B82F6' },
          { label: "Total Hits", value: cache.total_hits || 0, color: '#10B981' },
          { label: "Hit Rate", value: cache.hit_rate || '0%', color: '#F59E0B' },
          { label: "TTL", value: `${cache.ttl_minutes || 60} min`, color: '#8B5CF6' },
        ].map((s, i) => (
          <div key={i} style={{
            background: 'var(--bg-secondary)',
            borderRadius: '12px', padding: '14px',
            border: '1px solid var(--border-color)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '20px', fontWeight: '700', color: s.color }}>{s.value}</div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>{s.label}</div>
          </div>
        ))}
      </div>

      {cache.top_queries && cache.top_queries.length > 0 && (
        <div style={{ marginTop: '16px' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginBottom: '8px' }}>
            Top Cached Queries:
          </p>
          {cache.top_queries.map((q, i) => (
            <div key={i} style={{
              display: 'flex', justifyContent: 'space-between',
              padding: '6px 0',
              borderBottom: '1px solid var(--border-color)'
            }}>
              <span style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>{q.query}</span>
              <span style={{ color: '#3B82F6', fontSize: '12px' }}>{q.hits} hits</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}