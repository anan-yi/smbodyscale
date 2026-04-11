<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          智能体重体脂分析仪
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          实时监测 · AI分析 · 健康管理
        </p>
        
        <div class="flex justify-center gap-4">
          <router-link 
            to="/measurement"
            class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
          >
            开始测量
            <svg class="ml-2 -mr-1 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- 功能介绍 -->
      <div class="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-blue-600 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 text-center mb-2">精准测量</h3>
          <p class="text-gray-500 text-center">通过STM32传感器实时采集体重、体脂、肌肉量等多项指标</p>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-purple-600 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 text-center mb-2">AI智能分析</h3>
          <p class="text-gray-500 text-center">基于DeepSeek大模型，提供个性化健康建议和改善方案</p>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-green-600 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 text-center mb-2">数据追踪</h3>
          <p class="text-gray-500 text-center">记录历史数据，可视化展示身体指标变化趋势</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 首页组件
</script>