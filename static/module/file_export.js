function ExportFileProc() {
   // 导出Word文档
    document.getElementById('exportBtn').addEventListener('click', async function() {
        if (!patentContent) return;
        
        try {
            updateStatus('正在导出Word文档...');
            const response = await fetch('/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(patentContent)
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'patent.docx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                updateStatus('Word文档导出完成');
            } else {
                throw new Error('导出失败');
            }
        } catch (error) {
            alert('导出失败: ' + error.message);
            updateStatus('导出失败');
        }
    });
}