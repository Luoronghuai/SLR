<template>
  <view class="container">
    <view class="background-layer"></view>
    
    <view class="content-wrapper">
      <!-- 加载状态显示 -->
      <uni-load-more v-if="loading" status="loading" :content-text="loadingText"></uni-load-more>
      
      <view class="slogan-box">
        <text class="slogan-text">{{ comment }}</text>
      </view>

      <view class="category-card-index dark" @click="handleVideoUpload">
        <text class="card-text">{{ loading ? '识别中...' : '视频识别' }}</text>
      </view>

      <view class="cenema" v-if="videoUrl">
        <view class="video-container">
          <video 
            :src="videoUrl" 
            controls
            class="main-video"
            @error="handleVideoError"
          ></video>
          <view class="video-info">
            <text class="video-title">手语视频识别</text>
          </view>
        </view>
      </view>

      <view class="card-container">
        <view class="category-card diary" @click="clickDiary">
          <text class="card-text">识别日志</text>
        </view>
        <view class="category-card aboutUs" @click="clickUs">
          <text class="card-text">关于我们</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
const db = uniCloud.database()

const API_CONFIG = {
  // 替换为您的云服务器域名
  BASE_URL: 'https://your-domain.com'
};

export default {
  data() {
    return {
      videoUrl: '',
      currentFileID: '',
      comment: "手语识爱 , 温暖常在 。",
      loading: false,
      loadingText: {
        contentdown: '上传识别中...',
        contentrefresh: '处理中...',
        contentnomore: '完成'
      }
    };
  },
  methods: {
    // 处理视频错误
    async handleVideoError(err) {
      console.error('视频播放错误:', err);
      
      try {
        // 尝试重新获取临时URL
        if (this.currentFileID) {
          const urlRes = await uniCloud.getTempFileURL({
            fileList: [this.currentFileID]
          });
          
          if (urlRes.fileList && urlRes.fileList[0]) {
            this.videoUrl = urlRes.fileList[0].tempFileURL + '?t=' + Date.now();
            return;
          }
        }
        
        uni.showToast({
          title: '视频加载失败，请重试',
          icon: 'none'
        });
      } catch (error) {
        console.error('重新获取视频URL失败:', error);
        uni.showToast({
          title: '视频加载失败',
          icon: 'none'
        });
      }
    },

    // 主要的视频上传和识别处理函数
    async handleVideoUpload() {
      if (this.loading) {
        uni.showToast({
          title: '正在处理中，请稍候',
          icon: 'none'
        });
        return;
      }

      let loadingShown = false;
      
      try {
        this.loading = true;
        
        // 选择视频
        const chooseRes = await uni.chooseVideo({
          sourceType: ['album'],
          compressed: true,
          maxDuration: 15,
          camera: 'back'
        });

        // 检查视频大小
        if (chooseRes.size > 10 * 1024 * 1024) {
          throw new Error('视频大小不能超过10MB，请选择较短的视频');
        }

        // 显示上传提示
        uni.showLoading({
          title: '上传中...',
          mask: true
        });
        loadingShown = true;

        // 上传到云存储
        const uploadRes = await uniCloud.uploadFile({
          filePath: chooseRes.tempFilePath,
          cloudPath: `videos/${Date.now()}_${Math.random().toString(36).slice(-6)}.mp4`,
          cloudPathAsRealPath: true // 使用真实路径
        });

        this.currentFileID = uploadRes.fileID;

        // 获取临时访问链接
        const urlRes = await uniCloud.getTempFileURL({
          fileList: [uploadRes.fileID]
        });
        
        const videoUrl = urlRes.fileList[0].tempFileURL;
        this.videoUrl = videoUrl;

        // 存储到videos表
        const videoAddRes = await db.collection('videos').add({
          fileID: uploadRes.fileID,
          status: 'uploaded',
          created: Date.now()
        });

        // 更新加载提示
        uni.showLoading({
          title: '识别中...',
          mask: true
        });

        // 调用Python后端API进行识别
        const recognizeResponse = await uni.request({
          url: `${API_CONFIG.BASE_URL}/api/recognize`,
          method: 'POST',
          data: {
            video_url: videoUrl
          },
          header: {
            'content-type': 'application/json'
          }
        });

        const result = recognizeResponse.data;
        
        if (!result || result.code !== 200) {
          throw new Error(result?.error || '识别失败');
        }
        
        this.comment = result.data.result;

        // 保存识别日志
        await db.collection('recognition_logs').add({
          result: this.comment,
          created: Date.now(),
          fileID: uploadRes.fileID
        });

        // 更新视频状态
        if (videoAddRes.id) {
          await db.collection('videos').doc(videoAddRes.id).update({
            status: 'processed',
            result: this.comment,
            processed: Date.now()
          });
        }

        uni.showToast({
          title: '识别成功',
          icon: 'success'
        });

      } catch (err) {
        console.error("处理错误:", err);
        const errorMessage = err.message || '处理失败';
        uni.showToast({
          title: errorMessage,
          icon: 'none',
          duration: 3000
        });
      } finally {
        this.loading = false;
        if (loadingShown) {
          uni.hideLoading();
        }
      }
    },

    // 查看日志
    clickDiary() {
      uni.navigateTo({
        url: '/pages/diary/diary'
      });
    },
    
    // 关于我们
    clickUs() {
      uni.navigateTo({
        url: '/pages/about/about'
      });
    }
  }
};
</script>

<style scoped>
.container {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: #ffffff;
  padding-top: var(--status-bar-height);
}

.background-layer {
  position: absolute;
  width: 150%;
  height: 150%;
  background: linear-gradient(135deg, 
    rgba(227, 242, 253, 0.8) 0%, 
    rgba(187, 222, 251, 0.8) 50%, 
    rgba(144, 202, 249, 0.8) 100%
  );
  transform: rotate(-15deg);
  top: -30%;
  left: -25%;
  filter: blur(90px);
  opacity: 0.7;
  animation: rotateGradient 15s ease infinite;
}

.content-wrapper {
  position: relative;
  padding: 40rpx 32rpx;
  z-index: 1;
  animation: fadeIn 0.8s ease-in-out;
  max-width: 1000rpx;
  margin: 0 auto;
}

@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translateY(30rpx); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.slogan-box {
  margin: 40rpx 0 60rpx;
  padding: 45rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  border-radius: 36rpx;
  box-shadow: 0 15rpx 35rpx rgba(31, 38, 135, 0.1);
  transform: translateZ(0);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  animation: floatAnimation 3s ease-in-out infinite;
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.slogan-box::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  animation: rotateGradient 8s linear infinite;
}

.slogan-text {
  display: block;
  font-size: 42rpx;
  background: linear-gradient(45deg, #2196F3, #1976D2);
  -webkit-background-clip: text;
  color: transparent;
  text-align: center;
  line-height: 1.6;
  font-weight: 600;
  letter-spacing: 3rpx;
  text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.1);
}

.category-card-index.dark {
  height: 280rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(-45deg, #2196F3, #1976D2, #2196F3);
  background-size: 200% 200%;
  animation: rotateGradient 5s ease infinite, scaleBreath 3s ease-in-out infinite;
  color: white;
  box-shadow: 0 12rpx 36rpx rgba(33, 150, 243, 0.25);
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.category-card-index.dark::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.category-card-index.dark:active::after {
  transform: translateX(100%);
}

.card-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
  margin: 40rpx 0;
  padding: 0 4rpx;
}

.category-card {
  height: 240rpx;
  border-radius: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-card::before,
.category-card-index.dark::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: 0.5s;
}

.category-card:active::before,
.category-card-index.dark:active::before {
  left: 100%;
}

.card-text {
  font-size: 36rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

.diary {
  background: linear-gradient(-45deg, #5C6BC0, #3F51B5, #5C6BC0);
  background-size: 200% 200%;
  animation: rotateGradient 6s ease infinite, glowPulse 4s infinite;
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.aboutUs {
  background: linear-gradient(-45deg, #26A69A, #00897B, #26A69A);
  background-size: 200% 200%;
  animation: rotateGradient 7s ease infinite, floatAnimation 4s ease-in-out infinite;
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.cenema {
  margin: 40rpx auto;
  width: 92%;
  border-radius: 36rpx;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.05);
  box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.15);
  transform: translateZ(0);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  backdrop-filter: blur(10px);
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.video-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 宽高比 */
  background: #000;
  overflow: hidden;
}

.main-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 24rpx;
  transition: all 0.3s ease;
}

.video-info {
  position: absolute;
  top: 20rpx;
  left: 20rpx;
  right: 20rpx;
  padding: 16rpx 24rpx;
  background: rgba(33, 150, 243, 0.2);
  backdrop-filter: blur(8px);
  border-radius: 16rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  opacity: 0;
  transform: translateY(-10rpx);
  animation: fadeInDown 0.3s ease forwards;
}

.video-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.3);
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 视频控件美化 */
.main-video::-webkit-media-controls-panel {
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}

.main-video::-webkit-media-controls-play-button {
  background-color: rgba(255,255,255,0.9);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.main-video::-webkit-media-controls-timeline {
  background-color: rgba(255,255,255,0.2);
}

.main-video::-webkit-media-controls-current-time-display,
.main-video::-webkit-media-controls-time-remaining-display {
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

/* 视频悬浮效果 */
.cenema:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.2);
}

/* 适配深色模式 */
@media (prefers-color-scheme: dark) {
  .cenema {
    background: rgba(255, 255, 255, 0.05);
  }
  
  .video-info {
    background: rgba(255,255,255,0.1);
  }
}

/* 加载状态样式 */
.loading-box {
  text-align: center;
  padding: 32rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 24rpx;
  margin: 24rpx 0;
  backdrop-filter: blur(12px);
}

/* 适配刘海屏 */
.safe-area-inset-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}

/* 新增动画效果 */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.category-card-index.dark {
  background-size: 200% 100%;
  animation: shimmer 3s infinite;
  background-image: linear-gradient(
    45deg,
    #2196F3 0%,
    #1976D2 45%,
    #2196F3 55%,
    #1976D2 100%
  );
}

/* 动画关键帧定义 */
@keyframes floatAnimation {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10rpx); }
}

@keyframes glowPulse {
  0%, 100% { box-shadow: 0 8rpx 24rpx rgba(33, 150, 243, 0.2); }
  50% { box-shadow: 0 12rpx 36rpx rgba(33, 150, 243, 0.4); }
}

@keyframes rotateGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes scaleBreath {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes borderGlow {
  0%, 100% { border: 2rpx solid rgba(255, 255, 255, 0.1); }
  50% { border: 2rpx solid rgba(255, 255, 255, 0.3); }
}
</style>