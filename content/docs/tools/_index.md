---
title: "Network Tools"
type: docs
bookToC: false
---

<style>
  /* 彻底隐藏左侧的整块菜单区域 */
  aside.book-menu {
    display: none !important;
  }
  /* 让主页内容在屏幕中居中显示 */
  .book-page {
    margin: 0 auto !important;
    max-width: 1600px;
    padding: 2rem;
  }

  /* 顶部标题区样式 */
  .tools-header {
    text-align: center;
    margin-bottom: 3rem;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #eef2f5 0%, #e0eaf5 100%);
    border-radius: 20px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
    border: 1px solid rgba(255, 255, 255, 0.7);
  }
  
  .tools-header h1 {
    color: #102a43;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
    letter-spacing: -0.5px;
  }
  
  .tools-header p {
    color: #486581;
    font-size: 1.2rem;
    margin: 0;
  }

/* =========================================
     工具卡片网格布局
     ========================================= */
  
  .tools-grid {
    display: grid;
    /* 自动排版，固定最小宽度，让屏幕变窄自动换行 */
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 2.5rem; 
  }

  /* 工具卡片样式 - 规整的正方形显示 */
  a.tool-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    aspect-ratio: 1 / 1; /* 固定长宽比为1:1，呈现规整的正方形 */
    text-decoration: none !important;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    position: relative;
    overflow: hidden;
  }

  /* 顶部色彩条点缀 */
  a.tool-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: #3b7bbd;
    transition: all 0.3s ease;
  }

  /* 鼠标悬浮时的效果 */
  a.tool-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 25px 35px -5px rgba(0, 0, 0, 0.1), 0 15px 15px -5px rgba(0, 0, 0, 0.04);
    border-color: #bcd1eb;
  }
  
  a.tool-card:hover::before {
    height: 8px;
    background: #CF0A2C; /* 华为红作为高亮点缀 */
  }

  /* 卡片里面的图标 */
  .tool-icon {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 90px;
    height: 90px;
    background: #f8fafc;
    border-radius: 50%;
    transition: all 0.4s ease;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
  }

  a.tool-card:hover .tool-icon {
    transform: scale(1.15) rotate(5deg);
    background: #f1f5f9;
  }

  /* 标题和文字 */
  .tool-card h3 {
    color: #1e293b !important;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
  }

  .tool-card p {
    color: #64748b !important;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
    /* 限制最多显示三行 */
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

</style>

<div class="tools-header">
  <h1>Networking Toolkit</h1>
  <p>Essential utilities for network engineering, configuration, and diagnostics.</p>
</div>

<div class="tools-grid">
  <!-- Option 43 Tool -->
  <a href="/docs/tools/option43/" class="tool-card">
    <div class="tool-icon">🧮</div>
    <h3>Huawei Option 43</h3>
    <p>Quickly calculate DHCP Option 43 hexadecimal strings for Huawei WLAN AP deployments.</p>
  </a>

  <!-- Subnet Calculator Tool -->
  <a href="/docs/tools/subnet/" class="tool-card">
    <div class="tool-icon">🌐</div>
    <h3>IP & Subnet</h3>
    <p>Calculate network addresses, subnets, usable hosts, and convert wildcard masks easily.</p>
  </a>

  <!-- Public IP Lookup Tool -->
  <a href="/docs/tools/ip-lookup/" class="tool-card">
    <div class="tool-icon">🔍</div>
    <h3>Public IP Lookup</h3>
    <p>Automatically detect your public IP and look up detailed location, ASN, and ISP info for any IP.</p>
  </a>

  <!-- Batch Config Generator Tool -->
  <a href="/docs/tools/batch-generator/" class="tool-card">
    <div class="tool-icon">🛠️</div>
    <h3>Batch Config Generator</h3>
    <p>Automatically generate repetitive configuration scripts or JSON based on templates with dynamic variables.</p>
  </a>

  <!-- Time & Timestamp Tool -->
  <a href="/docs/tools/time/" class="tool-card">
    <div class="tool-icon">⏱️</div>
    <h3>Time & Timestamp</h3>
    <p>Real-time clock comparison (兑时), network time sync, timestamp conversion, and timezone calculations.</p>
  </a>
</div>
