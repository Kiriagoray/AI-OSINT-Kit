import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, Scan } from '../lib/api'
import { format } from 'date-fns'

export default function Dashboard() {
  const [scans, setScans] = useState<Scan[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadScans()
    // Refresh every 5 seconds to get updated scan statuses
    const interval = setInterval(loadScans, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadScans = async () => {
    try {
      setLoading(true)
      const data = await api.getScans()
      setScans(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load scans')
      console.error('Failed to load scans:', err)
    } finally {
      setLoading(false)
    }
  }

  const activeScans = scans.filter(s => s.status === 'running' || s.status === 'queued').length
  const completedScans = scans.filter(s => s.status === 'completed').length
  const recentScans = scans.slice(0, 10)

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-500'
      case 'running':
        return 'text-blue-500'
      case 'failed':
        return 'text-red-500'
      case 'queued':
        return 'text-yellow-500'
      default:
        return 'text-gray-500'
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-4">
          <p className="text-red-500">Error: {error}</p>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h3 className="text-sm text-dark-muted mb-2">Total Scans</h3>
          <p className="text-2xl font-bold">{loading ? '...' : scans.length}</p>
        </div>
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h3 className="text-sm text-dark-muted mb-2">Active Scans</h3>
          <p className="text-2xl font-bold">{loading ? '...' : activeScans}</p>
        </div>
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h3 className="text-sm text-dark-muted mb-2">Completed</h3>
          <p className="text-2xl font-bold">{loading ? '...' : completedScans}</p>
        </div>
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h3 className="text-sm text-dark-muted mb-2">Failed</h3>
          <p className="text-2xl font-bold text-red-500">
            {loading ? '...' : scans.filter(s => s.status === 'failed').length}
          </p>
        </div>
      </div>

      {/* Recent Scans */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Recent Scans</h2>
          <Link
            to="/scan/new"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            New Scan
          </Link>
        </div>
        
        {loading ? (
          <p className="text-dark-muted">Loading scans...</p>
        ) : recentScans.length === 0 ? (
          <p className="text-dark-muted">No scans yet. Start a new scan to begin.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dark-border">
                  <th className="text-left py-2 px-4">ID</th>
                  <th className="text-left py-2 px-4">Target</th>
                  <th className="text-left py-2 px-4">Type</th>
                  <th className="text-left py-2 px-4">Status</th>
                  <th className="text-left py-2 px-4">Created</th>
                  <th className="text-left py-2 px-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {recentScans.map((scan) => (
                  <tr key={scan.scan_id} className="border-b border-dark-border hover:bg-dark-bg">
                    <td className="py-2 px-4">{scan.scan_id}</td>
                    <td className="py-2 px-4">{scan.target}</td>
                    <td className="py-2 px-4 capitalize">{scan.type}</td>
                    <td className="py-2 px-4">
                      <span className={getStatusColor(scan.status)}>
                        {scan.status}
                      </span>
                    </td>
                    <td className="py-2 px-4 text-sm text-dark-muted">
                      {format(new Date(scan.created_at), 'MMM d, yyyy HH:mm')}
                    </td>
                    <td className="py-2 px-4">
                      <Link
                        to={`/scan/${scan.scan_id}`}
                        className="text-blue-500 hover:text-blue-400"
                      >
                        View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}








