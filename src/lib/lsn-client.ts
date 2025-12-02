/**
 * LSN-Online API Client
 *
 * TypeScript client for the LSN (Landesamt für Statistik Niedersachsen) database.
 * See docs/LSN_API.md for API documentation.
 */

export interface LSNTableRow {
  jahr: number;
  einwohner: number;
  steuereinnahmenGesamt: number;
  grundsteuerA: number;
  grundsteuerB: number;
  gewerbesteuer: number;
  einkommensteueranteil: number;
  umsatzsteueranteil: number | null;
}

export interface LSNRegion {
  id: string;
  schluessel: string;
  name: string;
}

export interface LSNTableResult {
  tableId: string;
  region: LSNRegion;
  data: LSNTableRow[];
  timestamp: Date;
}

export type GebietsEbene =
  | 'land'
  | 'region'
  | 'kreis'
  | 'samtgemeinde'
  | 'gemeinde';

const EBENE_MAP: Record<GebietsEbene, number> = {
  land: 1,
  region: 2,
  kreis: 3,
  samtgemeinde: 4,
  gemeinde: 5,
};

const BASE_URL = 'https://www1.nls.niedersachsen.de/statistik';

/**
 * LSN-Online API Client
 */
export class LSNClient {
  private cookies: Map<string, string> = new Map();
  private sessionInitialized = false;

  /**
   * Initialize a new LSN session
   */
  async initSession(): Promise<boolean> {
    try {
      // Step 1: Load main page
      const mainResponse = await fetch(`${BASE_URL}/default.asp`, {
        headers: this.getHeaders(),
      });

      // Extract cookies
      this.extractCookies(mainResponse);

      // Step 2: Submit WEITER form to start session
      const formData = new URLSearchParams();
      formData.append('LOGIN1', 'WEITER');

      const sessionResponse = await fetch(`${BASE_URL}/default.asp`, {
        method: 'POST',
        headers: {
          ...this.getHeaders(),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      this.extractCookies(sessionResponse);
      this.sessionInitialized = sessionResponse.ok;

      return this.sessionInitialized;
    } catch (error) {
      console.error('Session init failed:', error);
      return false;
    }
  }

  /**
   * Fetch tax revenue data for a region
   */
  async fetchSteuereinnahmen(
    regionId: string,
    ebene: GebietsEbene = 'gemeinde'
  ): Promise<LSNTableResult | null> {
    if (!this.sessionInitialized) {
      await this.initSession();
    }

    const tableId = 'Z9200001';
    const schluessel = regionId.replace(/0+$/, '').slice(0, 6);
    const ln = EBENE_MAP[ebene];

    try {
      // Step 1: Submit table request
      const formData = new URLSearchParams();
      formData.append('DT', tableId);
      formData.append('ZUFALL', Math.random().toFixed(6));
      formData.append('UG', regionId);
      formData.append('LN', ln.toString());
      formData.append('LN2', '9');
      formData.append('RANGE0', schluessel);
      formData.append('RANGE1', schluessel);
      formData.append('TEXTSORT', '');

      const tableResponse = await fetch(`${BASE_URL}/html/mustertabelle.asp`, {
        method: 'POST',
        headers: {
          ...this.getHeaders(),
          'Content-Type': 'application/x-www-form-urlencoded',
          Referer: `${BASE_URL}/html/param_haupt.asp?DT=${tableId}`,
        },
        body: formData.toString(),
      });

      const tableHtml = await tableResponse.text();

      // Extract redirect URL from meta refresh
      const redirectMatch = tableHtml.match(/url='([^']+)'/i);
      if (!redirectMatch) {
        console.error('No redirect URL found');
        return null;
      }

      // Step 2: Wait and fetch result
      await this.delay(2000);

      const resultUrl = `https://www1.nls.niedersachsen.de${redirectMatch[1]}`;
      const resultResponse = await fetch(resultUrl, {
        headers: this.getHeaders(),
      });

      const resultHtml = await resultResponse.text();

      // Parse the HTML table
      return this.parseTableHtml(resultHtml, tableId, regionId);
    } catch (error) {
      console.error('Fetch failed:', error);
      return null;
    }
  }

  /**
   * Parse HTML table to structured data
   */
  private parseTableHtml(
    html: string,
    tableId: string,
    regionId: string
  ): LSNTableResult | null {
    const data: LSNTableRow[] = [];

    // Extract region name
    const regionMatch = html.match(
      /<TD class=left COLSPAN=\d+>(\d+)\s+([^<]+)</
    );
    const regionName = regionMatch ? regionMatch[2].trim() : 'Unknown';
    const schluessel = regionMatch ? regionMatch[1] : regionId.slice(0, 6);

    // Extract data rows
    // Pattern: Jahr, Einwohner, Gesamt, GrStA, GrStB, GewSt, EStAnteil, UStAnteil
    const rowPattern =
      /<TR class=line\d+>[\s\S]*?<TD class=left>&nbsp;(\d{4})<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>[\s\S]*?<TD>([0-9.,\-]+)<\/TD>/g;

    let match;
    while ((match = rowPattern.exec(html)) !== null) {
      data.push({
        jahr: parseInt(match[1]),
        einwohner: this.parseNumber(match[2]),
        steuereinnahmenGesamt: this.parseNumber(match[3]),
        grundsteuerA: this.parseNumber(match[4]),
        grundsteuerB: this.parseNumber(match[5]),
        gewerbesteuer: this.parseNumber(match[6]),
        einkommensteueranteil: this.parseNumber(match[7]),
        umsatzsteueranteil: this.parseNullableNumber(match[8]),
      });
    }

    if (data.length === 0) {
      // Fallback: simpler pattern for rows
      const simplePattern =
        /<TD class=left>&nbsp;+(\d{4})<\/TD>\s*<TD>(\d+)<\/TD>/g;
      while ((match = simplePattern.exec(html)) !== null) {
        // Just mark that we found rows but couldn't parse fully
        console.warn('Partial data match for year:', match[1]);
      }
    }

    return {
      tableId,
      region: {
        id: regionId,
        schluessel,
        name: regionName,
      },
      data,
      timestamp: new Date(),
    };
  }

  /**
   * Parse German number format
   */
  private parseNumber(value: string): number {
    if (value === '-' || value === '') return 0;
    // German format: 1.234,56 -> 1234.56
    return parseFloat(value.replace(/\./g, '').replace(',', '.'));
  }

  /**
   * Parse nullable number
   */
  private parseNullableNumber(value: string): number | null {
    if (value === '-' || value === '') return null;
    return this.parseNumber(value);
  }

  /**
   * Get request headers
   */
  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9',
      'Accept-Language': 'de-DE,de;q=0.9',
    };

    if (this.cookies.size > 0) {
      headers['Cookie'] = Array.from(this.cookies.entries())
        .map(([k, v]) => `${k}=${v}`)
        .join('; ');
    }

    return headers;
  }

  /**
   * Extract cookies from response
   */
  private extractCookies(response: Response): void {
    const setCookie = response.headers.get('set-cookie');
    if (setCookie) {
      const matches = setCookie.matchAll(/([^=]+)=([^;]+)/g);
      for (const match of matches) {
        this.cookies.set(match[1].trim(), match[2].trim());
      }
    }
  }

  /**
   * Delay helper
   */
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * Known regions
 */
export const REGIONS = {
  NIEDERSACHSEN: '000000000',
  NORDSTEMMEN: '254026000',
  HILDESHEIM_KREIS: '254000000',
} as const;

/**
 * Known tables
 */
export const TABLES = {
  STEUEREINNAHMEN_ZEITREIHE: 'Z9200001',
  STEUEREINNAHMEN_EINZELJAHR: 'K9200001',
  STEUERKRAFT_ZEITREIHE: 'Z9200002',
  STEUERKRAFT_EINZELJAHR: 'K9200002',
} as const;
