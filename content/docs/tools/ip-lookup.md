---
title: "Public IP Lookup"
weight: 3
---

# Public IP Lookup

This tool displays your current public IP address and allows you to query any IP address to find its location, AS number, ISP, and other details.

<div style="margin-top: 2rem; padding: 2rem; border: 1px solid var(--gray-200); border-radius: 8px; background-color: var(--gray-100);">

  <!-- Feature 1: Current IP -->
  <div style="margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #ccc;">
    <h3 style="margin-top: 0;">1. Your Current Public IP</h3>
    <div id="currentIpResult" style="padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem;">Loading your IP information...</div>
  </div>

  <!-- Feature 2: IP Lookup -->
  <div>
    <h3 style="margin-top: 0;">2. IP Lookup</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">Enter IP Address:</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="ipInput" placeholder="e.g., 8.8.8.8" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="lookupIp()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Lookup</button>
    </div>
    <div id="lookupIpResult" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

</div>

<script>
function formatIpData(data) {
    if (!data.success) {
        return `Error: ${data.message}`;
    }
    
    return [
        `IP              : ${data.ip}`,
        `Type            : ${data.type}`,
        `Country         : ${data.country} (${data.country_code})`,
        `Region          : ${data.region}`,
        `City            : ${data.city}`,
        `Latitude        : ${data.latitude}`,
        `Longitude       : ${data.longitude}`,
        `ASN             : ${data.connection.asn}`,
        `ISP / Org       : ${data.connection.org} / ${data.connection.isp}`,
        `Domain          : ${data.connection.domain}`,
        `Timezone        : ${data.timezone.id} (UTC ${data.timezone.utc})`
    ].join('\n');
}

// Fetch current IP on load
window.addEventListener('DOMContentLoaded', () => {
    fetch('https://ipwho.is/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentIpResult').innerText = formatIpData(data);
        })
        .catch(error => {
            document.getElementById('currentIpResult').innerText = 'Error fetching IP information: ' + error.message;
        });
});

function lookupIp() {
    const ip = document.getElementById('ipInput').value.trim();
    const resultDiv = document.getElementById('lookupIpResult');
    resultDiv.style.display = 'block';
    
    if (!ip) {
        resultDiv.innerText = 'Please enter an IP address.';
        return;
    }

    resultDiv.innerText = 'Searching...';

    fetch(`https://ipwho.is/${ip}`)
        .then(response => response.json())
        .then(data => {
            resultDiv.innerText = formatIpData(data);
        })
        .catch(error => {
            resultDiv.innerText = 'Error fetching IP information: ' + error.message;
        });
}
</script>
