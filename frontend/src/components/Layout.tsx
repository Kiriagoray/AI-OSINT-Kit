import { Link, useLocation } from 'react-router-dom'
import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/scan/new', label: 'New Scan' },
    { path: '/network', label: 'Network' },
    { path: '/reports', label: 'Reports' },
    { path: '/settings', label: 'Settings' },
  ]

  return (
    <div className="min-h-screen bg-dark-bg text-dark-text">
      {/* Top Navigation */}
      <nav className="bg-dark-surface border-b border-dark-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-white">AI OSINT Kit</h1>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 ${
                      location.pathname === item.path
                        ? 'border-blue-500 text-white'
                        : 'border-transparent text-dark-muted hover:border-gray-300 hover:text-white'
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>
            {/* Search bar */}
            <div className="flex items-center">
              <input
                type="text"
                placeholder="Search entities..."
                className="px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-sm text-white placeholder-dark-muted focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}












