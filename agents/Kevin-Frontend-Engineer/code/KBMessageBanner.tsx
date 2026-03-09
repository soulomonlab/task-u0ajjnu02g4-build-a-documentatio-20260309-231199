import React, { useEffect, useState } from 'react';

export interface KBMessageCTA {
  label: string;
  href: string;
  external?: boolean;
}

export interface KBMessage {
  id: string;
  title?: string;
  body: string;
  cta?: KBMessageCTA;
  severity?: 'info' | 'warning' | 'critical';
  // free-form metadata; frontend should not assume shape beyond these
  metadata?: Record<string, any>;
}

export interface KBMessageBannerProps {
  message: KBMessage;
  version?: string | number;
  // persistence strategy: 'local' = localStorage, 'server' = call onDismiss, 'both' = both
  persistence?: 'local' | 'server' | 'both';
  // optional key prefix for localStorage (defaults to `kb_dismiss_`)
  storageKeyPrefix?: string;
  // optional callback used when dismissing; if provided, called after persistence.
  // can return a Promise if dismissal must wait on network call.
  onDismiss?: (messageId: string, version?: string | number) => void | Promise<void>;
  // optional className override
  className?: string;
}

const DEFAULT_PREFIX = 'kb_dismiss_';

function storageKeyFor(messageId: string, version?: string | number, prefix = DEFAULT_PREFIX) {
  const v = version === undefined ? 'v0' : `v${version}`;
  return `${prefix}${messageId}_${v}`;
}

export const KBMessageBanner: React.FC<KBMessageBannerProps> = ({
  message,
  version,
  persistence = 'local',
  storageKeyPrefix = DEFAULT_PREFIX,
  onDismiss,
  className = '',
}) => {
  const [visible, setVisible] = useState<boolean>(true);

  useEffect(() => {
    // Check local storage first when local persistence is enabled
    if (persistence === 'local' || persistence === 'both') {
      try {
        const key = storageKeyFor(message.id, version, storageKeyPrefix);
        const stored = localStorage.getItem(key);
        if (stored === 'dismissed') {
          setVisible(false);
        }
      } catch (e) {
        // localStorage may throw in some environments; fail open (show banner)
        // Swallow error to avoid breaking the app
        // eslint-disable-next-line no-console
        console.warn('KBMessageBanner: localStorage read failed', e);
      }
    }
  }, [message.id, version, persistence, storageKeyPrefix]);

  async function handleDismiss() {
    setVisible(false);

    if (persistence === 'local' || persistence === 'both') {
      try {
        const key = storageKeyFor(message.id, version, storageKeyPrefix);
        localStorage.setItem(key, 'dismissed');
      } catch (e) {
        // ignore
        // eslint-disable-next-line no-console
        console.warn('KBMessageBanner: localStorage write failed', e);
      }
    }

    if ((persistence === 'server' || persistence === 'both') && typeof onDismiss === 'function') {
      try {
        // allow caller to perform network call; don't block UI
        await onDismiss(message.id, version);
      } catch (e) {
        // Caller should handle errors; log for observability
        // eslint-disable-next-line no-console
        console.warn('KBMessageBanner: onDismiss failed', e);
      }
    }
  }

  if (!visible) return null;

  // Simple visual differentiation by severity
  const base = 'w-full px-4 py-3 flex items-start justify-between gap-4';
  const severityStyle =
    message.severity === 'critical'
      ? 'bg-red-50 text-red-900 border border-red-100'
      : message.severity === 'warning'
      ? 'bg-yellow-50 text-yellow-900 border border-yellow-100'
      : 'bg-sky-50 text-sky-900 border border-sky-100';

  return (
    <div
      role="region"
      aria-label={message.title || 'KB message'}
      aria-live="polite"
      className={`${base} ${severityStyle} ${className}`}
      data-kb-id={message.id}
      data-kb-version={String(version ?? '')}
    >
      <div className="flex-1 min-w-0">
        {message.title && <div className="font-semibold mb-0.5">{message.title}</div>}
        <div className="text-sm break-words">{message.body}</div>
        {message.cta && (
          <div className="mt-2">
            <a
              href={message.cta.href}
              target={message.cta.external ? '_blank' : undefined}
              rel={message.cta.external ? 'noopener noreferrer' : undefined}
              className="underline text-sm"
            >
              {message.cta.label}
            </a>
          </div>
        )}
      </div>

      <div className="flex-shrink-0 ml-4">
        <button
          aria-label="Dismiss KB message"
          onClick={handleDismiss}
          className="inline-flex items-center justify-center h-8 w-8 rounded-md text-sm text-gray-700 hover:bg-gray-100"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default KBMessageBanner;
