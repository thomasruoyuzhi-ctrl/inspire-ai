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

    // 在 generate() 函数的 try 块内，setTimeout 之前添加：
    let count = parseInt(localStorage.getItem('generateCount') || '0');
    count++;
    localStorage.setItem('generateCount', count);
    // 然后在 setTimeout 里显示
    document.getElementById('count').innerText = count;
    document.getElementById('stats').style.display = 'block';

    
    setTimeout(() => {
      document.getElementById('quote').innerText = data.quote;
      document.getElementById('tags').innerText = data.tags.join(' ');
      document.getElementById('desc').innerText = data.desc;
      result.style.display = "block";
      loading.style.display = "none";
      btn.disabled = false;
      btn.innerText = "生成抖音文案";
      // 在 setTimeout 里，result 显示后添加：
      /////////////
      ////////////
    document.getElementById('stats').style.display = 'block';
    let count = localStorage.getItem('generateCount') || 0;
    count++;
    localStorage.setItem('generateCount', count);
    document.getElementById('count').innerText = count;
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


function generateAgain() {
  const theme = document.getElementById('theme').value || '励志';
  // 重新触发生成
  document.getElementById('generateBtn').click();
}

function copyAsScript() {
  const quote = document.getElementById('quote').innerText;
  const tags = document.getElementById('tags').innerText;
  const desc = document.getElementById('desc').innerText;
  const script = `${quote}\n\n${desc}\n\n${tags}`;
  copyToClipboard(script, '已复制为抖音脚本格式！');
}
