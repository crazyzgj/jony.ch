---
title: "Huawei Option 43"
weight: 1
---

# Huawei Option 43 Online Calculator

In WLAN deployment, APs typically obtain the WAC's IP address through the DHCP Option 43 field. This tool can be used to quickly calculate the Option 43 Hex configuration string.

<div style="margin-top: 2rem; padding: 2rem; border: 1px solid var(--gray-200); border-radius: 8px; background-color: var(--gray-100);">
  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">WAC IP Address 1:</label>
    <input type="text" id="ip1" placeholder="e.g. 192.168.1.1" style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
  </div>
  <div style="margin-bottom: 1rem;">
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">WAC IP Address 2 (Optional, active/standby scenario):</label>
    <input type="text" id="ip2" placeholder="e.g. 192.168.1.2" style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
  </div>
  <button onclick="calculateOption43()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">
    Calculate Option 43
  </button>

  <div style="margin-top: 2rem;">
    <strong style="display: block; margin-bottom: 0.5rem;">Calculation Result:</strong>
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
        document.getElementById('result').innerText = 'Please enter at least one IP address';
        return;
    }

    // Simple Regex validation for IP
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    if (ip1 && !ipRegex.test(ip1)) {
        document.getElementById('result').innerText = 'IP Address 1 format is incorrect';
        return;
    }
    if (ip2 && !ipRegex.test(ip2)) {
        document.getElementById('result').innerText = 'IP Address 2 format is incorrect';
        return;
    }

    let hexStr = '';
    for (let i = 0; i < ipStr.length; i++) {
        hexStr += ipStr.charCodeAt(i).toString(16).toUpperCase();
    }
    
    // Length (Hexadecimal)
    let lengthHex = ipStr.length.toString(16).toUpperCase().padStart(2, '0');
    // Sub-option type 03 + length + Hex converted from string
    let result = '03' + lengthHex + hexStr;
    
    document.getElementById('result').innerText = result;
}
</script>

## Calculation Instructions

The format of Huawei Option 43 field is usually: `03` (sub-option type) + `Length` (hexadecimal, 1 byte) + `ASCII Hexadecimal of comma-separated IP string`.

* **Single IP Example**: Input `192.168.1.1` (length 11 bytes, hexadecimal is `0B`)
  Output: `030B3139322E3136382E312E31`

* **Dual IP Example**: Input `192.168.1.1` and `192.168.1.2`, concatenated as `192.168.1.1,192.168.1.2` (length 23 bytes, hexadecimal is `17`)
  Output: `03173139322E3136382E312E312C3139322E3136382E312E32`
*(Note: According to the standard, when configuring two IP addresses, the calculation length should be the total length of the two IPs and the comma, which is `17`.)*
