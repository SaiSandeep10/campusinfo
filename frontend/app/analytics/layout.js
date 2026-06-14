// frontend/app/analytics/layout.js
export default function AnalyticsLayout({ children }) {
  return (
    <div style={{
      height: '100vh',
      overflowY: 'auto',
      background: '#080C14'
    }}>
      {children}
    </div>
  )
}