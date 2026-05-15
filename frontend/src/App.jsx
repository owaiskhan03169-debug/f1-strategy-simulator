import { useState, useEffect } from 'react'

function App() {
  const [telemetry, setTelemetry] = useState({
    speed_kmh: 0,
    engine_rpm: 0,
    gear: 0,
    throttle_percent: 0
  })

  useEffect(() => {
    // Backend se WebSocket connect kar rahe hain
    const ws = new WebSocket("ws://localhost:8000/ws/telemetry")

    ws.onopen = () => console.log("React UI Connected to Telemetry Stream!")
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setTelemetry(data) // Live data state me save ho raha hai
    }

    // Cleanup function: jab component unmount ho toh connection close kar do
    return () => ws.close()
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', backgroundColor: '#1e1e1e', color: '#00ff00', minHeight: '100vh' }}>
      <h2>🏁 F1 Race Dashboard (React Integration)</h2>
      <div style={{ border: '1px solid #00ff00', padding: '20px', maxWidth: '400px', marginTop: '20px' }}>
        <p><strong>Speed:</strong> {telemetry.speed_kmh} km/h</p>
        <p><strong>RPM:</strong> {telemetry.engine_rpm}</p>
        <p><strong>Gear:</strong> {telemetry.gear}</p>
        <p><strong>Throttle:</strong> {telemetry.throttle_percent}%</p>
      </div>
    </div>
  )
}

export default App