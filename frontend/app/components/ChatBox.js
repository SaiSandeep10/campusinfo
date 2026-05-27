'use client'
import { useState, useRef, useEffect } from 'react'
import Message from './Message'

const API_URL = process.env.NEXT_PUBLIC_API_URL

const SUGGESTED_QUESTIONS = [
  "What departments are available in ANITS?",
  "Where is the placement cell?",
  "What are the library timings?",
  "How do I join a club?",
  "When is TechNova fest?",
]

export default function ChatBox({ activeCategory = "general" }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  // Load personalized greeting
  useEffect(() => {
    const loadGreeting = async () => {
      try {
        const res = await fetch(`${API_URL}/api/personalization/greeting?session_id=default`)
        const data = await res.json()
        setMessages([{
          role: 'assistant',
          content: data.greeting || 'Hi! 👋 I am your ANITS Campus Assistant!',
          media: null,
          recommendations: [],
          timestamp: new Date().toLocaleTimeString()
        }])
      } catch {
        setMessages([{
          role: 'assistant',
          content: 'Hi! 👋 I am your ANITS Campus Assistant. Ask me anything about ANITS!',
          media: null,
          recommendations: [],
          timestamp: new Date().toLocaleTimeString()
        }])
      }
    }
    loadGreeting()
  }, [])

  // Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const sendMessage = async (question) => {
    const userQuestion = question || input.trim()
    if (!userQuestion || isLoading) return

    // Validate input
    if (userQuestion.length > 500) {
      alert('Question too long! Please keep it under 500 characters.')
      return
    }

    setMessages(prev => [...prev, {
      role: 'user',
      content: userQuestion,
      timestamp: new Date().toLocaleTimeString()
    }])
    setInput('')
    setIsLoading(true)

    try {
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), 30000)

      const response = await fetch(`${API_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userQuestion,
          category: activeCategory === "general" ? null : activeCategory,
          session_id: "default"
        }),
        signal: controller.signal
      })

      clearTimeout(timeout)

      if (!response.ok) throw new Error(`Server error: ${response.status}`)

      const data = await response.json()

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer || "No response received.",
        media: data.media || null,
        recommendations: data.recommendations || [],
        timestamp: new Date().toLocaleTimeString()
      }])

    } catch (error) {
      const msg = error.name === 'AbortError'
        ? 'Request timed out. Please try again.'
        : `Connection error: ${error.message}`

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `⚠️ ${msg}`,
        media: null,
        recommendations: [],
        timestamp: new Date().toLocaleTimeString()
      }])
    } finally {
      setIsLoading(false)
      textareaRef.current?.focus()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleExport = () => {
    const text = messages
      .map(m => `[${m.timestamp}] ${m.role === 'user' ? 'You' : 'ANITS Assistant'}: ${m.content}`)
      .join('\n\n')
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ANITS_Chat_${new Date().toLocaleDateString()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">

        {/* Suggested questions - shown on first load */}
        {messages.length <= 1 && (
          <div className="max-w-2xl mx-auto mt-4 fade-in-up">
            <p className="text-xs font-medium uppercase tracking-widest mb-3 text-center"
              style={{ color: 'var(--text-muted)' }}>
              Popular Questions
            </p>
            <div className="flex flex-wrap gap-2 justify-center">
              {SUGGESTED_QUESTIONS.map((q, i) => (
                <button key={i} onClick={() => sendMessage(q)}
                  className="px-3 py-2 rounded-xl text-sm transition-all"
                  style={{
                    background: 'var(--bg-card)',
                    color: 'var(--text-secondary)',
                    border: '1px solid var(--border-color)'
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.background = 'var(--bg-hover)'
                    e.currentTarget.style.color = 'var(--text-primary)'
                    e.currentTarget.style.borderColor = 'rgba(59,130,246,0.4)'
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.background = 'var(--bg-card)'
                    e.currentTarget.style.color = 'var(--text-secondary)'
                    e.currentTarget.style.borderColor = 'var(--border-color)'
                  }}>
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        {messages.map((msg, i) => (
          <Message key={i} message={msg} onSuggestionClick={sendMessage} />
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex gap-3 max-w-3xl fade-in-up">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0"
              style={{ background: 'linear-gradient(135deg, #1e293b, #0f172a)', border: '1px solid rgba(59,130,246,0.2)', color: 'white' }}>
              AI
            </div>
            <div className="px-4 py-3 rounded-2xl rounded-tl-sm flex items-center gap-1.5"
              style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
              {[0, 150, 300].map((delay, i) => (
                <div key={i} className="w-2 h-2 rounded-full"
                  style={{
                    background: '#3B82F6',
                    animation: `bounce-dot 1s ${delay}ms infinite`
                  }} />
              ))}
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="px-4 py-4 border-t"
        style={{ borderColor: 'var(--border-color)', background: 'rgba(13,19,33,0.9)', backdropFilter: 'blur(12px)' }}>

        {/* Active category badge */}
        {activeCategory !== 'general' && (
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs px-2 py-1 rounded-md mono"
              style={{ background: 'rgba(59,130,246,0.1)', color: '#3B82F6', border: '1px solid rgba(59,130,246,0.2)' }}>
              Filter: {activeCategory}
            </span>
          </div>
        )}

        <div className="max-w-3xl mx-auto flex gap-2 items-end">

          {/* Export button */}
          <button onClick={handleExport}
            title="Export chat"
            className="p-3 rounded-xl transition-all shrink-0"
            style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', color: 'var(--text-muted)' }}
            onMouseEnter={e => e.currentTarget.style.color = 'var(--text-primary)'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}>
            ↓
          </button>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about ANITS..."
            rows={1}
            maxLength={500}
            className="flex-1 resize-none outline-none rounded-xl px-4 py-3 text-sm transition-all"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              fontFamily: 'Space Grotesk, sans-serif',
            }}
            onFocus={e => e.target.style.borderColor = 'rgba(59,130,246,0.5)'}
            onBlur={e => e.target.style.borderColor = 'var(--border-color)'}
          />

          {/* Send button */}
          <button onClick={() => sendMessage()}
            disabled={isLoading || !input.trim()}
            className="px-4 py-3 rounded-xl text-sm font-medium transition-all shrink-0"
            style={{
              background: isLoading || !input.trim()
                ? 'var(--bg-card)'
                : 'linear-gradient(135deg, #3B82F6, #2563EB)',
              color: isLoading || !input.trim() ? 'var(--text-muted)' : 'white',
              border: '1px solid var(--border-color)',
            }}>
            {isLoading ? '...' : 'Send →'}
          </button>

        </div>

        <p className="text-center text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
          Enter to send · Shift+Enter for new line · ↓ to export chat
        </p>

      </div>
    </div>
  )
}