import { useEffect, useState, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api, type ScanDetail } from '../lib/api'
import { format } from 'date-fns'

export default function ScanDetail() {
  const { id } = useParams()
  const [scan, setScan] = useState<ScanDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadScan = useCallback(async () => {
    if (!id) return
    try {
      setLoading(true)
      const data = await api.getScan(parseInt(id))
      setScan(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load scan')
      console.error('Failed to load scan:', err)
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    if (id) {
      loadScan()
    }
  }, [id, loadScan])

  useEffect(() => {
    if (!id || !scan) return
    // Refresh every 2 seconds if scan is still running
    if (scan.status === 'running' || scan.status === 'queued') {
      const interval = setInterval(() => {
        loadScan()
      }, 2000)
      return () => clearInterval(interval)
    }
  }, [id, scan?.status, loadScan])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-500 bg-green-500/20'
      case 'running':
        return 'text-blue-500 bg-blue-500/20'
      case 'failed':
        return 'text-red-500 bg-red-500/20'
      case 'queued':
        return 'text-yellow-500 bg-yellow-500/20'
      default:
        return 'text-gray-500 bg-gray-500/20'
    }
  }

  if (loading) {
    return (
      <div>
        <h1 className="text-3xl font-bold mb-6">Scan Details</h1>
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <p className="text-dark-muted">Loading scan details...</p>
        </div>
      </div>
    )
  }

  if (error || !scan) {
    return (
      <div>
        <h1 className="text-3xl font-bold mb-6">Scan Details</h1>
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <p className="text-red-500">Error: {error || 'Scan not found'}</p>
          <Link to="/" className="text-blue-500 hover:text-blue-400 mt-4 inline-block">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Scan Details</h1>
        <Link
          to="/"
          className="px-4 py-2 bg-dark-surface border border-dark-border rounded-lg hover:bg-dark-bg"
        >
          ← Back to Dashboard
        </Link>
      </div>

      {/* Scan Info */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-sm text-dark-muted mb-1">Scan ID</h3>
            <p className="text-lg font-semibold">#{scan.scan_id}</p>
          </div>
          <div>
            <h3 className="text-sm text-dark-muted mb-1">Status</h3>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(scan.status)}`}>
              {scan.status}
            </span>
          </div>
          <div>
            <h3 className="text-sm text-dark-muted mb-1">Target</h3>
            <p className="text-lg">{scan.target}</p>
          </div>
          <div>
            <h3 className="text-sm text-dark-muted mb-1">Type</h3>
            <p className="text-lg capitalize">{scan.type}</p>
          </div>
          <div>
            <h3 className="text-sm text-dark-muted mb-1">Created</h3>
            <p className="text-sm">{format(new Date(scan.created_at), 'PPpp')}</p>
          </div>
          {scan.started_at && (
            <div>
              <h3 className="text-sm text-dark-muted mb-1">Started</h3>
              <p className="text-sm">{format(new Date(scan.started_at), 'PPpp')}</p>
            </div>
          )}
          {scan.finished_at && (
            <div>
              <h3 className="text-sm text-dark-muted mb-1">Finished</h3>
              <p className="text-sm">{format(new Date(scan.finished_at), 'PPpp')}</p>
            </div>
          )}
          {scan.settings?.modules && (
            <div className="md:col-span-2">
              <h3 className="text-sm text-dark-muted mb-2">Modules</h3>
              <div className="flex flex-wrap gap-2">
                {scan.settings.modules.map((module) => (
                  <span
                    key={module}
                    className="px-3 py-1 bg-dark-bg border border-dark-border rounded-lg text-sm"
                  >
                    {module}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Entities */}
      {scan.entities && scan.entities.length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Entities Found ({scan.entities.length})</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dark-border">
                  <th className="text-left py-2 px-4">Type</th>
                  <th className="text-left py-2 px-4">Value</th>
                  <th className="text-left py-2 px-4">First Seen</th>
                </tr>
              </thead>
              <tbody>
                {scan.entities.map((entity) => (
                  <tr key={entity.id} className="border-b border-dark-border hover:bg-dark-bg">
                    <td className="py-2 px-4 capitalize">{entity.type}</td>
                    <td className="py-2 px-4">{entity.canonical_value}</td>
                    <td className="py-2 px-4 text-sm text-dark-muted">
                      {format(new Date(entity.first_seen), 'PPpp')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Findings */}
      {scan.findings && scan.findings.length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Findings ({scan.findings.length})</h2>
          <div className="space-y-4">
            {scan.findings.map((finding) => (
              <div
                key={finding.id}
                className="bg-dark-bg border border-dark-border rounded-lg p-4"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="font-semibold capitalize">{finding.source}</span>
                    <span className="text-dark-muted mx-2">•</span>
                    <span className="text-sm text-dark-muted">{finding.type}</span>
                  </div>
                  {finding.confidence_score !== undefined && (
                    <span className="text-sm text-dark-muted">
                      Confidence: {Math.round(finding.confidence_score * 100)}%
                    </span>
                  )}
                </div>
                {finding.raw_result && (
                  <pre className="text-xs bg-dark-surface p-3 rounded overflow-x-auto mt-2">
                    {JSON.stringify(finding.raw_result, null, 2)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {scan.status === 'completed' && (!scan.entities || scan.entities.length === 0) && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <p className="text-dark-muted">No entities or findings found for this scan.</p>
        </div>
      )}
    </div>
  )
}








