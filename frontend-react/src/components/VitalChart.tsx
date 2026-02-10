import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

interface VitalChartProps {
  data: Array<{ time: string; value: number }>
  color: string
  label: string
}

export default function VitalChart({ data, color, label }: VitalChartProps) {
  console.log(`[VitalChart] ${label}:`, data.length, 'points')
  
  if (!data || data.length === 0) {
    return (
      <div className="vital-chart">
        <div className="chart-label">{label}</div>
        <div style={{ 
          height: '200px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: '#94a3b8',
          fontSize: '14px',
          border: '1px dashed #2a2a2a',
          borderRadius: '8px'
        }}>
          Waiting for data...
        </div>
      </div>
    )
  }
  
  return (
    <div className="vital-chart">
      <div className="chart-label">
        {label} <span style={{ fontSize: '12px', color: '#94a3b8', fontWeight: 'normal' }}>({data.length} points)</span>
      </div>
      <LineChart 
        width={1000} 
        height={200} 
        data={data}
        margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
        <XAxis 
          dataKey="time" 
          stroke="#94a3b8"
          tick={{ fill: '#94a3b8', fontSize: 11 }}
        />
        <YAxis 
          stroke="#94a3b8"
          tick={{ fill: '#94a3b8', fontSize: 11 }}
        />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#0a0a0a', 
            border: '1px solid #2a2a2a',
            borderRadius: '8px',
            color: '#ffffff',
            fontSize: '12px'
          }}
          labelStyle={{ color: '#94a3b8' }}
        />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke={color} 
          strokeWidth={2}
          dot={{ fill: color, r: 3 }}
          activeDot={{ r: 5, fill: color }}
          isAnimationActive={false}
        />
      </LineChart>
    </div>
  )
}
