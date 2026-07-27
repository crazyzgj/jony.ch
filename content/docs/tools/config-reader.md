---
title: "Configuration Reader"
weight: 6
bookToC: false
---

# Configuration Reader

Interactive Monaco Editor for Network Device Configurations. Select vendor syntax (Huawei VRP, Cisco IOS, Juniper JunOS, Arista EOS), view syntax highlighting, custom decorations for cipher keys, and analyze configurations directly in Monaco Editor.

<style>
  .cr-container {
    margin-top: 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  .cr-toolbar {
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

  .cr-toolbar-group {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
  }

  .cr-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
  }

  .cr-select {
    padding: 0.45rem 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 0.875rem;
    background-color: #ffffff;
    color: #0f172a;
    outline: none;
    cursor: pointer;
  }

  .cr-select:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
  }

  .cr-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.45rem 0.9rem;
    font-size: 0.85rem;
    font-weight: 600;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #334155;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .cr-btn:hover {
    background: #f1f5f9;
    color: #0f172a;
  }

  .cr-btn-primary {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
  }

  .cr-btn-primary:hover {
    background: #1d4ed8;
    color: #ffffff;
  }

  .cr-btn-danger {
    background: #fff1f2;
    color: #e11d48;
    border-color: #fecdd3;
  }

  .cr-btn-danger:hover {
    background: #ffe4e6;
  }

  .cr-editor-frame {
    border: 1px solid #cbd5e1;
    border-top: none;
    border-radius: 0 0 10px 10px;
    overflow: hidden;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
  }

  #monacoContainer {
    width: 100%;
    height: 650px;
  }

  /* Custom Monaco Cipher Highlight */
  .monaco-cipher-highlight {
    background-color: rgba(239, 68, 68, 0.18) !important;
    border: 1px dashed #ef4444 !important;
    border-radius: 3px;
  }
</style>

<div class="cr-container">
  <!-- Toolbar -->
  <div class="cr-toolbar">
    <div class="cr-toolbar-group">
      <span class="cr-label">Language:</span>
      <select id="vendorSelect" class="cr-select" onchange="onVendorChange()">
        <option value="huawei">Huawei VRP</option>
        <option value="cisco">Cisco IOS / NX-OS</option>
        <option value="juniper">Juniper JunOS</option>
        <option value="arista">Arista EOS</option>
      </select>
      <span class="cr-label" style="margin-left: 0.5rem;">Theme:</span>
      <select id="themeSelect" class="cr-select" onchange="onThemeChange()">
        <option value="vs">vs (Light)</option>
        <option value="vs-dark">vs-dark (Dark)</option>
      </select>
    </div>
    <div class="cr-toolbar-group">
      <button class="cr-btn" onclick="loadHuaweiSample()">📋 Huawei Sample</button>
      <button class="cr-btn" onclick="loadCiscoSample()">📋 Cisco Sample</button>
      <button class="cr-btn cr-btn-primary" onclick="analyzeConfiguration()">⚡ Analyze & Highlight</button>
      <button class="cr-btn" onclick="copyConfig()">📋 Copy</button>
      <button class="cr-btn" onclick="downloadConfig()">💾 Download</button>
      <button class="cr-btn cr-btn-danger" onclick="clearConfig()">🗑️ Clear</button>
    </div>
  </div>

  <!-- Monaco Editor Frame -->
  <div class="cr-editor-frame">
    <div id="monacoContainer"></div>
  </div>
</div>

<!-- RequireJS & Monaco Loader -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js"></script>

<script>
// Huawei sample configuration from user prompt
const HUAWEI_SAMPLE = `[V300R024C00SPC100]
#
 drop illegal-mac alarm
#
ipv6
#
authentication-profile name default_authen_profile
authentication-profile name dot1x_authen_profile
authentication-profile name dot1xmac_authen_profile
authentication-profile name mac_authen_profile
authentication-profile name multi_authen_profile
authentication-profile name portal_authen_profile
#
dns resolve 
#
dhcp enable
#
radius-server template default
#
pki realm default
 certificate-check none
#
ssl policy default_policy type server
 pki-realm default
 version tls1.2 
 ciphersuite rsa_aes_128_sha256 rsa_aes_256_sha256 ecdhe_rsa_aes128_gcm_sha256 ecdhe_rsa_aes256_gcm_sha384 
#
ike proposal default
 encryption-algorithm aes-256 aes-192 aes-128 
 dh group14 
 authentication-algorithm sha2-512 sha2-384 sha2-256 
 authentication-method pre-share
 integrity-algorithm hmac-sha2-256 
 prf hmac-sha2-256 
#
free-rule-template name default_free_rule
#
portal-access-profile name portal_access_profile
#
aaa
 authentication-scheme default
  authentication-mode local
 authentication-scheme radius
  authentication-mode radius
 authorization-scheme default
  authorization-mode local
 accounting-scheme default
  accounting-mode none
 local-aaa-user password policy administrator
 domain default
  authentication-scheme default
  accounting-scheme default
  radius-server default
 domain default_admin
  authentication-scheme default
  accounting-scheme default
#
web
 set fast-configuration state disable
#
firewall zone Local
#
mi-server
#
interface Vlanif1
 ip address 10.0.0.1 255.255.255.0
#
interface GigabitEthernet0/0/0
#
interface GigabitEthernet0/0/1
#
interface GigabitEthernet0/0/2
#
interface GigabitEthernet0/0/3
#
interface GigabitEthernet0/0/4
#
interface GigabitEthernet0/0/5
#
interface GigabitEthernet0/0/6
#
interface GigabitEthernet0/0/7
#
interface GigabitEthernet0/0/8
#
interface GigabitEthernet0/0/9
 ip address dhcp-alloc
#
interface GigabitEthernet0/0/10
#
interface Cellular0/0/0
#
interface NULL0
#
cellular profile default
 modem auto-recovery dial action modem-reboot fail-times 128
 modem auto-recovery icmp-unreachable action modem-reboot
 modem auto-recovery services-unavailable action modem-reboot test-times 0 interval 3600
#
undo icmp name timestamp-request receive
#
 snmp-agent trap enable
#
 http secure-server ssl-policy default_policy
 http secure-server enable
 http server permit interface GigabitEthernet0/0/0
#
fib regularly-refresh disable
#
 agile controller host 80.158.50.5 port 10020 vpn-instance underlay_3
#
user-interface con 0
 authentication-mode aaa
user-interface vty 0
 authentication-mode aaa
 user privilege level 15
user-interface vty 1 4
#
wlan ac
 traffic-profile name default
 security-profile name default
 security-profile name default-wds
  security wpa2 psk pass-phrase %^%#/6e3Sy(2D<@GzXGU&XXP>@])(3LI"8WL<zDnYWf)%^%# aes
 ssid-profile name default
 vap-profile name default
 wds-profile name default
 regulatory-domain-profile name default
 air-scan-profile name default
 rrm-profile name default
 radio-2g-profile name default
 radio-5g-profile name default
 wids-spoof-profile name default
 wids-profile name default
 ap-system-profile name default
 port-link-profile name default
 wired-port-profile name default
 ap-group name default
#
dot1x-access-profile name dot1x_access_profile
#
mac-access-profile name mac_access_profile
#
ops
#
autostart
#
secelog
#
 ms-channel 

#
return`;

const CISCO_SAMPLE = `! Cisco IOS Gateway Configuration Example
version 15.6
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname Core-Router-01
!
vrf definition CORP_INTERNAL
 rd 65000:100
 address-family ipv4
 exit-address-family
!
crypto ikev2 proposal DEFAULT-IKEV2-PROP
 encryption aes-cbc-256
 integrity sha256
 group 14
!
interface Loopback0
 ip address 10.255.255.1 255.255.255.255
!
interface GigabitEthernet0/0/0
 description WAN Uplink Primary
 vrf forwarding CORP_INTERNAL
 ip address 192.168.1.1 255.255.255.252
 duplex auto
 speed auto
!
interface GigabitEthernet0/0/1
 description LAN Trunk
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,100
!
router ospf 1 vrf CORP_INTERNAL
 router-id 10.255.255.1
 network 10.255.255.1 0.0.0.0 area 0
 network 192.168.1.0 0.0.0.3 area 0
!
ip route vrf CORP_INTERNAL 0.0.0.0 0.0.0.0 192.168.1.2
!
line con 0
 logging synchronous
line vty 0 4
 exec-timeout 15 0
 privilege level 15
 login local
 transport input ssh
!
end`;

let editorInstance = null;
let currentDecorations = [];

require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});

require(['vs/editor/editor.main'], function() {
  registerLanguages();

  const container = document.getElementById('monacoContainer');
  editorInstance = monaco.editor.create(container, {
    value: HUAWEI_SAMPLE,
    language: 'huawei-vrp',
    theme: 'vs',
    automaticLayout: true,
    fontFamily: '"Fira Code", Consolas, Monaco, monospace',
    fontSize: 13,
    minimap: { enabled: true },
    scrollBeyondLastLine: false,
    renderLineHighlight: 'all',
    folding: true,
    lineNumbers: 'on'
  });

  // Highlight initial sample
  analyzeConfiguration();
});

function registerLanguages() {
  // Huawei VRP Monarch Tokenizer
  monaco.languages.register({ id: 'huawei-vrp' });
  monaco.languages.setMonarchTokensProvider('huawei-vrp', {
    defaultToken: '',
    tokenPostfix: '.huawei',
    keywords: [
      'interface', 'ip', 'route-static', 'aaa', 'vlan', 'vpn-instance', 'wlan', 'ac', 'dhcp',
      'authentication-profile', 'security-profile', 'vap-profile', 'ssid-profile', 'wds-profile',
      'ssl', 'policy', 'ike', 'proposal', 'firewall', 'zone', 'snmp-agent', 'user-interface',
      'cellular', 'profile', 'undo', 'return', 'quit', 'ipv6', 'dns', 'pki', 'realm',
      'portal-access-profile', 'free-rule-template', 'ops', 'autostart', 'secelog', 'agile',
      'controller', 'fib', 'enable', 'disable', 'permit', 'description', 'bind', 'binding'
    ],
    tokenizer: {
      root: [
        [/^\s*#.*$/, 'comment'],
        [/^\[.*\]$/, 'keyword.flow'],
        [/%^%#[^%]+%^%#/, 'string.cipher'],
        [/\b(GigabitEthernet|Vlanif|Eth-Trunk|Cellular|NULL|LoopBack)\d+(\/\d+)*(\.\d+)?\b/, 'type.identifier'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });

  // Cisco IOS Monarch Tokenizer
  monaco.languages.register({ id: 'cisco-ios' });
  monaco.languages.setMonarchTokensProvider('cisco-ios', {
    defaultToken: '',
    tokenPostfix: '.cisco',
    keywords: [
      'interface', 'ip', 'route', 'router', 'ospf', 'bgp', 'line', 'vty', 'con', 'crypto',
      'ipsec', 'isakmp', 'vlan', 'username', 'enable', 'secret', 'hostname', 'no', 'end', 'exit',
      'vrf', 'definition', 'description', 'duplex', 'speed', 'switchport', 'mode', 'trunk', 'allowed'
    ],
    tokenizer: {
      root: [
        [/^\s*!.*$/, 'comment'],
        [/\b(GigabitEthernet|TenGigabitEthernet|FastEthernet|Loopback|Vlan)\d+(\/\d+)*\b/, 'type.identifier'],
        [/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, 'number.float'],
        [/[a-zA-Z0-9_\-]+/, {
          cases: {
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });
}

function onVendorChange() {
  const vendor = document.getElementById('vendorSelect').value;
  if (!editorInstance) return;
  
  const langMap = {
    'huawei': 'huawei-vrp',
    'cisco': 'cisco-ios',
    'juniper': 'huawei-vrp',
    'arista': 'cisco-ios'
  };
  monaco.editor.setModelLanguage(editorInstance.getModel(), langMap[vendor] || 'huawei-vrp');
  analyzeConfiguration();
}

function onThemeChange() {
  const theme = document.getElementById('themeSelect').value;
  if (!editorInstance) return;
  monaco.editor.setTheme(theme);
}

function loadHuaweiSample() {
  document.getElementById('vendorSelect').value = 'huawei';
  if (editorInstance) editorInstance.setValue(HUAWEI_SAMPLE);
  onVendorChange();
}

function loadCiscoSample() {
  document.getElementById('vendorSelect').value = 'cisco';
  if (editorInstance) editorInstance.setValue(CISCO_SAMPLE);
  onVendorChange();
}

function analyzeConfiguration() {
  if (!editorInstance) return;
  const content = editorInstance.getValue();
  const lines = content.split('\n');

  const newDecorations = [];
  lines.forEach((lineText, idx) => {
    const lineNum = idx + 1;
    const cipherRegex = /%^%#[^%]+%^%#/g;
    let match;
    while ((match = cipherRegex.exec(lineText)) !== null) {
      newDecorations.push({
        range: new monaco.Range(lineNum, match.index + 1, lineNum, match.index + 1 + match[0].length),
        options: {
          inlineClassName: 'monaco-cipher-highlight',
          hoverMessage: { value: '🔒 Encrypted Cipher Key String' }
        }
      });
    }
  });

  currentDecorations = editorInstance.deltaDecorations(currentDecorations, newDecorations);
}

function copyConfig() {
  if (!editorInstance) return;
  const content = editorInstance.getValue();
  navigator.clipboard.writeText(content).then(() => {
    alert('Configuration copied to clipboard!');
  });
}

function downloadConfig() {
  if (!editorInstance) return;
  const content = editorInstance.getValue();
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `config-${Date.now()}.cfg`;
  a.click();
}

function clearConfig() {
  if (editorInstance) editorInstance.setValue('');
}
</script>
