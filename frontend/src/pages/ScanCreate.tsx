import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'

const OSINT_MODULES = [
  { id: 'whois', label: 'WHOIS Lookup' },
  { id: 'ssl', label: 'SSL Certificates' },
  { id: 'dns', label: 'Passive DNS' },
  { id: 'shodan', label: 'Shodan Scan' },
  { id: 'hibp', label: 'HaveIBeenPwned' },
  { id: 'social', label: 'Social Handle Discovery' },
]

export default function ScanCreate() {
  const [target, setTarget] = useState('')
  const [scanType, setScanType] = useState('domain')
  const [selectedModules, setSelectedModules] = useState<string[]>(['whois', 'ssl'])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleModuleToggle = (moduleId: string) => {
    setSelectedModules((prev) =>
      prev.includes(moduleId)
        ? prev.filter((id) => id !== moduleId)
        : [...prev, moduleId]
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const scan = await api.createScan({
        target,
        type: scanType,
        modules: selectedModules,
      })
      navigate(`/scan/${scan.scan_id}`)
    } catch (error) {
      console.error('Failed to create scan:', error)
      alert(error instanceof Error ? error.message : 'Failed to create scan')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Create New Scan</h1>

      <form onSubmit={handleSubmit} className="bg-dark-surface border border-dark-border rounded-lg p-6">
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Target</label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="example.com, user@example.com, or 192.168.1.1"
            className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Scan Type</label>
          <select
            value={scanType}
            onChange={(e) => setScanType(e.target.value)}
            className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="domain">Domain</option>
            <option value="email">Email</option>
            <option value="ip">IP Address</option>
            <option value="handle">Social Handle</option>
          </select>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">OSINT Modules</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {OSINT_MODULES.map((module) => (
              <label
                key={module.id}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedModules.includes(module.id)}
                  onChange={() => handleModuleToggle(module.id)}
                  className="w-4 h-4 text-blue-600 bg-dark-bg border-dark-border rounded focus:ring-blue-500"
                />
                <span>{module.label}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !target}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating...' : 'Start Scan'}
        </button>
      </form>
    </div>
  )
}








