/**
 * StudyBalance AI - Main JavaScript File
 * Core functionality for the StudyBalance AI web application
 * Author: AyaanRathod
 */

// Global variables
let currentAnalysis = null;
let currentSchedule = null;
let wellnessChart = null;
let emailChart = null;

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('🚀 StudyBalance AI initializing...');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize charts if on dashboard
    if (document.getElementById('wellnessChart')) {
        initializeDashboardCharts();
    }
    
    // Load initial data
    loadInitialData();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize auto-refresh
    setupAutoRefresh();
    
    console.log('✅ StudyBalance AI initialized successfully!');
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Navigation active state
    updateActiveNavigation();
    
    // Form submissions
    const analysisForm = document.getElementById('analysisForm');
    if (analysisForm) {
        analysisForm.addEventListener('submit', handleAnalysisSubmit);
    }
    
    const scheduleForm = document.getElementById('scheduleForm');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', handleScheduleSubmit);
    }
    
    // Quick action buttons
    setupQuickActionListeners();
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

/**
 * Load initial data for the current page
 */
async function loadInitialData() {
    const currentPage = getCurrentPage();
    
    // Check authentication status first
    await checkAuthenticationStatus();
    
    switch (currentPage) {
        case 'dashboard':
            await loadDashboardData();
            break;
        case 'analyze':
            await loadAnalysisPreferences();
            break;
        case 'schedule':
            await loadSchedulePreferences();
            break;
        case 'wellness':
            await loadWellnessData();
            break;
    }
}

/**
 * Get current page identifier
 */
function getCurrentPage() {
    const path = window.location.pathname;
    if (path.includes('/analyze')) return 'analyze';
    if (path.includes('/schedule')) return 'schedule';
    if (path.includes('/wellness')) return 'wellness';
    return 'dashboard';
}

/**
 * Check authentication status with arcade.dev
 */
async function checkAuthenticationStatus() {
    try {
        const response = await fetch('/api/auth_status');
        const data = await response.json();
        
        if (data.success) {
            const authStatus = data.auth_status;
            
            if (!authStatus.arcade_configured) {
                showAuthenticationPrompt(authStatus);
            } else {
                // Show authentication success message briefly
                showToast('🔐 Arcade.dev ready! OAuth will prompt when you access Gmail/Calendar', 'success', 5000);
            }
        }
    } catch (error) {
        console.error('Error checking authentication status:', error);
    }
}

/**
 * Show authentication setup prompt
 */
function showAuthenticationPrompt(authStatus) {
    const alertHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert" id="authAlert">
            <div class="d-flex align-items-center">
                <i class="fas fa-key me-2"></i>
                <div class="flex-grow-1">
                    <strong>🔐 Setup Required:</strong> ${authStatus.message}
                    ${authStatus.auth_url ? `
                        <br><small class="text-muted">
                            1. Get credentials from <a href="${authStatus.auth_url}" target="_blank">arcade.dev dashboard</a><br>
                            2. Copy .env.example to .env<br>
                            3. Add your ARCADE_API_KEY and ARCADE_USER_ID<br>
                            4. Restart the application
                        </small>
                    ` : ''}
                </div>
                <button type="button" class="btn btn-sm btn-outline-primary me-2" onclick="window.open('${authStatus.auth_url}', '_blank')">
                    Get Credentials
                </button>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Add to the top of the main content
    const mainContent = document.querySelector('.container-fluid') || document.querySelector('main') || document.body;
    if (mainContent) {
        mainContent.insertAdjacentHTML('afterbegin', alertHTML);
    }
}

/**
 * Update active navigation item
 */
function updateActiveNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Dashboard Functions
 */

/**
 * Load dashboard data
 */
async function loadDashboardData() {
    try {
        showLoading();
        
        const response = await fetch('/api/dashboard_stats');
        const data = await response.json();
        
        if (data.success) {
            updateDashboardStats(data.stats);
            updateRecentActivity(data.recent_activity || []);
        } else {
            showToast('Failed to load dashboard data', 'error');
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showToast('Error loading dashboard data', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Update dashboard statistics
 */
function updateDashboardStats(stats) {
    // Update stat cards
    updateElement('wellnessScore', stats.wellness_score || '7.5');
    updateElement('emailCount', stats.weekly_emails || '42');
    updateElement('studyHours', stats.study_hours_today || '6.5h');
    updateElement('nudgeCount', stats.active_nudges || '3');
    
    // Update stat badges
    updateStatBadges(stats);
    
    // Update wellness insights
    updateWellnessInsights(stats);
}

/**
 * Update recent activity section
 */
function updateRecentActivity(activities) {
    const activityContainer = document.getElementById('recentActivity');
    if (!activityContainer) return;
    
    if (!activities || activities.length === 0) {
        activityContainer.innerHTML = '<p class="text-muted">No recent activity</p>';
        return;
    }
    
    const activityHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon">
                <i class="fas ${getActivityIcon(activity.type)}"></i>
            </div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${formatTimeAgo(activity.timestamp)}</div>
            </div>
        </div>
    `).join('');
    
    activityContainer.innerHTML = activityHTML;
}

/**
 * Get icon for activity type
 */
function getActivityIcon(type) {
    const icons = {
        'email_analysis': 'fa-envelope',
        'schedule_created': 'fa-calendar',
        'wellness_nudge': 'fa-heart',
        'break_reminder': 'fa-coffee',
        'study_session': 'fa-book'
    };
    return icons[type] || 'fa-info-circle';
}

/**
 * Format timestamp to relative time
 */
function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMs = now - time;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
}

/**
 * Update stat badge colors based on values
 */
function updateStatBadges(stats) {
    const wellnessBadge = document.querySelector('#wellnessScore').parentElement.querySelector('.stat-badge');
    const emailBadge = document.querySelector('#emailCount').parentElement.querySelector('.stat-badge');
    
    // Wellness score badge
    if (wellnessBadge) {
        const score = parseFloat(stats.wellness_score || 7.5);
        if (score >= 8) {
            wellnessBadge.className = 'stat-badge good';
            wellnessBadge.textContent = 'Excellent';
        } else if (score >= 6) {
            wellnessBadge.className = 'stat-badge warning';
            wellnessBadge.textContent = 'Good';
        } else {
            wellnessBadge.className = 'stat-badge danger';
            wellnessBadge.textContent = 'Needs Attention';
        }
    }
    
    // Email count badge
    if (emailBadge) {
        const count = parseInt(stats.weekly_emails || 42);
        if (count > 80) {
            emailBadge.className = 'stat-badge danger';
            emailBadge.textContent = 'High';
        } else if (count > 50) {
            emailBadge.className = 'stat-badge warning';
            emailBadge.textContent = 'Monitor';
        } else {
            emailBadge.className = 'stat-badge good';
            emailBadge.textContent = 'Normal';
        }
    }
}

/**
 * Update wellness insights
 */
function updateWellnessInsights(stats) {
    const insights = generateWellnessInsights(stats);
    const insightsContainer = document.querySelector('.insights-card .card-body .row');
    
    if (insightsContainer && insights.length > 0) {
        insightsContainer.innerHTML = insights.map(insight => `
            <div class="col-md-4">
                <div class="insight-item">
                    <div class="insight-icon">
                        <i class="fas fa-${insight.icon} text-${insight.color}"></i>
                    </div>
                    <div class="insight-content">
                        <h6>${insight.title}</h6>
                        <p>${insight.message}</p>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

/**
 * Generate wellness insights based on stats
 */
function generateWellnessInsights(stats) {
    const insights = [];
    const wellnessScore = parseFloat(stats.wellness_score || 7.5);
    const emailCount = parseInt(stats.weekly_emails || 42);
    const studyHours = parseFloat(stats.study_hours_today || 6.5);
    
    // Wellness score insight
    if (wellnessScore >= 8) {
        insights.push({
            icon: 'trophy',
            color: 'warning',
            title: 'Great Progress!',
            message: 'You\'re maintaining excellent wellness balance.'
        });
    } else if (wellnessScore < 6) {
        insights.push({
            icon: 'exclamation-triangle',
            color: 'danger',
            title: 'Wellness Alert',
            message: 'Consider taking more breaks and reducing stress.'
        });
    }
    
    // Email insight
    if (emailCount > 80) {
        insights.push({
            icon: 'envelope',
            color: 'orange',
            title: 'High Email Volume',
            message: 'Try email batching to reduce stress.'
        });
    }
    
    // Study hours insight
    if (studyHours > 8) {
        insights.push({
            icon: 'clock',
            color: 'warning',
            title: 'Long Study Day',
            message: 'Make sure to take adequate breaks.'
        });
    } else if (studyHours < 4) {
        insights.push({
            icon: 'book',
            color: 'info',
            title: 'Light Study Day',
            message: 'Good balance between study and rest.'
        });
    }
    
    // Default insights if none generated
    if (insights.length === 0) {
        insights.push(
            {
                icon: 'heart',
                color: 'success',
                title: 'Stay Hydrated',
                message: 'Remember to drink water throughout the day.'
            },
            {
                icon: 'moon',
                color: 'purple',
                title: 'Sleep Well',
                message: 'Aim for 7-8 hours of quality sleep.'
            },
            {
                icon: 'smile',
                color: 'info',
                title: 'Take Breaks',
                message: 'Regular breaks improve focus and creativity.'
            }
        );
    }
    
    return insights.slice(0, 3); // Return max 3 insights
}

/**
 * Initialize dashboard charts
 */
function initializeDashboardCharts() {
    // Initialize wellness trend chart if container exists
    const wellnessChartCanvas = document.getElementById('wellnessChart');
    if (wellnessChartCanvas) {
        createWellnessTrendChart();
    }
    
    // Initialize activity chart if container exists
    const activityChartCanvas = document.getElementById('activityChart');
    if (activityChartCanvas) {
        createActivityChart();
    }
}

/**
 * Create wellness trend chart
 */
function createWellnessTrendChart() {
    const ctx = document.getElementById('wellnessChart').getContext('2d');
    
    const data = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Wellness Score',
            data: [7.2, 7.8, 6.5, 8.1, 7.9, 8.5, 7.5],
            borderColor: 'rgb(79, 70, 229)',
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            tension: 0.4,
            fill: true
        }]
    };
    
    wellnessChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Weekly Wellness Trend'
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0,
                    max: 10,
                    ticks: {
                        stepSize: 2
                    }
                }
            }
        }
    });
}

/**
 * Analysis Page Functions
 */

/**
 * Load analysis preferences
 */
async function loadAnalysisPreferences() {
    const savedPreferences = localStorage.getItem('analysisPreferences');
    if (savedPreferences) {
        const preferences = JSON.parse(savedPreferences);
        
        // Apply saved preferences to form
        const rangeSelect = document.getElementById('analysisRange');
        if (rangeSelect && preferences.range) {
            rangeSelect.value = preferences.range;
        }
        
        // Apply checkbox states
        ['stressAnalysis', 'workloadAnalysis', 'patternAnalysis'].forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox && preferences[id] !== undefined) {
                checkbox.checked = preferences[id];
            }
        });
    }
}

/**
 * Start email analysis
 */
async function startAnalysis() {
    const daysBack = document.getElementById('analysisRange')?.value || 7;
    const analysisTypes = {
        stress: document.getElementById('stressAnalysis')?.checked || true,
        workload: document.getElementById('workloadAnalysis')?.checked || true,
        pattern: document.getElementById('patternAnalysis')?.checked || true
    };
    
    // Save preferences
    saveAnalysisPreferences({ range: daysBack, ...analysisTypes });
    
    showLoading();
    
    try {
        const response = await fetch('/api/analyze_gmail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                days: parseInt(daysBack),
                analysis_types: analysisTypes
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAnalysis = data.analysis;
            displayAnalysisResults(data.analysis);
            showToast('Email analysis completed successfully!', 'success');
        } else {
            showToast('Analysis failed: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showToast('Failed to complete analysis. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Display analysis results
 */
function displayAnalysisResults(analysis) {
    // Show results section
    const resultsSection = document.getElementById('analysisResults');
    if (resultsSection) {
        resultsSection.style.display = 'block';
        
        // Update summary cards
        updateAnalysisSummary(analysis);
        
        // Display stress keywords
        displayStressKeywords(analysis.stress_keywords_found || []);
        
        // Display recommendations
        displayRecommendations(analysis.recommendations || []);
        
        // Create charts
        createEmailPatternChart(analysis);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Update analysis summary cards
 */
function updateAnalysisSummary(analysis) {
    updateElement('totalEmails', analysis.total_emails || 0);
    updateElement('urgentEmails', analysis.urgent_emails || 0);
    updateElement('workloadScore', analysis.workload_score || 0);
    
    // Update burnout risk with appropriate styling
    const burnoutElement = document.getElementById('burnoutRisk');
    if (burnoutElement) {
        const risk = analysis.burnout_risk || 'Low';
        burnoutElement.textContent = risk;
        
        // Add color class based on risk level
        burnoutElement.className = 'result-number';
        if (risk.toLowerCase() === 'high') {
            burnoutElement.classList.add('text-danger');
        } else if (risk.toLowerCase() === 'moderate') {
            burnoutElement.classList.add('text-warning');
        } else {
            burnoutElement.classList.add('text-success');
        }
    }
}

/**
 * Display stress keywords
 */
function displayStressKeywords(keywords) {
    const container = document.getElementById('stressKeywords');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (keywords.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="fas fa-smile text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No stress keywords detected. Great job!</p>
            </div>
        `;
        return;
    }
    
    keywords.forEach(keyword => {
        const badge = document.createElement('span');
        badge.className = 'badge bg-danger me-2 mb-2';
        badge.innerHTML = `<i class="fas fa-exclamation-triangle me-1"></i>${keyword}`;
        container.appendChild(badge);
    });
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (recommendations.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="fas fa-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">You're doing great! No specific recommendations at this time.</p>
            </div>
        `;
        return;
    }
    
    recommendations.forEach((rec, index) => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <div class="recommendation-icon">
                <i class="fas fa-lightbulb text-warning"></i>
            </div>
            <div class="recommendation-text">
                <p>${rec}</p>
            </div>
        `;
        container.appendChild(item);
    });
}

/**
 * Create email pattern chart
 */
function createEmailPatternChart(analysis) {
    const ctx = document.getElementById('emailPatternChart')?.getContext('2d');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (emailChart) {
        emailChart.destroy();
    }
    
    // Generate sample hourly data based on analysis
    const hourlyData = generateHourlyEmailData(analysis);
    
    const chartData = {
        labels: Array.from({length: 24}, (_, i) => `${i.toString().padStart(2, '0')}:00`),
        datasets: [{
            label: 'Total Emails',
            data: hourlyData.total,
            borderColor: 'rgb(79, 70, 229)',
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            tension: 0.4,
            fill: true
        }, {
            label: 'Urgent Emails',
            data: hourlyData.urgent,
            borderColor: 'rgb(239, 68, 68)',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.4,
            fill: false
        }]
    };
    
    emailChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Email Distribution by Hour'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Emails'
                    }
                }
            }
        }
    });
}

/**
 * Generate hourly email data for chart
 */
function generateHourlyEmailData(analysis) {
    const totalEmails = analysis.total_emails || 0;
    const urgentEmails = analysis.urgent_emails || 0;
    const peakHours = analysis.peak_hours || [];
    
    const hourlyTotal = new Array(24).fill(0);
    const hourlyUrgent = new Array(24).fill(0);
    
    // Distribute emails across hours with peaks
    const baseEmailsPerHour = Math.floor(totalEmails / 12); // Spread across business hours
    const baseUrgentPerHour = Math.floor(urgentEmails / 12);
    
    // Add base distribution (9 AM to 9 PM)
    for (let hour = 9; hour < 21; hour++) {
        hourlyTotal[hour] = Math.max(1, baseEmailsPerHour + Math.floor(Math.random() * 3));
        hourlyUrgent[hour] = Math.max(0, baseUrgentPerHour + Math.floor(Math.random() * 2));
    }
    
    // Enhance peak hours
    peakHours.forEach(peakRange => {
        const match = peakRange.match(/(\d+):00-(\d+):00/);
        if (match) {
            const startHour = parseInt(match[1]);
            const endHour = parseInt(match[2]);
            for (let hour = startHour; hour < endHour; hour++) {
                hourlyTotal[hour] = Math.floor(hourlyTotal[hour] * 1.5);
                hourlyUrgent[hour] = Math.floor(hourlyUrgent[hour] * 1.3);
            }
        }
    });
    
    return {
        total: hourlyTotal,
        urgent: hourlyUrgent
    };
}

/**
 * Save analysis preferences
 */
function saveAnalysisPreferences(preferences) {
    localStorage.setItem('analysisPreferences', JSON.stringify(preferences));
}

/**
 * Schedule Page Functions
 */

/**
 * Load schedule preferences
 */
async function loadSchedulePreferences() {
    const savedPreferences = localStorage.getItem('schedulePreferences');
    if (savedPreferences) {
        const preferences = JSON.parse(savedPreferences);
        
        // Apply saved preferences to form
        Object.keys(preferences).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = preferences[key];
                } else {
                    element.value = preferences[key];
                }
            }
        });
    }
}

/**
 * Quick Action Functions
 */

/**
 * Set up quick action button listeners
 */
function setupQuickActionListeners() {
    // Request break button
    const requestBreakBtn = document.querySelector('[onclick*="requestBreak"]');
    if (requestBreakBtn) {
        requestBreakBtn.addEventListener('click', requestBreak);
    }
    
    // Add study session button
    const addSessionBtn = document.querySelector('[onclick*="addStudySession"]');
    if (addSessionBtn) {
        addSessionBtn.addEventListener('click', addStudySession);
    }
    
    // Send wellness nudge button
    const wellnessBtn = document.querySelector('[onclick*="sendWellnessNudge"]');
    if (wellnessBtn) {
        wellnessBtn.addEventListener('click', sendWellnessNudge);
    }
}

/**
 * Request break reminder
 */
async function requestBreak() {
    const btn = event.target.closest('button');
    const originalText = btn.innerHTML;
    
    // Show loading state
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/send_wellness_nudge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: 'break_reminder',
                recipient: 'current_user'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Break reminder sent! Take a 10-minute break to recharge. 🌟', 'success');
            
            // Show break suggestions modal
            showBreakSuggestionsModal();
        } else {
            showToast('Failed to send break reminder. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Error sending break reminder:', error);
        showToast('Error sending break reminder.', 'error');
    } finally {
        // Restore button
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

/**
 * Add study session to calendar
 */
async function addStudySession() {
    const now = new Date();
    const startTime = now.toTimeString().slice(0, 5);
    const endTime = new Date(now.getTime() + 90 * 60000).toTimeString().slice(0, 5);
    
    const confirmed = await showConfirmDialog(
        'Add Study Session',
        `Add a 90-minute study session from ${startTime} to ${endTime}?`,
        'Add Session'
    );
    
    if (confirmed) {
        showLoading();
        
        try {
            const response = await fetch('/api/send_calendar_event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: 'Study Session',
                    start_time: startTime,
                    end_time: endTime,
                    description: 'Optimized study session created by StudyBalance AI'
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast('Study session added to your calendar! 📅', 'success');
            } else {
                showToast('Failed to add study session to calendar.', 'error');
            }
        } catch (error) {
            console.error('Error adding study session:', error);
            showToast('Error adding study session.', 'error');
        } finally {
            hideLoading();
        }
    }
}

/**
 * Send wellness nudge
 */
async function sendWellnessNudge() {
    const nudgeTypes = [
        { value: 'motivation', label: '🚀 Motivation Boost', description: 'Get energized and motivated' },
        { value: 'hydration', label: '💧 Hydration Reminder', description: 'Stay hydrated for better focus' },
        { value: 'posture_check', label: '🪑 Posture Check', description: 'Take care of your body' },
        { value: 'eye_strain', label: '👀 Eye Care', description: 'Rest your eyes from screens' }
    ];
    
    const selectedType = await showSelectionDialog(
        'Choose Wellness Nudge',
        'What type of wellness reminder would you like?',
        nudgeTypes
    );
    
    if (selectedType) {
        showLoading();
        
        try {
            const response = await fetch('/api/send_wellness_nudge', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: selectedType,
                    recipient: 'current_user'
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast('Wellness nudge sent to your email! Check your inbox. 💚', 'success');
            } else {
                showToast('Failed to send wellness nudge.', 'error');
            }
        } catch (error) {
            console.error('Error sending wellness nudge:', error);
            showToast('Error sending wellness nudge.', 'error');
        } finally {
            hideLoading();
        }
    }
}

/**
 * UI Helper Functions
 */

/**
 * Show loading overlay
 */
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: type === 'error' ? 5000 : 3000
    });
    
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Get icon for toast type
 */
function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

/**
 * Update element content safely
 */
function updateElement(id, content) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = content;
    }
}

/**
 * Show confirmation dialog
 */
async function showConfirmDialog(title, message, confirmText = 'Confirm') {
    return new Promise((resolve) => {
        // Create modal HTML
        const modalHTML = `
            <div class="modal fade" id="confirmModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="confirmBtn">${confirmText}</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = document.getElementById('confirmModal');
        const bsModal = new bootstrap.Modal(modal);
        
        // Handle confirm button
        document.getElementById('confirmBtn').addEventListener('click', () => {
            bsModal.hide();
            resolve(true);
        });
        
        // Handle modal close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
            resolve(false);
        });
        
        bsModal.show();
    });
}

/**
 * Show selection dialog
 */
async function showSelectionDialog(title, message, options) {
    return new Promise((resolve) => {
        // Create modal HTML
        const optionsHTML = options.map(opt => `
            <div class="form-check mb-3">
                <input class="form-check-input" type="radio" name="selection" value="${opt.value}" id="option_${opt.value}">
                <label class="form-check-label" for="option_${opt.value}">
                    <strong>${opt.label}</strong><br>
                    <small class="text-muted">${opt.description}</small>
                </label>
            </div>
        `).join('');
        
        const modalHTML = `
            <div class="modal fade" id="selectionModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                            ${optionsHTML}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="selectBtn" disabled>Select</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = document.getElementById('selectionModal');
        const bsModal = new bootstrap.Modal(modal);
        const selectBtn = document.getElementById('selectBtn');
        
        // Handle radio button changes
        modal.addEventListener('change', (e) => {
            if (e.target.name === 'selection') {
                selectBtn.disabled = false;
            }
        });
        
        // Handle select button
        selectBtn.addEventListener('click', () => {
            const selected = modal.querySelector('input[name="selection"]:checked');
            bsModal.hide();
            resolve(selected ? selected.value : null);
        });
        
        // Handle modal close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
            resolve(null);
        });
        
        bsModal.show();
    });
}

/**
 * Show break suggestions modal
 */
function showBreakSuggestionsModal() {
    const suggestions = [
        { icon: 'walking', text: 'Take a 5-10 minute walk', color: 'success' },
        { icon: 'glass-water', text: 'Drink a glass of water', color: 'info' },
        { icon: 'eye', text: 'Rest your eyes (20-20-20 rule)', color: 'warning' },
        { icon: 'wind', text: 'Do some deep breathing exercises', color: 'primary' },
        { icon: 'stretch', text: 'Gentle stretching or yoga', color: 'purple' }
    ];
    
    const suggestionsHTML = suggestions.map(s => `
        <div class="suggestion-item">
            <div class="suggestion-icon bg-${s.color}">
                <i class="fas fa-${s.icon}"></i>
            </div>
            <span>${s.text}</span>
        </div>
    `).join('');
    
    const modalHTML = `
        <div class="modal fade" id="breakModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-pause text-primary me-2"></i>
                            Break Time Suggestions
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-4">Here are some great ways to spend your break:</p>
                        <div class="suggestions-list">
                            ${suggestionsHTML}
                        </div>
                        <div class="mt-4 p-3 bg-light rounded">
                            <small class="text-muted">
                                <i class="fas fa-lightbulb me-1"></i>
                                <strong>Tip:</strong> Even a 5-minute break can help reset your focus and reduce stress!
                            </small>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                            <i class="fas fa-check me-2"></i>Got it!
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            .suggestions-list {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .suggestion-item {
                display: flex;
                align-items: center;
                padding: 1rem;
                background: rgba(79, 70, 229, 0.05);
                border-radius: 0.75rem;
                border-left: 3px solid var(--primary-color);
                transition: all 0.3s ease;
            }
            
            .suggestion-item:hover {
                background: rgba(79, 70, 229, 0.1);
                transform: translateX(5px);
            }
            
            .suggestion-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                margin-right: 1rem;
                flex-shrink: 0;
            }
            
            .bg-purple {
                background-color: #8b5cf6 !important;
            }
        </style>
    `;
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = document.getElementById('breakModal');
    const bsModal = new bootstrap.Modal(modal);
    
    // Remove modal when hidden
    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
    });
    
    bsModal.show();
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + K for quick search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        // Implement quick search functionality
        showToast('Quick search coming soon!', 'info');
    }
    
    // Ctrl/Cmd + B for break reminder
    if ((event.ctrlKey || event.metaKey) && event.key === 'b') {
        event.preventDefault();
        requestBreak();
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay && loadingOverlay.style.display === 'flex') {
            hideLoading();
        }
    }
}

/**
 * Auto-refresh functionality
 */
function setupAutoRefresh() {
    // Refresh dashboard stats every 5 minutes
    if (getCurrentPage() === 'dashboard') {
        setInterval(loadDashboardData, 5 * 60 * 1000);
    }
    
    // Update time-based elements every minute
    setInterval(updateTimeElements, 60 * 1000);
}

/**
 * Update time-based elements
 */
function updateTimeElements() {
    const timeElements = document.querySelectorAll('[data-time]');
    timeElements.forEach(element => {
        const timestamp = element.getAttribute('data-time');
        if (timestamp) {
            element.textContent = formatTimeAgo(new Date(timestamp));
        }
    });
}

/**
 * Format time ago
 */
function formatTimeAgo(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
}

/**
 * Export functions for global access
 */
window.StudyBalanceAI = {
    startAnalysis,
    requestBreak,
    addStudySession,
    sendWellnessNudge,
    showLoading,
    hideLoading,
    showToast
};

// Analytics tracking (optional)
function trackEvent(eventName, properties = {}) {
    console.log('Event tracked:', eventName, properties);
    // You can integrate with analytics services here
}

// Performance monitoring
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log(`StudyBalance AI loaded in ${Math.round(loadTime)}ms`);
    trackEvent('app_loaded', { load_time: loadTime });
});

// Error handling for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('An unexpected error occurred. Please refresh the page.', 'error');
});

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}