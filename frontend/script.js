document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const providerSelect = document.getElementById('provider-select');
    const instructionSelect = document.getElementById('instruction-select');
    const providerDescription = document.getElementById('provider-description');
    const instructionDescription = document.getElementById('instruction-description');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // State
    let selectedProvider = null;
    let selectedInstruction = null;
    let conversationId = null;
    
    // API base URL - adjust for production
    const API_BASE_URL = 'http://localhost:8000/api';
    
    // Load available providers and instructions
    async function loadConfigurations() {
        try {
            // Load providers
            const providersResponse = await fetch(`${API_BASE_URL}/providers`);
            const providers = await providersResponse.json();
            
            // Clear existing options
            providerSelect.innerHTML = '<option value="" disabled selected>Select a provider</option>';
            
            // Add options for each provider
            providers.forEach(provider => {
                const option = document.createElement('option');
                option.value = provider.id;
                option.textContent = provider.name;
                option.dataset.description = provider.description;
                providerSelect.appendChild(option);
            });
            
            // Load instruction sets
            const instructionsResponse = await fetch(`${API_BASE_URL}/instructions`);
            const instructions = await instructionsResponse.json();
            
            // Clear existing options
            instructionSelect.innerHTML = '<option value="" disabled selected>Select instructions</option>';
            
            // Add options for each instruction set
            instructions.forEach(instruction => {
                const option = document.createElement('option');
                option.value = instruction.id;
                option.textContent = instruction.name;
                option.dataset.description = instruction.description;
                instructionSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading configurations:', error);
            addSystemMessage('Error loading configurations. Please check if the server is running.');
        }
    }
    
    // Handle provider selection
    providerSelect.addEventListener('change', (e) => {
        selectedProvider = e.target.value;
        const selectedOption = providerSelect.options[providerSelect.selectedIndex];
        providerDescription.textContent = selectedOption.dataset.description;
        updateSendButtonState();
    });
    
    // Handle instruction selection
    instructionSelect.addEventListener('change', (e) => {
        selectedInstruction = e.target.value;
        const selectedOption = instructionSelect.options[instructionSelect.selectedIndex];
        instructionDescription.textContent = selectedOption.dataset.description;
        updateSendButtonState();
        
        // Reset conversation when changing configurations
        resetChat();
    });
    
    // Update send button state based on selections
    function updateSendButtonState() {
        sendButton.disabled = !(selectedProvider && selectedInstruction);
    }
    
    // Reset chat when configurations change
    function resetChat() {
        conversationId = null;
        chatMessages.innerHTML = '';
        
        // Add welcome message
        if (selectedProvider && selectedInstruction) {
            const providerName = providerSelect.options[providerSelect.selectedIndex].textContent;
            const instructionName = instructionSelect.options[instructionSelect.selectedIndex].textContent;
            addSystemMessage(`Using ${providerName} with the "${instructionName}" instruction set. Start chatting!`);
        } else {
            addSystemMessage('Select a provider and instruction set to begin chatting.');
        }
    }
    
    // Handle send button click
    sendButton.addEventListener('click', sendMessage);
    
    // Handle Enter key press
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send message to API
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message || !selectedProvider || !selectedInstruction) return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider_id: selectedProvider,
                    instruction_id: selectedInstruction,
                    message: message,
                    conversation_id: conversationId
                })
            });
            
            // Hide typing indicator
            hideTypingIndicator();
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            const data = await response.json();
            conversationId = data.conversation_id;
            
            // Add bot response to chat
            addBotMessage(data.response);
            
        } catch (error) {
            hideTypingIndicator();
            console.error('Error sending message:', error);
            addSystemMessage('Error communicating with the server. Please try again.');
        }
    }
    
    // Add user message to chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add bot message to chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        // Process markdown-like code blocks
        message = message.replace(/```([\s\S]*?)```/g, (match, code) => {
            return `<pre><code>${escapeHtml(code)}</code></pre>`;
        });
        
        messageElement.innerHTML = message;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add system message to chat
    function addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message system-message';
        messageElement.style.backgroundColor = '#fffde7';
        messageElement.style.border = '1px solid #fff9c4';
        messageElement.style.margin = '10px auto';
        messageElement.style.textAlign = 'center';
        messageElement.style.maxWidth = '100%';
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(indicator);
        scrollToBottom();
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    // Scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Helper to escape HTML in code blocks
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // Initialize
    loadConfigurations();
});