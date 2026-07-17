---
title: "MAC Address Lookup"
weight: 4
---

# MAC Address Lookup

This tool allows you to query a MAC address to find its manufacturer/vendor details.

<div style="margin-top: 2rem; padding: 2rem; border: 1px solid var(--gray-200); border-radius: 8px; background-color: var(--gray-100);">

  <div>
    <h3 style="margin-top: 0;">MAC Address Lookup</h3>
    <label style="display: block; font-weight: bold; margin-bottom: 0.5rem;">Enter MAC Address (e.g., 00:1A:2B:3C:4D:5E):</label>
    <div style="display: flex; gap: 1rem;">
      <input type="text" id="macInput" placeholder="00:1A:2B:3C:4D:5E" style="flex: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;" />
      <button onclick="lookupMac()" style="background-color: #CF0A2C; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Lookup</button>
    </div>
    <div id="lookupMacResult" style="margin-top: 1rem; padding: 1rem; background-color: #fff; border: 1px dashed #ccc; border-radius: 4px; font-family: monospace; white-space: pre-wrap; min-height: 1.5rem; display: none;"></div>
  </div>

</div>

<script>
function lookupMac() {
    let mac = document.getElementById('macInput').value.trim();
    const resultDiv = document.getElementById('lookupMacResult');
    resultDiv.style.display = 'block';
    
    if (!mac) {
        resultDiv.innerText = 'Please enter a MAC address.';
        return;
    }

    // Clean the MAC address: remove all non-alphanumeric characters (colons, hyphens, dots, spaces)
    let cleanMac = mac.replace(/[^a-fA-F0-9]/g, '');
    
    // An OUI (Organizationally Unique Identifier) is 24 bits, which means 6 hex characters.
    if (cleanMac.length < 6) {
        resultDiv.innerText = 'Error: Please enter at least 6 valid hexadecimal characters (the OUI prefix).';
        return;
    }

    // Format to XX:XX:XX... for the API request to strictly match the requested format
    let formattedMac = "";
    for (let i = 0; i < cleanMac.length; i += 2) {
        formattedMac += cleanMac.substring(i, i + 2);
        if (i + 2 < cleanMac.length) formattedMac += ":";
    }

    resultDiv.innerText = 'Searching...';

    // We use the requested api.macvendors.com directly.
    // They natively support CORS for browser requests.
    const apiUrl = `https://api.maclookup.app/v2/macs/${formattedMac}`;
    
    // Add an abort controller for timeout (e.g. 8 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    fetch(apiUrl, { signal: controller.signal })
        .then(response => {
            clearTimeout(timeoutId);
            if (response.status === 404) {
                return 'Vendor not found';
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(text => {
            // Some proxies or firewalls return JSON error pages instead of text. Catch that.
            if (text.includes('Free usage is limited') || text.includes('{"error"')) {
                throw new Error('Proxy or API limit reached');
            }
            if (text === 'Vendor not found') {
                 resultDiv.innerText = `MAC Input   : ${mac}\nFormatted   : ${formattedMac}\nResult      : Vendor not found`;
            } else {
                 resultDiv.innerText = `MAC Input   : ${mac}\nFormatted   : ${formattedMac}\nCompany     : ${text}`;
            }
        })
        .catch(error => {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                resultDiv.innerText = 'Error: Request timed out. The API might be down.';
            } else {
                // If direct fetch fails (e.g., rate limited or strict CORS), fallback to allorigins
                const proxyUrl = 'https://api.allorigins.win/get?url=' + encodeURIComponent(apiUrl);
                fetch(proxyUrl)
                    .then(res => {
                        if (!res.ok) throw new Error('Proxy failed');
                        return res.json();
                    })
                    .then(data => {
                        if (!data.contents || data.contents.includes('Not Found')) {
                             resultDiv.innerText = `MAC Input   : ${mac}\nFormatted   : ${formattedMac}\nResult      : Vendor not found`;
                             return;
                        }
                        resultDiv.innerText = `MAC Input   : ${mac}\nFormatted   : ${formattedMac}\nCompany     : ${data.contents}\n(Result via fallback proxy)`;
                    })
                    .catch(fallbackError => {
                        resultDiv.innerText = `Error fetching MAC information.\nMake sure you have an internet connection and your browser is not blocking cross-origin requests (CORS).\nOriginal Error: ${error.message}`;
                    });
            }
        });
}
</script>
