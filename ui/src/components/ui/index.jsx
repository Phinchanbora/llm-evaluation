/**
 * UI Component Library
 * Professional, reusable components for LLM Benchmark Dashboard
 */

import { forwardRef } from 'react'
import { Loader2, Check, AlertCircle, Info, CheckCircle, XCircle, AlertTriangle, Clock } from 'lucide-react'

// ============================================
// BUTTON COMPONENT
// ============================================

export const Button = forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon: Icon,
  iconPosition = 'left',
  className = '',
  ...props
}, ref) => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    ghost: 'btn-ghost',
    danger: 'btn-danger',
    accent: 'btn-accent',
  }

  const sizes = {
    sm: 'btn-sm',
    md: '',
    lg: 'btn-lg',
    icon: 'btn-icon',
  }

  return (
    <button
      ref={ref}
      disabled={disabled || loading}
      className={`btn ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : Icon && iconPosition === 'left' ? (
        <Icon className="w-4 h-4" />
      ) : null}
      {children}
      {!loading && Icon && iconPosition === 'right' && (
        <Icon className="w-4 h-4" />
      )}
    </button>
  )
})

Button.displayName = 'Button'

// ============================================
// CARD COMPONENT
// ============================================

export function Card({
  children,
  interactive = false,
  selected = false,
  padding = 'md',
  className = '',
  ...props
}) {
  const paddingSizes = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  }

  return (
    <div
      className={`
        ${interactive ? 'card-interactive cursor-pointer' : 'card'}
        ${selected ? 'card-selected' : ''}
        ${paddingSizes[padding]}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardHeader({ children, className = '' }) {
  return (
    <div className={`flex items-center justify-between mb-4 ${className}`}>
      {children}
    </div>
  )
}

export function CardTitle({ children, icon: Icon, className = '' }) {
  return (
    <h3 className={`section-title ${className}`}>
      {Icon && <Icon className="w-5 h-5 text-tertiary" />}
      {children}
    </h3>
  )
}

export function CardDescription({ children, className = '' }) {
  return (
    <p className={`section-subtitle ${className}`}>
      {children}
    </p>
  )
}

// ============================================
// BADGE COMPONENT
// ============================================

export function Badge({
  children,
  variant = 'neutral',
  size = 'md',
  dot = false,
  className = '',
}) {
  const variants = {
    primary: 'badge-primary',
    success: 'badge-success',
    error: 'badge-error',
    warning: 'badge-warning',
    neutral: 'badge-neutral',
  }

  const sizes = {
    sm: 'text-2xs px-1.5 py-0',
    md: '',
    lg: 'text-sm px-3 py-1',
  }

  return (
    <span className={`${variants[variant]} ${sizes[size]} ${className}`}>
      {dot && (
        <span className={`w-1.5 h-1.5 rounded-full ${variant === 'success' ? 'bg-success-400' :
          variant === 'error' ? 'bg-error-400' :
            variant === 'warning' ? 'bg-warning-400' :
              variant === 'primary' ? 'bg-primary-400' :
                'bg-slate-400'
          }`} />
      )}
      {children}
    </span>
  )
}

// ============================================
// PROGRESS BAR COMPONENT
// ============================================

export function ProgressBar({
  value = 0,
  max = 100,
  variant = 'primary',
  size = 'md',
  showLabel = false,
  animated = false,
  className = '',
}) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100))

  const variants = {
    primary: 'progress-fill-primary',
    success: 'progress-fill-success',
    accent: 'progress-fill-accent',
  }

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  }

  return (
    <div className={className}>
      {showLabel && (
        <div className="flex justify-between mb-1.5 text-sm">
          <span className="text-tertiary">Progress</span>
          <span className="text-primary font-mono">{percentage.toFixed(0)}%</span>
        </div>
      )}
      <div className={`progress-bar ${sizes[size]}`}>
        <div
          className={`${variants[variant]} ${animated ? 'animate-pulse-slow' : ''}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

// ============================================
// SCORE DISPLAY COMPONENT
// ============================================

export function ScoreDisplay({
  score,
  label,
  baseline,
  size = 'md',
  showBar = true,
  className = '',
}) {
  const percentage = (score * 100).toFixed(1)
  const diff = baseline ? ((score - baseline) * 100).toFixed(1) : null

  const getScoreClass = (s) => {
    if (s >= 0.8) return 'score-excellent'
    if (s >= 0.6) return 'score-good'
    if (s >= 0.4) return 'score-average'
    return 'score-poor'
  }

  const getBarClass = (s) => {
    if (s >= 0.8) return 'bg-success-500'
    if (s >= 0.6) return 'bg-primary-500'
    if (s >= 0.4) return 'bg-accent-500'
    return 'bg-error-500'
  }

  const sizes = {
    sm: 'text-xl',
    md: 'text-3xl',
    lg: 'text-4xl',
  }

  return (
    <div className={`card p-4 ${className}`}>
      {label && <div className="text-sm text-tertiary mb-1">{label}</div>}
      <div className="flex items-baseline gap-2">
        <span className={`${sizes[size]} font-bold font-mono ${getScoreClass(score)}`}>
          {percentage}%
        </span>
        {diff && (
          <span className={`text-sm ${parseFloat(diff) >= 0 ? 'text-success-400' : 'text-error-400'}`}>
            {parseFloat(diff) >= 0 ? '+' : ''}{diff}%
          </span>
        )}
      </div>
      {showBar && (
        <div className="mt-3 h-1.5 bg-surface-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${getBarClass(score)}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      )}
    </div>
  )
}

// ============================================
// STATUS INDICATOR COMPONENT
// ============================================

export function StatusIndicator({
  status,
  label,
  showLabel = true,
  size = 'md',
}) {
  const config = {
    success: { dot: 'status-dot-success', icon: CheckCircle, color: 'text-success-400', text: 'Completed' },
    error: { dot: 'status-dot-error', icon: XCircle, color: 'text-error-400', text: 'Failed' },
    warning: { dot: 'status-dot-warning', icon: AlertTriangle, color: 'text-warning-400', text: 'Warning' },
    running: { dot: 'status-dot-running', icon: Loader2, color: 'text-primary-400', text: 'Running' },
    queued: { dot: 'status-dot bg-yellow-500', icon: Clock, color: 'text-yellow-400', text: 'Queued' },
    pending: { dot: 'status-dot bg-slate-500', icon: null, color: 'text-tertiary', text: 'Pending' },
  }

  const { dot, icon: Icon, color, text } = config[status] || config.pending

  const sizes = {
    sm: 'text-xs gap-1.5',
    md: 'text-sm gap-2',
    lg: 'text-base gap-2.5',
  }

  return (
    <div className={`flex items-center ${sizes[size]}`}>
      {Icon ? (
        <Icon className={`w-4 h-4 ${color} ${status === 'running' ? 'animate-spin' : ''}`} />
      ) : (
        <span className={dot} />
      )}
      {showLabel && (
        <span className={color}>{label || text}</span>
      )}
    </div>
  )
}

// ============================================
// EMPTY STATE COMPONENT
// ============================================

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className = '',
}) {
  return (
    <div className={`empty-state ${className}`}>
      {Icon && <Icon className="empty-state-icon" />}
      <h3 className="empty-state-title">{title}</h3>
      {description && <p className="empty-state-description">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  )
}

// ============================================
// SKELETON LOADER COMPONENT
// ============================================

export function Skeleton({ className = '', variant = 'default' }) {
  const variants = {
    default: 'skeleton',
    shimmer: 'skeleton-shimmer',
  }

  return <div className={`${variants[variant]} ${className}`} />
}

export function SkeletonCard() {
  return (
    <Card padding="lg">
      <Skeleton className="h-4 w-1/3 mb-4" />
      <Skeleton className="h-8 w-1/2 mb-4" />
      <Skeleton className="h-2 w-full" />
    </Card>
  )
}

// ============================================
// ALERT COMPONENT
// ============================================

export function Alert({
  variant = 'info',
  title,
  children,
  onClose,
  className = '',
}) {
  const config = {
    info: { icon: Info, bg: 'bg-primary-500/10', border: 'border-primary-500/30', text: 'text-primary-400' },
    success: { icon: CheckCircle, bg: 'bg-success-500/10', border: 'border-success-500/30', text: 'text-success-400' },
    warning: { icon: AlertTriangle, bg: 'bg-warning-500/10', border: 'border-warning-500/30', text: 'text-warning-400' },
    error: { icon: AlertCircle, bg: 'bg-error-500/10', border: 'border-error-500/30', text: 'text-error-400' },
  }

  const { icon: Icon, bg, border, text } = config[variant]

  return (
    <div className={`${bg} ${border} border rounded-lg p-4 ${className}`}>
      <div className="flex items-start gap-3">
        <Icon className={`w-5 h-5 ${text} flex-shrink-0 mt-0.5`} />
        <div className="flex-1">
          {title && <h4 className={`font-medium ${text} mb-1`}>{title}</h4>}
          <div className={text}>{children}</div>
        </div>
        {onClose && (
          <button onClick={onClose} className={`${text} hover:opacity-70`}>
            <XCircle className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  )
}

// ============================================
// DIVIDER COMPONENT
// ============================================

export function Divider({ className = '' }) {
  return <div className={`divider ${className}`} />
}

// ============================================
// BENCHMARK CARD COMPONENT
// ============================================

export function BenchmarkCard({
  benchmark,
  selected = false,
  onToggle,
  showStats = false,
  score,
  className = '',
}) {
  const icons = {
    mmlu: '📚',
    truthfulqa: '✓',
    hellaswag: '💭',
    arc: '🔬',
    winogrande: '🧩',
    commonsenseqa: '💡',
    boolq: '❓',
    gsm8k: '🔢',
    safetybench: '🛡️',
    donotanswer: '🚫',
  }

  const descriptions = {
    mmlu: '57 subjects, knowledge breadth',
    truthfulqa: 'Truthfulness evaluation',
    hellaswag: 'Common sense reasoning',
    arc: 'Science reasoning (Challenge)',
    winogrande: 'Pronoun resolution',
    commonsenseqa: 'Commonsense knowledge',
    boolq: 'Yes/No comprehension',
    gsm8k: 'Grade school math',
    safetybench: 'Safety scenarios',
    donotanswer: 'Harmful prompt rejection',
  }

  return (
    <button
      onClick={onToggle}
      className={`
        p-4 rounded-xl border-2 text-left transition-all w-full
        ${selected
          ? 'border-primary-500 bg-primary-500/10 shadow-glow-sm'
          : 'border-surface-700 hover:border-surface-500 bg-surface-800/50'
        }
        ${className}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">{icons[benchmark.id] || '📋'}</span>
          <span className="font-medium text-primary">{benchmark.name}</span>
        </div>
        <div className={`
          w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all
          ${selected
            ? 'border-primary-500 bg-primary-500'
            : 'border-surface-600'
          }
        `}>
          {selected && <Check className="w-3 h-3 text-primary" />}
        </div>
      </div>
      <p className="text-xs text-tertiary mt-1.5">
        {descriptions[benchmark.id] || benchmark.description || 'Benchmark evaluation'}
      </p>
      <div className="flex items-center justify-between mt-2">
        <span className="text-xs text-tertiary font-mono">
          {benchmark.question_count?.toLocaleString() || '?'} questions
        </span>
        {showStats && score !== undefined && (
          <span className={`text-xs font-mono font-medium ${score >= 0.8 ? 'text-success-400' :
            score >= 0.6 ? 'text-primary-400' :
              score >= 0.4 ? 'text-accent-400' :
                'text-error-400'
            }`}>
            {(score * 100).toFixed(1)}%
          </span>
        )}
      </div>
    </button>
  )
}

// ============================================
// PROVIDER BADGE COMPONENT
// ============================================

export function ProviderBadge({ provider, size = 'md' }) {
  const config = {
    ollama: { color: 'bg-purple-500/20 text-purple-400 border-purple-500/30', label: 'Ollama' },
    openai: { color: 'bg-green-500/20 text-green-400 border-green-500/30', label: 'OpenAI' },
    anthropic: { color: 'bg-orange-500/20 text-orange-400 border-orange-500/30', label: 'Anthropic' },
    deepseek: { color: 'bg-blue-500/20 text-blue-400 border-blue-500/30', label: 'DeepSeek' },
    huggingface: { color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30', label: 'HuggingFace' },
    groq: { color: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30', label: 'Groq' },
    together: { color: 'bg-pink-500/20 text-pink-400 border-pink-500/30', label: 'Together' },
    fireworks: { color: 'bg-red-500/20 text-red-400 border-red-500/30', label: 'Fireworks' },
  }

  const { color, label } = config[provider?.toLowerCase()] || { color: 'badge-neutral', label: provider }

  const sizes = {
    sm: 'text-2xs px-1.5 py-0',
    md: 'text-xs px-2 py-0.5',
    lg: 'text-sm px-2.5 py-1',
  }

  return (
    <span className={`inline-flex items-center rounded-md border font-medium ${color} ${sizes[size]}`}>
      {label}
    </span>
  )
}
