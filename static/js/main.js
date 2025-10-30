async function generate() {
  const btn = document.getElementById('generateBtn');
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');
  const progressBar = document.getElementById('progressBar');

  btn.disabled = true;
  btn.innerText = "生成中...";
  loading.style.display = "block";
  result.style.display = "none";

  let width = 0;
  const interval = setInterval(() => {
    if (width >= 90) clearInterval(interval);
    else { width += 5; progressBar.style.width = width + '%'; }
  }, 100);

  try {
    const theme = document.getElementById('theme').value;
    const res = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme })
    });
    const data = await res.json();

    clearInterval(interval);
    progressBar.style.width = '100%';
    setTimeout(() => {
      document.getElementById('quote').innerText = data.quote;
      document.getElementById('tags').innerText = data.tags.join(' ');
      document.getElementById('desc').innerText = data.desc;
      result.style.display = "block";
      loading.style.display = "none";
      btn.disabled = false;
      btn.innerText = "生成抖音文案";
    }, 300);
  } catch (e) {
    alert("生成失败，请重试！");
    btn.disabled = false;
    btn.innerText = "生成抖音文案";
    loading.style.display = "none";
  }
}

function copyQuote() { copyToClipboard(document.getElementById('quote').innerText, '金句已复制！'); }
function copyTags() { copyToClipboard(document.getElementById('tags').innerText, '标签已复制！'); }
function copyDesc() { copyToClipboard(document.getElementById('desc').innerText, '描述已复制！'); }
function copyAll() {
  const text = `${document.getElementById('quote').innerText}\n${document.getElementById('tags').innerText}\n${document.getElementById('desc').innerText}`;
  copyToClipboard(text, '已复制全部！');
}

function copyToClipboard(text, message) {
  navigator.clipboard.writeText(text).then(() => alert(message));
}
