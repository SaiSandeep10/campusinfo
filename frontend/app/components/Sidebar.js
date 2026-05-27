'use client'
import { useState } from 'react'

const CATEGORIES = [
  { id: "general",    label: "All Topics",  icon: "⬡", desc: "Everything" },
  { id: "academics",  label: "Academics",   icon: "◈", desc: "Courses & Exams" },
  { id: "facilities", label: "Facilities",  icon: "◎", desc: "Campus Services" },
  { id: "placements", label: "Placements",  icon: "◆", desc: "Jobs & Internships" },
  { id: "clubs",      label: "Clubs",       icon: "◉", desc: "Events & Fests" },
  { id: "contacts",   label: "Contacts",    icon: "◐", desc: "Faculty & Staff" },
  { id: "locations",  label: "Locations",   icon: "◑", desc: "Campus Map" },
]

export default function Sidebar({ activeCategory, onCategoryChange }) {
  return (
    <div className="h-full flex flex-col border-r"
      style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border-color)', width: '256px' }}>

      {/* Logo */}
      <div className="p-5 border-b" style={{ borderColor: 'var(--border-color)' }}>
        <div className="flex items-center gap-3 mb-1">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm"
            style={{ background: 'linear-gradient(135deg, #3B82F6, #06B6D4)', color: 'white' }}>
            AN
          </div>
          <div>
            <div className="font-bold text-sm" style={{ color: 'var(--text-primary)' }}>ANITS</div>
            <div className="text-xs" style={{ color: 'var(--text-muted)' }}>Campus Assistant</div>
          </div>
        </div>
        <div className="mt-3 px-3 py-1.5 rounded-lg text-xs mono"
          style={{ background: 'rgba(59,130,246,0.08)', color: '#3B82F6', border: '1px solid rgba(59,130,246,0.2)' }}>
          ◈ Llama 3.3 · FAISS · RAG
        </div>
      </div>

      {/* Categories */}
      <div className="flex-1 p-3 overflow-y-auto">
        <p className="text-xs font-medium uppercase tracking-widest mb-3 px-2"
          style={{ color: 'var(--text-muted)' }}>
          Filter Topics
        </p>

        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => onCategoryChange(cat.id)}
            className="w-full text-left px-3 py-2.5 rounded-xl mb-1 flex items-center gap-3 transition-all duration-200 group"
            style={{
              background: activeCategory === cat.id ? 'rgba(59,130,246,0.12)' : 'transparent',
              border: activeCategory === cat.id ? '1px solid rgba(59,130,246,0.25)' : '1px solid transparent',
            }}
          >
            <span className="text-base transition-transform group-hover:scale-110"
              style={{ color: activeCategory === cat.id ? '#3B82F6' : 'var(--text-muted)' }}>
              {cat.icon}
            </span>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium transition-colors"
                style={{ color: activeCategory === cat.id ? 'var(--text-primary)' : 'var(--text-secondary)' }}>
                {cat.label}
              </div>
              <div className="text-xs truncate" style={{ color: 'var(--text-muted)' }}>
                {cat.desc}
              </div>
            </div>
            {activeCategory === cat.id && (
              <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#3B82F6' }} />
            )}
          </button>
        ))}
      </div>

      {/* Footer */}
      <div className="p-3 border-t" style={{ borderColor: 'var(--border-color)' }}>
        <a href="/analytics"
          className="flex items-center gap-2 w-full px-3 py-2.5 rounded-xl text-sm transition-all duration-200 mb-2"
          style={{ color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}
          onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-hover)'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <span>📊</span>
          <span>Analytics Dashboard</span>
        </a>
        <div className="px-2 pt-1">
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            Anil Neerukonda Institute
          </p>
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            Visakhapatnam, AP
          </p>
        </div>
      </div>

    </div>
  )
}