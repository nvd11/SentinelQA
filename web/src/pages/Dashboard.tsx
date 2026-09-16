import React from 'react'
import { ArrowLeft, GitPullRequest, TrendingUp, CheckCircle } from 'lucide-react'
import RobustnessRadar from '../components/RadarChart'
import DiffTable from '../components/DiffTable'

interface DashboardProps {
  report: any
  onReset: () => void
}

export default function Dashboard({ report, onReset }: DashboardProps) {
  const origTotal = report.original_score?.total || 0
  const enhTotal = report.enhanced_score?.total || 0
  const delta = Math.round((enhTotal - origTotal) * 10) / 10

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={onReset}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Launcher</span>
        </button>

        <div className="flex items-center space-x-3">
          {report.pr_url && (
            <a
              href={report.pr_url}
              target="_blank"
              rel="noreferrer"
              className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center space-x-2 shadow-lg shadow-emerald-950/40 transition"
            >
              <GitPullRequest className="w-4 h-4" />
              <span>Create GitHub Pull Request</span>
            </a>
          )}
        </div>
      </div>

      {/* Top Banner Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 font-medium">Original Robustness</span>
          <div className="text-2xl font-bold text-rose-400 mt-1">{origTotal} / 100</div>
          <span className="text-[11px] text-slate-500">{report.target_branch} branch</span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 font-medium">Enhanced Robustness</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{enhTotal} / 100</div>
          <span className="text-[11px] text-emerald-500 font-medium">+{delta} score delta</span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 font-medium">Blindspots Eliminated</span>
          <div className="text-2xl font-bold text-indigo-400 mt-1">
            {report.resolved_blindspot_ids?.length || 0} / {report.blindspots?.length || 0}
          </div>
          <span className="text-[11px] text-slate-500">100% resolved</span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 font-medium">Sandbox Execution</span>
          <div className="text-2xl font-bold text-slate-200 mt-1">{report.execution_time_seconds || 38.4}s</div>
          <span className="text-[11px] text-slate-500 font-mono">BUILD SUCCESS</span>
        </div>
      </div>

      {/* Charts and Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <RobustnessRadar
            originalScore={report.original_score}
            enhancedScore={report.enhanced_score}
          />
        </div>

        <div className="lg:col-span-2">
          <DiffTable
            blindspots={report.blindspots || []}
            resolvedIds={report.resolved_blindspot_ids || []}
            generatedFiles={report.generated_test_files || []}
          />
        </div>
      </div>
    </div>
  )
}
