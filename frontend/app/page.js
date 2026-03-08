'use client'

import { useState } from "react"
import ChatBox from "./components/ChatBox"
import Sidebar from "./components/Sidebar"

export default function Home() {

  const [activeCategory, setActiveCategory] = useState("general")
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex flex-col h-screen bg-gray-950">

      {/* HEADER */}
      <header className="bg-gray-900 border-b border-gray-700 px-4 py-3 flex items-center justify-between">

        <div className="flex items-center gap-3">

          {/* Toggle Button */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-gray-300 hover:text-white text-xl"
          >
            ☰
          </button>

          <h1 className="text-white font-bold text-lg">
            🎓 ANITS Campus Assistant
          </h1>

        </div>

      </header>

      {/* MAIN AREA */}
      <div className="flex flex-1 overflow-hidden">

        {/* Sidebar */}
        {sidebarOpen && (
          <Sidebar
            activeCategory={activeCategory}
            onCategoryChange={setActiveCategory}
          />
        )}

        {/* Chat */}
        <ChatBox activeCategory={activeCategory} />

      </div>

    </div>
  )
}