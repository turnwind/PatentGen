import datetime

class EventEmitter:
    def __init__(self):
        self._socketio = None
        self._steps = []
        self._last_step = None
    
    def init_app(self, socketio):
        self._socketio = socketio
    
    def emit_step_update(self, step_data):
        if not self._socketio:
            print("Warning: SocketIO not initialized")
            return
            
        try:
            # 确保step_data包含所有必要字段
            if not isinstance(step_data, dict):
                step_data = {
                    'message': str(step_data),
                    'status': 'processing',
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # 添加必要的字段
            if 'status' not in step_data:
                step_data['status'] = 'processing'
            if 'timestamp' not in step_data:
                step_data['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
            # 更新上一步的状态为completed（除非是错误状态）
            if (self._last_step and 
                self._last_step.get('status') == 'processing' and 
                step_data.get('status') != 'error'):
                self._last_step['status'] = 'completed'
                self._socketio.emit('step_update', {'step': self._last_step})
            
            # 保存当前步骤
            self._steps.append(step_data)
            self._last_step = step_data
            
            # 发送当前步骤
            print(f"Emitting step update: {step_data}")  # 调试日志
            self._socketio.emit('step_update', {'step': step_data})
            
        except Exception as e:
            print(f"Error in emit_step_update: {str(e)}")
    
    def get_steps(self):
        """获取所有步骤"""
        return self._steps.copy()
    
    def clear_steps(self):
        """清除所有步骤"""
        self._steps = []
        self._last_step = None

# 创建全局事件发射器
event_emitter = EventEmitter()
