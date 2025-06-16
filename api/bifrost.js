const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const axios = require("axios");
const app = express();
const port = 3000;

app.use(express.json());

// 🚀 bifrost.log 내용 반환
app.get("/log", (req, res) => {
  const logPath = path.join(__dirname, "bifrost.log");

  fs.readFile(logPath, "utf8", (err, data) => {
    if (err) {
      console.error("❌ 로그 파일 읽기 실패:", err);
      return res.status(500).send("로그 파일을 읽을 수 없습니다.");
    }

    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.send(data);
  });
});

app.get("/domestic", async (req, res) => {
  try {
    const domestic_res = await axios.post(
      "http://localhost:7777/run_domestic",
      {}
    );
    console.log("✅ 결과:", domestic_res.data);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.send(domestic_res.data);
  } catch (err) {
    console.error("❌ 요청 실패:", err.message);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.send("❌ 요청 실패:", err);
  }
});

app.get("/foreign", async (req, res) => {
  try {
    const domestic_res = await axios.post(
      "http://localhost:7777/run_foreign",
      {}
    );
    console.log("✅ 결과:", domestic_res.data);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.send(domestic_res.data);
  } catch (err) {
    console.error("❌ 요청 실패:", err.message);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.send("❌ 요청 실패:", err);
  }
});

// 🔁 Streamlit 대시보드를 /dashboard 경로로 프록시
app.use(
  "/dashboard",
  createProxyMiddleware({
    target: "http://localhost:5555", // Streamlit 서버 주소
    changeOrigin: true,
    pathRewrite: { "^/dashboard": "" }, // Streamlit이 루트에서 시작하므로 제거
  })
);

app.listen(port, "0.0.0.0", () => {
  console.log(`🚀 Bifrost 서버 실행 중: http://localhost:${port}`);
});
