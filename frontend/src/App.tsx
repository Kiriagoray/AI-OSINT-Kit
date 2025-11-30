import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ScanCreate from './pages/ScanCreate'
import ScanDetail from './pages/ScanDetail'
import EntityDetail from './pages/EntityDetail'
import NetworkGraph from './pages/NetworkGraph'
import Reports from './pages/Reports'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scan/new" element={<ScanCreate />} />
          <Route path="/scan/:id" element={<ScanDetail />} />
          <Route path="/entity/:id" element={<EntityDetail />} />
          <Route path="/network" element={<NetworkGraph />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App












