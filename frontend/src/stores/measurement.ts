import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface MeasurementData {
  weight?: number
  body_fat_percent?: number
  muscle_percent?: number
  water_percent?: number
  bone_mass?: number
  bmr?: number
  timestamp?: string
}

export interface UserProfile {
  age: number
  gender: 'male' | 'female'
  height: number
  target_weight?: number
  activity_level: 'sedentary' | 'light' | 'moderate' | 'active'
}

export const useMeasurementStore = defineStore('measurement', () => {
  // 状态
  const currentData = ref<MeasurementData>({})
  const userProfile = ref<UserProfile>({
    age: 25,
    gender: 'male',
    height: 170,
    activity_level: 'moderate',
  })
  const isMeasuring = ref(false)
  const wsConnected = ref(false)
  const analysisResult = ref<any>(null)

  // 计算属性
  const bmi = computed(() => {
    if (!currentData.value.weight || !userProfile.value.height) return null
    const heightM = userProfile.value.height / 100
    return (currentData.value.weight / (heightM * heightM)).toFixed(1)
  })

  const canAnalyze = computed(() => {
    return currentData.value.weight && userProfile.value.age && userProfile.value.height
  })

  const weightStatus = computed(() => {
    const val = parseFloat(bmi.value || '0')
    if (val === 0) return ''
    if (val < 18.5) return '偏瘦'
    if (val < 24) return '正常'
    if (val < 28) return '超重'
    return '肥胖'
  })

  // 方法
  function setMeasurementData(data: MeasurementData) {
    currentData.value = { ...currentData.value, ...data }
  }

  function clearData() {
    currentData.value = {}
    analysisResult.value = null
  }

  function updateUserProfile(profile: Partial<UserProfile>) {
    userProfile.value = { ...userProfile.value, ...profile }
  }

  function setAnalysisResult(result: any) {
    analysisResult.value = result
  }

  return {
    currentData,
    userProfile,
    isMeasuring,
    wsConnected,
    analysisResult,
    bmi,
    canAnalyze,
    weightStatus,
    setMeasurementData,
    clearData,
    updateUserProfile,
    setAnalysisResult,
  }
})