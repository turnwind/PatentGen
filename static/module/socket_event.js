function SocketEventProc() {
    // WebSocket事件处理
    socket.on('step_update', (data) => {
    const step = data.step;
    if (!step) return;
    
    console.log('Received step update:', step);  // 调试日志
    
    // 处理步骤更新
    const container = document.getElementById('stepsContent');
    if (container) {
        // 创建或更新步骤显示
        let stepElement = document.getElementById(`step-${step.message}`);
        if (!stepElement) {
            stepElement = document.createElement('div');
            stepElement.id = `step-${step.message}`;
            stepElement.className = 'step-item';
            container.appendChild(stepElement);
        }
        
        // 更新步骤状态
        stepElement.innerHTML = `
            <span class="step-icon codicon codicon-${step.status === 'completed' ? 'check' : 
                                                    step.status === 'error' ? 'error' : 'loading'}"></span>
            <span class="step-message">${step.message}</span>
            ${step.timestamp ? `<span class="step-time">${step.timestamp}</span>` : ''}
        `;
        
        // 设置状态类
        stepElement.className = `step-item ${step.status}`;
        
        // 滚动到底部
        container.scrollTop = container.scrollHeight;
    }
    
    // 处理内容更新
    if (step.type === 'content' && step.part && step.content) {
        console.log('Updating content:', step.part);  // 调试日志
        const editor = document.getElementById(`${step.part}Editor`);
        if (editor) {
            editor.value = step.content;
            
            // 更新专利内容对象
            if (!patentContent) patentContent = {};
            patentContent[step.part] = step.content;
            
            // 检查是否所有部分都已生成
            if (patentContent.abstract && patentContent.claims && patentContent.description) {
                document.getElementById('exportBtn').disabled = false;
            }
            
            // 触发编辑器的change事件
            const event = new Event('change');
            editor.dispatchEvent(event);
        }
    }
    
    // 更新状态栏
    if (step.message) {
        updateStatus(step.message);
    }
    });
    
    // 定期获取最新步骤
    setInterval(async () => {
        try {
            const response = await fetch('/get_steps');
            const data = await response.json();
            if (data.success) {
                updateSteps(data.steps);
            }
        } catch (error) {
            console.error('Error fetching steps:', error);
        }
    }, 1000);
}