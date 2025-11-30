// API client for backend API

const API_BASE_URL = '/api/v1'

export interface Scan {
  scan_id: number
  target: string
  type: string
  status: 'queued' | 'running' | 'failed' | 'completed'
  settings?: {
    modules?: string[]
  }
  created_at: string
  started_at?: string
  finished_at?: string
}

export interface Entity {
  id: number
  scan_id?: number
  type: string
  canonical_value: string
  metadata?: any
  first_seen: string
  last_seen: string
}

export interface Finding {
  id: number
  entity_id: number
  source: string
  type: string
  confidence_score?: number
  raw_result?: any
  created_at: string
}

export interface ScanDetail extends Scan {
  entities?: Entity[]
  findings?: Finding[]
}

// API client functions
export const api = {
  // Get all scans
  async getScans(): Promise<Scan[]> {
    const response = await fetch(`${API_BASE_URL}/scan`)
    if (!response.ok) {
      throw new Error('Failed to fetch scans')
    }
    return response.json()
  },

  // Get scan by ID
  async getScan(id: number): Promise<ScanDetail> {
    const response = await fetch(`${API_BASE_URL}/scan/${id}`)
    if (!response.ok) {
      throw new Error('Failed to fetch scan')
    }
    return response.json()
  },

  // Create a new scan
  async createScan(data: {
    target: string
    type: string
    modules: string[]
  }): Promise<Scan> {
    const response = await fetch(`${API_BASE_URL}/scan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to create scan' }))
      throw new Error(error.detail || 'Failed to create scan')
    }
    return response.json()
  },

  // Search entities
  async searchEntities(query: string): Promise<Entity[]> {
    const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`)
    if (!response.ok) {
      throw new Error('Failed to search entities')
    }
    const data = await response.json()
    return data.entities || []
  },

  // Get entity by ID
  async getEntity(id: number): Promise<Entity> {
    const response = await fetch(`${API_BASE_URL}/entity/${id}`)
    if (!response.ok) {
      throw new Error('Failed to fetch entity')
    }
    return response.json()
  },

  // Get health status
  async getHealth(): Promise<{ status: string; service: string; version: string }> {
    const response = await fetch('/health')
    if (!response.ok) {
      throw new Error('Failed to fetch health status')
    }
    return response.json()
  },
}





