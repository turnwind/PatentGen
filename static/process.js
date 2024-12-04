const socket = io();
patentContent = null;

UploadFileProc();
PatentGenProc();
ExportFileProc();
SocketEventProc();

// 更新步骤显示
function updateSteps(steps) {
    const container = document.getElementById('stepsContent');
    if (!container) return;
    
    // 保留最后10个步骤
    const recentSteps = steps.slice(-10);
    
    container.innerHTML = '';
    
    recentSteps.forEach((step, index) => {
        const stepElement = document.createElement('div');
        stepElement.className = 'step-item' + (index === recentSteps.length - 1 ? ' active' : '');
        
        // 图标
        const iconSpan = document.createElement('span');
        iconSpan.className = 'codicon ' + (step.message.includes('完成') ? 'codicon-check' : 'codicon-sync');
        iconSpan.classList.add('step-icon');
        
        // 消息
        const messageSpan = document.createElement('span');
        messageSpan.className = 'step-message';
        messageSpan.textContent = step.message;
        
        // 时间
        const timeSpan = document.createElement('span');
        timeSpan.className = 'step-time';
        timeSpan.textContent = step.timestamp;
        
        stepElement.appendChild(iconSpan);
        stepElement.appendChild(messageSpan);
        stepElement.appendChild(timeSpan);
        container.appendChild(stepElement);
    });
    
    // 自动滚动到最新步骤
    container.scrollTop = container.scrollHeight;
}

// 更新状态栏
function updateStatus(message) {
    document.getElementById('statusBar').textContent = message;
}

// LLM对话框相关函数
function askLLM(type) {
    const message = document.getElementById(`${type}Editor`).value;
    socket.emit('ask_llm', { type, message });
}

function sendMessage() {
    const message = document.getElementById('chatInput').value;
    socket.emit('send_message', message);
    document.getElementById('chatInput').value = '';
}

socket.on('llm_response', (data) => {
    const messageElement = document.createElement('div');
    messageElement.className = 'message assistant';
    messageElement.textContent = data.message;
    document.getElementById('chatMessages').appendChild(messageElement);
});

socket.on('message', (data) => {
    const messageElement = document.createElement('div');
    messageElement.className = 'message user';
    messageElement.textContent = data.message;
    document.getElementById('chatMessages').appendChild(messageElement);
});