// VLTRN SDK Tools - Main JavaScript

let currentCategory = 'all';
let searchTerm = '';

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    renderSDKGrid();
    setupFilters();
    setupSearch();
});

// Render SDK cards
function renderSDKGrid() {
    const grid = document.getElementById('sdkGrid');
    const filteredSDKs = filterSDKs();

    if (filteredSDKs.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
                <p style="font-size: 18px; color: var(--text-secondary);">No SDKs found matching your criteria</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = filteredSDKs.map(sdk => createSDKCard(sdk)).join('');

    // Add click handlers
    document.querySelectorAll('.sdk-card').forEach(card => {
        card.addEventListener('click', () => {
            const sdkId = card.dataset.sdk;
            openModal(sdkId);
        });
    });
}

// Create SDK card HTML
function createSDKCard(sdk) {
    const statusClass = sdk.status === 'ready' ? 'status-ready' : 'status-dev';
    const statusText = sdk.status === 'ready' ? 'Production Ready' : `In Development (${sdk.completion})`;

    return `
        <div class="sdk-card" data-sdk="${sdk.id}" data-category="${sdk.category}">
            <div class="sdk-header">
                <div>
                    <h3 class="sdk-name">${sdk.name}</h3>
                    <span class="sdk-category">${sdk.category}</span>
                </div>
                <div class="sdk-status ${statusClass}">
                    <span class="status-dot"></span>
                    ${statusText}
                </div>
            </div>

            <p class="sdk-description">${sdk.description}</p>

            <div class="sdk-examples">
                <div class="example-label">Key Use Cases</div>
                ${sdk.examples.map(ex => `
                    <div class="example-item">
                        <div class="example-title">${ex.title}</div>
                        <div class="example-desc">${ex.description}</div>
                    </div>
                `).join('')}
            </div>

            <div class="sdk-footer">
                <div class="sdk-price">
                    <span class="amount">$${sdk.price}</span>/year
                </div>
                <button class="sdk-cta" onclick="event.stopPropagation(); installSDK('${sdk.id}')">
                    ${sdk.status === 'ready' ? 'Get Started' : 'Join Waitlist'}
                </button>
            </div>
        </div>
    `;
}

// Filter SDKs
function filterSDKs() {
    return SDK_DATA.filter(sdk => {
        const matchesCategory = currentCategory === 'all' || sdk.category === currentCategory;
        const matchesSearch = searchTerm === '' ||
            sdk.name.toLowerCase().includes(searchTerm) ||
            sdk.description.toLowerCase().includes(searchTerm) ||
            sdk.category.toLowerCase().includes(searchTerm);

        return matchesCategory && matchesSearch;
    });
}

// Setup filter pills
function setupFilters() {
    document.querySelectorAll('.filter-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            // Update active state
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            // Update category
            currentCategory = pill.dataset.category;
            renderSDKGrid();
        });
    });
}

// Setup search
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value.toLowerCase();
        renderSDKGrid();
    });
}

// Open modal with SDK details
function openModal(sdkId) {
    const sdk = SDK_DATA.find(s => s.id === sdkId);
    if (!sdk) return;

    const modal = document.getElementById('sdkModal');
    const modalBody = document.getElementById('modalBody');

    modalBody.innerHTML = createModalContent(sdk);
    modal.classList.add('active');

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('sdkModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Create modal content
function createModalContent(sdk) {
    const statusClass = sdk.status === 'ready' ? 'status-ready' : 'status-dev';
    const statusText = sdk.status === 'ready' ? 'Production Ready' : `In Development (${sdk.completion})`;

    return `
        <div>
            <div style="margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div>
                        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace;">
                            ${sdk.name}
                        </h2>
                        <div style="display: flex; gap: 15px; align-items: center;">
                            <span class="sdk-category">${sdk.category}</span>
                            <span class="sdk-status ${statusClass}">
                                <span class="status-dot"></span>
                                ${statusText}
                            </span>
                            <span style="font-size: 13px; color: var(--text-secondary); font-weight: 500;">
                                ${sdk.language}
                            </span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 14px; color: var(--text-secondary); margin-bottom: 5px;">Starting at</div>
                        <div style="font-size: 36px; font-weight: 700; background: var(--vltrn-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                            $${sdk.price}
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary);">per year</div>
                    </div>
                </div>

                <p style="font-size: 16px; line-height: 1.8; color: var(--text-secondary); margin-bottom: 30px;">
                    ${sdk.description}
                </p>
            </div>

            ${sdk.stats ? `
                <div style="display: flex; gap: 30px; margin-bottom: 30px; padding: 20px; background: var(--bg-tertiary); border-radius: 8px;">
                    ${Object.entries(sdk.stats).map(([key, value]) => `
                        <div>
                            <div style="font-size: 24px; font-weight: 700; color: var(--accent-primary);">${value}</div>
                            <div style="font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em;">${key}</div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            <div style="margin-bottom: 30px;">
                <h3 style="font-size: 18px; font-weight: 600; margin-bottom: 15px;">Key Features</h3>
                <ul style="list-style: none; padding: 0;">
                    ${sdk.features.map(feature => `
                        <li style="padding: 10px 0; border-bottom: 1px solid var(--border-color); color: var(--text-secondary);">
                            <span style="color: var(--accent-primary); margin-right: 10px;">✓</span>
                            ${feature}
                        </li>
                    `).join('')}
                </ul>
            </div>

            <div style="margin-bottom: 30px;">
                <h3 style="font-size: 18px; font-weight: 600; margin-bottom: 15px;">Use Case Examples</h3>
                ${sdk.examples.map((ex, i) => `
                    <div style="margin-bottom: 20px; padding: 20px; background: var(--bg-tertiary); border-radius: 8px; border-left: 3px solid var(--accent-primary);">
                        <h4 style="font-size: 16px; font-weight: 600; color: var(--accent-primary); margin-bottom: 8px;">
                            Example ${i + 1}: ${ex.title}
                        </h4>
                        <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.6;">
                            ${ex.description}
                        </p>
                    </div>
                `).join('')}
            </div>

            <div style="display: flex; gap: 15px; justify-content: flex-end; padding-top: 30px; border-top: 1px solid var(--border-color);">
                <button onclick="window.open('https://docs.vltrn.io/${sdk.id}', '_blank')"
                        style="padding: 14px 28px; background: transparent; border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-primary); cursor: pointer; font-size: 13px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; transition: all 0.3s;"
                        onmouseover="this.style.background='rgba(255,255,255,0.05)'"
                        onmouseout="this.style.background='transparent'">
                    View Docs
                </button>
                <button onclick="installSDK('${sdk.id}')"
                        style="padding: 14px 28px; background: var(--accent-primary); border: none; border-radius: 6px; color: white; cursor: pointer; font-size: 13px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; transition: all 0.3s;"
                        onmouseover="this.style.background='var(--accent-secondary)'"
                        onmouseout="this.style.background='var(--accent-primary)'">
                    ${sdk.status === 'ready' ? 'Get Started' : 'Join Waitlist'}
                </button>
            </div>
        </div>
    `;
}

// Install SDK action
function installSDK(sdkId) {
    const sdk = SDK_DATA.find(s => s.id === sdkId);
    if (!sdk) return;

    // Check if user is logged in
    const token = localStorage.getItem('token');

    if (!token) {
        // Redirect to login with return URL
        window.location.href = `/login?redirect=/tools&install=${sdkId}`;
        return;
    }

    // If production ready, redirect to dashboard with install parameter
    if (sdk.status === 'ready') {
        window.location.href = `/dashboard?install=${sdkId}`;
    } else {
        // Join waitlist for dev SDKs
        window.location.href = `/signup?waitlist=${sdkId}`;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Close modal on Escape
    if (e.key === 'Escape') {
        closeModal();
    }

    // Focus search on /
    if (e.key === '/' && e.target.tagName !== 'INPUT') {
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }
});

// Close modal on background click
document.getElementById('sdkModal').addEventListener('click', (e) => {
    if (e.target.id === 'sdkModal') {
        closeModal();
    }
});
