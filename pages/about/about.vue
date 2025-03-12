<template>
  <view class="about-container">
    <view class="header">

      <text class="title">关于我们</text>
    </view>

    <view class="content">
      <!-- Logo区域 -->
      <view class="logo-section">
        <image class="team-logo" src="https://mp-cb3abd12-6ea4-42d8-9f4d-57d803f8e395.cdn.bspapp.com/1741760455330wc92zo98.jpg" mode="aspectFit"></image>
        <text class="team-name">手语识别团队</text>
        <text class="slogan">让手语交流更便捷，让温暖传递更远</text>
      </view>

      <!-- 使命愿景 -->
      <view class="mission-section">
        <text class="section-title">我们的使命</text>
        <view class="mission-card">
          <text class="mission-text">致力于通过技术创新，打破交流障碍，让每个手势都能被理解，让每个故事都能被倾听。</text>
        </view>
      </view>

      <!-- 团队成员 -->
      <view class="team-section">
        <text class="section-title">核心团队</text>
        <view class="team-members">
          <view class="member-card">
            <view class="member-avatar">
              <text class="member-initial">S</text>
            </view>
            <view class="member-info">
              <text class="member-name">孙晨雨</text>
              <text class="member-role">手语识别算法</text>
              <text class="member-desc">机器深度学习</text>
            </view>
          </view>

          <view class="member-card">
            <view class="member-avatar">
              <text class="member-initial">P</text>
            </view>
            <view class="member-info">
              <text class="member-name">彭振彦</text>
              <text class="member-role">手语识别算法</text>
              <text class="member-desc">模型优化</text>
            </view>
          </view>

          <view class="member-card">
            <view class="member-avatar">
              <text class="member-initial">L</text>
            </view>
            <view class="member-info">
              <text class="member-name">罗荣怀</text>
              <text class="member-role">全栈开发</text>
              <text class="member-desc">应用架构</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 联系我们 -->
      <view class="contact-section">
        <text class="contact-title">联系我们</text>
        <view class="contact-card" @click="copyEmail">
          <text class="contact-text">1355178356@qq.com</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  },
  methods: {
    goBack() {
      uni.navigateTo({
      	url:"/pages/firstShow/firstShow"
      })
    },
    copyEmail() {
      uni.setClipboardData({
        data: '1355178356@qq.com',
        success: () => {
          uni.showToast({
            title: '邮箱已复制',
            icon: 'none'
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.about-container {
  min-height: 100vh;
  background: #f8f9fa;
  padding-bottom: 40rpx;
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
  width: 88rpx;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
}

.content {
  padding: 128rpx 32rpx 40rpx;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;
}

.team-logo {
  width: 180rpx;
  height: 180rpx;
  margin-bottom: 24rpx;
  border-radius: 36rpx;
  background: linear-gradient(135deg, #2196F3, #1976D2);
  box-shadow: 0 8rpx 24rpx rgba(33, 150, 243, 0.2);
}

.team-name {
  font-size: 40rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 16rpx;
}

.slogan {
  font-size: 28rpx;
  color: #666;
  text-align: center;
}

.mission-section {
  margin-bottom: 60rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 24rpx;
  padding-left: 24rpx;
  border-left: 8rpx solid #2196F3;
}

.mission-card {
  background: white;
  padding: 32rpx;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.mission-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.team-section {
  margin-bottom: 60rpx;
}

.team-members {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.member-card {
  background: white;
  padding: 24rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.member-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 44rpx;
  background: linear-gradient(135deg, #2196F3, #1976D2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
}

.member-initial {
  color: white;
  font-size: 36rpx;
  font-weight: 600;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 8rpx;
}

.member-role {
	margin-left: 10rpx;
  font-size: 26rpx;
  color: #2196F3;
  margin-bottom: 8rpx;
}

.member-desc {
	margin-left: 20rpx;
  font-size: 24rpx;
  color: #666;
}

.contact-section {
  margin-top: 80rpx;
}

.contact-title {
  font-size: 28rpx;
  color: #999;
  text-align: center;
  margin-bottom: 16rpx;
}

.contact-card {
  background: white;
  padding: 24rpx;
  border-radius: 16rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.contact-text {
  font-size: 28rpx;
  color: #2196F3;
}

/* 动画效果 */
.member-card {
  transition: all 0.3s ease;
}

.member-card:active {
  transform: scale(0.98);
}

.member-avatar {
  transition: all 0.3s ease;
}

.member-card:active .member-avatar {
  transform: rotate(5deg);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content > view {
  animation: fadeIn 0.6s ease-out forwards;
  opacity: 0;
}

.content > view:nth-child(1) { animation-delay: 0.1s; }
.content > view:nth-child(2) { animation-delay: 0.2s; }
.content > view:nth-child(3) { animation-delay: 0.3s; }
.content > view:nth-child(4) { animation-delay: 0.4s; }
</style> 