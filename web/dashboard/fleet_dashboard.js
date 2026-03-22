/**
 * Fleet Dashboard — real-time monitoring with WebSocket
 */
class FleetDashboard {
  constructor(apiUrl = '/api/v1', wsUrl = null) {
    this.apiUrl = apiUrl;
    this.wsUrl = wsUrl || `ws://${location.host}/ws/dashboard`;
    this.nodes = {};
    this.agents = {};
    this.ws = null;
    this.listeners = new Map();
  }

  async init() {
    await this.fetchInitialState();
    this.connectWebSocket();
    this.startPolling();
  }

  async fetchInitialState() {
    try {
      const [fleetResp, agentsResp] = await Promise.all([
        fetch(`${this.apiUrl}/fleet/nodes`),
        fetch(`${this.apiUrl}/agents`),
      ]);
      const fleet = await fleetResp.json();
      const agents = await agentsResp.json();
      fleet.nodes?.forEach(n => { this.nodes[n.name] = n; });
      agents.agents?.forEach(a => { this.agents[a.name] = a; });
      this.emit('state-updated', { nodes: this.nodes, agents: this.agents });
    } catch (e) {
      console.error('Failed to fetch initial state:', e);
    }
  }

  connectWebSocket() {
    try {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'node-update') {
          this.nodes[data.node] = { ...this.nodes[data.node], ...data.metrics };
          this.emit('node-updated', data);
        } else if (data.type === 'agent-update') {
          this.agents[data.agent] = { ...this.agents[data.agent], ...data };
          this.emit('agent-updated', data);
        } else if (data.type === 'alert') {
          this.emit('alert', data);
        }
      };
      this.ws.onclose = () => { setTimeout(() => this.connectWebSocket(), 5000); };
    } catch (e) {
      console.warn('WebSocket not available, using polling only');
    }
  }

  startPolling(intervalMs = 30000) {
    setInterval(() => this.fetchInitialState(), intervalMs);
  }

  on(event, handler) {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event).push(handler);
  }

  emit(event, data) {
    (this.listeners.get(event) || []).forEach(fn => fn(data));
  }

  renderNodeGrid(container) {
    const el = document.getElementById(container);
    if (!el) return;
    el.innerHTML = Object.values(this.nodes).map(n => `
      <div class="br-card" style="min-width:200px">
        <div class="br-flex br-flex-between" style="align-items:center;margin-bottom:12px">
          <h3 style="font-size:1.1rem;font-family:var(--br-font-heading)">${n.name}</h3>
          <span class="br-status-dot br-status-dot-${n.status || 'online'}"></span>
        </div>
        <div style="font-size:0.85rem;color:#999">
          <div>IP: ${n.ip || 'unknown'}</div>
          <div>Role: ${n.role || 'general'}</div>
          ${n.cpu ? `<div>CPU: ${n.cpu}%</div>` : ''}
          ${n.memory ? `<div>RAM: ${n.memory}%</div>` : ''}
        </div>
      </div>
    `).join('');
  }

  getHealthSummary() {
    const nodes = Object.values(this.nodes);
    return {
      total: nodes.length,
      online: nodes.filter(n => n.status === 'online').length,
      offline: nodes.filter(n => n.status === 'offline').length,
      agents: Object.keys(this.agents).length,
    };
  }
}

if (typeof window !== 'undefined') {
  window.FleetDashboard = FleetDashboard;
}
