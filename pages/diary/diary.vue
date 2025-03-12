<template>
  <view class="diary-container">
    <view class="header">
      <view class="back-button" @click="goBack">
        <text class="iconfont">返回</text>
      </view>
      <text class="title">识别日志</text>
    </view>

    <view class="content">
      <!-- 顶部统计卡片 -->
      <view class="stats-card">
        <text class="stats-title">识别记录</text>
        <text class="stats-count">共 {{ logs.length }} 条</text>
      </view>

      <!-- 日志列表 -->
      <view class="logs-list" v-if="logs.length">
        <view 
          class="log-card" 
          v-for="(log, index) in logs" 
          :key="log._id"
          :style="{ animationDelay: index * 0.1 + 's' }"
        >
          <view class="log-content">
            <text class="log-text">{{ log.result || '无识别结果' }}</text>
            <view class="log-meta">
              <text class="log-time">{{ formatDateTime(log.created) }}</text>
            </view>
          </view>
          <view class="log-indicator"></view>
        </view>
      </view>

      <!-- 空状态 -->
      <view class="empty-state" v-else>
        <image class="empty-icon" src="https://mp-cb3abd12-6ea4-42d8-9f4d-57d803f8e395.cdn.bspapp.com/1741760455330wc92zo98.jpg" mode="aspectFit"></image>
        <text class="empty-text">暂无识别记录</text>
        <button class="refresh-btn" @click="fetchRecognitionLogs">刷新试试</button>
      </view>
    </view>

    <!-- 加载动画 -->
    <view class="loading-overlay" v-if="isLoading">
      <view class="loading-spinner"></view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      logs: [],
      isLoading: false
    };
  },
  onLoad() {
    this.fetchRecognitionLogs();
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    async fetchRecognitionLogs() {
      this.isLoading = true;
      try {
        const db = uniCloud.database();
        const res = await db.collection('recognition_logs')
          .orderBy('created', 'desc')
          .get();
        
        this.logs = res.result.data;
      } catch (error) {
        console.error('获取日志失败:', error);
        uni.showToast({
          title: '获取日志失败',
          icon: 'none'
        });
      } finally {
        this.isLoading = false;
      }
    },
    formatDateTime(timestamp) {
      if (!timestamp) return '未知时间';
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
  }
};
</script>

<style scoped>
.diary-container {
  min-height: 100vh;
  
  background: #f8f9fa;
  padding-bottom: env(safe-area-inset-bottom);
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 88rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.back-button {
  position: absolute;
  left: 30rpx;
  height: 88rpx;
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: #2196F3;
}

.title {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
}

.content {
  padding: 108rpx 32rpx 40rpx;
}

.stats-card {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  padding: 40rpx;
  border-radius: 24rpx;
  color: white;
  margin-bottom: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(33, 150, 243, 0.2);
  animation: fadeInDown 0.6s ease-out;
}

.stats-title {
  font-size: 28rpx;
  opacity: 0.9;
}

.stats-count {
  display: block;
  font-size: 48rpx;
  font-weight: 600;
  margin-top: 16rpx;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.log-card {
  background: white;
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  position: relative;
  animation: slideIn 0.6s ease-out forwards;
  opacity: 0;
  transform: translateX(-20rpx);
}

.log-content {
  flex: 1;
}

.log-text {
  font-size: 32rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.log-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.log-time {
  font-size: 24rpx;
  color: #999;
}

.log-indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6rpx;
  background: #2196F3;
  border-radius: 6rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 0;
  animation: fadeIn 0.6s ease-out;
}

.empty-icon {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 32rpx;
  opacity: 0.5;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 32rpx;
}

.refresh-btn {
  background: #2196F3;
  color: white;
  padding: 16rpx 48rpx;
  border-radius: 100rpx;
  font-size: 28rpx;
  border: none;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.loading-spinner {
  width: 60rpx;
  height: 60rpx;
  border: 4rpx solid #f3f3f3;
  border-top: 4rpx solid #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 添加悬浮效果 */
.log-card {
  transition: all 0.3s ease;
}

.log-card:active {
  transform: scale(0.98);
}

/* 添加渐变背景动画 */
.stats-card {
  background-size: 200% 200%;
  animation: gradientMove 6s ease infinite;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
