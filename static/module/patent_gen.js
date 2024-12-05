function PatentGenProc() {
    // 生成专利文档
    document.getElementById('generateBtn').addEventListener('click', async function() {
        try {
            this.disabled = true;
            updateStatus('正在生成专利文档...');
            result = {
                'abstract': '',
                'claims': '',
                'description': ''
            }
            // 生成专利摘要
            const abstractResponse = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ step: 'abstract' })
            });
            const abstractResult = await abstractResponse.json();
            if (abstractResult.success) {
                document.getElementById('abstractEditor').value = abstractResult.content;
                result['abstract'] = abstractResult.content;
                updateStatus('专利摘要生成完成');
            }

            // 生成专利权利要求
            const claimsResponse = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ step: 'claims' })
            });
            const claimsResult = await claimsResponse.json();
            if (claimsResult.success) {
                document.getElementById('claimsEditor').value = claimsResult.content;
                result['claims'] = claimsResult.content;
                updateStatus('专利权利要求生成完成');
            }

            // 生成专利描述
            const descriptionResponse = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ step: 'description' })
            });
            const descriptionResult = await descriptionResponse.json();
            if (descriptionResult.success) {
                document.getElementById('descriptionEditor').value = descriptionResult.content;
                result['description'] = descriptionResult.content;
                updateStatus('专利描述生成完成');
            }

            if (result.abstract!=null && result.claims!=null && result.description!=null) {
                patentContent = result;
                document.getElementById('exportBtn').disabled = false;
                updateStatus('专利文档生成完成');
            } else {
                throw new Error(result.error);
            }

        } catch (error) {
            alert('生成失败: ' + error.message);
            updateStatus('生成失败');
        } finally {
            this.disabled = false;
        }
    });
}