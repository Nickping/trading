const cron = require("node-cron");
const axios = require("axios");


cron.schedule("0 * * * *", async () => {
  console.log("⏰ 60분마다 로직 서버에 요청 시작");

  try {
    const res = await axios.post("http://localhost:7777/run-strategy", {
      symbol: "005930"
    });
    console.log("✅ 결과:", res.data);
  } catch (err) {
    console.error("❌ 요청 실패:", err.message);
  }
});
