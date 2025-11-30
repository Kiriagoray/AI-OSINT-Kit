import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api, Entity, Finding } from '../lib/api'
import { format } from 'date-fns'

export default function EntityDetail() {
  const { id } = useParams<{ id: string }>()
  const [entity, setEntity] = useState<Entity | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return

    const fetchEntity = async () => {
      try {
        setLoading(true)
        const data = await api.getEntity(parseInt(id))
        setEntity(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load entity')
      } finally {
        setLoading(false)
      }
    }

    fetchEntity()
  }, [id])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-dark-muted">Loading entity details...</div>
      </div>
    )
  }

  if (error || !entity) {
    return (
      <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-6">
        <p className="text-red-400">{error || 'Entity not found'}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Entity Details</h1>
        {entity.scan_id && (
          <Link
            to={`/scan/${entity.scan_id}`}
            className="text-blue-400 hover:text-blue-300"
          >
            ← Back to Scan
          </Link>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Entity Information */}
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Entity Information</h2>
          <dl className="space-y-3">
            <div>
              <dt className="text-sm text-dark-muted">Type</dt>
              <dd className="text-white capitalize">{entity.type}</dd>
            </div>
            <div>
              <dt className="text-sm text-dark-muted">Value</dt>
              <dd className="text-white font-mono">{entity.canonical_value}</dd>
            </div>
            {entity.scan_id && (
              <div>
                <dt className="text-sm text-dark-muted">Scan ID</dt>
                <dd className="text-white">
                  <Link
                    to={`/scan/${entity.scan_id}`}
                    className="text-blue-400 hover:text-blue-300"
                  >
                    #{entity.scan_id}
                  </Link>
                </dd>
              </div>
            )}
            <div>
              <dt className="text-sm text-dark-muted">First Seen</dt>
              <dd className="text-white">
                {format(new Date(entity.first_seen), 'PPpp')}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-dark-muted">Last Seen</dt>
              <dd className="text-white">
                {format(new Date(entity.last_seen), 'PPpp')}
              </dd>
            </div>
            {entity.metadata && (
              <div>
                <dt className="text-sm text-dark-muted">Metadata</dt>
                <dd className="text-white">
                  <pre className="bg-dark-bg p-3 rounded text-xs overflow-auto">
                    {JSON.stringify(entity.metadata, null, 2)}
                  </pre>
                </dd>
              </div>
            )}
          </dl>
        </div>

        {/* Findings */}
        <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">
            Findings ({entity.findings?.length || 0})
          </h2>
          {entity.findings && entity.findings.length > 0 ? (
            <div className="space-y-3">
              {entity.findings.map((finding: Finding) => (
                <div
                  key={finding.id}
                  className="bg-dark-bg border border-dark-border rounded p-4"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-white capitalize">
                      {finding.source}
                    </span>
                    <span className="text-xs text-dark-muted">
                      {format(new Date(finding.created_at), 'PPp')}
                    </span>
                  </div>
                  <div className="text-sm text-dark-muted mb-2">
                    Type: <span className="text-white capitalize">{finding.type}</span>
                  </div>
                  {finding.confidence_score !== undefined && (
                    <div className="text-sm text-dark-muted mb-2">
                      Confidence: <span className="text-white">{finding.confidence_score.toFixed(2)}</span>
                    </div>
                  )}
                  {finding.raw_result && (
                    <details className="mt-2">
                      <summary className="text-sm text-blue-400 cursor-pointer hover:text-blue-300">
                        View Raw Result
                      </summary>
                      <pre className="mt-2 bg-dark-surface p-2 rounded text-xs overflow-auto">
                        {JSON.stringify(finding.raw_result, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-dark-muted">No findings available for this entity.</p>
          )}
        </div>
      </div>
    </div>
  )
}
