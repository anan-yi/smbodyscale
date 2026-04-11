<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
    <div class="max-w-4xl mx-auto space-y-6">
      
      <!-- 头部 -->
      <header class="text-center py-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">智能体脂分析仪</h1>
        <p class="text-gray-600">实时监测 · AI分析 · 健康管理</p>
      </header>

      <!-- 连接状态 -->
      <div class="flex justify-center gap-4 mb-6 flex-wrap">
        <div 
          class="flex items-center gap-2 px-4 py-2 rounded-full bg-white shadow-sm cursor-pointer hover:shadow-md transition"
          @click="toggleConnection"
        >
          <span 
            class="w-3 h-3 rounded-full transition-colors duration-300"
            :class="connectionStatusClass"
          ></span>
          <span class="text-sm text-gray-600">{{ connectionStatusText }}</span>
        </div>
        
        <button
          v-if="!store.wsConnected"
          @click="toggleMockMode"
          class="flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 text-purple-700 hover:bg-purple-200 transition text-sm font-medium"
        >
          {{ isMockMode ? '关闭模拟' : '启用模拟' }}
        </button>
      </div>

      <!-- 测量数据卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- 体重 -->
        <div class="bg-white rounded-2xl p-6 shadow-lg transform hover:scale-105 transition-transform">
          <div class="flex items-center justify-between mb-4">
            <span class="text-gray-500 font-medium">体重</span>
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
            </svg>
          </div>
          <div class="text-3xl font-bold text-gray-800">
            {{ formatNumber(store.currentData.weight) }}
            <span class="text-lg text-gray-500 font-normal">kg</span>
          </div>
          <div v-if="store.currentData.weight" class="mt-2 text-sm text-green-600">✓ 已测量</div>
        </div>

        <!-- 体脂率 -->
        <div class="bg-white rounded-2xl p-6 shadow-lg">
          <div class="flex items-center justify-between mb-4">
            <span class="text-gray-500 font-medium">体脂率</span>
            <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </div>
          <div class="text-3xl font-bold text-gray-800">
            {{ formatNumber(store.currentData.body_fat_percent) }}
            <span class="text-lg text-gray-500 font-normal">%</span>
          </div>
          <div v-if="store.currentData.body_fat_percent" class="mt-2 text-sm" :class="fatStatusColor">
            {{ fatStatusText }}
          </div>
        </div>

        <!-- BMI -->
        <div class="bg-white rounded-2xl p-6 shadow-lg">
          <div class="flex items-center justify-between mb-4">
            <span class="text-gray-500 font-medium">BMI指数</span>
            <svg class="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <div class="text-3xl font-bold text-gray-800">
            {{ store.bmi || '--' }}
          </div>
          <div v-if="store.bmi" class="mt-2 text-sm" :class="bmiStatusColor">
            {{ store.weightStatus }}
          </div>
        </div>
      </div>

      <!-- 更多数据 -->
      <div v-if="hasDetailData" class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-4 shadow text-center">
          <div class="text-gray-500 text-sm mb-1">肌肉率</div>
          <div class="text-xl font-bold text-gray-800">{{ formatNumber(store.currentData.muscle_percent) }}%</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow text-center">
          <div class="text-gray-500 text-sm mb-1">水分率</div>
          <div class="text-xl font-bold text-gray-800">{{ formatNumber(store.currentData.water_percent) }}%</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow text-center">
          <div class="text-gray-500 text-sm mb-1">骨量</div>
          <div class="text-xl font-bold text-gray-800">{{ formatNumber(store.currentData.bone_mass) }}kg</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow text-center">
          <div class="text-gray-500 text-sm mb-1">基础代谢</div>
          <div class="text-xl font-bold text-gray-800">{{ formatNumber(store.currentData.bmr) }}kcal</div>
        </div>
      </div>

      <!-- 用户信息表单 -->
      <div class="bg-white rounded-2xl p-6 shadow-lg">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          个人信息
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">年龄</label>
            <input 
              v-model.number="store.userProfile.age" 
              type="number" 
              min="1"
              max="120"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="25"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
            <select 
              v-model="store.userProfile.gender"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            >
              <option value="male">男</option>
              <option value="female">女</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">身高 (cm)</label>
            <input 
              v-model.number="store.userProfile.height" 
              type="number" 
              min="50"
              max="250"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="170"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">目标体重 (kg, 可选)</label>
            <input 
              v-model.number="store.userProfile.target_weight" 
              type="number" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="65"
            >
          </div>
          
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">日常活动量</label>
            <div class="flex gap-2 flex-wrap">
              <label 
                v-for="level in activityLevels" 
                :key="level.value" 
                class="flex-1 min-w-[120px] cursor-pointer"
              >
                <input 
                  type="radio" 
                  :value="level.value" 
                  v-model="store.userProfile.activity_level"
                  class="hidden peer"
                >
                <div class="text-center p-3 rounded-lg border-2 border-gray-200 peer-checked:border-blue-500 peer-checked:bg-blue-50 transition">
                  <div class="font-medium text-gray-800 text-sm">{{ level.label }}</div>
                  <div class="text-xs text-gray-500 mt-1">{{ level.desc }}</div>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-4">
        <button 
          @click="startMeasurement"
          :disabled="!canStartMeasurement"
          class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-4 px-6 rounded-xl shadow-lg transform active:scale-95 transition-all flex items-center justify-center gap-2"
        >
          <svg v-if="store.isMeasuring" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          {{ store.isMeasuring ? '测量中...' : '开始测量' }}
        </button>
        
        <button 
          @click="requestAnalysis"
          :disabled="!store.canAnalyze || analyzing"
          class="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-4 px-6 rounded-xl shadow-lg transform active:scale-95 transition-all flex items-center justify-center gap-2"
        >
          <svg v-if="analyzing" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
          </svg>
          {{ analyzing ? 'AI分析中...' : '获取AI健康建议' }}
        </button>
      </div>

      <!-- AI分析结果 -->
      <div v-if="store.analysisResult" class="bg-white rounded-2xl p-6 shadow-lg border-l-4 border-purple-500 animate-fade-in">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
          AI健康分析报告
        </h2>
        
        <div class="space-y-4">
          <!-- 指标概览 -->
          <div class="grid grid-cols-3 gap-4 p-4 bg-gray-50 rounded-xl">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ store.bmi }}</div>
              <div class="text-xs text-gray-500">BMI</div>
              <div class="text-sm font-medium" :class="getStatusColor(store.weightStatus)">
                {{ store.weightStatus }}
              </div>
            </div>
            <div class="text-center border-l border-gray-200">
              <div class="text-2xl font-bold text-purple-600">{{ formatNumber(store.currentData.body_fat_percent) }}%</div>
              <div class="text-xs text-gray-500">体脂率</div>
              <div class="text-sm font-medium" :class="fatStatusColor">{{ fatStatusText }}</div>
            </div>
            <div class="text-center border-l border-gray-200">
              <div class="text-2xl font-bold text-green-600">{{ formatNumber(store.currentData.bmr) }}</div>
              <div class="text-xs text-gray-500">基础代谢</div>
              <div class="text-sm text-gray-600">kcal</div>
            </div>
          </div>

          <!-- AI建议 -->
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">综合评估</h3>
            <p class="text-gray-600 leading-relaxed">{{ store.analysisResult.summary }}</p>
            
            <h3 class="text-lg font-semibold text-gray-800 mb-2 mt-4">详细建议</h3>
            <div class="bg-purple-50 rounded-xl p-4 text-gray-700 leading-relaxed whitespace-pre-line text-sm">
              {{ store.analysisResult.full_analysis }}
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useMeasurementStore } from '../stores/measurement'
import { wsService } from '../services/websocket'

const store = useMeasurementStore()
const analyzing = ref(false)
const isMockMode = ref(false)

// 活动量选项
const activityLevels = [
  { value: 'sedentary', label: '久坐', desc: '办公室工作，极少运动' },
  { value: 'light', label: '轻度', desc: '每周轻度运动1-2次' },
  { value: 'moderate', label: '中度', desc: '每周中度运动3-5次' },
  { value: 'active', label: '活跃', desc: '每天运动或体力劳动' }
]

// 计算属性
const connectionStatusClass = computed(() => {
  if (isMockMode.value) return 'bg-purple-500 animate-pulse'
  if (store.wsConnected) return 'bg-green-500 animate-pulse'
  return 'bg-red-500'
})

const connectionStatusText = computed(() => {
  if (isMockMode.value) return '🎭 模拟模式'
  if (store.wsConnected) return '设备已连接'
  return '点击连接设备'
})

const canStartMeasurement = computed(() => {
  return (store.wsConnected || isMockMode.value) && !store.isMeasuring
})

const hasDetailData = computed(() => {
  return store.currentData.muscle_percent || 
         store.currentData.water_percent || 
         store.currentData.bone_mass || 
         store.currentData.bmr
})

const fatStatusText = computed(() => {
  const fat = store.currentData.body_fat_percent
  if (!fat) return ''
  const gender = store.userProfile.gender
  if (gender === 'male') {
    if (fat < 10) return '偏低'
    if (fat < 20) return '正常'
    if (fat < 25) return '偏高'
    return '过高'
  } else {
    if (fat < 20) return '偏低'
    if (fat < 30) return '正常'
    if (fat < 35) return '偏高'
    return '过高'
  }
})

const fatStatusColor = computed(() => {
  const text = fatStatusText.value
  if (text === '正常') return 'text-green-600'
  if (text === '偏低') return 'text-blue-600'
  return 'text-orange-600'
})

const bmiStatusColor = computed(() => {
  const text = store.weightStatus
  if (text === '正常') return 'text-green-600'
  if (text === '偏瘦') return 'text-blue-600'
  return 'text-orange-600'
})

// 方法
const formatNumber = (num: number | undefined, digits: number = 1) => {
  if (num === undefined || num === null) return '--'
  return num.toFixed(digits)
}

const toggleConnection = () => {
  if (store.wsConnected) {
    wsService.disconnect()
    isMockMode.value = false
  } else {
    wsService.connect()
  }
}

const toggleMockMode = () => {
  if (isMockMode.value) {
    wsService.disableMockMode()
    isMockMode.value = false
    store.wsConnected = false
  } else {
    wsService.enableMockMode()
    isMockMode.value = true
    store.wsConnected = true
  }
}

const startMeasurement = () => {
  if (!store.wsConnected && !isMockMode.value) {
    alert('请先连接设备或启用模拟模式')
    return
  }
  
  store.isMeasuring = true
  store.clearData()
  store.analysisResult = null
  
  wsService.send('start_measurement')
}

const requestAnalysis = async () => {
  if (!store.canAnalyze) {
    alert('请先完成测量并填写个人信息')
    return
  }
  
  analyzing.value = true
  
  // 模拟模式
  if (isMockMode.value) {
    setTimeout(() => {
      const mockResult = generateMockAnalysis()
      store.setAnalysisResult(mockResult)
      analyzing.value = false
    }, 1500)
    return
  }
  
  // 真实API调用
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        measurement: store.currentData,
        user: store.userProfile
      })
    })
    
    if (!response.ok) throw new Error('分析请求失败')
    
    const result = await response.json()
    store.setAnalysisResult(result)
  } catch (error) {
    console.error('分析失败:', error)
    alert('分析失败，请检查后端服务或启用模拟模式')
  } finally {
    analyzing.value = false
  }
}

const generateMockAnalysis = () => {
  const bmi = parseFloat(store.bmi || '0')
  let summary = ''
  let analysis = ''
  
  if (bmi < 18.5) {
    summary = '您的体重偏轻，建议适当增加营养摄入。'
    analysis = '根据您的身体数据，BMI指数显示体重偏轻。建议：\n1. 增加蛋白质摄入，多吃瘦肉、鸡蛋、牛奶\n2. 适当进行力量训练，增加肌肉量\n3. 保证充足睡眠，促进身体恢复\n4. 定期监测体重变化，每周增重0.5kg为宜'
  } else if (bmi < 24) {
    summary = '您的体重在正常范围内，保持良好的生活习惯。'
    analysis = '恭喜！您的身体指标处于健康范围。建议：\n1. 继续保持均衡饮食，多吃蔬菜水果\n2. 每周进行3-5次有氧运动，每次30分钟\n3. 注意体脂率变化，适当进行力量训练\n4. 定期测量，追踪身体数据趋势'
  } else {
    summary = '您的体重偏重，建议适当控制饮食并增加运动。'
    analysis = '根据分析，您的BMI指数略高。建议：\n1. 控制热量摄入，减少高糖高脂食物\n2. 增加有氧运动，如慢跑、游泳、骑车\n3. 每周运动4-5次，每次45分钟以上\n4. 多喝水，保证充足睡眠\n5. 设定合理目标，每月减重2-4kg'
  }
  
  return {
    summary,
    full_analysis: analysis
  }
}

const getStatusColor = (status: string) => {
  if (status.includes('正常')) return 'text-green-600'
  if (status.includes('偏')) return 'text-blue-600'
  return 'text-orange-600'
}

// 生命周期
onMounted(() => {
  wsService.on('connected', (connected: boolean) => {
    store.wsConnected = connected
  })
  
  wsService.on('new_measurement', (data: any) => {
    store.setMeasurementData(data)
    store.isMeasuring = false
  })
})

onUnmounted(() => {
  wsService.disconnect()
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>