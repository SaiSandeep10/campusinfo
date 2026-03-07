'use client';

import { useState } from 'react';
import ChatBox from './components/ChatBox';
import Sidebar from './components/Sidebar';

export default function Home() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <main className="flex h-screen bg-gray-950 text-white">
      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
      />
      <div className="flex flex-col flex-1 h-screen overflow-hidden">
        <header className="flex items-center justify-between px-6 py-4 bg-gray-900 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="text-gray-400 hover:text-white transition"
            >
              ☰
            </button>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🎓</span>
              <div>
                <h1 className="text-lg font-bold text-white">
                  ANITS Campus Assistant
                </h1>
                <p className="text-xs text-green-400">
                  ● Online — Powered by Llama 3
                </p>
              </div>
            </div>
          </div>
          <div className="text-sm text-gray-400 hidden md:block">
            Anil Neerukonda Institute of Technology & Sciences
          </div>
        </header>
        <ChatBox />
      </div>
    </main>
  );
}