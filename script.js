const API_BASE = ''; // Leave empty for same origin. After hosting, set to your backend URL if frontend hosted separately (e.g. https://your-backend.onrender.com)

document.getElementById("generateBtn").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;
  const style = document.getElementById("style").value;
  const duration = parseInt(document.getElementById("duration").value) || 5;
  const status = document.getElementById("status");
  const video = document.getElementById("outputVideo");

  if (!prompt.trim()) { status.innerText = "প্লিজ প্রম্পট লিখুন"; return; }

  status.innerText = "⏳ ভিডিও তৈরি হচ্ছে...";
  video.style.display = "none";

  try {
    const res = await fetch((API_BASE || window.location.origin) + "/generate", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({prompt, style, duration})
    });
    const data = await res.json();
    if (res.status === 202 || data.status === "pending") {
      status.innerText = "প্রসেসিং হচ্ছে — কিছুক্ষণ সময় লাগতে পারে। (এই ডেমোতে polling করা হয়)";
    } else if (data.status === "success") {
      status.innerText = "✅ ভিডিও তৈরি সম্পন্ন!";
      video.src = data.video_url;
      video.style.display = "block";
    } else {
      status.innerText = "❌ এরর: " + (data.error || 'Unknown');
    }
  } catch (err) {
    status.innerText = "❌ নেটওয়ার্ক ত্রুটি: " + err.message;
  }
});
