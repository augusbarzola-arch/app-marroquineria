/**
 * pos.js - Lógica del Punto de Venta (POS) en tiempo real
 */

let cart = []; // Array de ítems: { id_variante, id_producto, nombre_producto, nombre_color, nombre_tamano, precio_lista, stock_disponible, cantidad }
let mediosPago = [];
let selectedMedioPagoId = null;
let searchTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
    initMediosPago();
    initSearch();
    loadCatalog('');

    // Atajo: Enter en el buscador de productos agrega el primer resultado disponible
    const searchInput = document.getElementById('pos-search-input');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const firstAddBtn = document.querySelector('.btn-add-first-variant');
                if (firstAddBtn) {
                    firstAddBtn.click();
                }
            }
        });
    }
});

function initMediosPago() {
    const radioInputs = document.querySelectorAll('input[name="medio_pago_radio"]');
    radioInputs.forEach(radio => {
        if (radio.checked) {
            selectedMedioPagoId = parseInt(radio.value);
        }
        radio.addEventListener('change', () => {
            selectedMedioPagoId = parseInt(radio.value);
            renderCart();
        });
    });
}

function initSearch() {
    const searchInput = document.getElementById('pos-search-input');
    const catSelect = document.getElementById('pos-categoria-select');

    const triggerSearch = () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = searchInput.value.trim();
            const catId = catSelect.value;
            loadCatalog(query, catId);
        }, 250);
    };

    if (searchInput) searchInput.addEventListener('input', triggerSearch);
    if (catSelect) catSelect.addEventListener('change', triggerSearch);
}

async function loadCatalog(query = '', idCategoria = '') {
    const container = document.getElementById('pos-product-list');
    if (!container) return;

    container.innerHTML = `
        <div class="text-center py-4 text-muted">
            <span class="spinner-border spinner-border-sm me-2"></span> Cargando catálogo...
        </div>
    `;

    try {
        let url = `/api/ventas/buscar-productos?query=${encodeURIComponent(query)}`;
        if (idCategoria) url += `&id_categoria=${encodeURIComponent(idCategoria)}`;

        const res = await fetch(url);
        const products = await res.json();

        if (products.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-search fs-3 d-block mb-2"></i>
                    No se encontraron productos coincidentes.
                </div>
            `;
            return;
        }

        let html = '';
        products.forEach((p, index) => {
            const hasStock = p.variantes.some(v => v.stock_actual > 0);
            const firstAvailableVariant = p.variantes.find(v => v.stock_actual > 0);

            html += `
                <div class="card border mb-2 shadow-sm product-card ${!hasStock ? 'opacity-75' : ''}">
                    <div class="card-body p-2">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <span class="badge bg-secondary-subtle text-secondary-emphasis border me-1">${p.nombre_categoria}</span>
                                <strong class="d-block mt-1">${p.nombre_producto}</strong>
                                <small class="text-muted">${p.nombre_material}</small>
                            </div>
                            <div class="text-end">
                                <span class="fw-bold text-success fs-6">$${p.precio_lista.toFixed(2)}</span>
                                ${index === 0 && firstAvailableVariant ? `
                                    <button class="d-none btn-add-first-variant" 
                                            onclick="addToCart(${firstAvailableVariant.id_variante}, ${p.id_producto}, '${p.nombre_producto.replace(/'/g, "\\'")}', '${firstAvailableVariant.nombre_color.replace(/'/g, "\\'")}', '${firstAvailableVariant.nombre_tamano.replace(/'/g, "\\'")}', ${p.precio_lista}, ${firstAvailableVariant.stock_actual})">
                                    </button>
                                ` : ''}
                            </div>
                        </div>

                        <!-- Variantes disponibles -->
                        <div class="mt-2 pt-2 border-top">
                            <span class="small text-muted d-block mb-1">Seleccionar variante:</span>
                            <div class="d-flex flex-wrap gap-1">
                                ${p.variantes.map(v => {
                                    const available = v.stock_actual > 0;
                                    return `
                                        <button type="button" 
                                                class="btn btn-sm ${available ? 'btn-outline-primary' : 'btn-outline-secondary disabled'} py-1 px-2 text-start"
                                                ${!available ? 'disabled' : ''}
                                                onclick="addToCart(${v.id_variante}, ${p.id_producto}, '${p.nombre_producto.replace(/'/g, "\\'")}', '${v.nombre_color.replace(/'/g, "\\'")}', '${v.nombre_tamano.replace(/'/g, "\\'")}', ${p.precio_lista}, ${v.stock_actual})">
                                            <strong>${v.nombre_color}</strong> - ${v.nombre_tamano}
                                            <span class="badge ${available ? (v.stock_actual <= v.stock_minimo ? 'bg-danger' : 'bg-success') : 'bg-secondary'} ms-1">
                                                ${v.stock_actual} disp.
                                            </span>
                                        </button>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (err) {
        container.innerHTML = `
            <div class="alert alert-danger py-2 small">Error al cargar productos: ${err.message}</div>
        `;
    }
}

function addToCart(idVariante, idProducto, nombreProducto, nombreColor, nombreTamano, precioLista, stockDisponible) {
    const existingIndex = cart.findIndex(item => item.id_variante === idVariante);

    if (existingIndex >= 0) {
        if (cart[existingIndex].cantidad + 1 > stockDisponible) {
            showToast(`No hay más stock disponible para ${nombreProducto} (${nombreColor} - ${nombreTamano}). Stock: ${stockDisponible}`, 'danger');
            return;
        }
        cart[existingIndex].cantidad += 1;
    } else {
        if (stockDisponible <= 0) {
            showToast(`Sin stock para ${nombreProducto} (${nombreColor} - ${nombreTamano})`, 'danger');
            return;
        }
        cart.push({
            id_variante: idVariante,
            id_producto: idProducto,
            nombre_producto: nombreProducto,
            nombre_color: nombreColor,
            nombre_tamano: nombreTamano,
            precio_lista: parseFloat(precioLista),
            stock_disponible: parseInt(stockDisponible),
            cantidad: 1
        });
    }

    renderCart();
    showToast(`Agregado: ${nombreProducto} (${nombreColor} - ${nombreTamano})`, 'success');
}

function updateQuantity(idVariante, newQty) {
    const item = cart.find(i => i.id_variante === idVariante);
    if (!item) return;

    newQty = parseInt(newQty);
    if (isNaN(newQty) || newQty <= 0) {
        removeFromCart(idVariante);
        return;
    }

    if (newQty > item.stock_disponible) {
        showToast(`Stock insuficiente. Disponible: ${item.stock_disponible} unidad(es)`, 'danger');
        item.cantidad = item.stock_disponible;
    } else {
        item.cantidad = newQty;
    }
    renderCart();
}

function removeFromCart(idVariante) {
    cart = cart.filter(i => i.id_variante !== idVariante);
    renderCart();
}

function clearCart() {
    if (cart.length === 0) return;
    cart = [];
    renderCart();
    showToast('Carrito vaciado.', 'info');
}

function renderCart() {
    const tbody = document.getElementById('pos-cart-tbody');
    const emptyMsg = document.getElementById('pos-cart-empty');
    const cartTable = document.getElementById('pos-cart-table');
    const btnConfirm = document.getElementById('btn-confirm-sale');

    if (!tbody) return;

    if (cart.length === 0) {
        emptyMsg.classList.remove('d-none');
        cartTable.classList.add('d-none');
        btnConfirm.disabled = true;
        updateTotals(0, 0);
        return;
    }

    emptyMsg.classList.add('d-none');
    cartTable.classList.remove('d-none');
    btnConfirm.disabled = false;

    let subtotalLista = 0;

    tbody.innerHTML = cart.map(item => {
        const itemSubtotal = item.precio_lista * item.cantidad;
        subtotalLista += itemSubtotal;

        return `
            <tr>
                <td>
                    <strong class="d-block">${item.nombre_producto}</strong>
                    <small class="text-secondary">${item.nombre_color} | ${item.nombre_tamano}</small>
                </td>
                <td class="text-end text-muted">$${item.precio_lista.toFixed(2)}</td>
                <td style="width: 120px;">
                    <div class="input-group input-group-sm">
                        <button class="btn btn-outline-secondary" type="button" onclick="updateQuantity(${item.id_variante}, ${item.cantidad - 1})">-</button>
                        <input type="number" min="1" max="${item.stock_disponible}" class="form-control text-center px-1" value="${item.cantidad}" onchange="updateQuantity(${item.id_variante}, this.value)">
                        <button class="btn btn-outline-secondary" type="button" onclick="updateQuantity(${item.id_variante}, ${item.cantidad + 1})">+</button>
                    </div>
                </td>
                <td class="text-end fw-bold">$${itemSubtotal.toFixed(2)}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${item.id_variante})" title="Quitar">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    updateTotals(subtotalLista);
}

function updateTotals(subtotalLista) {
    const subtotalEl = document.getElementById('pos-subtotal');
    const ajusteLabelEl = document.getElementById('pos-ajuste-label');
    const ajusteMontoEl = document.getElementById('pos-ajuste-monto');
    const totalEl = document.getElementById('pos-total');

    if (!subtotalEl || !totalEl) return;

    subtotalEl.textContent = `$${subtotalLista.toFixed(2)}`;

    // Obtener porcentaje del medio de pago seleccionado
    const selectedRadio = document.querySelector('input[name="medio_pago_radio"]:checked');
    const pct = selectedRadio ? parseFloat(selectedRadio.dataset.porcentaje || 0) : 0;

    const factor = 1.0 + (pct / 100.0);
    const totalFinal = subtotalLista * factor;
    const diferencia = totalFinal - subtotalLista;

    if (pct < 0) {
        ajusteLabelEl.textContent = `Descuento (${pct.toFixed(2)}%):`;
        ajusteMontoEl.textContent = `-$${Math.abs(diferencia).toFixed(2)}`;
        ajusteMontoEl.className = 'text-success fw-bold';
    } else if (pct > 0) {
        ajusteLabelEl.textContent = `Recargo (+${pct.toFixed(2)}%):`;
        ajusteMontoEl.textContent = `+$${diferencia.toFixed(2)}`;
        ajusteMontoEl.className = 'text-warning fw-bold';
    } else {
        ajusteLabelEl.textContent = 'Ajuste medio de pago:';
        ajusteMontoEl.textContent = '$0.00';
        ajusteMontoEl.className = 'text-muted';
    }

    totalEl.textContent = `$${totalFinal.toFixed(2)}`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function openConfirmationModal() {
    if (cart.length === 0) {
        showToast('El carrito está vacío.', 'danger');
        return;
    }

    const selectedRadio = document.querySelector('input[name="medio_pago_radio"]:checked');
    if (!selectedRadio) {
        showToast('Seleccione un medio de pago.', 'danger');
        return;
    }

    // Fecha y hora del ticket
    const fechaEl = document.getElementById('modal-ticket-fecha');
    if (fechaEl) {
        const ahora = new Date();
        fechaEl.textContent = ahora.toLocaleDateString('es-AR') + ' ' + ahora.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' }) + ' hs';
    }

    // Calcular subtotales
    let subtotalLista = 0;
    const tbody = document.getElementById('modal-sale-items-tbody');
    tbody.innerHTML = cart.map(item => {
        const itemSubtotal = item.precio_lista * item.cantidad;
        subtotalLista += itemSubtotal;
        return `
            <tr>
                <td class="fw-semibold">${escapeHtml(item.nombre_producto)}</td>
                <td>
                    <span class="badge bg-secondary-subtle text-secondary-emphasis border me-1">${escapeHtml(item.nombre_color)}</span>
                    <span class="badge bg-primary-subtle text-primary border">${escapeHtml(item.nombre_tamano)}</span>
                </td>
                <td class="text-center fw-bold font-monospace">${item.cantidad}</td>
                <td class="text-end text-muted font-monospace">$${item.precio_lista.toFixed(2)}</td>
                <td class="text-end fw-bold font-monospace">$${itemSubtotal.toFixed(2)}</td>
            </tr>
        `;
    }).join('');

    // Medio de pago y ajustes
    const radioLabel = selectedRadio.closest('.form-check') ? selectedRadio.closest('.form-check').querySelector('label').textContent.trim() : 'Medio de pago';
    const pct = parseFloat(selectedRadio.dataset.porcentaje || 0);
    const factor = 1.0 + (pct / 100.0);
    const totalFinal = subtotalLista * factor;
    const diferencia = totalFinal - subtotalLista;

    document.getElementById('modal-medio-pago').textContent = radioLabel;
    document.getElementById('modal-subtotal-lista').textContent = `$${subtotalLista.toFixed(2)}`;

    const ajusteEl = document.getElementById('modal-ajuste-texto');
    if (pct < 0) {
        ajusteEl.innerHTML = `<span class="badge bg-success-subtle text-success border">Descuento ${pct.toFixed(2)}% (-$${Math.abs(diferencia).toFixed(2)})</span>`;
    } else if (pct > 0) {
        ajusteEl.innerHTML = `<span class="badge bg-warning-subtle text-warning-emphasis border">Recargo +${pct.toFixed(2)}% (+$${diferencia.toFixed(2)})</span>`;
    } else {
        ajusteEl.innerHTML = `<span class="badge bg-secondary-subtle text-secondary border">Sin ajuste (0%)</span>`;
    }

    document.getElementById('modal-total-final').textContent = `$${totalFinal.toFixed(2)}`;

    // Restablecer botón confirmar modal
    const btnModal = document.getElementById('btn-modal-confirm-sale');
    if (btnModal) {
        btnModal.disabled = false;
        btnModal.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Confirmar Venta';
    }

    // Abrir modal de confirmación
    const modalEl = document.getElementById('modalConfirmarVenta');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
}

// Alias para compatibilidad
function confirmSale() {
    openConfirmationModal();
}

async function submitFinalSale() {
    if (cart.length === 0) return;

    const selectedRadio = document.querySelector('input[name="medio_pago_radio"]:checked');
    if (!selectedRadio) return;

    const btnModal = document.getElementById('btn-modal-confirm-sale');
    const originalText = btnModal.innerHTML;
    btnModal.disabled = true;
    btnModal.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Registrando Venta...';

    const payload = {
        id_medio_pago: parseInt(selectedRadio.value),
        items: cart.map(i => ({
            id_variante: i.id_variante,
            cantidad: i.cantidad
        }))
    };

    try {
        const res = await fetch('/ventas', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error al procesar la venta.');

        // Ocultar modal y redirigir
        const modalEl = document.getElementById('modalConfirmarVenta');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();

        window.location.href = `/ventas/${data.id_venta}/comprobante`;
    } catch (err) {
        showToast(err.message, 'danger');
        btnModal.disabled = false;
        btnModal.innerHTML = originalText;
    }
}
