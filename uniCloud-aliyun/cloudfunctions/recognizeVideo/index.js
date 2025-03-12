'use strict';

const axios = require('axios');

// Python服务配置
const PYTHON_SERVICE = {
  // 替换为您部署的Python服务地址（如Vercel、Heroku等）
  URL: 'https://your-python-service.vercel.app/api/recognize',
  TIMEOUT: 30000
};

exports.main = async (event, context) => {
  const { video_url } = event;
  
  try {
    if (!video_url) {
      return {
        code: 400,
        error: "缺少视频URL"
      };
    }

    console.log('开始请求Python服务:', video_url);
    
    // 调用Python服务
    const response = await axios({
      method: 'POST',
      url: PYTHON_SERVICE.URL,
      data: { video_url },
      timeout: PYTHON_SERVICE.TIMEOUT,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('Python服务响应:', response.data);

    // 检查响应
    if (!response.data || response.data.code !== 200) {
      throw new Error(response.data?.error || '识别服务异常');
    }

    return response.data;

  } catch (error) {
    console.error('识别错误:', error);
    return {
      code: 500,
      error: error.message || '识别服务异常'
    };
  }
}; 