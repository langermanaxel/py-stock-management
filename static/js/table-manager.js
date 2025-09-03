/**
 * Table Manager - Gestión avanzada de tablas
 * Búsqueda, filtros, ordenamiento, paginación y acciones seguras
 */

class TableManager {
    constructor(tableId, options = {}) {
        this.tableId = tableId;
        this.table = document.getElementById(tableId);
        this.options = {
            searchDebounce: 300,
            pageSize: 10,
            pageSizes: [10, 25, 50],
            enableSorting: true,
            enablePagination: true,
            enableSearch: true,
            enableFilters: true,
            ...options
        };
        
        this.data = [];
        this.filteredData = [];
        this.sortedData = [];
        this.currentPage = 1;
        this.pageSize = this.options.pageSize;
        this.sortColumn = null;
        this.sortDirection = 'asc';
        this.searchTerm = '';
        this.filters = {};
        this.deletedItems = [];
        
        this.init();
    }

    init() {
        if (!this.table) {
            console.error(`Table with id "${this.tableId}" not found`);
            return;
        }

        this.setupTable();
        this.setupSearch();
        this.setupFilters();
        this.setupSorting();
        this.setupPagination();
        this.setupActions();
    }

    /**
     * Setup table structure
     */
    setupTable() {
        // Add table wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        this.table.parentNode.insertBefore(wrapper, this.table);
        wrapper.appendChild(this.table);

        // Add table controls
        this.addTableControls(wrapper);
        
        // Add sticky header
        this.addStickyHeader();
    }

    /**
     * Add table controls (search, filters, pagination)
     */
    addTableControls(wrapper) {
        const controls = document.createElement('div');
        controls.className = 'table-controls';
        
        // Search and filters row
        const searchRow = document.createElement('div');
        searchRow.className = 'table-controls__row';
        
        if (this.options.enableSearch) {
            searchRow.appendChild(this.createSearchInput());
        }
        
        if (this.options.enableFilters) {
            searchRow.appendChild(this.createFiltersContainer());
        }
        
        controls.appendChild(searchRow);
        
        // Pagination and info row
        const paginationRow = document.createElement('div');
        paginationRow.className = 'table-controls__row table-controls__row--pagination';
        paginationRow.appendChild(this.createPaginationInfo());
        paginationRow.appendChild(this.createPaginationControls());
        
        controls.appendChild(paginationRow);
        
        wrapper.insertBefore(controls, this.table);
    }

    /**
     * Create search input
     */
    createSearchInput() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'table-search';
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'input input--md';
        searchInput.placeholder = 'Buscar...';
        searchInput.setAttribute('aria-label', 'Buscar en la tabla');
        
        const searchIcon = document.createElement('div');
        searchIcon.className = 'table-search__icon';
        searchIcon.innerHTML = `
            <svg class="icon icon--md" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
        `;
        
        searchContainer.appendChild(searchIcon);
        searchContainer.appendChild(searchInput);
        
        // Debounced search
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.searchTerm = e.target.value.toLowerCase();
                this.applyFiltersAndSort();
            }, this.options.searchDebounce);
        });
        
        this.searchInput = searchInput;
        return searchContainer;
    }

    /**
     * Create filters container
     */
    createFiltersContainer() {
        const filtersContainer = document.createElement('div');
        filtersContainer.className = 'table-filters';
        
        // Add filter buttons based on table columns
        const headers = this.table.querySelectorAll('th[data-filter]');
        headers.forEach(header => {
            const filterType = header.getAttribute('data-filter');
            const filterKey = header.getAttribute('data-filter-key') || header.textContent.toLowerCase();
            
            if (filterType === 'select') {
                filtersContainer.appendChild(this.createSelectFilter(filterKey, header));
            } else if (filterType === 'date') {
                filtersContainer.appendChild(this.createDateFilter(filterKey, header));
            }
        });
        
        return filtersContainer;
    }

    /**
     * Create select filter
     */
    createSelectFilter(key, header) {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'table-filter';
        
        const label = document.createElement('label');
        label.className = 'table-filter__label';
        label.textContent = header.textContent;
        
        const select = document.createElement('select');
        select.className = 'input input--md';
        select.setAttribute('aria-label', `Filtrar por ${header.textContent}`);
        
        const allOption = document.createElement('option');
        allOption.value = '';
        allOption.textContent = 'Todos';
        select.appendChild(allOption);
        
        // Get unique values from data
        const uniqueValues = [...new Set(this.data.map(item => item[key]))];
        uniqueValues.forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            select.appendChild(option);
        });
        
        select.addEventListener('change', (e) => {
            if (e.target.value) {
                this.filters[key] = e.target.value;
            } else {
                delete this.filters[key];
            }
            this.applyFiltersAndSort();
        });
        
        filterContainer.appendChild(label);
        filterContainer.appendChild(select);
        
        return filterContainer;
    }

    /**
     * Create date filter
     */
    createDateFilter(key, header) {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'table-filter';
        
        const label = document.createElement('label');
        label.className = 'table-filter__label';
        label.textContent = header.textContent;
        
        const input = document.createElement('input');
        input.type = 'date';
        input.className = 'input input--md';
        input.setAttribute('aria-label', `Filtrar por ${header.textContent}`);
        
        input.addEventListener('change', (e) => {
            if (e.target.value) {
                this.filters[key] = e.target.value;
            } else {
                delete this.filters[key];
            }
            this.applyFiltersAndSort();
        });
        
        filterContainer.appendChild(label);
        filterContainer.appendChild(input);
        
        return filterContainer;
    }

    /**
     * Create pagination info
     */
    createPaginationInfo() {
        const info = document.createElement('div');
        info.className = 'table-pagination__info';
        this.paginationInfo = info;
        return info;
    }

    /**
     * Create pagination controls
     */
    createPaginationControls() {
        const controls = document.createElement('div');
        controls.className = 'table-pagination__controls';
        
        // Page size selector
        const pageSizeContainer = document.createElement('div');
        pageSizeContainer.className = 'table-pagination__page-size';
        
        const pageSizeLabel = document.createElement('label');
        pageSizeLabel.textContent = 'Mostrar:';
        pageSizeLabel.className = 'table-pagination__label';
        
        const pageSizeSelect = document.createElement('select');
        pageSizeSelect.className = 'input input--sm';
        pageSizeSelect.setAttribute('aria-label', 'Elementos por página');
        
        this.options.pageSizes.forEach(size => {
            const option = document.createElement('option');
            option.value = size;
            option.textContent = size;
            if (size === this.pageSize) option.selected = true;
            pageSizeSelect.appendChild(option);
        });
        
        pageSizeSelect.addEventListener('change', (e) => {
            this.pageSize = parseInt(e.target.value);
            this.currentPage = 1;
            this.updatePagination();
        });
        
        pageSizeContainer.appendChild(pageSizeLabel);
        pageSizeContainer.appendChild(pageSizeSelect);
        
        // Page navigation
        const navigation = document.createElement('div');
        navigation.className = 'table-pagination__navigation';
        
        const prevButton = document.createElement('button');
        prevButton.className = 'btn btn--sm btn--secondary';
        prevButton.innerHTML = `
            <svg class="icon icon--sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            Anterior
        `;
        prevButton.addEventListener('click', () => this.previousPage());
        
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn--sm btn--secondary';
        nextButton.innerHTML = `
            Siguiente
            <svg class="icon icon--sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
        `;
        nextButton.addEventListener('click', () => this.nextPage());
        
        navigation.appendChild(prevButton);
        navigation.appendChild(nextButton);
        
        controls.appendChild(pageSizeContainer);
        controls.appendChild(navigation);
        
        this.prevButton = prevButton;
        this.nextButton = nextButton;
        
        return controls;
    }

    /**
     * Add sticky header
     */
    addStickyHeader() {
        const header = this.table.querySelector('thead');
        if (header) {
            header.classList.add('table__header--sticky');
        }
    }

    /**
     * Setup sorting
     */
    setupSorting() {
        if (!this.options.enableSorting) return;
        
        const headers = this.table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.classList.add('table__header-cell--sortable');
            header.setAttribute('tabindex', '0');
            header.setAttribute('role', 'button');
            header.setAttribute('aria-label', `Ordenar por ${header.textContent}`);
            
            header.addEventListener('click', () => {
                const sortKey = header.getAttribute('data-sort');
                this.sortBy(sortKey);
            });
            
            header.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const sortKey = header.getAttribute('data-sort');
                    this.sortBy(sortKey);
                }
            });
        });
    }

    /**
     * Sort by column
     */
    sortBy(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }
        
        this.updateSortIndicators();
        this.applyFiltersAndSort();
    }

    /**
     * Update sort indicators
     */
    updateSortIndicators() {
        const headers = this.table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            const sortKey = header.getAttribute('data-sort');
            const indicator = header.querySelector('.sort-indicator');
            
            if (indicator) {
                indicator.remove();
            }
            
            if (this.sortColumn === sortKey) {
                const newIndicator = document.createElement('span');
                newIndicator.className = 'sort-indicator';
                newIndicator.innerHTML = this.sortDirection === 'asc' ? '↑' : '↓';
                newIndicator.setAttribute('aria-label', `Ordenado ${this.sortDirection === 'asc' ? 'ascendente' : 'descendente'}`);
                header.appendChild(newIndicator);
            }
        });
    }

    /**
     * Apply filters and sorting
     */
    applyFiltersAndSort() {
        // Apply search
        let filtered = this.data.filter(item => {
            if (!this.searchTerm) return true;
            
            return Object.values(item).some(value => 
                String(value).toLowerCase().includes(this.searchTerm)
            );
        });
        
        // Apply filters
        Object.keys(this.filters).forEach(key => {
            filtered = filtered.filter(item => {
                const value = item[key];
                const filterValue = this.filters[key];
                
                if (typeof value === 'string') {
                    return value.toLowerCase().includes(filterValue.toLowerCase());
                } else if (value instanceof Date) {
                    return value.toISOString().split('T')[0] === filterValue;
                } else {
                    return value === filterValue;
                }
            });
        });
        
        // Apply sorting
        if (this.sortColumn) {
            filtered.sort((a, b) => {
                const aVal = a[this.sortColumn];
                const bVal = b[this.sortColumn];
                
                if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });
        }
        
        this.filteredData = filtered;
        this.currentPage = 1;
        this.updateTable();
    }

    /**
     * Update table display
     */
    updateTable() {
        const tbody = this.table.querySelector('tbody');
        if (!tbody) return;
        
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        const pageData = this.filteredData.slice(startIndex, endIndex);
        
        // Clear existing rows
        tbody.innerHTML = '';
        
        // Add new rows
        pageData.forEach(item => {
            const row = this.createTableRow(item);
            tbody.appendChild(row);
        });
        
        this.updatePagination();
    }

    /**
     * Create table row
     */
    createTableRow(item) {
        const row = document.createElement('tr');
        row.className = 'table__row';
        row.setAttribute('data-id', item.id);
        
        // Add cells based on table headers
        const headers = this.table.querySelectorAll('th');
        headers.forEach(header => {
            const cell = document.createElement('td');
            cell.className = 'table__cell';
            
            const dataKey = header.getAttribute('data-key');
            if (dataKey && item[dataKey] !== undefined) {
                cell.textContent = item[dataKey];
            }
            
            row.appendChild(cell);
        });
        
        return row;
    }

    /**
     * Update pagination
     */
    updatePagination() {
        const totalPages = Math.ceil(this.filteredData.length / this.pageSize);
        
        // Update pagination info
        const startItem = (this.currentPage - 1) * this.pageSize + 1;
        const endItem = Math.min(this.currentPage * this.pageSize, this.filteredData.length);
        
        this.paginationInfo.textContent = 
            `Mostrando ${startItem}-${endItem} de ${this.filteredData.length} elementos`;
        
        // Update navigation buttons
        this.prevButton.disabled = this.currentPage === 1;
        this.nextButton.disabled = this.currentPage === totalPages;
        
        // Update table
        this.updateTable();
    }

    /**
     * Previous page
     */
    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.updateTable();
        }
    }

    /**
     * Next page
     */
    nextPage() {
        const totalPages = Math.ceil(this.filteredData.length / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.updateTable();
        }
    }

    /**
     * Setup actions
     */
    setupActions() {
        // Add action buttons to table rows
        this.table.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="delete"]')) {
                e.preventDefault();
                this.handleDeleteAction(e.target);
            } else if (e.target.matches('[data-action="edit"]')) {
                e.preventDefault();
                this.handleEditAction(e.target);
            }
        });
    }

    /**
     * Handle delete action
     */
    handleDeleteAction(button) {
        const row = button.closest('tr');
        const itemId = row.getAttribute('data-id');
        const item = this.data.find(item => item.id == itemId);
        
        if (!item) return;
        
        // Show confirmation dialog
        this.showDeleteConfirmation(item, () => {
            this.deleteItem(itemId);
        });
    }

    /**
     * Show delete confirmation
     */
    showDeleteConfirmation(item, onConfirm) {
        const modal = document.createElement('div');
        modal.className = 'modal modal--open';
        modal.innerHTML = `
            <div class="modal__content modal--sm">
                <div class="modal__header">
                    <h2 class="modal__title">Confirmar eliminación</h2>
                    <button class="modal__close" onclick="this.closest('.modal').remove()">
                        <svg class="modal__close-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="modal__body">
                    <p>¿Estás seguro de que quieres eliminar este elemento?</p>
                    <div class="card card--flat mt-4">
                        <strong>${item.name || item.title || 'Elemento'}</strong>
                    </div>
                </div>
                <div class="modal__footer">
                    <button class="btn btn--secondary" onclick="this.closest('.modal').remove()">
                        Cancelar
                    </button>
                    <button class="btn btn--error" onclick="this.closest('.modal').remove(); arguments[0]();">
                        Eliminar
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add click handler for confirm button
        const confirmButton = modal.querySelector('.btn--error');
        confirmButton.addEventListener('click', onConfirm);
    }

    /**
     * Delete item
     */
    deleteItem(itemId) {
        const item = this.data.find(item => item.id == itemId);
        if (!item) return;
        
        // Store for undo
        this.deletedItems.push({
            item: item,
            timestamp: Date.now()
        });
        
        // Remove from data
        this.data = this.data.filter(item => item.id != itemId);
        
        // Update table
        this.applyFiltersAndSort();
        
        // Show undo notification
        this.showUndoNotification(item);
    }

    /**
     * Show undo notification
     */
    showUndoNotification(item) {
        if (window.feedbackManager) {
            const toast = window.feedbackManager.success(
                'Elemento eliminado',
                `${item.name || item.title || 'Elemento'} ha sido eliminado`,
                5000
            );
            
            // Add undo button
            const undoButton = document.createElement('button');
            undoButton.className = 'btn btn--sm btn--outline ml-2';
            undoButton.textContent = 'Deshacer';
            undoButton.addEventListener('click', () => {
                this.undoDelete(item.id);
                toast.remove();
            });
            
            const toastContent = toast.querySelector('.toast-content');
            toastContent.appendChild(undoButton);
        }
    }

    /**
     * Undo delete
     */
    undoDelete(itemId) {
        const deletedItem = this.deletedItems.find(deleted => deleted.item.id == itemId);
        if (!deletedItem) return;
        
        // Restore item
        this.data.push(deletedItem.item);
        
        // Remove from deleted items
        this.deletedItems = this.deletedItems.filter(deleted => deleted.item.id != itemId);
        
        // Update table
        this.applyFiltersAndSort();
        
        // Show success message
        if (window.feedbackManager) {
            window.feedbackManager.success(
                'Elemento restaurado',
                'El elemento ha sido restaurado exitosamente'
            );
        }
    }

    /**
     * Handle edit action
     */
    handleEditAction(button) {
        const row = button.closest('tr');
        const itemId = row.getAttribute('data-id');
        const item = this.data.find(item => item.id == itemId);
        
        if (!item) return;
        
        // Trigger edit event
        const event = new CustomEvent('table:edit', {
            detail: { item: item, itemId: itemId }
        });
        this.table.dispatchEvent(event);
    }

    /**
     * Set table data
     */
    setData(data) {
        this.data = data;
        this.applyFiltersAndSort();
    }

    /**
     * Add new item
     */
    addItem(item) {
        this.data.push(item);
        this.applyFiltersAndSort();
    }

    /**
     * Update item
     */
    updateItem(itemId, updatedItem) {
        const index = this.data.findIndex(item => item.id == itemId);
        if (index !== -1) {
            this.data[index] = { ...this.data[index], ...updatedItem };
            this.applyFiltersAndSort();
        }
    }

    /**
     * Get current data
     */
    getData() {
        return this.data;
    }

    /**
     * Get filtered data
     */
    getFilteredData() {
        return this.filteredData;
    }

    /**
     * Clear filters
     */
    clearFilters() {
        this.filters = {};
        this.searchTerm = '';
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        this.applyFiltersAndSort();
    }

    /**
     * Export data
     */
    exportData(format = 'csv') {
        const data = this.filteredData;
        
        if (format === 'csv') {
            this.exportToCSV(data);
        } else if (format === 'json') {
            this.exportToJSON(data);
        }
    }

    /**
     * Export to CSV
     */
    exportToCSV(data) {
        const headers = this.table.querySelectorAll('th[data-key]');
        const csvHeaders = Array.from(headers).map(header => header.textContent);
        
        const csvContent = [
            csvHeaders.join(','),
            ...data.map(item => 
                headers.map(header => {
                    const key = header.getAttribute('data-key');
                    const value = item[key] || '';
                    return `"${String(value).replace(/"/g, '""')}"`;
                }).join(',')
            )
        ].join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `tabla_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Export to JSON
     */
    exportToJSON(data) {
        const jsonContent = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonContent], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `tabla_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Initialize table managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Auto-initialize tables with data-table attribute
    const tables = document.querySelectorAll('[data-table]');
    tables.forEach(table => {
        const tableId = table.id;
        const options = JSON.parse(table.getAttribute('data-table-options') || '{}');
        window[`tableManager_${tableId}`] = new TableManager(tableId, options);
    });
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TableManager;
}
