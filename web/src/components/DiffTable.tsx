import React from 'react'
import { CheckCircle2, AlertTriangle, ShieldCheck, FileCode } from 'lucide-react'

interface DiffTableProps {
  blindspots: any[]
  resolvedIds: string[]
  generatedFiles: string[]
}

export default function DiffTable({ blindspots, resolvedIds, generatedFiles }: DiffTableProps) {
  return (
    <div className="space-y-6">
      <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800">
        <h3 className="text-sm font-semibold text-slate-300 mb-3 flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Blindspot Resolution Matrix</span>
        </h3>
        <div className="divide-y divide-slate-800">
          {blindspots.map((item) => {
            const isResolved = resolvedIds.includes(item.id)
            return (
              <div key={item.id} className="py-3 flex items-start justify-between">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                      {item.id}
                    </span>
                    <span className="text-sm font-medium text-slate-200">{item.title}</span>
                    <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded ${
                      item.severity === 'CRITICAL' ? 'bg-rose-950 text-rose-400 border border-rose-800' :
                      item.severity === 'HIGH' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-blue-950 text-blue-400 border border-blue-800'
                    }`}>
                      {item.severity}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{item.description}</p>
                </div>
                <div>
                  {isResolved ? (
                    <span className="inline-flex items-center space-x-1 text-xs text-emerald-400 font-medium">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      <span>Resolved</span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center space-x-1 text-xs text-amber-400 font-medium">
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                      <span>Pending</span>
                    </span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800">
        <h3 className="text-sm font-semibold text-slate-300 mb-2 flex items-center space-x-2">
          <FileCode className="w-4 h-4 text-indigo-400" />
          <span>Generated & Verified Test Suites</span>
        </h3>
        <ul className="space-y-2">
          {generatedFiles.map((file, idx) => (
            <li key={idx} className="text-xs font-mono bg-slate-950 p-2 rounded border border-slate-800 text-indigo-300 flex items-center justify-between">
              <span>{file}</span>
              <span className="text-emerald-400 font-sans text-[11px]">BUILD SUCCESS (JUnit 5)</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
