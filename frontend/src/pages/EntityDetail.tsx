import { useParams } from 'react-router-dom'

export default function EntityDetail() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Entity Details</h1>
      <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
        <p className="text-dark-muted">Entity ID: {id}</p>
        <p className="text-dark-muted mt-4">Entity detail page coming soon...</p>
      </div>
    </div>
  )
}












