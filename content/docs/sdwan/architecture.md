---
title: "2. 架构与组件"
weight: 20
draft: true
---

# 架构与组件

华为 SD-WAN 架构分为三层：

## 1. 编排与管理层 (iMaster NCE-Campus)
全网的统一大脑，提供网络配置、编排、自动化运维能力。

## 2. 控制层 (Route Reflector - RR)
负责在各个站点之间反射和分发 VPN 路由及策略信息。

## 3. 转发层 (NetEngine AR)
部署在分支企业和总部的 CPE 设备，负责实际的数据报文转发。
