"""Provider contract: fetch(series_id, start, as_of) -> FRED-shaped observations.
No provider may silently substitute a different instrument or vintage.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request


class ProviderError(Exception):
    pass


class FredProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self, series_id, start, as_of):
        params = dict(series_id=series_id, api_key=self.api_key, file_type='json',
                      observation_start=start, observation_end=as_of,
                      realtime_start=as_of, realtime_end=as_of,
                      sort_order='asc', limit=100000)
        url = 'https://api.stlouisfed.org/fred/series/observations?' + urllib.parse.urlencode(params)
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'US-Financial-Stress-Radar/1.0'})
                with urllib.request.urlopen(req, timeout=25) as response:
                    payload = json.load(response)
                if 'observations' not in payload:
                    raise ProviderError('FRED response missing observations')
                if int(payload.get('count', len(payload['observations']))) > len(payload['observations']):
                    raise ProviderError('FRED response truncated; pagination required')
                return payload['observations']
            except urllib.error.HTTPError as exc:
                # Never expose exception URL/body: they can contain the API key.
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise ProviderError(f'FRED HTTP {exc.code}') from None
            except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                if attempt == 2:
                    raise ProviderError('FRED network/JSON failure after 3 attempts') from None
            time.sleep(1 + attempt)


class NYFedProvider:
    """Reserved adapter. Implement fetch with official Markets Data API, including effectiveDate."""
    def fetch(self, series_id, start, as_of):
        raise ProviderError('NY Fed direct adapter is reserved, not implemented; use FRED')


class FederalReserveProvider:
    """Reserved adapter for H.4.1 / H.8; preserve release, units and vintage metadata."""
    def fetch(self, series_id, start, as_of):
        raise ProviderError('Federal Reserve direct adapter is reserved, not implemented; use FRED')
