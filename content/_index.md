---
title: "Jonys Tech Book"
type: docs
bookToC: false
---

<style>
  /* 全局样式覆盖：针对首页，隐藏侧边栏并使主内容居中 */
  aside.book-menu {
    display: none !important;
  }
  .book-page {
    margin: 0 auto !important;
    max-width: 1600px !important;
    padding: 2rem !important;
  }

  /* =========================================
     Hero Section (产品展示区)
     ========================================= */
  .hero-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4rem;
    padding: 4rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #ffffff 0%, #f4f7fb 100%);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
    margin-bottom: 5rem;
    position: relative;
    overflow: hidden;
  }

  /* 添加一些背景装饰 */
  .hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(59,123,189,0.08) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    z-index: 0;
  }

  .hero-text {
    flex: 1;
    min-width: 300px;
    z-index: 1;
  }

  .hero-image {
    flex: 1;
    max-width: 500px;
    z-index: 1;
  }

  .hero-image img {
    width: 100%;
    border-radius: 16px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.12);
    transition: transform 0.5s ease;
  }

  .hero-image img:hover {
    transform: translateY(-10px);
  }

  .hero-title-wrapper {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 1rem;
  }

  .hero-logo {
    height: 4.5rem;
    width: auto;
    object-fit: contain;
    padding: 0.6rem;
    background-color: #ffffff;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }

  .hero-logo:hover {
    transform: scale(1.1) rotate(-5deg);
  }

  .hero-text h1 { 
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
  }

  .hero-text h2 { 
    color: #00b09b; 
    font-size: 1.3rem; 
    font-weight: 600;
    margin-bottom: 1.5rem; 
    letter-spacing: 0.5px;
  }

  .hero-text p {
    font-size: 1rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 2.5rem;
  }

  /* 按钮组样式 */
  .hero-buttons {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.8rem 2.2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    text-decoration: none !important;
    transition: all 0.3s ease;
  }

  .btn-primary {
    background: linear-gradient(135deg, #3b7bbd 0%, #2a5298 100%);
    color: white !important;
    box-shadow: 0 8px 16px rgba(59, 123, 189, 0.3);
  }

  .btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(59, 123, 189, 0.4);
  }

  .btn-outline {
    background: transparent;
    border: 2px solid #3b7bbd;
    color: #3b7bbd !important;
  }

  .btn-outline:hover {
    background: #3b7bbd;
    color: white !important;
    transform: translateY(-3px);
  }

  /* =========================================
     卡片式导航链接的样式设计
     ========================================= */
  .section-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    color: #1e3c72;
    margin-bottom: 3rem;
    position: relative;
  }

  .section-title::after {
    content: '';
    display: block;
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #3b7bbd, #00b09b);
    margin: 1rem auto 0;
    border-radius: 2px;
  }
  
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem; 
    margin-bottom: 4rem;
  }

  .nav-card {
    display: flex;
    flex-direction: column;
    text-decoration: none !important; 
    background-color: #ffffff; 
    border: 1px solid rgba(225, 234, 245, 0.8); 
    border-radius: 20px;       
    padding: 2.5rem 2rem;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); 
    box-shadow: 0 4px 12px rgba(0,0,0,0.03); 
    position: relative;
    overflow: hidden;
  }

  .nav-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3b7bbd, #00b09b);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .nav-card:hover {
    transform: translateY(-8px); 
    box-shadow: 0 20px 40px rgba(0,0,0,0.08); 
    border-color: transparent;
  }

  .nav-card:hover::before {
    opacity: 1;
  }

  .nav-card-icon {
    font-size: 1.9rem;
    margin-bottom: 0.5rem;
    display: inline-block;
    padding: 0.4rem 0.6rem;
    background: #f4f7fb;
    border-radius: 16px;
    align-self: flex-start;
    transition: transform 0.3s ease;
  }

  .nav-card:hover .nav-card-icon {
    transform: scale(1.1);
  }

  .nav-card h3 {
    color: #1e3c72 !important; 
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
  }

  .nav-card p {
    color: #64748b !important;    
    font-size: 1.05rem;
    line-height: 1.6;
    margin: 0;
  }

  /* 响应式调整 */
  @media (max-width: 768px) {
    .hero-section {
      flex-direction: column;
      text-align: center;
      padding: 3rem 1.5rem;
    }
    
    .hero-title-wrapper {
      justify-content: center;
      flex-direction: column;
    }
    
    .hero-buttons {
      justify-content: center;
    }
    
    .hero-text h1 {
      font-size: 2.4rem;
    }
    
    .hero-image {
      margin-top: 2rem;
    }
  }

  /* 暗色模式支持 (如果有主题切换) */
  html.dark .hero-section {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  }
  html.dark .hero-text h1 {
    background: linear-gradient(90deg, #93c5fd 0%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  html.dark .hero-text p { color: #cbd5e1; }
  html.dark .nav-card {
    background-color: #1e293b;
    border-color: #334155;
  }
  html.dark .nav-card:hover { box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
  html.dark .nav-card h3 { color: #f8fafc !important; }
  html.dark .nav-card p { color: #94a3b8 !important; }
  html.dark .nav-card-icon { background: #0f172a; }
  html.dark .section-title { color: #f8fafc; }
</style>

<div class="hero-section">
  <!-- 左侧文案 -->
  <div class="hero-text">
    <div class="hero-title-wrapper">
      <img src="logo.svg" alt="Logo" class="hero-logo" style="height: 80px; width: 80px;" />
      <h1>Jonys Tech Book</h1>
    </div>
    <h2>Systematic summary, Reject invalid involution.</h2>
    <p>Sharing Networking, Data Center and Automation Programming Technologies.</p>
    <div class="hero-buttons">
      <a href="/docs/sdwan/" class="btn btn-primary">Read Now</a>
      <a href="/about/" class="btn btn-outline">About Me</a>
    </div>
  </div>

  <!-- 右侧图片 -->
  <div class="hero-image">
    <!-- 确保这张图放在 static 文件夹里 -->
    <img src="/book-cover.png" alt="书本封面">
  </div>
</div>

<h2 class="section-title">All For the Networking</h2>

<div class="card-grid">
  <a href="/docs/tools" class="nav-card">
    <div class="nav-card-icon">🛠️</div>
    <h3>Network Tools</h3>
    <p>You can find some useful tools here.</p>
  </a>

  <a href="/docs/sdwan" class="nav-card">
    <div class="nav-card-icon">🌍</div>
    <h3>SD-WAN Technology</h3>
    <p>Deep dive into Huawei SD-WAN architecture, deployment, and best practices.</p>
  </a>

  <a href="/docs/wlan" class="nav-card">
    <div class="nav-card-icon">📶</div>
    <h3>WLAN Technology</h3>
    <p>Explore wireless networking technologies and applications, including AP deployment and Option 43 calculation tools.</p>
  </a>

  <a href="/docs/nac" class="nav-card">
    <div class="nav-card-icon">🔒</div>
    <h3>NAC Technology</h3>
    <p>Network Access Control technologies for ensuring enterprise network security.</p>
  </a>

  <a href="/docs/switch" class="nav-card">
    <div class="nav-card-icon">⚡</div>
    <h3>Switch Technology</h3>
    <p>Insights on Huawei Switch network architecture, and other technologies.</p>
  </a>

  <a href="/docs/python" class="nav-card">
    <div class="nav-card-icon">🚀</div>
    <h3>Python & Network</h3>
    <p>Python and network automation.</p>
  </a>

  <a href="/" class="nav-card">
    <div class="nav-card-icon">🎶</div>
    <h3>Stay Tuned</h3>
    <p>More exciting content is under construction.</p>
  </a>
</div>
