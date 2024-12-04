function UploadFileProc() {
    // 文件上传处理
    document.getElementById('pdfFile').addEventListener('change', async function(e) {
        if (!this.files.length) return;
        
        const file = this.files[0];
        if (!file.name.endsWith('.pdf')) {
            alert('请上传PDF文件');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            updateStatus('正在上传文件...');
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            if (result.success) {
                document.getElementById('generateBtn').disabled = false;
                updateStatus('文件上传成功，可以开始生成');
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            alert('上传失败: ' + error.message);
            updateStatus('上传失败');
        }
    });

}