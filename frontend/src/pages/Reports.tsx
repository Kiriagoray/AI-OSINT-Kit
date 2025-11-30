import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, Scan } from '../lib/api'
import { format } from 'date-fns'

interface Report {
  id: number
  scan_id: number
  title: string | null
  generated_text: string | null
  sections: any
  score: number | null
  created_at: string
}

export default function Reports() {
  const [scans, setScans] = useState<Scan[]>([])
  const [selectedScan, setSelectedScan] = useState<number | null>(null)
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const data = await api.getScans()
        setScans(data)
      } catch (err) {
        console.error('Failed to fetch scans:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchScans()
  }, [])

  useEffect(() => {
    if (!selectedScan) {
      setReports([])
      return
    }

    const fetchReports = async () => {
      try {
        const data = await api.getScanReports(selectedScan)
        setReports(data)
      } catch (err) {
        console.error('Failed to fetch reports:', err)
        setReports([])
      }
    }

    fetchReports()
  }, [selectedScan])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-dark-muted">Loading...</div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Reports</h1>

      <div className="mb-6">
        <label className="block text-sm font-medium text-dark-muted mb-2">
          Select Scan
        </label>
        <select
          value={selectedScan || ''}
          onChange={(e) => setSelectedScan(parseInt(e.target.value))}
          className="bg-dark-surface border border-dark-border rounded px-4 py-2 text-white w-full max-w-md"
        >
          <option value="">Select a scan to view reports</option>
          {scans.map((scan) => (
            <option key={scan.scan_id} value={scan.scan_id}>
              {scan.target} - {scan.status} ({format(new Date(scan.created_at), 'PPp')})
            </option>
          ))}
        </select>
      </div>

      {selectedScan && (
        <div className="mb-4">
          <Link
            to={`/scan/${selectedScan}`}
            className="text-blue-400 hover:text-blue-300 text-sm"
          >
            View Scan Details →
          </Link>
        </div>
      )}

      {reports.length === 0 && selectedScan && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <p className="text-dark-muted">No reports available for this scan.</p>
          <p className="text-dark-muted text-sm mt-2">
            Reports are generated using LLM analysis. This feature is coming soon.
          </p>
        </div>
      )}

      {reports.length > 0 && (
        <div className="space-y-4">
          {reports.map((report) => (
            <div
              key={report.id}
              className="bg-dark-surface border border-dark-border rounded-lg p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold">
                    {report.title || `Report #${report.id}`}
                  </h2>
                  <p className="text-sm text-dark-muted mt-1">
                    Generated {format(new Date(report.created_at), 'PPpp')}
                  </p>
                </div>
                {report.score !== null && (
                  <div className="text-right">
                    <div className="text-sm text-dark-muted">Risk Score</div>
                    <div
                      className={`text-2xl font-bold ${
                        report.score >= 7
                          ? 'text-red-400'
                          : report.score >= 4
                          ? 'text-yellow-400'
                          : 'text-green-400'
                      }`}
                    >
                      {report.score}/10
                    </div>
                  </div>
                )}
              </div>

              {report.generated_text && (
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-dark-muted mb-2">Summary</h3>
                  <p className="text-white whitespace-pre-wrap">{report.generated_text}</p>
                </div>
              )}

              {report.sections && (
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-dark-muted mb-2">Sections</h3>
                  <pre className="bg-dark-bg p-3 rounded text-xs overflow-auto">
                    {JSON.stringify(report.sections, null, 2)}
                  </pre>
                </div>
              )}

              <div className="mt-4 pt-4 border-t border-dark-border">
                <Link
                  to={`/scan/${report.scan_id}`}
                  className="text-blue-400 hover:text-blue-300 text-sm"
                >
                  View related scan →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
