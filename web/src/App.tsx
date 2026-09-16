import React, { useState } from 'react'
import Launcher from './pages/Launcher'
import Dashboard from './pages/Dashboard'

export default function App() {
  const [report, setReport] = useState<any>(null)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-lg">
            S
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">SentinelQA</h1>
            <p className="text-xs text-slate-400">Autonomous SDLC Quality Assurance Agent</p>
          </div>
        </div>
        <div className="text-xs text-slate-500 font-mono">
          Hackathon 2026 Edition
        </div>
      </header>

      <main className="flex-1 p-6">
        {!report ? (
          <Launcher onScanComplete={(data) => setReport(data)} />
        ) : (
          <Dashboard report={report} onReset={() => setReport(null)} />
        )}
      </main>
    </div>
  )
}
