/**
 * BlackRoad Cloudflare Worker — edge routing and API proxy
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return Response.json({ status: 'ok', edge: 'cloudflare', ts: Date.now() });
    }

    // API proxy to fleet
    if (url.pathname.startsWith('/api/')) {
      try {
        const upstream = env.UPSTREAM_URL || 'https://blackroad.io';
        const resp = await fetch(`${upstream}${url.pathname}`, {
          method: request.method,
          headers: request.headers,
          body: request.method !== 'GET' ? request.body : undefined,
        });
        return new Response(resp.body, { status: resp.status, headers: resp.headers });
      } catch (e) {
        return Response.json({ error: 'upstream_error', message: e.message }, { status: 502 });
      }
    }

    return Response.json({
      service: 'blackroad-edge',
      version: '1.0.0',
      routes: ['/health', '/api/*'],
    });
  },
};
