/**
 * Responsive Tables - Conversión de tablas a tarjetas en móvil
 * Maneja la transformación automática de tablas a vista de tarjetas
 */

class ResponsiveTableManager {
    constructor() {
        this.breakpoints = {
            mobile: 768,
            tablet: 1024
        };
        this.tables = new Map();
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupTables());
        } else {
            this.setupTables();
        }

        // Listen for window resize
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));

        // Listen for orientation change
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.handleResize(), 100);
        });
    }

    setupTables() {
        const tables = document.querySelectorAll('table[data-responsive]');
        tables.forEach(table => {
            this.setupTable(table);
        });
    }

    setupTable(table) {
        const tableId = table.id || `table-${Date.now()}`;
        if (!table.id) table.id = tableId;

        const config = {
            id: tableId,
            element: table,
            isMobile: window.innerWidth <= this.breakpoints.mobile,
            originalHTML: table.outerHTML,
            cardTemplate: this.createCardTemplate(table)
        };

        this.tables.set(tableId, config);
        this.transformTable(tableId);
    }

    createCardTemplate(table) {
        const headers = Array.from(table.querySelectorAll('th[data-key]'));
        const template = document.createElement('template');
        
        template.innerHTML = `
            <div class="mobile-card" data-id="">
                <div class="mobile-card__header">
                    <div class="mobile-card__icon">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                        </svg>
                    </div>
                    <div>
                        <h3 class="mobile-card__title"></h3>
                        <p class="mobile-card__subtitle"></p>
                    </div>
                </div>
                <div class="mobile-card__content">
                    ${headers.map(header => {
                        const key = header.getAttribute('data-key');
                        const label = header.textContent.trim();
                        if (key === 'name' || key === 'description') return '';
                        return `
                            <div class="mobile-card__field" data-key="${key}">
                                <span class="mobile-card__label">${label}</span>
                                <span class="mobile-card__value"></span>
                            </div>
                        `;
                    }).join('')}
                </div>
                <div class="mobile-card__actions">
                    <button class="mobile-card__action mobile-card__action--primary" data-action="view">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                        Ver
                    </button>
                    <button class="mobile-card__action mobile-card__action--primary" data-action="edit">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                        </svg>
                        Editar
                    </button>
                    <button class="mobile-card__action mobile-card__action--error" data-action="delete">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                        Eliminar
                    </button>
                </div>
            </div>
        `;

        return template;
    }

    transformTable(tableId) {
        const config = this.tables.get(tableId);
        if (!config) return;

        const table = config.element;
        const container = table.closest('.table-container') || table.parentNode;
        const isMobile = window.innerWidth <= this.breakpoints.mobile;

        if (isMobile && !config.isMobile) {
            // Transform to mobile cards
            this.transformToCards(table, container, config);
            config.isMobile = true;
        } else if (!isMobile && config.isMobile) {
            // Transform back to table
            this.transformToTable(table, container, config);
            config.isMobile = false;
        }
    }

    transformToCards(table, container, config) {
        // Create cards container
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'table-mobile-cards';
        cardsContainer.setAttribute('data-table-id', config.id);

        // Get table data
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        
        rows.forEach(row => {
            const card = this.createCardFromRow(row, config.cardTemplate);
            if (card) {
                cardsContainer.appendChild(card);
            }
        });

        // Hide table and show cards
        table.style.display = 'none';
        container.appendChild(cardsContainer);

        // Add event listeners to cards
        this.addCardEventListeners(cardsContainer, table);
    }

    createCardFromRow(row, template) {
        const card = template.content.cloneNode(true);
        const cardElement = card.querySelector('.mobile-card');
        
        // Get row data
        const cells = Array.from(row.querySelectorAll('td'));
        const rowId = row.getAttribute('data-id');
        
        if (!rowId) return null;

        cardElement.setAttribute('data-id', rowId);

        // Fill card data
        cells.forEach(cell => {
            const dataAttributes = Array.from(cell.attributes).filter(attr => 
                attr.name.startsWith('data-') && attr.name !== 'data-id'
            );

            dataAttributes.forEach(attr => {
                const key = attr.name.replace('data-', '').replace(/-/g, '_');
                const value = attr.value;

                if (key === 'name') {
                    const titleElement = cardElement.querySelector('.mobile-card__title');
                    if (titleElement) titleElement.textContent = value;
                } else if (key === 'description') {
                    const subtitleElement = cardElement.querySelector('.mobile-card__subtitle');
                    if (subtitleElement) subtitleElement.textContent = value;
                } else {
                    const fieldElement = cardElement.querySelector(`[data-key="${key}"]`);
                    if (fieldElement) {
                        const valueElement = fieldElement.querySelector('.mobile-card__value');
                        if (valueElement) {
                            valueElement.textContent = value;
                        }
                    }
                }
            });
        });

        return cardElement;
    }

    transformToTable(table, container, config) {
        // Remove cards container
        const cardsContainer = container.querySelector('.table-mobile-cards');
        if (cardsContainer) {
            cardsContainer.remove();
        }

        // Show table
        table.style.display = '';
    }

    addCardEventListeners(cardsContainer, originalTable) {
        cardsContainer.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]');
            if (!action) return;

            const card = action.closest('.mobile-card');
            const rowId = card.getAttribute('data-id');
            const actionType = action.getAttribute('data-action');

            // Find corresponding row in original table
            const originalRow = originalTable.querySelector(`tr[data-id="${rowId}"]`);
            if (!originalRow) return;

            // Find corresponding button in original row
            const originalButton = originalRow.querySelector(`[data-action="${actionType}"]`);
            if (originalButton) {
                // Trigger click on original button
                originalButton.click();
            }
        });
    }

    handleResize() {
        this.tables.forEach((config, tableId) => {
            this.transformTable(tableId);
        });
    }

    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Public methods
    addTable(table) {
        if (table && table.id) {
            this.setupTable(table);
        }
    }

    removeTable(tableId) {
        this.tables.delete(tableId);
    }

    refreshTable(tableId) {
        const config = this.tables.get(tableId);
        if (config) {
            this.transformTable(tableId);
        }
    }

    // Get current breakpoint
    getCurrentBreakpoint() {
        const width = window.innerWidth;
        if (width <= this.breakpoints.mobile) return 'mobile';
        if (width <= this.breakpoints.tablet) return 'tablet';
        return 'desktop';
    }

    // Check if currently in mobile view
    isMobile() {
        return window.innerWidth <= this.breakpoints.mobile;
    }

    // Check if currently in tablet view
    isTablet() {
        return window.innerWidth > this.breakpoints.mobile && 
               window.innerWidth <= this.breakpoints.tablet;
    }

    // Check if currently in desktop view
    isDesktop() {
        return window.innerWidth > this.breakpoints.tablet;
    }
}

// Initialize responsive table manager
const responsiveTableManager = new ResponsiveTableManager();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.responsiveTableManager = responsiveTableManager;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponsiveTableManager;
}
