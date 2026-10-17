/**
 * main.js - Atajos globales, notificaciones toast y modales de confirmación
 */

// Función global para mostrar Toasts
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const bgClass = type === 'success' ? 'text-bg-success' : (type === 'danger' ? 'text-bg-danger' : 'text-bg-primary');
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center ${bgClass} border-0 shadow`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
        </div>
    `;

    container.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl, { delay: 4000 });
    bsToast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

// Modal genérico de confirmación antes de eliminar
let pendingDeleteAction = null;

function confirmModal(title, message, onConfirmCallback) {
    const modalEl = document.getElementById('genericConfirmModal');
    if (!modalEl) {
        if (confirm(message)) onConfirmCallback();
        return;
    }

    document.getElementById('genericConfirmModalTitle').textContent = title;
    document.getElementById('genericConfirmModalBody').textContent = message;

    const confirmBtn = document.getElementById('genericConfirmModalBtn');
    
    // Clonar botón para remover listeners previos
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);

    const bsModal = new bootstrap.Modal(modalEl);

    newConfirmBtn.addEventListener('click', () => {
        bsModal.hide();
        onConfirmCallback();
    });

    bsModal.show();
}

// Atajos de teclado útiles
document.addEventListener('keydown', (e) => {
    // F2: Acceso rápido a Nueva Venta (POS)
    if (e.key === 'F2') {
        e.preventDefault();
        window.location.href = '/ventas/pos';
    }

    // ESC: Cerrar modales abiertos
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(m => {
            const instance = bootstrap.Modal.getInstance(m);
            if (instance) instance.hide();
        });
    }
});

// Inicialización de tooltips y toasts iniciales si vienen en query params
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // Revisar parámetros de URL por mensajes (ej: ?msg=Guardado con exito&msg_type=success)
    const urlParams = new URLSearchParams(window.location.search);
    const msg = urlParams.get('msg');
    const msgType = urlParams.get('msg_type') || 'success';
    if (msg) {
        showToast(decodeURIComponent(msg), msgType);
        // Limpiar URL sin recargar
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});
