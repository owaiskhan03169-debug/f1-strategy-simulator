import test from 'node:test'
import assert from 'node:assert/strict'
import {
  deriveTelemetryWsUrl,
  resolveBackendOrigin,
  resolveTelemetryWsUrl,
} from './connection.js'

test('resolveBackendOrigin prefers configured backend URL', () => {
  const origin = resolveBackendOrigin({
    backendUrl: 'https://api.example.com/base/path',
    mode: 'production',
    locationOrigin: 'https://f1-strategy-simulator-ten.vercel.app',
  })

  assert.equal(origin, 'https://api.example.com')
})

test('resolveBackendOrigin uses localhost in development when backend env is missing', () => {
  const origin = resolveBackendOrigin({
    mode: 'development',
    locationOrigin: 'http://localhost:5173',
    locationHostname: 'localhost',
  })

  assert.equal(origin, 'http://localhost:8000')
})

test('resolveBackendOrigin falls back to current origin in production', () => {
  const origin = resolveBackendOrigin({
    mode: 'production',
    locationOrigin: 'https://f1-strategy-simulator-ten.vercel.app',
    locationHostname: 'f1-strategy-simulator-ten.vercel.app',
  })

  assert.equal(origin, 'https://f1-strategy-simulator-ten.vercel.app')
})

test('deriveTelemetryWsUrl uses secure WebSocket for https backends', () => {
  assert.equal(
    deriveTelemetryWsUrl('https://api.example.com'),
    'wss://api.example.com/ws',
  )
})

test('resolveTelemetryWsUrl respects explicit override', () => {
  assert.equal(
    resolveTelemetryWsUrl({
      telemetryWsUrl: 'wss://socket.example.com/stream',
      backendOrigin: 'https://api.example.com',
    }),
    'wss://socket.example.com/stream',
  )
})
