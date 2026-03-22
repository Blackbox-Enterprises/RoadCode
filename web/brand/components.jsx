import React, { useState } from 'react';

export const Button = ({ children, variant = 'primary', size = 'md', onClick, disabled, ...props }) => {
  const base = 'br-btn';
  const variants = { primary: 'br-btn-primary', secondary: 'br-btn-secondary', ghost: 'br-btn-ghost' };
  const sizes = { sm: { padding: '6px 12px', fontSize: '0.8rem' }, md: {}, lg: { padding: '14px 28px', fontSize: '1rem' } };
  return (
    <button className={`${base} ${variants[variant]}`} style={sizes[size]} onClick={onClick} disabled={disabled} {...props}>
      {children}
    </button>
  );
};

export const Card = ({ title, children, footer, hoverable = true }) => (
  <div className={`br-card ${hoverable ? '' : ''}`}>
    {title && <div className="br-card-header"><h3 className="br-card-title">{title}</h3></div>}
    <div className="br-card-body">{children}</div>
    {footer && <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--br-border)' }}>{footer}</div>}
  </div>
);

export const Badge = ({ children, variant = 'info' }) => (
  <span className={`br-badge br-badge-${variant}`}>{children}</span>
);

export const StatusDot = ({ status = 'online' }) => (
  <span className={`br-status-dot br-status-dot-${status}`} />
);

export const Input = ({ label, error, ...props }) => (
  <div style={{ marginBottom: '16px' }}>
    {label && <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', color: '#999' }}>{label}</label>}
    <input className="br-input" {...props} />
    {error && <span style={{ color: 'var(--br-error)', fontSize: '0.8rem' }}>{error}</span>}
  </div>
);

export const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="br-modal-overlay" onClick={onClose}>
      <div className="br-modal" onClick={e => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
          <h2 style={{ fontSize: '1.25rem' }}>{title}</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#999', cursor: 'pointer', fontSize: '1.5rem' }}>&times;</button>
        </div>
        {children}
      </div>
    </div>
  );
};

export const Sidebar = ({ items, active, onSelect }) => (
  <nav className="br-sidebar">
    <div style={{ marginBottom: '24px' }}>
      <h2 style={{ fontSize: '1.2rem', fontFamily: 'var(--br-font-heading)' }}>BlackRoad OS</h2>
      <span style={{ color: '#666', fontSize: '0.8rem' }}>RoadCode Console</span>
    </div>
    {items.map(item => (
      <a key={item.id} href="#" className={`br-sidebar-link ${active === item.id ? 'active' : ''}`}
         onClick={e => { e.preventDefault(); onSelect(item.id); }}>
        {item.icon && <span style={{ marginRight: '8px' }}>{item.icon}</span>}
        {item.label}
      </a>
    ))}
  </nav>
);

export const Table = ({ columns, data }) => (
  <table className="br-table">
    <thead><tr>{columns.map(col => <th key={col.key}>{col.label}</th>)}</tr></thead>
    <tbody>
      {data.map((row, i) => (
        <tr key={i}>{columns.map(col => <td key={col.key}>{col.render ? col.render(row[col.key], row) : row[col.key]}</td>)}</tr>
      ))}
    </tbody>
  </table>
);

export const NodeCard = ({ name, ip, role, status, metrics }) => (
  <Card title={name} footer={<Badge variant={status === 'online' ? 'success' : 'error'}>{status}</Badge>}>
    <div style={{ display: 'grid', gap: '8px', fontSize: '0.9rem' }}>
      <div><span style={{ color: '#999' }}>IP:</span> {ip}</div>
      <div><span style={{ color: '#999' }}>Role:</span> {role}</div>
      {metrics && (
        <>
          <div><span style={{ color: '#999' }}>CPU:</span> {metrics.cpu}%</div>
          <div><span style={{ color: '#999' }}>RAM:</span> {metrics.memory}%</div>
        </>
      )}
    </div>
  </Card>
);

export const GradientBar = () => <div className="br-gradient-bar" />;

export const AgentChat = ({ agentName = 'cece' }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const send = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: input }, { role: 'assistant', content: `[${agentName}] Acknowledged.` }]);
    setInput('');
  };
  return (
    <Card title={`Chat with ${agentName}`}>
      <div style={{ maxHeight: '300px', overflow: 'auto', marginBottom: '12px' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ padding: '4px 0', color: m.role === 'user' ? '#f5f5f5' : 'var(--br-pink)' }}>
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '8px' }}>
        <Input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="Type a message..." />
        <Button onClick={send}>Send</Button>
      </div>
    </Card>
  );
};
