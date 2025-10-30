// AI Startup Framework - Interactive Script

class AIStartupFramework {
    constructor() {
        this.currentStage = 'conversation';
        this.progress = 0;
        this.userIdea = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateAIContext('Ready to help you build your startup');
        this.animateProgressBar();
        this.setupStageNavigation();
    }

    setupEventListeners() {
        // Input handling
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        
        if (userInput && sendBtn) {
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.processUserInput();
                }
            });
            
            sendBtn.addEventListener('click', () => {
                this.processUserInput();
            });
        }

        // Suggestion items
        const suggestions = document.querySelectorAll('.suggestion-item');
        suggestions.forEach(item => {
            item.addEventListener('click', () => {
                const text = item.getAttribute('data-text');
                document.getElementById('user-input').value = text;
                this.processUserInput();
            });
        });

        // Button interactions
        this.setupButtonInteractions();
    }

    setupButtonInteractions() {
        // Action buttons
        document.querySelectorAll('.btn-primary, .btn-secondary, .btn-action').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const buttonText = e.target.textContent;
                this.handleButtonAction(buttonText);
            });
        });

        // AI Orchestrator buttons
        document.querySelectorAll('.btn-link').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.textContent;
                this.handleOrchestratorAction(action);
            });
        });
    }

    setupStageNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const stage = btn.getAttribute('data-stage');
                this.switchStage(stage);
                
                // Update active state
                navButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    switchStage(stage) {
        // Hide all stages
        document.querySelectorAll('.stage').forEach(s => s.classList.remove('active'));
        
        // Show target stage
        const targetStage = document.getElementById(`${stage}-stage`);
        if (targetStage) {
            targetStage.classList.add('active');
        } else {
            // For stages not yet implemented, show canvas
            document.getElementById('canvas-stage').classList.add('active');
        }
        
        this.currentStage = stage;
        this.updateContextForStage(stage);
    }

    updateContextForStage(stage) {
        const contextMessages = {
            'conversation': 'Ready to help you build your startup',
            'canvas': 'Analyzing your startup across all playbooks',
            'customer-focus': 'Deep diving into customer discovery',
            'command-center': 'Mission control for your startup'
        };

        this.updateAIContext(contextMessages[stage] || 'AI analysis in progress...');
    }

    processUserInput() {
        const input = document.getElementById('user-input');
        const userMessage = input.value.trim();
        
        if (!userMessage) return;

        this.userIdea = userMessage;
        this.addMessageToHistory('user', userMessage);
        
        // Clear input
        input.value = '';
        
        // Simulate AI processing
        setTimeout(() => {
            this.simulateAIResponse(userMessage);
        }, 1000);
    }

    addMessageToHistory(type, message) {
        const messageHistory = document.getElementById('message-history');
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        
        if (type === 'user') {
            messageDiv.innerHTML = `
                <div class="user-avatar">👤</div>
                <div class="message-content">
                    <p>${message}</p>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="ai-avatar">🤖</div>
                <div class="message-content">
                    <p>${message}</p>
                </div>
            `;
        }
        
        messageHistory.appendChild(messageDiv);
        messageHistory.scrollTop = messageHistory.scrollHeight;
    }

    simulateAIResponse(userMessage) {
        // Simulate AI analysis
        this.updateAIContext('Analyzing your idea...');
        
        // Generate contextual response
        const responses = [
            `Excellent! "${userMessage}" addresses a real market need. I'm analyzing 47 similar startups and market data...`,
            `Interesting concept! Let me break this down into our framework. I see potential in 3 key areas...`,
            `Great timing for this idea! The market conditions are favorable. Let me generate your startup blueprint...`
        ];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        this.addMessageToHistory('ai', randomResponse);
        
        // Transition to canvas after response
        setTimeout(() => {
            this.transitionToCanvas();
        }, 2000);
    }

    transitionToCanvas() {
        // Update progress
        this.progress = 25;
        this.updateProgress();
        
        // Update AI context
        this.updateAIContext('Generating your startup blueprint...');
        
        // Switch to canvas stage
        this.switchStage('canvas');
        
        // Update vision statement
        if (this.userIdea) {
            document.getElementById('vision-statement').textContent = `"${this.userIdea}"`;
        }
        
        // Animate cards appearing
        this.animateCardAppearance();
        
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-stage') === 'canvas') {
                btn.classList.add('active');
            }
        });
    }

    animateCardAppearance() {
        const cards = document.querySelectorAll('.playbook-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    handleButtonAction(buttonText) {
        const actions = {
            'Dive Deeper': () => this.diveDeeper(),
            'Schedule Interview': () => this.scheduleInterview(),
            'Validate Pricing': () => this.validatePricing(),
            'Explore Models': () => this.exploreModels()
        };

        if (actions[buttonText]) {
            actions[buttonText]();
        }
    }

    diveDeeper() {
        this.updateAIContext('Analyzing customer feedback patterns...');
        this.showNotification('🔍 Deep analysis initiated. Reviewing 15 customer interviews...', 'info');
        
        // Simulate analysis results
        setTimeout(() => {
            this.updateCustomerInsights();
        }, 2000);
    }

    scheduleInterview() {
        this.updateAIContext('Optimizing interview schedule...');
        this.showNotification('📅 Interview scheduled! I\'ve prepared 12 targeted questions.', 'success');
    }

    validatePricing() {
        this.updateAIContext('Running pricing validation analysis...');
        this.showNotification('💰 Pricing analysis in progress. Comparing with 23 similar startups...', 'info');
        
        setTimeout(() => {
            this.updatePricingInsights();
        }, 2000);
    }

    exploreModels() {
        this.updateAIContext('Exploring revenue model alternatives...');
        this.showNotification('🔄 Generated 5 alternative revenue models for your review.', 'info');
    }

    updateCustomerInsights() {
        const customerCard = document.getElementById('customer-card');
        const aiInsight = customerCard.querySelector('.ai-insight');
        
        aiInsight.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <span>✨ NEW INSIGHT: 78% of parents prefer simple interfaces. Consider simplifying your design.</span>
        `;
        aiInsight.className = 'ai-insight';
        
        this.progress = 45;
        this.updateProgress();
    }

    updatePricingInsights() {
        const businessCard = document.getElementById('business-card');
        const aiInsight = businessCard.querySelector('.ai-insight');
        
        aiInsight.innerHTML = `
            <i class="fas fa-chart-line"></i>
            <span>📊 RECOMMENDATION: $15/month optimal price point based on customer feedback.</span>
        `;
        aiInsight.className = 'ai-insight';
        
        // Update revenue amount
        const revenueAmount = businessCard.querySelector('.revenue-amount');
        revenueAmount.textContent = '$15/month';
        
        this.progress = 60;
        this.updateProgress();
    }

    handleOrchestratorAction(action) {
        const actionHandlers = {
            'Align Now': () => this.alignPlaybooks(),
            'Review Changes': () => this.reviewChanges(),
            'See Analysis': () => this.seeAnalysis()
        };

        if (actionHandlers[action]) {
            actionHandlers[action]();
        }
    }

    alignPlaybooks() {
        this.updateAIContext('Aligning playbook inconsistencies...');
        this.showNotification('🔧 Alignment complete! All playbooks are now synchronized.', 'success');
        
        // Update orchestrator
        this.updateOrchestratorInsights();
    }

    reviewChanges() {
        this.updateAIContext('Reviewing suggested changes...');
        this.showNotification('📋 Change review initiated. Prioritizing 8 key updates.', 'info');
    }

    seeAnalysis() {
        this.updateAIContext('Displaying market analysis...');
        this.showNotification('📈 Market analysis complete. Opportunity score: 89%', 'success');
    }

    updateOrchestratorInsights() {
        const orchestratorContent = document.querySelector('.orchestrator-content');
        orchestratorContent.innerHTML = `
            <div class="insight-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>All playbooks are aligned and consistent</span>
                <button class="btn-link">View Details</button>
            </div>
            <div class="insight-item">
                <i class="fas fa-trending-up text-info"></i>
                <span>Market opportunity increased to 94%</span>
                <button class="btn-link">See Trends</button>
            </div>
            <div class="insight-item">
                <i class="fas fa-lightbulb text-warning"></i>
                <span>New partnership opportunity detected</span>
                <button class="btn-link">Explore</button>
            </div>
        `;
        
        // Re-setup button listeners
        this.setupButtonInteractions();
    }

    updateAIContext(message) {
        const contextText = document.getElementById('ai-context-text');
        if (contextText) {
            contextText.textContent = message;
        }
    }

    updateProgress() {
        const progressFill = document.getElementById('overall-progress');
        const progressText = document.getElementById('progress-text');
        
        if (progressFill && progressText) {
            progressFill.style.width = `${this.progress}%`;
            progressText.textContent = `${this.progress}% Complete`;
        }
    }

    animateProgressBar() {
        // Simulate gradual progress increase
        let currentProgress = 0;
        const interval = setInterval(() => {
            currentProgress += 1;
            if (currentProgress >= this.progress) {
                clearInterval(interval);
            } else {
                const progressFill = document.getElementById('overall-progress');
                if (progressFill) {
                    progressFill.style.width = `${currentProgress}%`;
                }
            }
        }, 50);
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="close-btn">&times;</button>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            max-width: 400px;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            z-index: 1001;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'info' ? '#6366f1' : '#f59e0b'};
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Setup close button
        const closeBtn = notification.querySelector('.close-btn');
        closeBtn.addEventListener('click', () => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (document.body.contains(notification)) {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }
        }, 5000);
    }

    // Simulate real-time updates
    startRealTimeUpdates() {
        setInterval(() => {
            this.simulateMetricUpdates();
        }, 10000); // Update every 10 seconds
    }

    simulateMetricUpdates() {
        // Randomly update metrics to show dynamism
        const metrics = document.querySelectorAll('.metric-value');
        metrics.forEach(metric => {
            const currentValue = metric.textContent;
            if (currentValue.includes('%')) {
                const numValue = parseInt(currentValue);
                const newValue = Math.min(100, numValue + Math.floor(Math.random() * 3));
                metric.textContent = `${newValue}%`;
            }
        });
    }
}

// Initialize the framework when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const framework = new AIStartupFramework();
    framework.startRealTimeUpdates();
});

// Add some CSS for notifications via JavaScript
const style = document.createElement('style');
style.textContent = `
    .notification {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .notification .close-btn {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: #6b7280;
        margin-left: 1rem;
    }
    
    .notification .close-btn:hover {
        color: #374151;
    }
    
    .user-message {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        justify-content: flex-end;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        background: #6366f1;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .user-message .message-content {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 12px;
        max-width: 70%;
    }
`;
document.head.appendChild(style); 