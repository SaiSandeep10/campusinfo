'use client'

export default function Message({ message, onSuggestionClick }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 message-enter ${isUser ? 'flex-row-reverse' : 'flex-row'} max-w-3xl ${isUser ? 'ml-auto' : 'mr-auto'} w-full`}>

      {/* Avatar */}
      <div className="shrink-0 w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold mt-1"
        style={{
          background: isUser
            ? 'linear-gradient(135deg, #3B82F6, #2563EB)'
            : 'linear-gradient(135deg, #1e293b, #0f172a)',
          border: isUser ? 'none' : '1px solid rgba(59,130,246,0.2)',
          color: 'white'
        }}>
        {isUser ? 'U' : 'AI'}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col gap-2 flex-1 ${isUser ? 'items-end' : 'items-start'}`}>

        {/* Sender label */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>
            {isUser ? 'You' : 'ANITS Assistant'}
          </span>
          <span className="text-xs mono" style={{ color: 'var(--text-muted)' }} suppressHydrationWarning>
            {message.timestamp}
          </span>
        </div>

        {/* Bubble */}
        <div className="px-4 py-3 rounded-2xl max-w-full"
          style={{
            background: isUser
              ? 'linear-gradient(135deg, #3B82F6, #2563EB)'
              : 'var(--bg-card)',
            border: isUser ? 'none' : '1px solid var(--border-color)',
            color: 'var(--text-primary)',
            lineHeight: '1.6',
            fontSize: '0.9rem',
            borderTopRightRadius: isUser ? '4px' : '16px',
            borderTopLeftRadius: isUser ? '16px' : '4px',
          }}>
          {message.content}
        </div>

        {/* Media Links */}
        {!isUser && message.media && Object.keys(message.media).length > 0 && (
          <div className="flex flex-wrap gap-2">
            {message.media.map && message.media.images?.map((img, i) => (
              <a key={i} href={img} target="_blank" rel="noreferrer"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all"
                style={{ background: 'rgba(59,130,246,0.1)', color: '#3B82F6', border: '1px solid rgba(59,130,246,0.2)' }}>
                🖼 View Image
              </a>
            ))}
            {message.media.map && (
              <a href={message.media.map} target="_blank" rel="noreferrer"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all"
                style={{ background: 'rgba(6,182,212,0.1)', color: '#06B6D4', border: '1px solid rgba(6,182,212,0.2)' }}>
                🗺 View on Map
              </a>
            )}
          </div>
        )}

        {/* Recommendations */}
        {!isUser && message.recommendations && message.recommendations.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-1">
            {message.recommendations.map((rec, i) => (
              <button key={i} onClick={() => onSuggestionClick(rec)}
                className="px-3 py-1.5 rounded-lg text-xs transition-all text-left"
                style={{
                  background: 'rgba(59,130,246,0.06)',
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border-color)'
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = 'rgba(59,130,246,0.12)'
                  e.currentTarget.style.color = 'var(--text-primary)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = 'rgba(59,130,246,0.06)'
                  e.currentTarget.style.color = 'var(--text-secondary)'
                }}>
                ↗ {rec}
              </button>
            ))}
          </div>
        )}

      </div>
    </div>
  )
}