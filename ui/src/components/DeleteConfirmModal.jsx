import { AlertTriangle, X, Loader2 } from 'lucide-react'

function DeleteConfirmModal({ isOpen, onClose, onConfirm, count, isDeleting }) {
    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="relative bg-surface rounded-xl border border-default p-6 max-w-md w-full mx-4 shadow-2xl">
                {/* Close button */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-tertiary hover:text-primary"
                    disabled={isDeleting}
                >
                    <X className="w-5 h-5" />
                </button>

                {/* Icon */}
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-red-500/20 mx-auto mb-4">
                    <AlertTriangle className="w-6 h-6 text-red-400" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-primary text-center mb-2">
                    Delete {count} {count === 1 ? 'Run' : 'Runs'}?
                </h3>
                <p className="text-tertiary text-center mb-6">
                    This action cannot be undone. The evaluation results and all associated data will be permanently deleted.
                </p>

                {/* Actions */}
                <div className="flex gap-3">
                    <button
                        onClick={onClose}
                        disabled={isDeleting}
                        className="flex-1 px-4 py-2.5 rounded-lg border border-default text-secondary hover:bg-surface-hover transition-colors disabled:opacity-50"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={onConfirm}
                        disabled={isDeleting}
                        className="flex-1 px-4 py-2.5 rounded-lg bg-red-600 text-primary hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                        {isDeleting ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Deleting...
                            </>
                        ) : (
                            'Delete'
                        )}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default DeleteConfirmModal
