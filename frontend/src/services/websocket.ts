// WebSocket 服务 - 支持真实连接和模拟模式
class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectTimer: number | null = null
  private listeners: Map<string, ((data: any) => void)[]> = new Map()
  
  public connected = false
  public mockMode = false

  // 连接到 WebSocket 服务器
  connect(url: string = 'ws://localhost:8000/ws') {
    if (this.mockMode) {
      console.log('🎭 当前处于模拟模式，无需连接')
      return
    }

    console.log('🚀 尝试连接 WebSocket:', url)
    
    try {
      this.ws = new WebSocket(url)
    } catch (error) {
      console.error('❌ 创建 WebSocket 失败:', error)
      alert('连接失败，请启用模拟模式进行测试')
      return
    }
    
    this.ws.onopen = () => {
      console.log('✅ WebSocket 连接成功')
      this.connected = true
      this.emit('connected', true)
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        console.log('📨 收到消息:', message)
        this.emit(message.event || 'message', message.data || message)
      } catch (error) {
        console.error('解析消息失败:', error)
      }
    }

    this.ws.onclose = (event) => {
      console.log(`🔌 WebSocket 断开 (code: ${event.code})`)
      this.connected = false
      this.emit('connected', false)
      
      // 自动重连
      if (!this.mockMode && event.code !== 1000) {
        this.reconnectTimer = window.setTimeout(() => {
          this.connect(url)
        }, 3000)
      }
    }

    this.ws.onerror = (error) => {
      console.error('❌ WebSocket 错误:', error)
    }
  }

  // 启用模拟模式
  enableMockMode() {
    console.log('🎭 启用模拟模式')
    this.mockMode = true
    this.connected = true
    this.emit('connected', true)
  }

  // 禁用模拟模式
  disableMockMode() {
    console.log('🛑 关闭模拟模式')
    this.mockMode = false
    this.connected = false
    this.emit('connected', false)
  }

  // 发送消息
  send(action: string, data?: any) {
    // 模拟模式：直接处理
    if (this.mockMode) {
      console.log('📤 模拟发送:', action, data)
      
      if (action === 'start_measurement') {
        // 模拟测量延迟
        setTimeout(() => {
          const mockData = {
            weight: 65.5 + (Math.random() * 4 - 2),  // 63.5-67.5kg
            body_fat_percent: 18.5 + (Math.random() * 4 - 2),  // 16.5-20.5%
            muscle_percent: 35.2 + (Math.random() * 2 - 1),
            water_percent: 55.0 + (Math.random() * 2 - 1),
            bone_mass: 2.8 + (Math.random() * 0.4 - 0.2),
            bmr: 1500 + Math.floor(Math.random() * 200 - 100),
            timestamp: new Date().toISOString()
          }
          console.log('📥 模拟收到数据:', mockData)
          this.emit('new_measurement', mockData)
        }, 2000)  // 2秒延迟模拟测量过程
      }
      return
    }

    // 真实模式：通过 WebSocket 发送
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action, ...data }))
    } else {
      console.warn('WebSocket 未连接')
      alert('设备未连接，请先连接设备或启用模拟模式')
    }
  }

  // 订阅事件
  on(event: string, callback: (data: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)?.push(callback)
  }

  // 取消订阅
  off(event: string, callback: (data: any) => void) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) callbacks.splice(index, 1)
    }
  }

  // 触发事件
  private emit(event: string, data: any) {
    const callbacks = this.listeners.get(event)
    callbacks?.forEach(cb => cb(data))
  }

  // 断开连接
  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
    }
    if (this.mockMode) {
      this.disableMockMode()
      return
    }
    this.ws?.close()
  }
}

// 单例模式导出
export const wsService = new WebSocketService()