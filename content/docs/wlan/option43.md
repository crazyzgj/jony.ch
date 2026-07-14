---
title: "华为 Option 43 在线计算"
weight: 1
---

# 华为 Option 43 在线计算

在 WLAN 部署中，AP 通常通过 DHCP Option 43 字段获取 WAC 的 IP 地址。本工具可用于快速计算 Option 43 的 Hex 配置字符串。

<div style="margin-top: 2rem; padding: 2rem; border: 1px solid var(--gray-200); border-radius: 8px; background-color: var(--gray-100);">
  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">WAC IP 地址 1：</label>
    <input type="text" id="ip1" placeholder="例如：10.5.204.10" style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
  </div>
  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">WAC IP 地址 2（可选，主备场景）：</label>
    <input type="text" id="ip2" placeholder="例如：192.168.1.1" style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
  </div>
  <button onclick="calculateOption43()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">
    计算 Option 43
  </button>

  <div style="margin-top: 2rem;">
    <strong style="display: block; margin-bottom: 0.5rem;">计算结果：</strong>
    <div id="result" style="padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; word-break: break-all; min-height: 1.5rem;">
    </div>
  </div>
</div>

<script>
function calculateOption43() {
    const ip1 = document.getElementById('ip1').value.trim();
    const ip2 = document.getElementById('ip2').value.trim();
    
    let ipStr = '';
    if (ip1 && ip2) {
        ipStr = ip1 + ',' + ip2;
    } else if (ip1) {
        ipStr = ip1;
    } else if (ip2) {
        ipStr = ip2;
    }

    if (!ipStr) {
        document.getElementById('result').innerText = '请输入至少一个 IP 地址';
        return;
    }

    // 正则简单校验 IP
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    if (ip1 && !ipRegex.test(ip1)) {
        document.getElementById('result').innerText = 'IP 地址 1 格式不正确';
        return;
    }
    if (ip2 && !ipRegex.test(ip2)) {
        document.getElementById('result').innerText = 'IP 地址 2 格式不正确';
        return;
    }

    let hexStr = '';
    for (let i = 0; i < ipStr.length; i++) {
        hexStr += ipStr.charCodeAt(i).toString(16).toUpperCase();
    }
    
    // 长度（十六进制）
    let lengthHex = ipStr.length.toString(16).toUpperCase().padStart(2, '0');
    // 子选项类型 03 + 长度 + 字符串转换的 Hex
    let result = '03' + lengthHex + hexStr;
    
    document.getElementById('result').innerText = result;
}
</script>

## 计算说明

华为 Option 43 字段的格式通常为：`03`（子选项类型） + `长度`（十六进制，占一字节） + `逗号分隔的 IP 字符串的 ASCII 十六进制`。

* **单 IP 示例**：输入 `10.5.204.10`（长度 11 字节，十六进制为 `0B`）
  输出：`030B31302E352E3230342E3130`

* **双 IP 示例**：输入 `192.168.1.2` 和 `192.168.1.1`，拼接后为 `192.168.1.2,192.168.1.1`（长度 23 字节，十六进制为 `17`）
  输出：`03173139322E3136382E312E322C3139322E3136382E312E31`
*(注：根据标准，当配置两个 IP 地址时，计算长度应为两个 IP 及逗号的总长度，即 `17`。)*
