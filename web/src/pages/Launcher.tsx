import React, { useState } from 'react'
import { Play, GitBranch, FolderGit2, BookOpen, ShieldAlert } from 'lucide-react'
import StreamConsole from '../components/StreamConsole'

interface LauncherProps {
  onScanComplete: (report: any) => void
}

export default function Launcher({ onScanComplete }: LauncherProps) {
  const [repoUrl, setRepoUrl] = useState('https://github.com/nvd11/SentinelQA')
  const [targetBranch, setTargetBranch] = useState('main')
  const [jiraIssueId, setJiraIssueId] = useState('FIN-1042')
  const [codingStandardUrl, setCodingStandardUrl] = useState('https://github.com/nvd11/finance-coding-standards')
  const [isScanning, setIsScanning] = useState(false)
  const [logs, setLogs] = useState<any[]>([])

  const handleStartScan = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsScanning(true)
    setLogs([])

    try {
      const response = await fetch('/api/v1/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          repo_url: repoUrl,
          target_branch: targetBranch,
          jira_issue_id: jiraIssueId,
          coding_standard_repo_url: codingStandardUrl,
        }),
      })

      if (!response.body) return
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim()
            if (!dataStr) continue
            try {
              const parsed = JSON.parse(dataStr)
              if (parsed.stage) {
                setLogs((prev) => [...prev, parsed])
              } else if (parsed.scan_id) {
                // Completed result
                setIsScanning(false)
                onScanComplete(parsed)
              }
            } catch (err) {
              console.error(err)
            }
          }
        }
      }
    } catch (err) {
      console.error(err)
      setIsScanning(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h2 className="text-xl font-bold mb-1 flex items-center space-x-2">
          <FolderGit2 className="w-5 h-5 text-indigo-400" />
          <span>Launch Autonomous Quality Audit</span>
        </h2>
        <p className="text-sm text-slate-400 mb-6">
          Specify target repository, acceptance criteria source, and optional department coding standards.
        </p>

        <form onSubmit={handleStartScan} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Target GitHub Repo</label>
              <input
                type="text"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Target Branch</label>
              <input
                type="text"
                value={targetBranch}
                onChange={(e) => setTargetBranch(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Jira Issue ID (Optional)</label>
              <input
                type="text"
                value={jiraIssueId}
                onChange={(e) => setJiraIssueId(e.target.value)}
                placeholder="e.g. FIN-1042"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Department Coding Standards Repo (Optional)</label>
              <input
                type="text"
                value={codingStandardUrl}
                onChange={(e) => setCodingStandardUrl(e.target.value)}
                placeholder="https://github.com/..."
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isScanning}
            className="w-full mt-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-900 text-white font-semibold py-2.5 rounded-lg flex items-center justify-center space-x-2 transition shadow-lg shadow-indigo-950/50"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{isScanning ? 'Autonomous Agent Running...' : 'Execute SentinelQA Agent'}</span>
          </button>
        </form>
      </div>

      <StreamConsole logs={logs} isScanning={isScanning} />
    </div>
  )
}
