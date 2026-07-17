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

    // We only need the first 6 characters to query the API.
    let oui = cleanMac.substring(0, 6).toUpperCase();

    resultDiv.innerText = 'Searching...';

    // We use corsproxy.io because direct API calls often fail due to strict CORS rules in modern browsers.
    const url = 'https://corsproxy.io/?' + encodeURIComponent('https://api.macvendors.com/' + oui);
    
    // Add an abort controller for timeout (e.g. 8 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    fetch(url, { signal: controller.signal })
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
            if (text === 'Vendor not found') {
                resultDiv.innerText = `MAC Input   : ${mac}\nOUI Prefix  : ${oui}\nResult      : Vendor not found`;
            } else {
                resultDiv.innerText = `MAC Input   : ${mac}\nOUI Prefix  : ${oui}\nCompany     : ${text}`;
            }
        })
        .catch(error => {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                resultDiv.innerText = 'Error: Request timed out. The API proxy might be down or blocked by your network.';
            } else {
                // If corsproxy fails, fallback to another free API
                fetch(`https://api.allorigins.win/get?url=${encodeURIComponent('https://api.macvendors.com/' + oui)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.contents && !data.contents.includes('Not Found') && !data.contents.includes('Error')) {
                             resultDiv.innerText = `MAC Input   : ${mac}\nOUI Prefix  : ${oui}\nCompany     : ${data.contents}\n(via fallback proxy)`;
                        } else {
                             resultDiv.innerText = `MAC Input   : ${mac}\nOUI Prefix  : ${oui}\nResult      : Vendor not found`;
                        }
                    })
                    .catch(fallbackError => {
                        resultDiv.innerText = `Error fetching MAC information.\nMake sure you have an internet connection and your browser is not blocking cross-origin requests (CORS).\nOriginal Error: ${error.message}`;
                    });
            }
        });
}
</script>
