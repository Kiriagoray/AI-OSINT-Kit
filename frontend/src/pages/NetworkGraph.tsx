import { useEffect, useState, useRef } from 'react'
import { api, Scan } from '../lib/api'
import cytoscape from 'cytoscape'

export default function NetworkGraph() {
  const [scans, setScans] = useState<Scan[]>([])
  const [selectedScan, setSelectedScan] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const cyRef = useRef<cytoscape.Core | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const data = await api.getScans()
        setScans(data)
        if (data.length > 0) {
          setSelectedScan(data[0].scan_id)
        }
      } catch (err) {
        console.error('Failed to fetch scans:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchScans()
  }, [])

  useEffect(() => {
    if (!selectedScan || !containerRef.current) return

    const renderGraph = async () => {
      try {
        const scanData = await api.getScan(selectedScan)
        
        // Destroy existing instance
        if (cyRef.current) {
          cyRef.current.destroy()
        }

        // Build graph elements
        const elements: cytoscape.ElementDefinition[] = []
        const nodeMap = new Map<string, number>()

        // Add scan as central node
        const scanNodeId = `scan-${scanData.scan_id}`
        elements.push({
          data: {
            id: scanNodeId,
            label: scanData.target,
            type: 'scan',
          },
          classes: 'scan-node',
        })

        // Add entities as nodes
        if (scanData.entities) {
          scanData.entities.forEach((entity) => {
            const entityId = `entity-${entity.id}`
            nodeMap.set(entity.canonical_value, entity.id)
            
            elements.push({
              data: {
                id: entityId,
                label: entity.canonical_value,
                type: entity.type,
                entityId: entity.id,
              },
              classes: `entity-node ${entity.type}-node`,
            })

            // Connect entity to scan
            elements.push({
              data: {
                id: `edge-${scanNodeId}-${entityId}`,
                source: scanNodeId,
                target: entityId,
              },
            })
          })
        }

        // Add relationships between entities (same domain, subdomain relationships)
        if (scanData.entities) {
          scanData.entities.forEach((entity1) => {
            scanData.entities!.forEach((entity2) => {
              if (entity1.id === entity2.id) return

              // Check for domain/subdomain relationships
              if (
                entity1.type === 'domain' &&
                entity2.type === 'subdomain' &&
                entity2.canonical_value.endsWith(`.${entity1.canonical_value}`)
              ) {
                const edgeId = `edge-entity-${entity1.id}-${entity2.id}`
                if (!elements.find((e) => e.data.id === edgeId)) {
                  elements.push({
                    data: {
                      id: edgeId,
                      source: `entity-${entity1.id}`,
                      target: `entity-${entity2.id}`,
                      relationship: 'subdomain',
                    },
                  })
                }
              }
            })
          })
        }

        // Create Cytoscape instance
        cyRef.current = cytoscape({
          container: containerRef.current,
          elements,
          style: [
            {
              selector: 'node',
              style: {
                'background-color': '#3b82f6',
                'label': 'data(label)',
                'width': 30,
                'height': 30,
                'text-valign': 'center',
                'text-halign': 'center',
                'color': '#ffffff',
                'font-size': '12px',
                'text-wrap': 'wrap',
                'text-max-width': '100px',
              },
            },
            {
              selector: '.scan-node',
              style: {
                'background-color': '#10b981',
                'width': 40,
                'height': 40,
                'font-size': '14px',
                'font-weight': 'bold',
              },
            },
            {
              selector: '.entity-node',
              style: {
                'background-color': '#6366f1',
              },
            },
            {
              selector: '.domain-node',
              style: {
                'background-color': '#8b5cf6',
              },
            },
            {
              selector: '.subdomain-node',
              style: {
                'background-color': '#ec4899',
              },
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'line-color': '#6b7280',
                'target-arrow-color': '#6b7280',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
              },
            },
          ],
          layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeOverlap: 20,
            refresh: 20,
            fit: true,
            padding: 30,
            randomize: false,
            componentSpacing: 40,
            nodeRepulsion: 4000000,
            nestingFactor: 5,
            gravity: 0.25,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0,
          },
        })

        // Add click handler to navigate to entity detail
        cyRef.current.on('tap', 'node', (evt) => {
          const node = evt.target
          const entityId = node.data('entityId')
          if (entityId) {
            window.location.href = `/entity/${entityId}`
          }
        })
      } catch (err) {
        console.error('Failed to render graph:', err)
      }
    }

    renderGraph()

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy()
        cyRef.current = null
      }
    }
  }, [selectedScan])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-dark-muted">Loading scans...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Network Graph</h1>
        <select
          value={selectedScan || ''}
          onChange={(e) => setSelectedScan(parseInt(e.target.value))}
          className="bg-dark-surface border border-dark-border rounded px-4 py-2 text-white"
        >
          <option value="">Select a scan</option>
          {scans.map((scan) => (
            <option key={scan.scan_id} value={scan.scan_id}>
              {scan.target} ({scan.status})
            </option>
          ))}
        </select>
      </div>

      <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
        <div
          ref={containerRef}
          className="w-full h-[600px] bg-dark-bg rounded"
          style={{ minHeight: '600px' }}
        />
        {!selectedScan && (
          <div className="flex items-center justify-center h-[600px]">
            <p className="text-dark-muted">Select a scan to view its network graph</p>
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-dark-muted">
        <p>Click on entity nodes to view details. Green nodes represent scans, colored nodes represent entities.</p>
      </div>
    </div>
  )
}
