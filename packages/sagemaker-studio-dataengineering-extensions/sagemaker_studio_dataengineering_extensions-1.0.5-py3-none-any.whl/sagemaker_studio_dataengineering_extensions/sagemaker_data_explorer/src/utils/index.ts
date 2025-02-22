export function isLocalhost() {
  return ['localhost', '127.0.0.1'].some(condition => document.location.href.includes(condition));
}

export const endpointPrefix = isLocalhost() ? 'http://localhost:3000' : '';
