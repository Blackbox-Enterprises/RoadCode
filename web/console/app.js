/**
 * Prism Console — monitoring dashboard
 */
class PrismConsole {
  constructor(apiUrl = '/api/v1') {
    this.apiUrl = apiUrl;
    this.refreshInterval = 30000;
  }

  async fetchStatus() {
    const resp = await fetch(`${this.apiUrl}/status`);
    return resp.json();
  }

  async fetchAgents() {
    const resp = await fetch(`${this.apiUrl}/agents`);
    return resp.json();
  }

  async fetchFleet() {
    const resp = await fetch(`${this.apiUrl}/fleet/nodes`);
    return resp.json();
  }

  renderNodeCard(node) {
    return `
      <div class="node-card" data-status="${node.status}">
        <h3>${node.name}</h3>
        <span class="ip">${node.ip}</span>
        <span class="role">${node.role}</span>
        <span class="status ${node.status}">${node.status}</span>
      </div>
    `;
  }

  async start() {
    await this.refresh();
    setInterval(() => this.refresh(), this.refreshInterval);
  }

  async refresh() {
    try {
      const [status, agents, fleet] = await Promise.all([
        this.fetchStatus(), this.fetchAgents(), this.fetchFleet(),
      ]);
      console.log('Dashboard refreshed:', { status, agents: agents.agents?.length, nodes: fleet.nodes?.length });
    } catch (e) {
      console.error('Refresh failed:', e);
    }
  }
}

if (typeof window !== 'undefined') {
  window.console_app = new PrismConsole();
}
