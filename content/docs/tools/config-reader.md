---
title: "Configuration Reader"
weight: 6
bookToC: false
---

# Configuration Reader

Interactive Monaco Editor for Network Device Configurations. Select vendor syntax (Huawei VRP, Cisco IOS, Juniper JunOS, Arista EOS), automatically fold configurations by category (e.g., matching 2-word prefixes like `authentication-profile name` or indented blocks), and use the interactive **Config Index** sidebar to search sections, inspect **VPN Instance**, **Interface**, **AAA Scheme**, and **Profile References** with full definition blocks, and maximize to browser full window with saved state.

<style>
  .cr-container {
    margin-top: 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  /* Browser Full Window Mode */
  .cr-container.cr-full-window {
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
  .cr-container.cr-full-window .cr-toolbar {
    border-radius: 0 !important;
  }
  .cr-container.cr-full-window .cr-main-layout {
    height: calc(100vh - 58px) !important;
    border-radius: 0 !important;
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
    gap: 0.5rem;
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
  .cr-find-container {
    position: relative;
    display: inline-flex;
    align-items: center;
  }
  .cr-search-input {
    padding: 0.45rem 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 0.85rem;
    background-color: #ffffff;
    color: #0f172a;
    outline: none;
    width: 170px;
    transition: all 0.15s ease;
  }
  .cr-search-input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
    width: 220px;
  }
  .cr-find-dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 340px;
    max-height: 300px;
    overflow-y: auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    margin-top: 4px;
    z-index: 9999;
    padding: 4px 0;
  }
  .cr-find-dropdown.active {
    display: block;
  }
  .cr-find-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 12px;
    font-size: 0.82rem;
    color: #334155;
    cursor: pointer;
    border-bottom: 1px solid #f1f5f9;
    transition: background 0.15s ease;
  }
  .cr-find-item:hover {
    background: #eff6ff;
    color: #1d4ed8;
  }
  .cr-find-line {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.72rem;
    color: #2563eb;
    background: #dbeafe;
    padding: 1px 6px;
    border-radius: 4px;
    margin-right: 8px;
    flex-shrink: 0;
  }
  .cr-find-text {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }
  .cr-find-empty {
    padding: 12px;
    font-size: 0.82rem;
    color: #94a3b8;
    text-align: center;
  }
  .cr-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.45rem 0.85rem;
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
  /* Main Split Layout: Sidebar + Monaco Editor */
  .cr-main-layout {
    display: flex;
    border: 1px solid #cbd5e1;
    border-top: none;
    border-radius: 0 0 10px 10px;
    overflow: hidden;
    height: 680px;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    position: relative;
  }
  /* Sidebar Styles (Default Visible) */
  .cr-sidebar {
    width: 290px;
    flex-shrink: 0;
    border-right: 1px solid #e2e8f0;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
    transition: width 0.2s ease;
  }
  .cr-sidebar.collapsed {
    display: none !important;
    width: 0 !important;
    margin-left: 0 !important;
    overflow: hidden !important;
    border-right: none !important;
  }
  .cr-sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0.85rem;
    background: #f1f5f9;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.875rem;
    font-weight: 700;
    color: #1e293b;
  }
  .cr-sidebar-title {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .cr-badge {
    font-size: 0.75rem;
    font-weight: 600;
    background: #2563eb;
    color: #ffffff;
    padding: 1px 7px;
    border-radius: 12px;
  }
  .cr-sidebar-search {
    padding: 0.6rem 0.85rem;
    border-bottom: 1px solid #e2e8f0;
    background: #ffffff;
  }
  .cr-sidebar-search input {
    width: 100%;
    padding: 0.4rem 0.65rem;
    font-size: 0.82rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    outline: none;
    box-sizing: border-box;
  }
  .cr-sidebar-search input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
  }
  .cr-index-list {
    flex: 1;
    overflow-y: auto;
    padding: 0.35rem 0;
  }
  .cr-index-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.45rem 0.85rem;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
    font-size: 0.82rem;
    color: #334155;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .cr-index-item:hover {
    background: #e2e8f0;
    color: #0f172a;
  }
  .cr-index-item.active {
    background: #eff6ff;
    color: #1d4ed8;
    font-weight: 600;
    border-left: 3px solid #2563eb;
  }
  .cr-index-left {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    min-width: 0;
    flex: 1;
  }
  .cr-index-icon {
    font-size: 0.85rem;
    flex-shrink: 0;
  }
  .cr-index-title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .cr-index-line {
    font-size: 0.72rem;
    color: #64748b;
    background: #e2e8f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    flex-shrink: 0;
    margin-left: 0.4rem;
  }
  .cr-index-count {
    font-size: 0.7rem;
    font-weight: 600;
    color: #2563eb;
    background: #dbeafe;
    border: 1px solid #bfdbfe;
    padding: 0 5px;
    border-radius: 10px;
    flex-shrink: 0;
  }
  .cr-vpn-ref-badge {
    font-size: 0.7rem;
    font-weight: 600;
    color: #059669;
    background: #d1fae5;
    border: 1px solid #a7f3d0;
    padding: 1px 6px;
    border-radius: 10px;
    margin-left: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
    flex-shrink: 0;
  }
  .cr-vpn-ref-badge:hover {
    background: #10b981;
    color: #ffffff;
  }
  .cr-if-ref-badge {
    font-size: 0.7rem;
    font-weight: 600;
    color: #d97706;
    background: #fef3c7;
    border: 1px solid #fde68a;
    padding: 1px 6px;
    border-radius: 10px;
    margin-left: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
    flex-shrink: 0;
  }
  .cr-if-ref-badge:hover {
    background: #f59e0b;
    color: #ffffff;
  }
  .cr-prof-ref-badge {
    font-size: 0.7rem;
    font-weight: 600;
    color: #7c3aed;
    background: #ede9fe;
    border: 1px solid #ddd6fe;
    padding: 1px 6px;
    border-radius: 10px;
    margin-left: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
    flex-shrink: 0;
  }
  .cr-prof-ref-badge:hover {
    background: #8b5cf6;
    color: #ffffff;
  }
  .cr-index-empty {
    padding: 2rem 1rem;
    text-align: center;
    font-size: 0.85rem;
    color: #94a3b8;
  }
  .cr-editor-frame {
    flex: 1;
    height: 100%;
    position: relative;
    overflow: hidden;
  }
  #monacoContainer {
    width: 100%;
    height: 100%;
  }
  /* Custom Monaco Underlines for Interactive Symbols */
  .monaco-vpn-underline {
    border-bottom: 1.5px dashed #2563eb !important;
    cursor: pointer;
  }
  .monaco-interface-underline {
    border-bottom: 1.5px dashed #d97706 !important;
    cursor: pointer;
  }
  .monaco-profile-underline {
    border-bottom: 1.5px dashed #8b5cf6 !important;
    cursor: pointer;
  }
  /* Custom Monaco Cipher Highlight */
  .monaco-cipher-highlight {
    background-color: rgba(239, 68, 68, 0.18) !important;
    border: 1px dashed #ef4444 !important;
    border-radius: 3px;
  }
  /* Reference Modal Overlay */
  .cr-modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(15, 23, 42, 0.5);
    backdrop-filter: blur(3px);
    z-index: 100000;
    align-items: center;
    justify-content: center;
  }
  .cr-modal-overlay.active {
    display: flex;
  }
  .cr-modal-card {
    background: #ffffff;
    border-radius: 12px;
    width: 90%;
    max-width: 720px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    overflow: hidden;
  }
  .cr-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    font-weight: 700;
    color: #0f172a;
  }
  .cr-modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #64748b;
    line-height: 1;
  }
  .cr-modal-body {
    padding: 1.25rem;
    overflow-y: auto;
    font-size: 0.875rem;
  }
  .cr-def-block-card {
    margin-bottom: 1.25rem;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 0.85rem 1rem;
  }
  .cr-def-block-title {
    font-weight: 700;
    color: #1d4ed8;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .cr-vpn-ref-group {
    margin-bottom: 1rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem 1rem;
  }
  .cr-vpn-ref-header {
    font-weight: 600;
    color: #2563eb;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .cr-vpn-ref-code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.82rem;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 0.45rem 0.75rem;
    border-radius: 6px;
    color: #334155;
    cursor: pointer;
    white-space: pre-wrap;
    word-break: break-all;
    transition: all 0.15s ease;
  }
  .cr-vpn-ref-code:hover {
    background: #eff6ff;
    border-color: #2563eb;
    color: #1d4ed8;
  }
  /* Dark Theme Adjustments */
  .cr-dark .cr-toolbar {
    background: #1e293b;
    border-color: #334155;
  }
  .cr-dark .cr-label {
    color: #94a3b8;
  }
  .cr-dark .cr-select, .cr-dark .cr-btn {
    background: #0f172a;
    color: #f1f5f9;
    border-color: #334155;
  }
  .cr-dark .cr-btn:hover {
    background: #1e293b;
  }
  .cr-dark .cr-search-input {
    background: #0f172a;
    color: #f1f5f9;
    border-color: #334155;
  }
  .cr-dark .cr-find-dropdown {
    background: #0f172a;
    border-color: #334155;
  }
  .cr-dark .cr-find-item {
    color: #cbd5e1;
    border-bottom-color: #1e293b;
  }
  .cr-dark .cr-find-item:hover {
    background: #1e3a8a;
    color: #93c5fd;
  }
  .cr-dark .cr-main-layout {
    border-color: #334155;
    background: #1e1e1e;
  }
  .cr-dark .cr-sidebar {
    background: #0f172a;
    border-color: #334155;
  }
  .cr-dark .cr-sidebar-header {
    background: #1e293b;
    border-color: #334155;
    color: #f1f5f9;
  }
  .cr-dark .cr-sidebar-search {
    background: #0f172a;
    border-color: #334155;
  }
  .cr-dark .cr-sidebar-search input {
    background: #1e293b;
    border-color: #334155;
    color: #f1f5f9;
  }
  .cr-dark .cr-index-item {
    border-bottom-color: #1e293b;
    color: #cbd5e1;
  }
  .cr-dark .cr-index-item:hover {
    background: #1e293b;
    color: #ffffff;
  }
  .cr-dark .cr-index-item.active {
    background: #1e3a8a;
    color: #93c5fd;
    border-left-color: #3b82f6;
  }
  .cr-dark .cr-index-line {
    background: #334155;
    color: #94a3b8;
  }
  .cr-dark.cr-full-window {
    background: #1e1e1e;
  }
  .cr-dark .cr-modal-card {
    background: #0f172a;
    color: #f1f5f9;
    border: 1px solid #334155;
  }
  .cr-dark .cr-modal-header {
    background: #1e293b;
    border-color: #334155;
    color: #f1f5f9;
  }
  .cr-dark .cr-def-block-card {
    background: #1e3a8a;
    border-color: #3b82f6;
  }
  .cr-dark .cr-def-block-title {
    color: #93c5fd;
  }
  .cr-dark .cr-vpn-ref-group {
    background: #1e293b;
    border-color: #334155;
  }
  .cr-dark .cr-vpn-ref-code {
    background: #0f172a;
    border-color: #334155;
    color: #cbd5e1;
  }
</style>

<div class="cr-container" id="crContainer">
  <!-- Toolbar -->
  <div class="cr-toolbar">
    <div class="cr-toolbar-group">
      <button class="cr-btn" id="crSidebarToggleBtn" onclick="toggleSidebar()">📑 Hide Index</button>
      <button class="cr-btn" id="fullWindowBtn" onclick="toggleFullWindow()">⛶ Full Window</button>
      <div class="cr-find-container">
        <span class="cr-label" style="margin-left: 0.4rem;">Find:</span>
        <input type="text" id="configFindInput" class="cr-search-input" placeholder="🔍 Find in config..." oninput="onConfigFindChange()" onfocus="onConfigFindFocus()" onblur="onConfigFindBlur()">
        <div id="configFindDropdown" class="cr-find-dropdown"></div>
      </div>
      <span class="cr-label" style="margin-left: 0.4rem;">Language:</span>
      <select id="vendorSelect" class="cr-select" onchange="onVendorChange()">
        <option value="huawei">Huawei VRP</option>
        <option value="cisco">Cisco IOS / NX-OS</option>
        <option value="juniper">Juniper JunOS</option>
        <option value="arista">Arista EOS</option>
      </select>
      <span class="cr-label" style="margin-left: 0.4rem;">Theme:</span>
      <select id="themeSelect" class="cr-select" onchange="onThemeChange()">
        <option value="vs">vs (Light)</option>
        <option value="vs-dark">vs-dark (Dark)</option>
      </select>
    </div>
    <div class="cr-toolbar-group">
      <button class="cr-btn cr-btn-primary" onclick="foldAll()">↔️ Fold All</button>
      <button class="cr-btn cr-btn-primary" onclick="unfoldAll()">↕️ Unfold All</button>
      <button class="cr-btn" onclick="copyConfig()">📋 Copy</button>
      <button class="cr-btn" onclick="downloadConfig()">💾 Download</button>
    </div>
  </div>

  <!-- Main Split View Layout -->
  <div class="cr-main-layout">
    <!-- Config Index Sidebar (Default Visible) -->
    <div class="cr-sidebar" id="crSidebar">
      <div class="cr-sidebar-header">
        <div class="cr-sidebar-title">
          <span>📑 Config Index</span>
          <span class="cr-badge" id="indexCountBadge">0</span>
        </div>
      </div>
      <div class="cr-sidebar-search">
        <input type="text" id="indexSearchInput" placeholder="Search index..." oninput="filterIndexList()">
      </div>
      <div class="cr-index-list" id="indexList">
        <!-- Dynamically rendered index items -->
      </div>
    </div>
    <!-- Monaco Editor Container -->
    <div class="cr-editor-frame">
      <div id="monacoContainer"></div>
    </div>
  </div>
</div>

<!-- Reference Details Modal -->
<div id="crVpnModal" class="cr-modal-overlay" onclick="closeVpnModal(event)">
  <div class="cr-modal-card" onclick="event.stopPropagation()">
    <div class="cr-modal-header">
      <span id="crVpnModalTitle">🔒 Reference Details</span>
      <button class="cr-modal-close" onclick="closeVpnModal()">×</button>
    </div>
    <div class="cr-modal-body" id="crVpnModalBody">
      <!-- Dynamically filled reference details -->
    </div>
  </div>
</div>

<!-- RequireJS & Monaco Loader -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js"></script>

<script>
// Huawei sample configuration including user's specific Eth-Trunk, WLAN AC, AAA & Profile examples
const HUAWEI_SAMPLE = `
[V300R024C00SPC100]
#
 drop illegal-mac alarm
#
ipv6
#
authentication-profile name default_authen_profile
#
dns resolve 
#
dhcp enable
#
ip vpn-instance vpn1
 ipv4-family
  route-distinguisher 1111:1111
  vpn-target 11:11 export-extcommunity
  vpn-target 11:11 import-extcommunity
#
radius-server template default
#
pki realm default
 certificate-check none
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
 ip address 10.155.154.1 255.255.255.0
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
 ip binding vpn-instance vpn1
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
ip route-static vpn-instance vpn1 80.158.50.5 255.255.255.255 GigabitEthernet0/0/9 dhcp tag 4400 description agile-controller
#
fib regularly-refresh disable
#
 agile controller host 80.158.50.5 port 10020 vpn-instance vpn1
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
  security wpa2 psk pass-phrase ***** aes
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
interface GigabitEthernet0/0/2
 description LAN Access Port
 switchport mode access
 switchport access vlan 10
!
interface GigabitEthernet0/0/3
 description LAN Access Port
 switchport mode access
 switchport access vlan 20
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
let allIndexItems = [];
let vpnAnalysisMap = new Map();
let interfaceAnalysisMap = new Map();
let profileAnalysisMap = new Map();

require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});

require(['vs/editor/editor.main'], function() {
  registerLanguages();
  registerFoldingProviders();
  registerMonacoJumpCommand();
  registerReferenceHoverProviders();

  const container = document.getElementById('monacoContainer');
  editorInstance = monaco.editor.create(container, {
    value: HUAWEI_SAMPLE,
    language: 'huawei-vrp',
    theme: 'vs',
    automaticLayout: true,
    fontFamily: '"Fira Code", Consolas, Monaco, monospace',
    fontSize: 13,
    minimap: {
      enabled: true,
      scale: 2,
      maxColumn: 120,
      showSlider: 'always',
      renderCharacters: true
    },
    scrollBeyondLastLine: false,
    renderLineHighlight: 'all',
    folding: true,
    foldingStrategy: 'auto',
    showFoldingControls: 'always',
    lineNumbers: 'on'
  });

  // Listen to document changes to update folding index & reference analysis
  editorInstance.onDidChangeModelContent(() => {
    analyzeVpnInstances();
    analyzeInterfaceReferences();
    analyzeProfiles();
    updateFoldingIndex();
    analyzeConfiguration();
    onConfigFindChange();
  });

  // Listen to Esc key to exit full window
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const crCont = document.getElementById('crContainer');
      if (crCont && crCont.classList.contains('cr-full-window')) {
        toggleFullWindow(false);
      }
    }
  });

  // Restore user preferences (Full Window & Sidebar state)
  restoreUserPreferences();

  // Initial analysis & index build
  analyzeVpnInstances();
  analyzeInterfaceReferences();
  analyzeProfiles();
  updateFoldingIndex();
  analyzeConfiguration();
});

function onConfigFindChange() {
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const inputEl = document.getElementById('configFindInput');
  const dropdownEl = document.getElementById('configFindDropdown');
  if (!inputEl || !dropdownEl) return;

  const query = (inputEl.value || '').toLowerCase().trim();
  if (!query) {
    dropdownEl.classList.remove('active');
    dropdownEl.innerHTML = '';
    return;
  }

  const lineCount = model.getLineCount();
  const matches = [];

  for (let i = 1; i <= lineCount; i++) {
    const lineText = model.getLineContent(i);
    if (lineText.toLowerCase().includes(query)) {
      matches.push({ lineNum: i, text: lineText.trim() });
    }
  }

  if (matches.length === 0) {
    dropdownEl.innerHTML = '<div class="cr-find-empty">No matching lines found</div>';
    dropdownEl.classList.add('active');
    return;
  }

  let html = '';
  matches.forEach(m => {
    html += `
      <div class="cr-find-item" onmousedown="jumpFromFind(${m.lineNum})">
        <span class="cr-find-line">L${m.lineNum}</span>
        <span class="cr-find-text" title="${escapeHtml(m.text)}">${escapeHtml(m.text)}</span>
      </div>
    `;
  });

  dropdownEl.innerHTML = html;
  dropdownEl.classList.add('active');
}

function jumpFromFind(lineNum) {
  if (!editorInstance) return;
  editorInstance.revealLineInCenter(lineNum);
  editorInstance.setPosition({ lineNumber: lineNum, column: 1 });
  editorInstance.focus();

  const dropdownEl = document.getElementById('configFindDropdown');
  if (dropdownEl) {
    dropdownEl.classList.remove('active');
  }
}

function onConfigFindFocus() {
  const inputEl = document.getElementById('configFindInput');
  if (inputEl && inputEl.value.trim().length > 0) {
    onConfigFindChange();
  }
}

function onConfigFindBlur() {
  setTimeout(() => {
    const dropdownEl = document.getElementById('configFindDropdown');
    if (dropdownEl) dropdownEl.classList.remove('active');
  }, 200);
}

function registerMonacoJumpCommand() {
  monaco.editor.registerCommand('configReader.jumpToLine', function(accessor, lineNum) {
    const line = parseInt(lineNum, 10);
    if (!isNaN(line) && editorInstance) {
      editorInstance.revealLineInCenter(line);
      editorInstance.setPosition({ lineNumber: line, column: 1 });
      editorInstance.focus();
    }
  });
}

function restoreUserPreferences() {
  const savedFullWindow = localStorage.getItem('configReader_fullWindow');
  if (savedFullWindow === 'true') {
    toggleFullWindow(true);
  }

  const savedShowIndex = localStorage.getItem('configReader_showIndex');
  if (savedShowIndex === 'false') {
    const sidebar = document.getElementById('crSidebar');
    const toggleBtn = document.getElementById('crSidebarToggleBtn');
    if (sidebar) sidebar.classList.add('collapsed');
    if (toggleBtn) toggleBtn.innerText = '📑 Show Index';
  }
}

function registerLanguages() {
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
      'controller', 'fib', 'enable', 'disable', 'permit', 'description', 'bind', 'binding', 'eth-trunk',
      'authentication-scheme', 'authorization-scheme', 'accounting-scheme', 'domain', 'radius-server'
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
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }]
      ]
    }
  });

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
        [/\b(GigabitEthernet|TenGigabitEthernet|FastEthernet|Loopback|Vlan)\d+(\/\d+)*\b/i, 'type.identifier'],
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

function registerFoldingProviders() {
  const languages = ['huawei-vrp', 'cisco-ios'];

  languages.forEach(langId => {
    monaco.languages.registerFoldingRangeProvider(langId, {
      provideFoldingRanges: function(model, context, token) {
        const ranges = [];
        const lineCount = model.getLineCount();
        const lines = model.getLinesContent();

        function isDelimiterLine(lineText) {
          const trimmed = lineText.trim();
          return trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!');
        }

        function getIndent(lineText) {
          let count = 0;
          for (let i = 0; i < lineText.length; i++) {
            if (lineText[i] === ' ') count += 1;
            else if (lineText[i] === '\t') count += 4;
            else break;
          }
          return count;
        }

        function getTwoWordPrefix(lineText) {
          const trimmed = lineText.trim();
          if (!trimmed) return '';
          const words = trimmed.split(/\s+/);
          if (words.length >= 2) {
            return (words[0] + ' ' + words[1]).toLowerCase();
          }
          return words[0].toLowerCase();
        }

        let segments = [];
        let currentSegment = [];

        for (let i = 0; i < lineCount; i++) {
          const line = lines[i];
          if (isDelimiterLine(line)) {
            if (currentSegment.length > 0) {
              segments.push(currentSegment);
              currentSegment = [];
            }
          } else {
            if (line.trim().length > 0) {
              currentSegment.push({ lineIndex: i, text: line });
            }
          }
        }
        if (currentSegment.length > 0) {
          segments.push(currentSegment);
        }

        segments.forEach(seg => {
          if (seg.length < 2) return;

          for (let idx = 0; idx < seg.length; idx++) {
            const parentItem = seg[idx];
            const parentIndent = getIndent(parentItem.text);

            let endIdx = idx;
            for (let j = idx + 1; j < seg.length; j++) {
              const childIndent = getIndent(seg[j].text);
              if (childIndent > parentIndent) {
                endIdx = j;
              } else {
                break;
              }
            }

            if (endIdx > idx) {
              ranges.push({
                start: parentItem.lineIndex + 1,
                end: seg[endIdx].lineIndex + 1,
                kind: monaco.languages.FoldingRangeKind.Region
              });
            }
          }

          let i = 0;
          while (i < seg.length) {
            const itemI = seg[i];
            const indentI = getIndent(itemI.text);
            const prefixI = getTwoWordPrefix(itemI.text);

            if (!prefixI) {
              i++;
              continue;
            }

            let j = i + 1;
            while (j < seg.length) {
              const itemJ = seg[j];
              const indentJ = getIndent(itemJ.text);
              const prefixJ = getTwoWordPrefix(itemJ.text);

              if (indentJ === indentI && prefixJ === prefixI) {
                j++;
              } else {
                break;
              }
            }

            if (j - i >= 2) {
              ranges.push({
                start: seg[i].lineIndex + 1,
                end: seg[j - 1].lineIndex + 1,
                kind: monaco.languages.FoldingRangeKind.Region
              });
              i = j;
            } else {
              i++;
            }
          }
        });

        return ranges;
      }
    });
  });
}

function getIndent(lineText) {
  let count = 0;
  for (let i = 0; i < lineText.length; i++) {
    if (lineText[i] === ' ') count += 1;
    else if (lineText[i] === '\t') count += 4;
    else break;
  }
  return count;
}

// Section-scoped definition block extraction
function getDefinitionBlockText(model, startLineNum) {
  const lineCount = model.getLineCount();
  const startLine = model.getLineContent(startLineNum);
  const currentIndent = getIndent(startLine);
  
  const blockLines = [];

  // If current line is indented (e.g. child under "wlan ac" or "aaa"), find top parent section header
  if (currentIndent > 0) {
    for (let k = startLineNum - 1; k >= 1; k--) {
      const pText = model.getLineContent(k);
      const pTrimmed = pText.trim();
      if (!pTrimmed || pTrimmed === '#' || pTrimmed === '!' || pTrimmed.startsWith('#') || pTrimmed.startsWith('!')) {
        break;
      }
      const pIndent = getIndent(pText);
      if (pIndent === 0) {
        blockLines.push(pText);
        break;
      }
    }
  }

  // Add the definition line itself
  blockLines.push(startLine);

  // Add any child sub-commands that belong directly to this line (indented further than currentIndent)
  for (let i = startLineNum; i < lineCount; i++) {
    const line = model.getLineContent(i + 1);
    const trimmed = line.trim();

    if (!trimmed || trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!')) {
      break;
    }

    const indent = getIndent(line);
    if (indent <= currentIndent) {
      break;
    }

    blockLines.push(line);
  }

  return blockLines.join('\n');
}

function analyzeVpnInstances() {
  vpnAnalysisMap.clear();
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const lines = model.getLinesContent();
  const lineCount = lines.length;

  function cleanTitle(str) {
    return str.replace(/[#!]/g, '').trim();
  }

  function getSectionHeader(lineIdx) {
    for (let k = lineIdx; k >= 0; k--) {
      const lText = lines[k];
      const trimmed = lText.trim();
      if (!trimmed || trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!')) continue;

      const indent = lText.search(/\S/);
      if (indent === 0) {
        return cleanTitle(trimmed);
      }
    }
    return 'Global Configuration';
  }

  const vpnDefRegex = /^\s*ip\s+vpn-instance\s+([a-zA-Z0-9_\-]+)/i;
  for (let i = 0; i < lineCount; i++) {
    const match = vpnDefRegex.exec(lines[i]);
    if (match) {
      const vpnName = match[1];
      if (!vpnAnalysisMap.has(vpnName.toLowerCase())) {
        const defLineNum = i + 1;
        const defBlockText = getDefinitionBlockText(model, defLineNum);
        vpnAnalysisMap.set(vpnName.toLowerCase(), {
          name: vpnName,
          defLineNum: defLineNum,
          defText: lines[i].trim(),
          defBlockText: defBlockText,
          references: []
        });
      }
    }
  }

  for (let i = 0; i < lineCount; i++) {
    const lineNum = i + 1;
    const lineText = lines[i];

    vpnAnalysisMap.forEach((vpnInfo) => {
      if (lineNum !== vpnInfo.defLineNum) {
        const refRegex = new RegExp(`\\bvpn-instance\\s+${vpnInfo.name}\\b`, 'i');
        if (refRegex.test(lineText)) {
          const sectionHeader = getSectionHeader(i);
          vpnInfo.references.push({
            lineNum: lineNum,
            text: lineText.trim(),
            sectionHeader: sectionHeader
          });
        }
      }
    });
  }
}

// Generic Interface Analyzer: 2-word rule "interface <ifName>" (case-insensitive) & Eth-Trunk association
function analyzeInterfaceReferences() {
  interfaceAnalysisMap.clear();
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const lines = model.getLinesContent();
  const lineCount = lines.length;

  function cleanTitle(str) {
    return str.replace(/[#!]/g, '').trim();
  }

  function getSectionHeader(lineIdx) {
    for (let k = lineIdx; k >= 0; k--) {
      const lText = lines[k];
      const trimmed = lText.trim();
      if (!trimmed || trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!')) continue;

      const indent = lText.search(/\S/);
      if (indent === 0) {
        return cleanTitle(trimmed);
      }
    }
    return 'Global Configuration';
  }

  // Generic 2-word rule: ^\s*interface\s+(\S+)\s*$ (case-insensitive)
  const ifDefRegex = /^\s*interface\s+(\S+)\s*$/i;
  for (let i = 0; i < lineCount; i++) {
    const match = ifDefRegex.exec(lines[i]);
    if (match) {
      const ifName = match[1];
      if (!interfaceAnalysisMap.has(ifName.toLowerCase())) {
        const defLineNum = i + 1;
        const defBlockText = getDefinitionBlockText(model, defLineNum);

        // Check if interface is Eth-Trunk<ID>
        const trunkMatch = /^Eth-Trunk(\d+)$/i.exec(ifName);
        const trunkId = trunkMatch ? trunkMatch[1] : null;

        interfaceAnalysisMap.set(ifName.toLowerCase(), {
          name: ifName,
          defLineNum: defLineNum,
          defText: lines[i].trim(),
          defBlockText: defBlockText,
          trunkId: trunkId,
          references: []
        });
      }
    }
  }

  for (let i = 0; i < lineCount; i++) {
    const lineNum = i + 1;
    const lineText = lines[i];

    interfaceAnalysisMap.forEach((ifInfo) => {
      if (lineNum !== ifInfo.defLineNum) {
        const escapedName = ifInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');

        const refRegex = new RegExp(`(?<![a-zA-Z0-9_./-])${escapedName}(?![a-zA-Z0-9_./-])`, 'i');

        let ethTrunkMatch = false;
        if (ifInfo.trunkId) {
          const ethTrunkRegex = new RegExp(`\\beth-trunk\\s+${ifInfo.trunkId}\\b`, 'i');
          if (ethTrunkRegex.test(lineText)) {
            ethTrunkMatch = true;
          }
        }

        if (refRegex.test(lineText) || ethTrunkMatch) {
          const sectionHeader = getSectionHeader(i);
          ifInfo.references.push({
            lineNum: lineNum,
            text: lineText.trim(),
            sectionHeader: sectionHeader
          });
        }
      }
    });
  }
}

// Generic Profile & AAA Scheme Analyzer
function analyzeProfiles() {
  profileAnalysisMap.clear();
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const lines = model.getLinesContent();
  const lineCount = lines.length;

  function cleanTitle(str) {
    return str.replace(/[#!]/g, '').trim();
  }

  function getSectionHeader(lineIdx) {
    for (let k = lineIdx; k >= 0; k--) {
      const lText = lines[k];
      const trimmed = lText.trim();
      if (!trimmed || trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!')) continue;

      const indent = lText.search(/\S/);
      if (indent === 0) {
        return cleanTitle(trimmed);
      }
    }
    return 'Global Configuration';
  }

  // Profile Definition Pattern 1: "<profile-type> name <profile-name>" or "<type> template <name>"
  const profDefRegex1 = /^\s*([a-zA-Z0-9_\-]+(?:\s+template|\s+profile)?)\s+name\s+([a-zA-Z0-9_\-]+)/i;
  const profDefRegex2 = /^\s*([a-zA-Z0-9_\-]+)\s+template\s+([a-zA-Z0-9_\-]+)/i;
  
  // AAA Level-1 Definition Pattern: 1 space indent under aaa (e.g. " authentication-scheme default", " domain default")
  const aaaDefRegex = /^ ([a-zA-Z0-9_\-]+(?:-scheme|-user|domain))\s+([a-zA-Z0-9_\-]+)/i;

  let inAaaSection = false;

  for (let i = 0; i < lineCount; i++) {
    const lineText = lines[i];
    const trimmed = lineText.trim();

    if (trimmed === 'aaa') {
      inAaaSection = true;
      continue;
    } else if (trimmed === '#' || trimmed === '!' || (trimmed && lineText.search(/\S/) === 0)) {
      if (trimmed !== 'aaa') inAaaSection = false;
    }

    let profType = null;
    let profName = null;
    let baseType = null;

    let match1 = profDefRegex1.exec(lineText);
    let match2 = profDefRegex2.exec(lineText);
    let matchAaa = inAaaSection ? aaaDefRegex.exec(lineText) : null;

    if (match1) {
      profType = match1[1].trim();
      profName = match1[2].trim();
      baseType = profType.replace(/\s+template$/i, '');
    } else if (match2) {
      profType = match2[1].trim() + ' template';
      profName = match2[2].trim();
      baseType = match2[1].trim();
    } else if (matchAaa) {
      profType = matchAaa[1].trim();
      profName = matchAaa[2].trim();
      baseType = profType;
    }

    if (profType && profName) {
      const key = `${profType.toLowerCase()}:${profName.toLowerCase()}`;
      if (!profileAnalysisMap.has(key)) {
        const defLineNum = i + 1;
        const defBlockText = getDefinitionBlockText(model, defLineNum);
        profileAnalysisMap.set(key, {
          type: profType,
          baseType: baseType,
          name: profName,
          defLineNum: defLineNum,
          defText: lineText.trim(),
          defBlockText: defBlockText,
          references: []
        });
      }
    }
  }

  for (let i = 0; i < lineCount; i++) {
    const lineNum = i + 1;
    const lineText = lines[i];

    profileAnalysisMap.forEach((profInfo) => {
      if (lineNum !== profInfo.defLineNum) {
        const escType = profInfo.type.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
        const escBaseType = profInfo.baseType.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
        const escName = profInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');

        // Usage pattern: "<type> <name>" OR "<baseType> <name>" OR "<type> name <name>" OR "<type> template <name>"
        const refRegex = new RegExp(`\\b(?:${escType}|${escBaseType})\\s+(?:name\\s+|template\\s+)?${escName}\\b`, 'i');
        if (refRegex.test(lineText)) {
          const sectionHeader = getSectionHeader(i);
          profInfo.references.push({
            lineNum: lineNum,
            text: lineText.trim(),
            sectionHeader: sectionHeader
          });
        }
      }
    });
  }
}

function escapeHoverText(str) {
  if (!str) return '';
  return str.replace(/`/g, "'").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function registerReferenceHoverProviders() {
  const languages = ['huawei-vrp', 'cisco-ios'];

  languages.forEach(langId => {
    monaco.languages.registerHoverProvider(langId, {
      provideHover: function(model, position) {
        const lineText = model.getLineContent(position.lineNumber);
        const col = position.column;

        // 1. VPN Instance Hover (column position check)
        const vpnRegex = /vpn-instance\s+([a-zA-Z0-9_\-]+)/gi;
        let match;
        while ((match = vpnRegex.exec(lineText)) !== null) {
          const startCol = match.index + 1;
          const endCol = match.index + 1 + match[0].length;

          if (col >= startCol && col <= endCol) {
            const vpnName = match[1];
            const vpnInfo = vpnAnalysisMap.get(vpnName.toLowerCase());
            if (vpnInfo) {
              const refCount = vpnInfo.references.length;
              const contents = [];

              contents.push({ value: `**🔒 VPN Instance:** \`${escapeHoverText(vpnInfo.name)}\` (Referenced **${refCount}** times)` });

              contents.push({
                value: `[**★ Definition Block (Line ${vpnInfo.defLineNum}):**](command:configReader.jumpToLine?${vpnInfo.defLineNum})\n\`\`\`\n${escapeHoverText(vpnInfo.defBlockText)}\n\`\`\``,
                isTrusted: true
              });

              if (refCount === 0) {
                contents.push({ value: '_No usage references found in configuration._' });
              } else {
                let refMarkdown = '**Usage Locations by Section (click line to jump):**\n';
                vpnInfo.references.forEach(ref => {
                  refMarkdown += `- [📍 **${escapeHoverText(ref.sectionHeader)}** (L${ref.lineNum}): \`${escapeHoverText(ref.text)}\`](command:configReader.jumpToLine?${ref.lineNum})\n`;
                });
                contents.push({ value: refMarkdown, isTrusted: true });
              }

              return {
                range: new monaco.Range(position.lineNumber, startCol, position.lineNumber, endCol),
                contents: contents
              };
            }
          }
        }

        // 2. Interface & Eth-Trunk Reference Hover
        let hoverResult = null;
        interfaceAnalysisMap.forEach((ifInfo) => {
          if (hoverResult) return;

          const escapedName = ifInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
          const ifRegex = new RegExp(`(?<![a-zA-Z0-9_./-])${escapedName}(?![a-zA-Z0-9_./-])`, 'gi');
          let ifMatch;
          while ((ifMatch = ifRegex.exec(lineText)) !== null) {
            const startCol = ifMatch.index + 1;
            const endCol = ifMatch.index + 1 + ifMatch[0].length;

            if (col >= startCol && col <= endCol) {
              hoverResult = buildInterfaceHover(ifInfo, position, startCol, endCol);
              break;
            }
          }

          if (!hoverResult && ifInfo.trunkId) {
            const ethTrunkRegex = new RegExp(`\\beth-trunk\\s+${ifInfo.trunkId}\\b`, 'gi');
            let trunkMatch;
            while ((trunkMatch = ethTrunkRegex.exec(lineText)) !== null) {
              const startCol = trunkMatch.index + 1;
              const endCol = trunkMatch.index + 1 + trunkMatch[0].length;

              if (col >= startCol && col <= endCol) {
                hoverResult = buildInterfaceHover(ifInfo, position, startCol, endCol);
                break;
              }
            }
          }
        });

        if (hoverResult) return hoverResult;

        // 3. Profile & AAA Scheme Reference Hover
        profileAnalysisMap.forEach((profInfo) => {
          if (hoverResult) return;

          const escType = profInfo.type.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
          const escBaseType = profInfo.baseType.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
          const escName = profInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
          const profRegex = new RegExp(`\\b(?:${escType}|${escBaseType})\\s+(?:name\\s+|template\\s+)?${escName}\\b`, 'gi');
          let profMatch;
          while ((profMatch = profRegex.exec(lineText)) !== null) {
            const startCol = profMatch.index + 1;
            const endCol = profMatch.index + 1 + profMatch[0].length;

            if (col >= startCol && col <= endCol) {
              const refCount = profInfo.references.length;
              const contents = [];

              contents.push({ value: `**🛡️ Profile / AAA Scheme:** \`${escapeHoverText(profInfo.type)} ${escapeHoverText(profInfo.name)}\` (Referenced **${refCount}** times)` });

              contents.push({
                value: `[**★ Definition Block (Line ${profInfo.defLineNum}):**](command:configReader.jumpToLine?${profInfo.defLineNum})\n\`\`\`\n${escapeHoverText(profInfo.defBlockText)}\n\`\`\``,
                isTrusted: true
              });

              if (refCount === 0) {
                contents.push({ value: '_No usage references found in configuration._' });
              } else {
                let refMarkdown = '**Usage Locations by Section (click line to jump):**\n';
                profInfo.references.forEach(ref => {
                  refMarkdown += `- [📍 **${escapeHoverText(ref.sectionHeader)}** (L${ref.lineNum}): \`${escapeHoverText(ref.text)}\`](command:configReader.jumpToLine?${ref.lineNum})\n`;
                });
                contents.push({ value: refMarkdown, isTrusted: true });
              }

              hoverResult = {
                range: new monaco.Range(position.lineNumber, startCol, position.lineNumber, endCol),
                contents: contents
              };
              break;
            }
          }
        });

        if (hoverResult) return hoverResult;
        return null;
      }
    });
  });
}

function buildInterfaceHover(ifInfo, position, startCol, endCol) {
  const refCount = ifInfo.references.length;
  const contents = [];

  contents.push({ value: `**🔌 Interface:** \`${escapeHoverText(ifInfo.name)}\` (Referenced **${refCount}** times)` });

  contents.push({
    value: `[**★ Definition Block (Line ${ifInfo.defLineNum}):**](command:configReader.jumpToLine?${ifInfo.defLineNum})\n\`\`\`\n${escapeHoverText(ifInfo.defBlockText)}\n\`\`\``,
    isTrusted: true
  });

  if (refCount === 0) {
    contents.push({ value: '_No usage references found in configuration._' });
  } else {
    let refMarkdown = '**Usage Locations by Section (click line to jump):**\n';
    ifInfo.references.forEach(ref => {
      refMarkdown += `- [📍 **${escapeHoverText(ref.sectionHeader)}** (L${ref.lineNum}): \`${escapeHoverText(ref.text)}\`](command:configReader.jumpToLine?${ref.lineNum})\n`;
    });
    contents.push({ value: refMarkdown, isTrusted: true });
  }

  return {
    range: new monaco.Range(position.lineNumber, startCol, position.lineNumber, endCol),
    contents: contents
  };
}

function updateFoldingIndex() {
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const lines = model.getLinesContent();
  const lineCount = lines.length;

  function isDelimiterLine(lineText) {
    const trimmed = lineText.trim();
    return trimmed === '#' || trimmed === '!' || trimmed.startsWith('#') || trimmed.startsWith('!');
  }

  function cleanTitle(str) {
    return str.replace(/[#!]/g, '').trim();
  }

  function getTwoWordPrefix(lineText) {
    const trimmed = lineText.trim();
    if (!trimmed) return '';
    const words = trimmed.split(/\s+/);
    if (words.length >= 2) {
      return words[0] + ' ' + words[1];
    }
    return words[0];
  }

  const items = [];
  let currentBlock = [];

  for (let i = 0; i < lineCount; i++) {
    const line = lines[i];
    if (isDelimiterLine(line)) {
      if (currentBlock.length > 0) {
        processBlock(currentBlock, items);
        currentBlock = [];
      }
    } else {
      if (line.trim().length > 0) {
        currentBlock.push({ lineNum: i + 1, text: line });
      }
    }
  }
  if (currentBlock.length > 0) {
    processBlock(currentBlock, items);
  }

  function processBlock(block, outItems) {
    if (block.length === 0) return;

    const firstPrefix = getTwoWordPrefix(block[0].text).toLowerCase();
    const allSamePrefix = block.length >= 2 && block.every(b => getTwoWordPrefix(b.text).toLowerCase() === firstPrefix);

    if (allSamePrefix) {
      const rawTitle = getTwoWordPrefix(block[0].text);
      const title = cleanTitle(rawTitle);
      if (title) {
        const item = {
          title: title,
          lineNum: block[0].lineNum,
          count: block.length,
          icon: getSectionIcon(title)
        };
        checkRefInfo(item, block[0].text);
        outItems.push(item);
      }
    } else {
      let minIndent = Infinity;
      block.forEach(b => {
        const indent = b.text.search(/\S/);
        if (indent !== -1 && indent < minIndent) minIndent = indent;
      });

      let i = 0;
      while (i < block.length) {
        const b = block[i];
        const indent = b.text.search(/\S/);
        const prefix = getTwoWordPrefix(b.text).toLowerCase();

        let j = i + 1;
        while (j < block.length) {
          const bNext = block[j];
          const indentNext = bNext.text.search(/\S/);
          const prefixNext = getTwoWordPrefix(bNext.text).toLowerCase();
          if (indentNext === indent && prefixNext === prefix) {
            j++;
          } else {
            break;
          }
        }

        if (j - i >= 2) {
          const title = cleanTitle(getTwoWordPrefix(b.text));
          if (title) {
            const item = {
              title: title,
              lineNum: b.lineNum,
              count: j - i,
              icon: getSectionIcon(title)
            };
            checkRefInfo(item, b.text);
            outItems.push(item);
          }
          i = j;
        } else {
          if (indent === minIndent) {
            const title = cleanTitle(b.text);
            if (title) {
              const item = {
                title: title,
                lineNum: b.lineNum,
                count: 1,
                icon: getSectionIcon(title)
              };
              checkRefInfo(item, b.text);
              outItems.push(item);
            }
          }
          i++;
        }
      }
    }
  }

  function checkRefInfo(item, lineText) {
    // Check VPN Instance
    const vpnMatch = /ip\s+vpn-instance\s+([a-zA-Z0-9_\-]+)/i.exec(lineText);
    if (vpnMatch) {
      const vpnName = vpnMatch[1];
      const vpnInfo = vpnAnalysisMap.get(vpnName.toLowerCase());
      if (vpnInfo) {
        item.isVpn = true;
        item.refName = vpnName;
        item.refCount = vpnInfo.references.length;
      }
    }

    // Check Interface
    const ifMatch = /^\s*interface\s+(\S+)\s*$/i.exec(lineText);
    if (ifMatch) {
      const ifName = ifMatch[1];
      const ifInfo = interfaceAnalysisMap.get(ifName.toLowerCase());
      if (ifInfo) {
        item.isInterface = true;
        item.refName = ifName;
        item.refCount = ifInfo.references.length;
      }
    }

    // Check Profile / AAA Scheme
    const profMatch1 = /^\s*([a-zA-Z0-9_\-]+(?:\s+template|\s+profile)?)\s+name\s+([a-zA-Z0-9_\-]+)/i.exec(lineText);
    const profMatch2 = /^\s*([a-zA-Z0-9_\-]+)\s+template\s+([a-zA-Z0-9_\-]+)/i.exec(lineText);
    const aaaMatch = /^ ([a-zA-Z0-9_\-]+(?:-scheme|-user|domain))\s+([a-zA-Z0-9_\-]+)/i.exec(lineText);

    let profType = null;
    let profName = null;

    if (profMatch1) {
      profType = profMatch1[1].trim();
      profName = profMatch1[2].trim();
    } else if (profMatch2) {
      profType = profMatch2[1].trim() + ' template';
      profName = profMatch2[2].trim();
    } else if (aaaMatch) {
      profType = aaaMatch[1].trim();
      profName = aaaMatch[2].trim();
    }

    if (profType && profName) {
      const key = `${profType.toLowerCase()}:${profName.toLowerCase()}`;
      const profInfo = profileAnalysisMap.get(key);
      if (profInfo) {
        item.isProfile = true;
        item.profKey = key;
        item.refName = `${profType} ${profName}`;
        item.refCount = profInfo.references.length;
      }
    }
  }

  allIndexItems = items;
  renderIndexList(items);
}

function getSectionIcon(title) {
  const t = title.toLowerCase();
  if (t.includes('interface') || t.includes('vlanif') || t.includes('gigabitethernet')) return '🔌';
  if (t.includes('route') || t.includes('bgp') || t.includes('ospf') || t.includes('vpn')) return '🌐';
  if (t.includes('authen') || t.includes('user') || t.includes('aaa') || t.includes('line') || t.includes('domain')) return '👤';
  if (t.includes('ssl') || t.includes('pki') || t.includes('ike') || t.includes('firewall') || t.includes('security')) return '🔒';
  if (t.includes('dhcp') || t.includes('dns') || t.includes('http')) return '⚡';
  if (t.includes('wlan') || t.includes('cellular')) return '📡';
  return '📄';
}

function renderIndexList(items) {
  const listEl = document.getElementById('indexList');
  const countBadgeEl = document.getElementById('indexCountBadge');
  if (!listEl) return;

  if (countBadgeEl) {
    countBadgeEl.innerText = items.length;
  }

  if (items.length === 0) {
    listEl.innerHTML = '<div class="cr-index-empty">No index items found</div>';
    return;
  }

  let html = '';
  items.forEach((item, idx) => {
    const countBadge = item.count > 1 ? `<span class="cr-index-count">${item.count}</span>` : '';
    let refBadge = '';
    if (item.isVpn) {
      refBadge = `<span class="cr-vpn-ref-badge" onclick="openRefModal('vpn', '${escapeHtml(item.refName)}', event)" title="View VPN References">Ref: ${item.refCount}</span>`;
    } else if (item.isInterface) {
      refBadge = `<span class="cr-if-ref-badge" onclick="openRefModal('interface', '${escapeHtml(item.refName)}', event)" title="View Interface References">Ref: ${item.refCount}</span>`;
    } else if (item.isProfile) {
      refBadge = `<span class="cr-prof-ref-badge" onclick="openRefModal('profile', '${escapeHtml(item.profKey)}', event)" title="View Profile References">Ref: ${item.refCount}</span>`;
    }

    html += `
      <div class="cr-index-item" onclick="jumpToLine(${item.lineNum}, this)" data-index="${idx}">
        <div class="cr-index-left">
          <span class="cr-index-icon">${item.icon}</span>
          <span class="cr-index-title" title="${escapeHtml(item.title)}">${escapeHtml(item.title)}</span>
          ${countBadge}
          ${refBadge}
        </div>
        <span class="cr-index-line">L${item.lineNum}</span>
      </div>
    `;
  });
  listEl.innerHTML = html;
}

function openRefModal(type, refName, event) {
  if (event) event.stopPropagation();

  let refInfo = null;
  let icon = '🔒';
  let titlePrefix = 'VPN Instance';

  if (type === 'interface') {
    refInfo = interfaceAnalysisMap.get(refName.toLowerCase());
    icon = '🔌';
    titlePrefix = 'Interface';
  } else if (type === 'profile') {
    refInfo = profileAnalysisMap.get(refName.toLowerCase());
    icon = '🛡️';
    titlePrefix = 'Profile / AAA Scheme';
  } else {
    refInfo = vpnAnalysisMap.get(refName.toLowerCase());
  }

  const modalBody = document.getElementById('crVpnModalBody');
  const modalTitle = document.getElementById('crVpnModalTitle');
  const modalOverlay = document.getElementById('crVpnModal');

  if (!refInfo || !modalBody || !modalOverlay) return;

  const displayName = refInfo.type ? `${refInfo.type} ${refInfo.name}` : refInfo.name;
  modalTitle.innerText = `${icon} ${titlePrefix}: ${displayName}`;

  let bodyHtml = `
    <!-- Top Creation/Definition Block Section -->
    <div class="cr-def-block-card">
      <div class="cr-def-block-title">
        <span>★ Definition Block (Line ${refInfo.defLineNum})</span>
        <span class="cr-index-line" style="cursor: pointer;" onclick="jumpToLine(${refInfo.defLineNum}); closeVpnModal();">L${refInfo.defLineNum}</span>
      </div>
      <div class="cr-vpn-ref-code" onclick="jumpToLine(${refInfo.defLineNum}); closeVpnModal();">
${escapeHtml(refInfo.defBlockText)}
      </div>
    </div>
    
    <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem; color: #0f172a;">
      Usage References (${refInfo.references.length} found):
    </div>
  `;

  if (refInfo.references.length === 0) {
    bodyHtml += `<div style="color: #94a3b8; font-style: italic;">No usage references found in this configuration.</div>`;
  } else {
    refInfo.references.forEach(ref => {
      bodyHtml += `
        <div class="cr-vpn-ref-group">
          <div class="cr-vpn-ref-header">
            <span>📁 Section: ${escapeHtml(ref.sectionHeader)}</span>
            <span class="cr-index-line">L${ref.lineNum}</span>
          </div>
          <div class="cr-vpn-ref-code" onclick="jumpToLine(${ref.lineNum}); closeVpnModal();">
            ${escapeHtml(ref.text)}
          </div>
        </div>
      `;
    });
  }

  modalBody.innerHTML = bodyHtml;
  modalOverlay.classList.add('active');
}

function closeVpnModal(event) {
  if (!event || event.target.id === 'crVpnModal' || event.target.classList.contains('cr-modal-close')) {
    const modalOverlay = document.getElementById('crVpnModal');
    if (modalOverlay) modalOverlay.classList.remove('active');
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function filterIndexList() {
  const query = (document.getElementById('indexSearchInput').value || '').toLowerCase().trim();
  if (!query) {
    renderIndexList(allIndexItems);
    return;
  }
  const filtered = allIndexItems.filter(item => 
    item.title.toLowerCase().includes(query) || (`l${item.lineNum}`).includes(query) || (item.refName && item.refName.toLowerCase().includes(query))
  );
  renderIndexList(filtered);
}

function jumpToLine(lineNum, element) {
  if (!editorInstance) return;
  editorInstance.revealLineInCenter(lineNum);
  editorInstance.setPosition({ lineNumber: lineNum, column: 1 });
  editorInstance.focus();

  const allItems = document.querySelectorAll('.cr-index-item');
  allItems.forEach(el => el.classList.remove('active'));
  if (element) {
    element.classList.add('active');
  }
}

function toggleSidebar() {
  const sidebar = document.getElementById('crSidebar');
  const toggleBtn = document.getElementById('crSidebarToggleBtn');
  if (!sidebar) return;

  const isCollapsed = sidebar.classList.toggle('collapsed');
  if (toggleBtn) {
    toggleBtn.innerText = isCollapsed ? '📑 Show Index' : '📑 Hide Index';
  }
  localStorage.setItem('configReader_showIndex', isCollapsed ? 'false' : 'true');

  setTimeout(() => {
    if (editorInstance) editorInstance.layout();
  }, 100);
}

function toggleFullWindow(forceState) {
  const container = document.getElementById('crContainer');
  const btn = document.getElementById('fullWindowBtn');
  if (!container) return;

  let isFull;
  if (typeof forceState === 'boolean') {
    if (forceState) container.classList.add('cr-full-window');
    else container.classList.remove('cr-full-window');
    isFull = forceState;
  } else {
    isFull = container.classList.toggle('cr-full-window');
  }

  if (btn) {
    btn.innerText = isFull ? '⛶ Normal Window' : '⛶ Full Window';
  }
  localStorage.setItem('configReader_fullWindow', isFull ? 'true' : 'false');

  setTimeout(() => {
    if (editorInstance) editorInstance.layout();
  }, 150);
}

function foldAll() {
  if (!editorInstance) return;
  editorInstance.getAction('editor.foldAll').run();
}

function unfoldAll() {
  if (!editorInstance) return;
  editorInstance.getAction('editor.unfoldAll').run();
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
  analyzeVpnInstances();
  analyzeInterfaceReferences();
  analyzeProfiles();
  updateFoldingIndex();
  analyzeConfiguration();
}

function onThemeChange() {
  const theme = document.getElementById('themeSelect').value;
  if (!editorInstance) return;
  monaco.editor.setTheme(theme);

  const container = document.getElementById('crContainer');
  if (container) {
    if (theme.includes('dark')) {
      container.classList.add('cr-dark');
    } else {
      container.classList.remove('cr-dark');
    }
  }
}

function analyzeConfiguration() {
  if (!editorInstance) return;
  const model = editorInstance.getModel();
  if (!model) return;

  const content = model.getValue();
  const lines = content.split('\n');

  const newDecorations = [];
  lines.forEach((lineText, idx) => {
    const lineNum = idx + 1;

    // Encrypted cipher decoration
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

    // VPN Instance dashed underline decoration
    const vpnRegex = /vpn-instance\s+([a-zA-Z0-9_\-]+)/gi;
    while ((match = vpnRegex.exec(lineText)) !== null) {
      newDecorations.push({
        range: new monaco.Range(lineNum, match.index + 1, lineNum, match.index + 1 + match[0].length),
        options: {
          inlineClassName: 'monaco-vpn-underline'
        }
      });
    }

    // Interface dashed underline decoration
    interfaceAnalysisMap.forEach((ifInfo) => {
      const escapedName = ifInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const ifRegex = new RegExp(`(?<![a-zA-Z0-9_./-])${escapedName}(?![a-zA-Z0-9_./-])`, 'gi');
      let ifMatch;
      while ((ifMatch = ifRegex.exec(lineText)) !== null) {
        newDecorations.push({
          range: new monaco.Range(lineNum, ifMatch.index + 1, lineNum, ifMatch.index + 1 + ifMatch[0].length),
          options: {
            inlineClassName: 'monaco-interface-underline'
          }
        });
      }

      if (ifInfo.trunkId) {
        const ethTrunkRegex = new RegExp(`\\beth-trunk\\s+${ifInfo.trunkId}\\b`, 'gi');
        let trunkMatch;
        while ((trunkMatch = ethTrunkRegex.exec(lineText)) !== null) {
          newDecorations.push({
            range: new monaco.Range(lineNum, trunkMatch.index + 1, lineNum, trunkMatch.index + 1 + trunkMatch[0].length),
            options: {
              inlineClassName: 'monaco-interface-underline'
            }
          });
        }
      }
    });

    // Profile & AAA Scheme dashed underline decoration
    profileAnalysisMap.forEach((profInfo) => {
      const escType = profInfo.type.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const escBaseType = profInfo.baseType.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const escName = profInfo.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const profRegex = new RegExp(`\\b(?:${escType}|${escBaseType})\\s+(?:name\\s+|template\\s+)?${escName}\\b`, 'gi');
      let profMatch;
      while ((profMatch = profRegex.exec(lineText)) !== null) {
        newDecorations.push({
          range: new monaco.Range(lineNum, profMatch.index + 1, lineNum, profMatch.index + 1 + profMatch[0].length),
          options: {
            inlineClassName: 'monaco-profile-underline'
          }
        });
      }
    });
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
</script>
