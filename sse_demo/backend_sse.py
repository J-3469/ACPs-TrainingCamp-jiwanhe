"""
SSE 服务端实现 - 替代轮询的核心代码
展示如何使用 FastAPI 实现 SSE 端点，推送任务状态
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

# 模拟任务状态
task_status = {
    "sessionId": "session_123",
    "taskId": "task_456",
    "status": "pending",  # pending, running, completed, failed
    "progress": 0,
    "result": None
}

# 模拟任务处理
async def process_task():
    """模拟任务处理过程，更新状态"""
    global task_status
    task_status["status"] = "running"
    for i in range(1, 101):
        await asyncio.sleep(0.5)
        task_status["progress"] = i
        if i == 100:
            task_status["status"] = "completed"
            task_status["result"] = "任务处理完成！"

@app.post("/api/start-task")
async def start_task():
    """启动任务处理"""
    asyncio.create_task(process_task())
    return {"sessionId": task_status["sessionId"], "taskId": task_status["taskId"]}

@app.get("/api/events/{session_id}")
async def events(session_id: str, taskId: str = None):
    """SSE 端点 - 推送任务状态"""
    async def event_generator():
        while True:
            # 1. 发送任务状态（SSE 的核心：服务器主动推送）
            yield f"data: {json.dumps(task_status)}\n\n"
            
            # 2. 如果任务完成，发送完成事件并退出
            if task_status["status"] in ["completed", "failed"]:
                yield "event: complete\n\n"
                break
            
            # 3. 短暂延迟，避免推送过快
            await asyncio.sleep(0.5)
    
    # 返回 StreamingResponse，媒体类型为 text/event-stream
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# 对比：传统轮询的后端端点（注释掉，仅作对比）
"""
@app.get("/api/result/{session_id}")
async def get_result(session_id: str, taskId: str = None):
    \"\"\"轮询端点 - 被动响应状态查询\"\"\"
    return task_status
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)