---
title: "Jonys Book Tech Blog"
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
  }
/* =========================================
     卡片式导航链接的样式设计
     ========================================= */
  
  /* 1. 网格布局容器：自动排版，每行 3 个，屏幕变窄自动换行 */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem; /* 卡片之间的间距 */
    margin: 2rem 0;
  }

  /* 2. 每一个可点击的卡片样式 */
  a.nav-card {
    display: block;
    text-decoration: none !important; /* 去掉链接默认的下划线 */
    background-color: #f8fbff; /* 极浅的蓝白色背景 */
    border: 1px solid #e1eaf5; /* 淡淡的边框 */
    border-radius: 12px;       /* 圆角 */
    padding: 1.5rem;
    transition: all 0.3s ease; /* 鼠标悬浮时的动画过渡时间 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.04); /* 默认有一点点阴影 */
  }

  /* 3. 鼠标放上去时的悬浮效果（卡片上浮并加深阴影） */
  a.nav-card:hover {
    transform: translateY(-5px); /* 向上浮动 5px */
    box-shadow: 0 12px 20px rgba(0,0,0,0.1); /* 阴影变大变深 */
    border-color: #bcd1eb; /* 边框颜色变深一点 */
  }

  /* 4. 卡片里面的图标、标题和文字 */
  .nav-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
  }
  .nav-card h3 {
    color: #3b7bbd !important; /* 截图里那种偏灰的蓝色标题 */
    font-size: 1.15rem;
    margin: 0 0 0.5rem 0;
  }
  .nav-card p {
    color: #666 !important;    /* 描述文字用灰色 */
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0;
  }

</style>

<div class="text-center" style="margin: 4rem 0;">
  <h1 style="font-size: 3rem; color: #CF0A2C;">Jonys Book Tech Blog</h1>
  <p style="font-size: 1.25rem; color: var(--gray-500);">Sharing Networking, Data Center and Automation Programming Technologies</p>
  <br/>
</div>

{{< columns >}}
<h2 style="text-align: center; color: #3b7bbd; margin-top: 2rem;">Topics</h2>

<div class="card-grid">


<a href="/docs/sdwan" class="nav-card">
    <div class="nav-card-icon">🎯</div>
    <h3>SD-WAN Technology</h3>
    <p>Deep dive into Huawei SD-WAN architecture, deployment, and best practices</p>
  </a>

<a href="/docs/wlan" class="nav-card">
    <div class="nav-card-icon">🚀</div>
    <h3>WLAN Technology</h3>
    <p>Explore wireless networking technologies and applications, including AP deployment and Option 43 calculation tools.</p>
  </a>

<a href="/docs/nac" class="nav-card">
    <div class="nav-card-icon">⚡</div>
    <h3>NAC Technology</h3>
    <p>Network Access Control technologies for ensuring enterprise network security.</p>
  </a>

  <a href="/docs/dc" class="nav-card">
    <div class="nav-card-icon">🎯</div>
    <h3>DC Data Center Technology</h3>
    <p>Insights on Data Center network architecture, VXLAN, and other cutting-edge technologies.</p>
  </a>

  <a href="/docs/python" class="nav-card">
    <div class="nav-card-icon">🎯</div>
    <h3>python</h3>
    <p>Insights on Data Center network architecture, VXLAN, and other cutting-edge technologies.</p>
  </a>

  <a href="/" class="nav-card">
    <div class="nav-card-icon">🎯</div>
    <h3>Stay Tuned</h3>
    <p>IMore exciting content is under construction.</p>
  </a>


{{< /columns >}}
