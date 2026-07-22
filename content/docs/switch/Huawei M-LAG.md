---
title: "Huawei M-LAG"
weight: 4
bookCollapseSection: false
---

# Huawei M-LAG technical details
## Concept
Multichassis Link Aggregation Group (M-LAG) implements link aggregation among multiple devices. In a dual-active system, one device is connected to two devices through M-LAG to achieve device-level link reliability.

**Advantages:**
- **High reliability:** M-LAG protects link reliability for entire devices.
- **Simplified network and configuration:** M-LAG is a horizontal virtualization technology that virtualizes two dual-homed devices into one device. M-LAG prevents loops on a Layer 2 network and implements redundancy.
- **Independent upgrade:** Two devices can be upgraded independently, preventing service interruption.

## Configuration
Based on Huawei CE switches (V200R025C00), M-LAG configuration supports multiple STP modes:
1. **Root bridge mode:** The M-LAG master and backup devices must be configured as root bridges with the same bridge ID.
2. **V-STP mode (Recommended):** V-STP virtualizes the M-LAG master and backup devices enabled with STP into one device to perform STP calculation. This mode supports flexible networking and multi-level M-LAG.
3. **V-VBST mode:** Virtualizes devices enabled with VBST into one device to perform VBST calculation, solving port blocking problems after STP is enabled.

When configuring the DFS Group on CE V200R025C00, you can specify the peer IP address to negotiate the HB DFS master/backup status and improve reliability:
`source ip <ip-address> [ peer <peer-ip-address> ]`

## Configuration Generator

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.premium-generator-wrapper {
  font-family: 'Inter', sans-serif;
  margin: 30px 0;
  padding: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(118, 75, 162, 0.2);
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.config-generator {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 14px;
  padding: 32px;
  color: #1a202c;
  position: relative;
  overflow: hidden;
}

:root[data-theme='dark'] .config-generator, .dark .config-generator {
  background: rgba(30, 30, 36, 0.95);
  color: #e2e8f0;
}

.config-generator h3 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 1.5rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:root[data-theme='dark'] .config-generator h3, .dark .config-generator h3 {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: #4a5568;
  transition: color 0.3s ease;
}

:root[data-theme='dark'] .form-group label, .dark .form-group label {
  color: #a0aec0;
}

.form-group select, .form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: 'Inter', sans-serif;
  background: #f7fafc;
  color: #2d3748;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group select:focus, .form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  background: #ffffff;
}

:root[data-theme='dark'] .form-group select, :root[data-theme='dark'] .form-group input, .dark .form-group select, .dark .form-group input {
  background: #2d3748;
  border-color: #4a5568;
  color: #e2e8f0;
}

:root[data-theme='dark'] .form-group select:focus, :root[data-theme='dark'] .form-group input:focus, .dark .form-group select:focus, .dark .form-group input:focus {
  background: #1a202c;
  border-color: #a18cd1;
  box-shadow: 0 0 0 3px rgba(161, 140, 209, 0.2);
}

.form-group small {
  color: #718096;
  font-size: 0.8rem;
  margin-top: 6px;
}

:root[data-theme='dark'] .form-group small, .dark .form-group small {
  color: #a0aec0;
}

.btn-generate {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 28px;
  font-size: 1.05rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  width: 100%;
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3);
}

.btn-generate:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4);
}

.btn-generate:active {
  transform: translateY(0);
}

.config-output-area {
  margin-top: 30px;
  animation: slideDown 0.4s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.config-output-area h4 {
  margin-bottom: 12px;
  color: #2d3748;
}

:root[data-theme='dark'] .config-output-area h4, .dark .config-output-area h4 {
  color: #e2e8f0;
}

.config-output-area pre {
  background: #1e1e1e !important;
  color: #d4d4d4 !important;
  padding: 20px !important;
  border-radius: 10px !important;
  overflow-x: auto !important;
  font-family: 'Fira Code', 'Courier New', monospace !important;
  font-size: 0.95rem !important;
  border: 1px solid #333 !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
}

.config-output-area code {
  font-family: inherit !important;
}

.mac-input-wrapper {
  transition: all 0.3s ease;
  opacity: 1;
  max-height: 100px;
  overflow: hidden;
}

.mac-input-wrapper.hidden {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
  border: none;
}
</style>

<div class="premium-generator-wrapper">
  <div class="config-generator" id="mlag-generator">
    <h3>M-LAG Dynamic Configurator</h3>
    <div class="form-row">
      <div class="form-group">
        <label for="dev-type">Device Type</label>
        <select id="dev-type">
          <option value="CE">Huawei CE switch</option>
          <option value="S">Huawei S switches</option>
        </select>
      </div>
      <div class="form-group">
        <label for="dev-version">Version</label>
        <select id="dev-version"></select>
        <small>Select the exact or closest approximate version.</small>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label for="stp-mode">STP Mode</label>
        <select id="stp-mode">
          <option value="root-bridge">Root bridge mode (根桥模式)</option>
          <option value="v-stp">V-STP mode (v-stp模式)</option>
          <option value="v-vbst">V-VBST mode (v-vbst模式)</option>
        </select>
      </div>
      <div class="form-group mac-input-wrapper" id="mac-input-container">
        <label for="root-mac">Root Bridge MAC</label>
        <input type="text" id="root-mac" placeholder="e.g. 00e0-fc00-0001">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label for="local-ip">DFS Local IP</label>
        <input type="text" id="local-ip" value="10.1.1.1" placeholder="e.g. 10.1.1.1">
      </div>
      <div class="form-group">
        <label for="peer-ip">DFS Peer IP (Optional)</label>
        <input type="text" id="peer-ip" placeholder="e.g. 10.1.1.2">
      </div>
    </div>
    <button class="btn-generate" id="btn-generate">
      <span style="margin-right: 8px;">⚡</span> Generate Configuration
    </button>
    <div class="config-output-area" style="display: none;" id="output-area">
      <h4>Generated Configuration:</h4>
      <pre><code id="config-output"></code></pre>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const devType = document.getElementById('dev-type');
  const devVersion = document.getElementById('dev-version');
  const stpMode = document.getElementById('stp-mode');
  const macContainer = document.getElementById('mac-input-container');
  const rootMac = document.getElementById('root-mac');
  const localIp = document.getElementById('local-ip');
  const peerIp = document.getElementById('peer-ip');
  const btnGenerate = document.getElementById('btn-generate');
  const outputArea = document.getElementById('output-area');
  const configOutput = document.getElementById('config-output');

  const versions = {
    'CE': ['V200R025C00', 'V500R025C00'],
    'S': ['V200R025C00', 'V60R025C00']
  };

  function updateVersions() {
    const type = devType.value;
    devVersion.innerHTML = '';
    versions[type].forEach(ver => {
      const opt = document.createElement('option');
      opt.value = ver;
      opt.textContent = ver;
      devVersion.appendChild(opt);
    });
  }

  function toggleMacInput() {
    if (stpMode.value === 'root-bridge') {
      macContainer.classList.remove('hidden');
    } else {
      macContainer.classList.add('hidden');
    }
  }

  devType.addEventListener('change', updateVersions);
  stpMode.addEventListener('change', toggleMacInput);

  btnGenerate.addEventListener('click', function() {
    let btnOriginalText = btnGenerate.innerHTML;
    btnGenerate.innerHTML = '<span style="margin-right: 8px;">⏳</span> Generating...';
    btnGenerate.style.opacity = '0.8';
    
    setTimeout(() => {
      let output = `! System view\n`;
      output += `system-view\n`;
      output += `sysname SwitchA\n\n`;

      output += `! Equipment: ${devType.options[devType.selectedIndex].text}\n`;
      output += `! Target Version: ${devVersion.value} (or approximate)\n\n`;

      if (stpMode.value === 'root-bridge') {
        const mac = rootMac.value || '00e0-fc00-0001';
        output += `! STP Mode: Root Bridge\n`;
        output += `stp mode rstp\n`;
        output += `stp root primary\n`;
        output += `! Note: Please ensure the peer device uses the same bridge ID.\n`;
        output += `! Root Bridge MAC configured as ${mac}\n`;
        output += `lacp system-mac ${mac}\n`;
      } else if (stpMode.value === 'v-stp') {
        output += `! STP Mode: V-STP\n`;
        output += `stp v-stp enable\n`;
      } else if (stpMode.value === 'v-vbst') {
        output += `! STP Mode: V-VBST\n`;
        output += `stp v-vbst enable\n`;
      }

      output += `\n! DFS Group Configuration\n`;
      output += `dfs-group 1\n`;
      output += ` priority 150\n`;
      let sourceIpCmd = ` source ip ${localIp && localIp.value ? localIp.value : '10.1.1.1'}`;
      if (devType.value === 'CE' && devVersion.value === 'V200R025C00' && peerIp && peerIp.value) {
        sourceIpCmd += ` peer ${peerIp.value}`;
      } else if (peerIp && peerIp.value) {
        sourceIpCmd += ` peer ${peerIp.value}`;
      }
      output += sourceIpCmd + `\n`;
      
      output += `\n! Peer-link Configuration\n`;
      output += `interface Eth-Trunk 0\n`;
      if (stpMode.value === 'root-bridge') {
        output += ` stp disable\n`;
      }
      output += ` trunkport m-lag peer-link 1\n`;
      
      output += `\n! M-LAG Member Interface Configuration\n`;
      output += `interface Eth-Trunk 10\n`;
      output += ` mode lacp-static\n`;
      output += ` dfs-group 1 m-lag 1\n`;

      output += `\n! Note: The above parameters are base templates derived from the training outputs\n`;
      output += `! located in doc_to_training/switch/m-lag/. Further parameters can be dynamically added later.\n`;

      configOutput.textContent = output;
      outputArea.style.display = 'block';
      
      btnGenerate.innerHTML = '<span style="margin-right: 8px;">✅</span> Generated Successfully';
      btnGenerate.style.opacity = '1';
      
      setTimeout(() => {
        btnGenerate.innerHTML = btnOriginalText;
      }, 2000);
    }, 400); // Simulate network or calculation delay for micro-animation effect
  });

  // Initialize
  updateVersions();
  toggleMacInput();
});
</script>