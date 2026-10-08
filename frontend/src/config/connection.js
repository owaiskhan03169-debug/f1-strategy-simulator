const LOCAL_DEV_BACKEND_ORIGIN = 'http://localhost:8000'

function parseUrl(value) {
  if (!value || typeof value !== 'string') return null
  try {
    return new URL(value.trim())
  } catch {
    return null
  }
}

function normalizeBackendOrigin(rawBackendUrl) {
  const parsed = parseUrl(rawBackendUrl)
  if (!parsed) return null

  const protocol = parsed.protocol === 'wss:' ? 'https:'
    : parsed.protocol === 'ws:' ? 'http:'
      : parsed.protocol

  if (protocol !== 'http:' && protocol !== 'https:') return null
  return `${protocol}//${parsed.host}`
}

export function resolveBackendOrigin({
  backendUrl,
  mode,
  locationOrigin,
  locationHostname,
} = {}) {
  const normalized = normalizeBackendOrigin(backendUrl)
  if (normalized) return normalized

  if (mode === 'development' || locationHostname === 'localhost' || locationHostname === '127.0.0.1') {
    return LOCAL_DEV_BACKEND_ORIGIN
  }

  return normalizeBackendOrigin(locationOrigin) || LOCAL_DEV_BACKEND_ORIGIN
}

export function deriveTelemetryWsUrl(backendOrigin) {
  const parsed = parseUrl(backendOrigin)
  if (!parsed) return 'ws://localhost:8000/ws'

  const protocol = parsed.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${parsed.host}/ws`
}

export function resolveTelemetryWsUrl({ telemetryWsUrl, backendOrigin } = {}) {
  const explicit = parseUrl(telemetryWsUrl)
  if (explicit && (explicit.protocol === 'ws:' || explicit.protocol === 'wss:')) {
    return explicit.toString()
  }
  return deriveTelemetryWsUrl(backendOrigin)
}

function runtimeContext() {
  const runtimeWindow = typeof window !== 'undefined' ? window : undefined
  const location = runtimeWindow?.location
  const env = import.meta.env || {}

  const backendOrigin = resolveBackendOrigin({
    backendUrl: env.VITE_BACKEND_URL,
    mode: env.MODE,
    locationOrigin: location?.origin,
    locationHostname: location?.hostname,
  })

  const telemetryWsUrl = resolveTelemetryWsUrl({
    telemetryWsUrl: env.VITE_TELEMETRY_WS_URL,
    backendOrigin,
  })

  return { backendOrigin, telemetryWsUrl }
}

export function getBackendOrigin() {
  return runtimeContext().backendOrigin
}

export function getTelemetryWsUrl() {
  return runtimeContext().telemetryWsUrl
}

export function getAiInsightUrl() {
  return `${getBackendOrigin()}/ai-insight`
}
