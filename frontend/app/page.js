'use client'
import { useState } from "react"
import ChatBox from "./components/ChatBox"
import Sidebar from "./components/Sidebar"

export default function Home() {
  const [activeCategory, setActiveCategory] = useState("general")
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <main className="flex h-screen overflow-hidden grid-bg" style={{ background: 'var(--bg-primary)' }}>

      {/* Ambient glow effects */}
      <div className="fixed top-0 left-0 w-96 h-96 rounded-full opacity-5 pointer-events-none"
        style={{ background: 'radial-gradient(circle, #3B82F6, transparent)', transform: 'translate(-30%, -30%)' }} />
      <div className="fixed bottom-0 right-0 w-96 h-96 rounded-full opacity-5 pointer-events-none"
        style={{ background: 'radial-gradient(circle, #06B6D4, transparent)', transform: 'translate(30%, 30%)' }} />

      {/* Sidebar */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-0 overflow-hidden'}`}>
        <Sidebar
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1 min-w-0">

        {/* Top bar */}
        <div className="flex items-center gap-3 px-4 py-3 border-b"
          style={{ borderColor: 'var(--border-color)', background: 'rgba(13,19,33,0.8)', backdropFilter: 'blur(12px)' }}>

          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg transition-colors hover:bg-white/5 text-slate-400 hover:text-white"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>

          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold"
              style={{ background: 'linear-gradient(135deg, #3B82F6, #06B6D4)' }}>
              A
            </div>
            <span className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
              ANITS Campus Assistant
            </span>
          </div>

          <div className="ml-auto flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>Online</span>
          </div>

        </div>

        <ChatBox activeCategory={activeCategory} />

      </div>
    </main>
  )
}