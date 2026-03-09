// useApiRetry.ts
// Lightweight fetch wrapper that handles 429 and DRY_RUN_LIMIT with retries + backoff.

export interface ApiFetchOptions extends RequestInit {
  maxRetries?: number;
  baseDelayMs?: number;
}

export interface ApiError extends Error {
  status?: number;
  code?: string;
  retryable?: boolean;
}

function wait(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}

function parseRetryAfter(header?: string | null): number | null {
  if (!header) return null;
  const s = header.trim();
  // If it's a number of seconds
  const seconds = Number(s);
  if (!Number.isNaN(seconds)) return seconds * 1000;
  // Else try to parse HTTP-date
  const date = Date.parse(s);
  if (!Number.isNaN(date)) return Math.max(date - Date.now(), 0);
  return null;
}

export async function apiFetch(input: RequestInfo, init: ApiFetchOptions = {}): Promise<any> {
  const { maxRetries = 4, baseDelayMs = 300, ...fetchInit } = init;

  let attempt = 0;
  let lastErr: ApiError | null = null;

  while (attempt <= maxRetries) {
    try {
      const res = await fetch(input, fetchInit as RequestInit);

      const contentType = res.headers.get('content-type') || '';
      const isJson = contentType.includes('application/json');
      const body = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);

      if (res.ok) return body;

      // Non-OK responses: build ApiError
      const err: ApiError = new Error(`HTTP ${res.status}`) as ApiError;
      err.status = res.status;

      // Handle common API error shapes
      if (body && typeof body === 'object') {
        // some APIs send { error: { code: 'DRY_RUN_LIMIT', message: '...' } }
        const maybeError = (body as any).error || (body as any);
        if (maybeError && typeof maybeError.code === 'string') {
          err.code = maybeError.code;
        }
        if (maybeError && typeof maybeError.message === 'string') {
          err.message = maybeError.message;
        }
      }

      // 429 handling — retryable
      if (res.status === 429) {
        err.retryable = true;
        lastErr = err;
        attempt += 1;

        // Respect Retry-After header when present
        const retryAfterMs = parseRetryAfter(res.headers.get('retry-after'));
        const backoff = retryAfterMs ?? Math.round(baseDelayMs * Math.pow(2, attempt) * (0.8 + Math.random() * 0.4));
        await wait(backoff);
        continue;
      }

      // DRY_RUN_LIMIT — surface a friendly, non-retryable error so UI/SDK can show guidance
      if (err.code === 'DRY_RUN_LIMIT') {
        err.retryable = false;
        throw err;
      }

      // For 5xx we may retry
      if (res.status >= 500 && res.status < 600) {
        err.retryable = true;
        lastErr = err;
        attempt += 1;
        const backoff = Math.round(baseDelayMs * Math.pow(2, attempt) * (0.8 + Math.random() * 0.4));
        await wait(backoff);
        continue;
      }

      // Otherwise non-retryable
      throw err;
    } catch (e) {
      // Network errors or thrown ApiError
      const err = e as ApiError;
      // If the error is marked retryable and we still have attempts -> retry
      if (err && err.retryable && attempt < maxRetries) {
        lastErr = err;
        attempt += 1;
        const backoff = Math.round(baseDelayMs * Math.pow(2, attempt) * (0.8 + Math.random() * 0.4));
        await wait(backoff);
        continue;
      }
      // Otherwise bubble up
      throw err;
    }
  }

  // If we exit loop, throw last error
  throw lastErr ?? new Error('apiFetch: Unknown error');
}

export default apiFetch;
