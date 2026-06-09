// API Configuration
const API_BASE_URL = '/api';

// Token management
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function getUser() {
    return JSON.parse(localStorage.getItem('user') || '{}');
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function clearSession() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/index.html';
}

// API request helper
async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            clearSession();
            return null;
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication API
const authAPI = {
    login: async (email, password, role) => {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, role }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        return await response.json();
    },
};

// Employee API
const employeeAPI = {
    create: (employee) => apiRequest('/employees/create', {
        method: 'POST',
        body: JSON.stringify(employee),
    }),

    list: () => apiRequest('/employees/list', { method: 'GET' }),

    getStatus: (employeeId) => apiRequest(`/employees/status/${employeeId}`, { method: 'GET' }),

    startOnboarding: (employeeId) => apiRequest(`/employees/start-onboarding/${employeeId}`, {
        method: 'POST',
    }),

    retryTask: (employeeId, taskName) => apiRequest(`/employees/retry-task/${employeeId}/${encodeURIComponent(taskName)}`, {
        method: 'POST',
    }),
};

// Dashboard API
const dashboardAPI = {
    getStats: () => apiRequest('/dashboard/stats', { method: 'GET' }),

    getOnboardingList: () => apiRequest('/dashboard/onboarding-list', { method: 'GET' }),
};

// Helper functions for UI
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.page-container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    }
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner-center"><div class="spinner"></div></div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Initialize navbar on all pages
function initializeNavbar() {
    const user = getUser();
    if (!user.email && window.location.pathname !== '/index.html') {
        window.location.href = '/index.html';
        return;
    }

    const userEmailEl = document.getElementById('user-email');
    const userRoleEl = document.getElementById('user-role');
    
    if (userEmailEl) userEmailEl.textContent = user.email;
    if (userRoleEl) userRoleEl.textContent = user.role.toUpperCase();
}

// Refresh dashboard stats periodically
function startAutoRefresh(callback, interval = 5000) {
    callback();
    return setInterval(callback, interval);
}

// Polling for task status
function pollTaskStatus(employeeId, callback, interval = 2000) {
    const poll = async () => {
        try {
            const status = await employeeAPI.getStatus(employeeId);
            callback(status);
        } catch (error) {
            console.error('Polling error:', error);
        }
    };

    poll();
    return setInterval(poll, interval);
}

// Format status badge
function getStatusBadge(status) {
    const badgeClass = {
        'pending': 'badge-pending',
        'running': 'badge-running',
        'completed': 'badge-completed',
        'failed': 'badge-failed',
        'onboarding': 'badge-onboarding',
        'partial': 'badge-partial',
    };

    return `<span class="badge ${badgeClass[status] || 'badge-pending'}">${status}</span>`;
}
