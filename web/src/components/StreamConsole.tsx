import React from 'react'
import { Terminal, Loader2 } from 'lucide-react'

interface ThoughtItem {
  timestamp: string
  stage: string
  message: string
}

interface StreamConsoleProps {
  logs: ThoughtItem[]
  isScanning: boolean
}

export default function StreamConsole({ logs, isScanning }: StreamConsoleProps) {
  return (
    <div className="bg-slate-950 rounded-xl border border-slate-800 p-4 font-mono text-xs flex flex-col h-72">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
        <div className="flex items-center space-x-2 text-slate-400">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-slate-300">SentinelQA Agent Runtime Stream</span>
        </div>
        {isScanning && (
          <div className="flex items-center space-x-2 text-indigo-400">
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span className="text-[11px]">Processing...</span>
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-2">
        {logs.length === 0 ? (
          <div className="text-slate-600 italic">Waiting for scan initiation...</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="flex items-start space-x-2">
              <span className="text-slate-500 select-none">[{log.timestamp}]</span>
              <span className="text-indigo-400 font-bold uppercase select-none">[{log.stage}]</span>
              <span className="text-slate-200">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
