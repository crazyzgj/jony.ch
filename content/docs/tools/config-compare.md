---
title: "Configuration Compare"
weight: 7
bookToC: false
---

# Configuration Compare

Interactive Monaco Diff Editor for comparing network device configurations side-by-side. Includes vendor syntax highlighting (Huawei VRP, Cisco IOS, Juniper JunOS, Arista EOS), **keyword color highlighting** (such as **`vpn-instance`** highlighted in a special color), visual code **minimap thumbnail**, and persistent **Full Window** view mode.

<style>
  .cc-container {
    margin-top: 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  /* Full Window Mode */
  .cc-container.cc-full-window {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 99999 !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #ffffff;
    border-radius: 0 !important;
  }
  .cc-container.cc-full-window .cc-toolbar {
    border-radius: 0 !important;
  }
  .cc-container.cc-full-window .cc-main-layout {
    height: calc(100vh - 58px) !important;
    border-radius: 0 !important;
  }
  .cc-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 10px 10px 0 0;
  }
  .cc-toolbar-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .cc-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
  }
  .cc-select {
    padding: 0.45rem 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 0.875rem;
    background-color: #ffffff;
    color: #0f172a;
    outline: none;
    cursor: pointer;
  }
  .cc-select:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
  }
  .cc-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.45rem 0.85rem;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #334155;
    font-size: 0.85rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    user-select: none;
  }
  .cc-btn:hover {
    background: #f1f5f9;
    color: #0f172a;
    border-color: #94a3b8;
  }
  .cc-btn-primary {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
  }
  .cc-btn-primary:hover {
    background: #1d4ed8;
    color: #ffffff;
    border-color: #1d4ed8;
  }
  .cc-badge {
    padding: 0.2rem 0.55rem;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 12px;
    background: #e2e8f0;
    color: #334155;
  }
  .cc-badge-success {
    background: #dcfce7;
    color: #166534;
  }
  .cc-badge-danger {
    background: #fee2e2;
    color: #991b1b;
  }
  .cc-badge-info {
    background: #dbeafe;
    color: #1e40af;
  }

  /* Main Editor Layout */
  .cc-main-layout {
    display: flex;
    flex-direction: column;
    height: 720px;
    border: 1px solid #cbd5e1;
    border-top: none;
    border-radius: 0 0 10px 10px;
    overflow: hidden;
    background: #ffffff;
    position: relative;
  }
  #diffContainer {
    width: 100%;
    height: 100%;
  }

  /* Dark Theme */
  .cc-container.cc-dark {
    background: #0f172a;
  }
  .cc-container.cc-dark .cc-toolbar {
    background: #1e293b;
    border-color: #334155;
  }
  .cc-container.cc-dark .cc-label {
    color: #94a3b8;
  }
  .cc-container.cc-dark .cc-select {
    background: #0f172a;
    border-color: #334155;
    color: #f8fafc;
  }
  .cc-container.cc-dark .cc-btn {
    background: #0f172a;
    border-color: #334155;
    color: #cbd5e1;
  }
  .cc-container.cc-dark .cc-btn:hover {
    background: #334155;
    color: #ffffff;
  }
  .cc-container.cc-dark .cc-main-layout {
    border-color: #334155;
    background: #1e293b;
  }
</style>

<div class="cc-container" id="ccContainer">
  <!-- Toolbar -->
  <div class="cc-toolbar">
    <div class="cc-toolbar-group">
      <button class="cc-btn" id="fullWindowBtn" onclick="toggleFullWindow()">⛶ Full Window</button>
      <span class="cc-label" style="margin-left: 0.4rem;">Language:</span>
      <select id="vendorSelect" class="cc-select" onchange="onVendorChange()">
        <option value="huawei">Huawei VRP</option>
        <option value="cisco">Cisco IOS / NX-OS</option>
        <option value="juniper">Juniper JunOS</option>
        <option value="arista">Arista EOS</option>
      </select>
      <span class="cc-label" style="margin-left: 0.4rem;">Theme:</span>
      <select id="themeSelect" class="cc-select" onchange="onThemeChange()">
        <option value="vs">Light</option>
        <option value="vs-dark">Dark</option>
      </select>
      <span class="cc-label" style="margin-left: 0.4rem;">View Mode:</span>
      <select id="viewModeSelect" class="cc-select" onchange="onViewModeChange()">
        <option value="side-by-side">Side-by-Side</option>
        <option value="inline">Inline</option>
      </select>
    </div>
    <div class="cc-toolbar-group">
      <span class="cc-badge cc-badge-success" id="diffAddCount">+0 Added</span>
      <span class="cc-badge cc-badge-danger" id="diffDelCount">-0 Deleted</span>
      <button class="cc-btn" onclick="swapConfigs()">🔀 Swap</button>
      <button class="cc-btn cc-btn-primary" onclick="loadSampleConfig()">📑 Sample Config</button>
      <button class="cc-btn" onclick="clearAll()">🗑️ Clear</button>
    </div>
  </div>

  <!-- Monaco Diff Container -->
  <div class="cc-main-layout">
    <div id="diffContainer"></div>
  </div>
</div>

<!-- RequireJS & Monaco Loader -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js"></script>

<script>
const HUAWEI_SAMPLE_ORIGINAL = `#
sysname Core-Switch-A
#
ip vpn-instance VPN_A
 ipv4-family
  route-distinguisher 100:1
  vpn-target 100:1 export-extcommunity
  vpn-target 100:1 import-extcommunity
#
vlan 10
 description Management_VLAN
#
vlan 20
 description User_VLAN_20
#
interface Vlanif10
 ip binding vpn-instance VPN_A
 ip address 192.168.10.1 255.255.255.0
#
interface Vlanif20
 ip address 192.168.20.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 port link-type access
 port default vlan 10
#
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20
#
ip route-static vpn-instance VPN_A 0.0.0.0 0.0.0.0 10.1.1.254
#
return`;

const HUAWEI_SAMPLE_MODIFIED = `#
sysname Core-Switch-A
#
ip vpn-instance VPN_A
 ipv4-family
  route-distinguisher 100:1
  vpn-target 100:1 export-extcommunity
  vpn-target 100:1 import-extcommunity
#
ip vpn-instance VPN_B
 ipv4-family
  route-distinguisher 200:1
  vpn-target 200:1 export-extcommunity
  vpn-target 200:1 import-extcommunity
#
vlan 10
 description Management_VLAN
#
vlan 20
 description User_VLAN_20
#
vlan 30
 description Guest_VLAN_30
#
interface Vlanif10
 ip binding vpn-instance VPN_A
 ip address 192.168.10.254 255.255.255.0
#
interface Vlanif20
 ip address 192.168.20.1 255.255.255.0
#
interface Vlanif30
 ip binding vpn-instance VPN_B
 ip address 192.168.30.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 port link-type access
 port default vlan 10
 undo shutdown
#
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20 30
#
ip route-static vpn-instance VPN_A 0.0.0.0 0.0.0.0 10.1.1.254
ip route-static vpn-instance VPN_B 0.0.0.0 0.0.0.0 10.2.2.254
#
return`;

let diffEditorInstance = null;
let originalModel = null;
let modifiedModel = null;

require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});

require(['vs/editor/editor.main'], function() {
  registerLanguages();

  const container = document.getElementById('diffContainer');
  diffEditorInstance = monaco.editor.createDiffEditor(container, {
    originalEditable: true,
    readOnly: false,
    theme: 'vs-config',
    automaticLayout: true,
    fontFamily: '"Fira Code", Consolas, Monaco, monospace',
    fontSize: 13,
    renderSideBySide: true,
    folding: false, // Disables folding as requested
    minimap: {
      enabled: true, // Enables thumbnail / minimap as requested
      scale: 2,
      maxColumn: 120,
      showSlider: 'always',
      renderCharacters: true
    },
    scrollBeyondLastLine: false,
    contextmenu: false
  });

  const savedOrig = localStorage.getItem('configCompare_savedOriginal');
  const savedMod = localStorage.getItem('configCompare_savedModified');
  const initialOrig = (savedOrig !== null && savedOrig !== undefined) ? savedOrig : HUAWEI_SAMPLE_ORIGINAL;
  const initialMod = (savedMod !== null && savedMod !== undefined) ? savedMod : HUAWEI_SAMPLE_MODIFIED;

  originalModel = monaco.editor.createModel(initialOrig, 'huawei-vrp');
  modifiedModel = monaco.editor.createModel(initialMod, 'huawei-vrp');

  diffEditorInstance.setModel({
    original: originalModel,
    modified: modifiedModel
  });

  originalModel.onDidChangeContent(() => {
    localStorage.setItem('configCompare_savedOriginal', originalModel.getValue());
    updateDiffStats();
  });

  modifiedModel.onDidChangeContent(() => {
    localStorage.setItem('configCompare_savedModified', modifiedModel.getValue());
    updateDiffStats();
  });

  diffEditorInstance.onDidUpdateDiff(updateDiffStats);

  restoreState();
  updateDiffStats();
});

function defineMonacoThemes() {
  monaco.editor.defineTheme('vs-config', {
    base: 'vs',
    inherit: true,
    rules: [
      { token: 'keyword.vpn', foreground: '9333EA', fontStyle: 'bold' },
      { token: 'keyword.interface', foreground: '0284C7', fontStyle: 'bold' },
      { token: 'keyword.vlan', foreground: '059669', fontStyle: 'bold' },
      { token: 'keyword.route', foreground: '4F46E5', fontStyle: 'bold' },
      { token: 'keyword.security', foreground: 'D97706', fontStyle: 'bold' },
      { token: 'keyword.undo', foreground: 'DC2626', fontStyle: 'bold' },
      { token: 'keyword.profile', foreground: '0891B2', fontStyle: 'bold' },
      { token: 'keyword', foreground: '2563EB', fontStyle: 'bold' },
      { token: 'comment', foreground: '64748B', fontStyle: 'italic' },
      { token: 'string.cipher', foreground: 'E11D48', fontStyle: 'bold' },
      { token: 'type.identifier', foreground: '0D9488' },
      { token: 'number.float', foreground: 'D97706' }
    ],
    colors: {}
  });

  monaco.editor.defineTheme('vs-dark-config', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword.vpn', foreground: 'C084FC', fontStyle: 'bold' },
      { token: 'keyword.interface', foreground: '38BDF8', fontStyle: 'bold' },
      { token: 'keyword.vlan', foreground: '34D399', fontStyle: 'bold' },
      { token: 'keyword.route', foreground: '818CF8', fontStyle: 'bold' },
      { token: 'keyword.security', foreground: 'FBBF24', fontStyle: 'bold' },
      { token: 'keyword.undo', foreground: 'F87171', fontStyle: 'bold' },
      { token: 'keyword.profile', foreground: '22D3EE', fontStyle: 'bold' },
      { token: 'keyword', foreground: '60A5FA', fontStyle: 'bold' },
      { token: 'comment', foreground: '94A3B8', fontStyle: 'italic' },
      { token: 'string.cipher', foreground: 'FB7185', fontStyle: 'bold' },
      { token: 'type.identifier', foreground: '2DD4BF' },
      { token: 'number.float', foreground: 'FBBF24' }
    ],
    colors: {}
  });
}

function registerLanguages() {
  defineMonacoThemes();

  // Huawei VRP Tokenizer
  monaco.languages.register({ id: 'huawei-vrp' });
  monaco.languages.setMonarchTokensProvider('huawei-vrp', {
    defaultToken: '',
    tokenPostfix: '.huawei',
    vpnKeywords: ['vpn-instance', 'vpn', 'vrf'],
    interfaceKeywords: ['interface', 'eth-trunk', 'port', 'GigabitEthernet', '10GE', '40GE', 'GE', 'XGigabitEthernet', 'Vlanif', 'vlanif', 'Cellular', 'NULL', 'LoopBack', 'Loopback'],
    vlanKeywords: ['vlan', 'vlan-id'],
    routeKeywords: ['route-static', 'route', 'router', 'ospf', 'bgp', 'isis', 'rip'],
    securityKeywords: ['aaa', 'domain', 'radius-server', 'authentication-scheme', 'authorization-scheme', 'accounting-scheme', 'acl', 'rule', 'permit', 'deny', 'security-profile', 'firewall', 'zone', 'policy', 'ike', 'proposal', 'pki', 'ssl', 'local-user'],
    undoKeywords: ['undo', 'no'],
    profileKeywords: ['authentication-profile', 'vap-profile', 'ssid-profile', 'wds-profile', 'portal-access-profile', 'free-rule-template'],
    keywords: [
      'ip', 'wlan', 'ac', 'dhcp', 'snmp-agent', 'user-interface', 'profile', 'return', 'quit', 'ipv6', 'dns', 'realm',
      'ops', 'autostart', 'secelog', 'agile', 'controller', 'fib', 'enable', 'disable', 'description', 'bind', 'binding'
    ],
    tokenizer: {
      root: [
        [/^\s*#.*$/, 'comment'],
        [/^\[.*\]$/, 'keyword.flow'],
        [/%^%#[^%]+%^%#/, 'string.cipher'],
        [/\b(GigabitEthernet|40GE|10GE|GE|XGigabitEthernet|Eth-Trunk|Vlanif|vlanif|Cellular|NULL|LoopBack|Loopback)\d+(\/\d+)*(\.\d+)?\b/i, 'type.identifier'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@vpnKeywords': 'keyword.vpn',
            '@interfaceKeywords': 'keyword.interface',
            '@vlanKeywords': 'keyword.vlan',
            '@routeKeywords': 'keyword.route',
            '@securityKeywords': 'keyword.security',
            '@undoKeywords': 'keyword.undo',
            '@profileKeywords': 'keyword.profile',
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });

  // Cisco IOS / NX-OS Tokenizer
  monaco.languages.register({ id: 'cisco-ios' });
  monaco.languages.setMonarchTokensProvider('cisco-ios', {
    defaultToken: '',
    tokenPostfix: '.cisco',
    vpnKeywords: ['vrf', 'definition'],
    interfaceKeywords: ['interface', 'trunk', 'switchport', 'GigabitEthernet', 'TenGigabitEthernet', 'FastEthernet', 'Loopback', 'Vlan'],
    vlanKeywords: ['vlan'],
    routeKeywords: ['route', 'router', 'ospf', 'bgp', 'eigrp'],
    securityKeywords: ['crypto', 'ipsec', 'isakmp', 'username', 'secret', 'enable', 'permit', 'deny'],
    undoKeywords: ['no'],
    keywords: [
      'ip', 'line', 'vty', 'con', 'hostname', 'end', 'exit', 'description', 'duplex', 'speed', 'mode', 'allowed'
    ],
    tokenizer: {
      root: [
        [/^\s*!.*$/, 'comment'],
        [/\b(GigabitEthernet|TenGigabitEthernet|FastEthernet|Loopback|Vlan)\d+(\/\d+)*\b/i, 'type.identifier'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@vpnKeywords': 'keyword.vpn',
            '@interfaceKeywords': 'keyword.interface',
            '@vlanKeywords': 'keyword.vlan',
            '@routeKeywords': 'keyword.route',
            '@securityKeywords': 'keyword.security',
            '@undoKeywords': 'keyword.undo',
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });

  // Juniper JunOS Tokenizer
  monaco.languages.register({ id: 'juniper-junos' });
  monaco.languages.setMonarchTokensProvider('juniper-junos', {
    defaultToken: '',
    tokenPostfix: '.junos',
    vpnKeywords: ['routing-instances', 'instance-type', 'vrf'],
    interfaceKeywords: ['interfaces', 'unit', 'family', 'inet'],
    vlanKeywords: ['vlan-id', 'vlans'],
    routeKeywords: ['routing-options', 'static', 'route', 'bgp', 'ospf'],
    securityKeywords: ['security', 'policies', 'zones', 'policy', 'permit', 'deny'],
    undoKeywords: ['delete'],
    keywords: ['system', 'host-name', 'services', 'protocols', 'set'],
    tokenizer: {
      root: [
        [/^\s*#.*$/, 'comment'],
        [/^\s*\*.*$/, 'comment'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@vpnKeywords': 'keyword.vpn',
            '@interfaceKeywords': 'keyword.interface',
            '@vlanKeywords': 'keyword.vlan',
            '@routeKeywords': 'keyword.route',
            '@securityKeywords': 'keyword.security',
            '@undoKeywords': 'keyword.undo',
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });

  // Arista EOS Tokenizer
  monaco.languages.register({ id: 'arista-eos' });
  monaco.languages.setMonarchTokensProvider('arista-eos', {
    defaultToken: '',
    tokenPostfix: '.arista',
    vpnKeywords: ['vrf', 'instance'],
    interfaceKeywords: ['interface', 'Ethernet', 'Management', 'Loopback', 'Vlan'],
    vlanKeywords: ['vlan'],
    routeKeywords: ['ip route', 'router', 'bgp', 'ospf'],
    securityKeywords: ['enable', 'secret', 'username', 'role'],
    undoKeywords: ['no'],
    keywords: ['hostname', 'transceiver', 'spanning-tree', 'mode'],
    tokenizer: {
      root: [
        [/^\s*!.*$/, 'comment'],
        [/\b(Ethernet|Management|Loopback|Vlan)\d+(\/\d+)*\b/i, 'type.identifier'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@vpnKeywords': 'keyword.vpn',
            '@interfaceKeywords': 'keyword.interface',
            '@vlanKeywords': 'keyword.vlan',
            '@routeKeywords': 'keyword.route',
            '@securityKeywords': 'keyword.security',
            '@undoKeywords': 'keyword.undo',
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });
}

function updateDiffStats() {
  if (!diffEditorInstance) return;
  const lineChanges = diffEditorInstance.getLineChanges() || [];
  let addedLines = 0;
  let deletedLines = 0;

  lineChanges.forEach(change => {
    if (change.modifiedEndLineNumber >= change.modifiedStartLineNumber) {
      addedLines += (change.modifiedEndLineNumber - change.modifiedStartLineNumber + 1);
    }
    if (change.originalEndLineNumber >= change.originalStartLineNumber) {
      deletedLines += (change.originalEndLineNumber - change.originalStartLineNumber + 1);
    }
  });

  document.getElementById('diffAddCount').innerText = `+${addedLines} Added`;
  document.getElementById('diffDelCount').innerText = `-${deletedLines} Deleted`;
}

function toggleFullWindow(forceState) {
  const container = document.getElementById('ccContainer');
  const btn = document.getElementById('fullWindowBtn');
  if (!container) return;

  const isFull = forceState !== undefined ? forceState : !container.classList.contains('cc-full-window');
  if (isFull) {
    container.classList.add('cc-full-window');
    if (btn) btn.innerText = '🗗 Exit Full Window';
    localStorage.setItem('configCompare_fullWindow', 'true');
  } else {
    container.classList.remove('cc-full-window');
    if (btn) btn.innerText = '⛶ Full Window';
    localStorage.setItem('configCompare_fullWindow', 'false');
  }

  if (diffEditorInstance) {
    diffEditorInstance.layout();
  }
}

function restoreState() {
  const savedFull = localStorage.getItem('configCompare_fullWindow');
  if (savedFull === 'true') {
    toggleFullWindow(true);
  }

  const savedTheme = localStorage.getItem('configCompare_theme');
  if (savedTheme) {
    const themeSelect = document.getElementById('themeSelect');
    if (themeSelect) {
      themeSelect.value = savedTheme;
      onThemeChange();
    }
  }
}

function onVendorChange() {
  const vendor = document.getElementById('vendorSelect').value;
  if (!originalModel || !modifiedModel) return;

  const langMap = {
    'huawei': 'huawei-vrp',
    'cisco': 'cisco-ios',
    'juniper': 'juniper-junos',
    'arista': 'arista-eos'
  };
  const targetLang = langMap[vendor] || 'huawei-vrp';

  monaco.editor.setModelLanguage(originalModel, targetLang);
  monaco.editor.setModelLanguage(modifiedModel, targetLang);
}

function onThemeChange() {
  const theme = document.getElementById('themeSelect').value;
  if (!diffEditorInstance) return;

  const targetTheme = theme.includes('dark') ? 'vs-dark-config' : 'vs-config';
  monaco.editor.setTheme(targetTheme);
  localStorage.setItem('configCompare_theme', theme);

  const container = document.getElementById('ccContainer');
  if (container) {
    if (theme.includes('dark')) {
      container.classList.add('cc-dark');
    } else {
      container.classList.remove('cc-dark');
    }
  }
}

function onViewModeChange() {
  const mode = document.getElementById('viewModeSelect').value;
  if (!diffEditorInstance) return;

  diffEditorInstance.updateOptions({
    renderSideBySide: mode === 'side-by-side'
  });
}

function swapConfigs() {
  if (!originalModel || !modifiedModel) return;
  const leftText = originalModel.getValue();
  const rightText = modifiedModel.getValue();
  originalModel.setValue(rightText);
  modifiedModel.setValue(leftText);
  updateDiffStats();
}

function loadSampleConfig() {
  if (!originalModel || !modifiedModel) return;
  originalModel.setValue(HUAWEI_SAMPLE_ORIGINAL);
  modifiedModel.setValue(HUAWEI_SAMPLE_MODIFIED);
  document.getElementById('vendorSelect').value = 'huawei';
  onVendorChange();
  updateDiffStats();
}

function clearAll() {
  if (!originalModel || !modifiedModel) return;
  originalModel.setValue('');
  modifiedModel.setValue('');
  updateDiffStats();
}
</script>
