import { useState, useEffect } from 'react'
import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import {
  Play,
  BarChart3,
  History,
  Activity,
  Zap,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
  Github,
  ExternalLink,
  Sparkles
} from 'lucide-react'

import RunManager from './components/RunManager'
import ProgressViewer from './components/ProgressViewer'
import ModelComparison from './components/ModelComparison'
import RunHistory from './components/RunHistory'
import RunDetail from './components/RunDetail'

const API_BASE = '/api'

function App() {
  const [activeRun, setActiveRun] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [runningCount, setRunningCount] = useState(0)
  const [historyCount, setHistoryCount] = useState(0)
  const location = useLocation()

  // Fetch counts for badges
  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const queueRes = await fetch('/api/queue/status')
        const queueData = await queueRes.json()
        setRunningCount(queueData.running ? 1 : 0)

        const historyRes = await fetch('/api/runs')
        const historyData = await historyRes.json()
        setHistoryCount(historyData.length || 0)
      } catch (e) {
        // Silently fail
      }
    }
    fetchCounts()
    const interval = setInterval(fetchCounts, 5000)
    return () => clearInterval(interval)
  }, [])

  const navItems = [
    {
      path: '/',
      icon: Play,
      label: 'Run Manager',
      description: 'Configure & start evaluations'
    },
    {
      path: '/progress',
      icon: Activity,
      label: 'Progress',
      description: 'Live evaluation status',
      badge: runningCount > 0 ? 'running' : null
    },
    {
      path: '/compare',
      icon: BarChart3,
      label: 'Compare',
      description: 'Analyze & visualize results'
    },
    {
      path: '/history',
      icon: History,
      label: 'History',
      description: 'Past evaluation runs',
      badge: historyCount > 0 ? historyCount : null
    },
  ]

  return (
    <div className="min-h-screen bg-surface-900 flex">
      {/* Sidebar */}
      <aside
        className={`
          ${sidebarOpen ? 'w-72' : 'w-20'} 
          bg-surface-800/50 backdrop-blur-sm
          border-r border-surface-700/50
          transition-all duration-300 
          flex flex-col
          relative
        `}
      >
        {/* Logo Header */}
        <div className="p-4 border-b border-surface-700/50">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 bg-amber-500 rounded-xl flex items-center justify-center shadow-lg shadow-amber-500/25">
              <Zap className="w-6 h-6 text-white" />
            </div>
            {sidebarOpen && (
              <div className="animate-fade-in">
                <h1 className="text-lg font-bold text-white tracking-tight">LLM Bench</h1>
                <p className="text-xs text-slate-500 font-medium">Dashboard v2.3</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1">
          {navItems.map(({ path, icon: Icon, label, description, badge }) => {
            const isActive = location.pathname === path ||
              (path === '/' && location.pathname === '/') ||
              (path !== '/' && location.pathname.startsWith(path))

            return (
              <NavLink
                key={path}
                to={path}
                className={`
                  group flex items-center gap-3 px-3 py-3 rounded-xl
                  transition-all duration-200
                  ${isActive
                    ? 'bg-primary-500/15 text-primary-400 shadow-lg shadow-primary-500/10'
                    : 'text-slate-400 hover:bg-surface-700/50 hover:text-white'
                  }
                `}
              >
                <div className={`
                  relative flex items-center justify-center w-9 h-9 rounded-lg
                  transition-all duration-200
                  ${isActive
                    ? 'bg-primary-500/20'
                    : 'bg-surface-700/50 group-hover:bg-surface-600/50'
                  }
                `}>
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {badge === 'running' && (
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-primary-500 rounded-full animate-pulse shadow-lg shadow-primary-500/50" />
                  )}
                </div>
                {sidebarOpen && (
                  <div className="flex-1 min-w-0 animate-fade-in">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">{label}</span>
                      {badge && badge !== 'running' && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-surface-700 text-slate-300 rounded-full">
                          {badge}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-500 truncate mt-0.5">{description}</p>
                  </div>
                )}
              </NavLink>
            )
          })}
        </nav>

        {/* Footer */}
        {sidebarOpen && (
          <div className="p-4 border-t border-surface-700/50 animate-fade-in">
            <a
              href="https://github.com/NahuelGiudizi/llm-evaluation"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-xs text-slate-500 hover:text-slate-300 transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>View on GitHub</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <div className="mt-3 flex items-center gap-2 text-xs text-slate-600">
              <Sparkles className="w-3 h-3" />
              <span>llm-benchmark-toolkit</span>
            </div>
          </div>
        )}

        {/* Collapse Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="
            absolute -right-3 top-20
            w-6 h-6 bg-surface-700 border border-surface-600
            rounded-full flex items-center justify-center
            text-slate-400 hover:text-white hover:bg-surface-600
            transition-all duration-200
            shadow-lg
          "
        >
          {sidebarOpen ? (
            <ChevronLeft className="w-4 h-4" />
          ) : (
            <ChevronRight className="w-4 h-4" />
          )}
        </button>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-6 max-w-7xl mx-auto">
          <Routes>
            <Route path="/" element={<RunManager onRunStart={setActiveRun} />} />
            <Route path="/progress" element={<ProgressViewer activeRun={activeRun} />} />
            <Route path="/compare" element={<ModelComparison />} />
            <Route path="/history" element={<RunHistory />} />
            <Route path="/run/:id" element={<RunDetail />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}

export default App
