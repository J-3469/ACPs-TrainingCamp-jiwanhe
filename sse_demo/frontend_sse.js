/**
 * SSE 客户端实现 - 替代轮询的核心代码
 * 展示如何使用 EventSource API 接收服务器推送的事件
 */

// 核心函数：建立 SSE 连接
function startSSE(sessionId, taskId) {
    // 1. 创建 EventSource 实例，连接到 SSE 端点
    const eventSource = new EventSource(`/api/events/${sessionId}?taskId=${taskId}`);
    
    // 2. 处理服务器推送的消息
    eventSource.addEventListener('message', (event) => {
        try {
            const result = JSON.parse(event.data);
            // 处理任务状态更新（替代轮询的核心逻辑）
            updateTaskStatus(result);
        } catch (error) {
            console.error('SSE 消息解析错误:', error);
        }
    });
    
    // 3. 处理完成事件
    eventSource.addEventListener('complete', () => {
        console.log('任务完成，关闭 SSE 连接');
        eventSource.close();
    });
    
    // 4. 处理错误事件
    eventSource.addEventListener('error', (event) => {
        if (event.readyState === EventSource.CLOSED) {
            console.log('SSE 连接已关闭');
        } else {
            console.error('SSE 错误:', event);
        }
    });
    
    return eventSource;
}

// 处理任务状态更新
function updateTaskStatus(result) {
    console.log('收到任务状态更新:', result);
    // 这里可以添加 UI 更新逻辑
    // 例如：更新状态显示、进度条等
}

// 对比：轮询实现
/*
function startPolling(sessionId, taskId) {
    let pollCount = 0;
    const MAX_POLLS = 60;
    
    function poll() {
        if (pollCount >= MAX_POLLS) {
            console.log('轮询达到最大次数');
            return;
        }
        
        pollCount++;
        fetch(`/api/result/${sessionId}?taskId=${taskId}`)
            .then(response => response.json())
            .then(result => {
                updateTaskStatus(result);
                // 继续轮询
                setTimeout(poll, 1000);
            })
            .catch(error => {
                console.error('轮询错误:', error);
                setTimeout(poll, 1000);
            });
    }
    
    poll();
}
*/

console.log('SSE 客户端代码示例 - 替代轮询');