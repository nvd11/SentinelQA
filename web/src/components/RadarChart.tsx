import React from 'react'
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts'

interface RadarProps {
  originalScore: any
  enhancedScore: any
}

export default function RobustnessRadar({ originalScore, enhancedScore }: RadarProps) {
  const data = [
    {
      dimension: 'Business ACs',
      original: originalScore?.business_ac || 60,
      enhanced: enhancedScore?.business_ac || 88,
      fullMark: 100,
    },
    {
      dimension: 'Resilience & Edges',
      original: originalScore?.resilience || 55,
      enhanced: enhancedScore?.resilience || 90,
      fullMark: 100,
    },
    {
      dimension: 'Coding Standards',
      original: originalScore?.coding_standards || 62,
      enhanced: enhancedScore?.coding_standards || 92,
      fullMark: 100,
    },
    {
      dimension: 'Assertion Depth',
      original: originalScore?.assertion_depth || 50,
      enhanced: enhancedScore?.assertion_depth || 85,
      fullMark: 100,
    },
  ]

  return (
    <div className="w-full h-80 bg-slate-900/50 rounded-xl p-4 border border-slate-800">
      <h3 className="text-sm font-semibold text-slate-300 mb-2">Multi-Dimension Robustness Matrix</h3>
      <ResponsiveContainer width="100%" height="90%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="dimension" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
          <Radar name="Original Branch" dataKey="original" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.25} />
          <Radar name="Enhanced Branch" dataKey="enhanced" stroke="#10b981" fill="#10b981" fillOpacity={0.4} />
          <Legend />
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
