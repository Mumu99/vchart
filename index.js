const express = require("express");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 3000;
const WEATHER_API_KEY = "23af373708bf4fd6bfb2d5ca5a456051"; // 替换为你的天气 API Key
const CITY = "Beijing"; // 替换为目标城市

app.get("/weather", async (req, res) => {
  try {
    const response = await axios.get(
      `https://api.qweather.com/v7/weather/now?location=${CITY}&key=${WEATHER_API_KEY}`
    );
    const weatherData = response.data.now;
    res.json({
      city: CITY,
      weather: weatherData.text,
      temp: weatherData.temp,
      time: new Date().toLocaleString(),
    });
    // 在获取天气数据后调用
    sendWechatMessage(
      `城市：${CITY}\n天气：${weatherData.text}\n温度：${weatherData.temp}°C`
    );
  } catch (error) {
    console.error("获取天气数据失败：", error);
    res.status(500).json({ error: "获取天气数据失败" });
  }
});

app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});

const sendWechatMessage = async (message) => {
  const SEND_KEY = "SCT166761TYzJAFqmm01tdhgL9adgXMLkc"; // 替换为你的 Server 酱 SendKey
  await axios.post(`https://sctapi.ftqq.com/${SEND_KEY}.send`, {
    title: "每日天气推送",
    desp: message,
  });
};
