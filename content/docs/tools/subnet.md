---
title: "IP & Subnet Calculator"
weight: 2
---

# IP & Subnet Calculator

This tool provides network address calculations, subnet mask conversions, and wildcard mask calculations.

<div style="margin-top: 2rem; padding: 2rem; border: 1px solid var(--gray-200); border-radius: 8px; background-color: var(--gray-100);">

  <!-- Feature 1 -->
  <div style="margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #ccc;">
    <h3 style="margin-top: 0;">1. Network Address Calculator</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">IP Address & Prefix (e.g., 192.168.1.2/25):</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="ipInput1" placeholder="192.168.1.2/25" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="calcFeature1()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Calculate</button>
    </div>
    <div id="result1" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

  <!-- Feature 2 -->
  <div style="margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #ccc;">
    <h3 style="margin-top: 0;">2. Mask & Host Calculator</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">Subnet Mask or Prefix Length (e.g., 25 or 255.255.255.128):</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="ipInput2" placeholder="25 or 255.255.255.128" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="calcFeature2()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Calculate</button>
    </div>
    <div id="result2" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

  <!-- Feature 3 -->
  <div style="margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #ccc;">
    <h3 style="margin-top: 0;">3. Wildcard Mask Calculator</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">Subnet Mask (e.g., 255.255.255.0):</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="ipInput3" placeholder="255.255.255.0" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="calcFeature3()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Calculate</button>
    </div>
    <div id="result3" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

  <!-- Feature 4 -->
  <div>
    <h3 style="margin-top: 0;">4. IP Range to Subnets (CIDR)</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">IP Range (e.g., 192.168.1.0-192.168.1.65):</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="ipInput4" placeholder="192.168.1.0-192.168.1.65" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="calcFeature4()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Calculate</button>
    </div>
    <div id="result4" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

</div>

<script>
function ip2long(ip) {
    return ip.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet, 10), 0) >>> 0;
}

function long2ip(long) {
    return [
        (long >>> 24) & 255,
        (long >>> 16) & 255,
        (long >>> 8) & 255,
        long & 255
    ].join('.');
}

function long2binary(long) {
    let bin = long.toString(2).padStart(32, '0');
    return [
        bin.slice(0, 8),
        bin.slice(8, 16),
        bin.slice(16, 24),
        bin.slice(24, 32)
    ].join('.');
}

function maskLen2long(len) {
    return len === 0 ? 0 : (~0 << (32 - len)) >>> 0;
}

function isValidIP(ip) {
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    if (!ipRegex.test(ip)) return false;
    return ip.split('.').every(octet => parseInt(octet, 10) >= 0 && parseInt(octet, 10) <= 255);
}

function calcFeature1() {
    const input = document.getElementById('ipInput1').value.trim();
    const resultDiv = document.getElementById('result1');
    resultDiv.style.display = 'block';

    if (!input.includes('/')) {
        resultDiv.innerText = 'Error: Please include a prefix length (e.g., 192.168.1.2/25)';
        return;
    }

    const parts = input.split('/');
    const ip = parts[0];
    const prefix = parseInt(parts[1], 10);

    if (!isValidIP(ip) || isNaN(prefix) || prefix < 0 || prefix > 32) {
        resultDiv.innerText = 'Error: Invalid IP address or prefix length';
        return;
    }

    const ipLong = ip2long(ip);
    const maskLong = maskLen2long(prefix);
    const networkLong = (ipLong & maskLong) >>> 0;
    const broadcastLong = (networkLong | (~maskLong)) >>> 0;
    
    let usableCount = 0;
    if (prefix <= 30) {
        usableCount = (broadcastLong - networkLong - 1);
    } else if (prefix === 31) {
        usableCount = 2; // point-to-point
    } else if (prefix === 32) {
        usableCount = 1;
    }

    const output = [
        `Address Range      : ${long2ip(networkLong)} - ${long2ip(broadcastLong)}`,
        `Network Address    : ${long2ip(networkLong)}`,
        `Broadcast Address  : ${long2ip(broadcastLong)}`,
        `Subnet Mask        : ${long2ip(maskLong)}`,
        `Usable Hosts       : ${usableCount}`,
        `Network (Binary)   : ${long2binary(networkLong)}`,
        `Broadcast (Binary) : ${long2binary(broadcastLong)}`,
        `Mask (Binary)      : ${long2binary(maskLong)}`
    ].join('\n');

    resultDiv.innerText = output;
}

function calcFeature2() {
    const input = document.getElementById('ipInput2').value.trim();
    const resultDiv = document.getElementById('result2');
    resultDiv.style.display = 'block';

    let prefix = parseInt(input, 10);
    let maskLong;
    let isPrefixInput = false;

    if (isValidIP(input)) {
        maskLong = ip2long(input);
        // Calculate prefix from mask (counting consecutive 1s from left is standard, but here we just count all 1s for simplicity, though real validation could be stricter)
        let m = maskLong;
        prefix = 0;
        while ((m & 0x80000000) !== 0) {
            prefix++;
            m = (m << 1) >>> 0;
        }
    } else if (!isNaN(prefix) && prefix >= 0 && prefix <= 32 && input === prefix.toString()) {
        maskLong = maskLen2long(prefix);
        isPrefixInput = true;
    } else {
        resultDiv.innerText = 'Error: Invalid Subnet Mask or Prefix Length';
        return;
    }

    // Number of addresses
    // Note: JS bitwise operators are 32-bit, but Math.pow handles up to 2^53. Total addresses for /0 is 2^32.
    const totalAddresses = prefix === 0 ? 4294967296 : (prefix === 32 ? 1 : Math.pow(2, 32 - prefix));
    
    let usableCount = 0;
    if (prefix <= 30) {
        usableCount = totalAddresses - 2;
    } else if (prefix === 31) {
        usableCount = 2;
    } else if (prefix === 32) {
        usableCount = 1;
    }

    let output = '';
    if (isPrefixInput) {
        output += `Subnet Mask     : ${long2ip(maskLong)}\n`;
    } else {
        output += `Mask Length     : ${prefix} bits\n`;
    }
    
    output += `Total Addresses : ${totalAddresses}\n`;
    output += `Usable Hosts    : ${usableCount}`;

    resultDiv.innerText = output;
}

function calcFeature3() {
    const input = document.getElementById('ipInput3').value.trim();
    const resultDiv = document.getElementById('result3');
    resultDiv.style.display = 'block';

    if (!isValidIP(input)) {
        resultDiv.innerText = 'Error: Invalid Subnet Mask';
        return;
    }

    const maskLong = ip2long(input);
    const wildcardLong = (~maskLong) >>> 0;

    const output = [
        `Wildcard Mask : ${long2ip(wildcardLong)}`,
        `Binary Format : ${long2binary(wildcardLong)}`
    ].join('\n');

    resultDiv.innerText = output;
}

function rangeToSubnets(startIpLong, endIpLong) {
    let subnets = [];
    let current = startIpLong;
    while (current <= endIpLong) {
        let maxPrefix = 32;
        while (maxPrefix > 0) {
            let pLen = maxPrefix - 1;
            let mask = maskLen2long(pLen);
            let network = (current & mask) >>> 0;
            let broadcast = (network | (~mask)) >>> 0;
            // The subnet must start exactly at 'current', and must end within the range
            if (network === current && broadcast <= endIpLong) {
                maxPrefix = pLen;
            } else {
                break;
            }
        }
        subnets.push(long2ip(current) + '/' + maxPrefix);
        
        // Move current to the next IP after the chosen subnet
        let mask = maskLen2long(maxPrefix);
        let broadcast = (current | (~mask)) >>> 0;
        
        // Prevent infinite loop on 255.255.255.255
        if (broadcast === 4294967295) {
            break;
        }
        current = broadcast + 1;
    }
    return subnets;
}

function calcFeature4() {
    const input = document.getElementById('ipInput4').value.trim();
    const resultDiv = document.getElementById('result4');
    resultDiv.style.display = 'block';

    const parts = input.split('-');
    if (parts.length !== 2) {
        resultDiv.innerText = 'Error: Please enter a valid IP range separated by a hyphen (e.g., 192.168.1.0-192.168.1.65)';
        return;
    }

    const startIp = parts[0].trim();
    const endIp = parts[1].trim();

    if (!isValidIP(startIp) || !isValidIP(endIp)) {
        resultDiv.innerText = 'Error: Invalid IP address format in range';
        return;
    }

    const startLong = ip2long(startIp);
    const endLong = ip2long(endIp);

    if (startLong > endLong) {
        resultDiv.innerText = 'Error: Start IP must be less than or equal to End IP';
        return;
    }

    const subnets = rangeToSubnets(startLong, endLong);
    
    resultDiv.innerText = subnets.join(', ');
}
</script>
