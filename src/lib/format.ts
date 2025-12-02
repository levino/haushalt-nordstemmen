/**
 * Formatiert einen Betrag in EUR als lesbare Zeichenkette
 */
export function formatEUR(value: number): string {
  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Formatiert einen Betrag in Millionen EUR
 */
export function formatMioEUR(value: number): string {
  const mio = value / 1_000_000;
  return `${mio.toFixed(1).replace('.', ',')} Mio. EUR`;
}

/**
 * Formatiert einen Betrag in Tausend EUR für Sankey-Diagramme
 */
export function formatTausendEUR(value: number): number {
  return Math.round(value / 1000);
}

/**
 * Beschreibungen für Ertragsarten
 */
export const ertraegeLabels: Record<string, string> = {
  steuern_und_abgaben: 'Steuern und Abgaben',
  zuwendungen_und_umlagen: 'Zuwendungen und Umlagen',
  aufloesungsertraege_sonderposten: 'Auflösungserträge',
  oeffentlich_rechtliche_entgelte: 'Öffentl.-rechtl. Entgelte',
  privatrechtliche_entgelte: 'Privatrechtl. Entgelte',
  kostenerstattungen: 'Kostenerstattungen',
  zinsen_finanzertraege: 'Zinserträge',
  sonstige_ertraege: 'Sonstige Erträge',
};

/**
 * Beschreibungen für Aufwendungsarten
 */
export const aufwendungenLabels: Record<string, string> = {
  personalaufwendungen: 'Personal',
  sach_und_dienstleistungen: 'Sach- & Dienstleistungen',
  abschreibungen: 'Abschreibungen',
  zinsen_aufwendungen: 'Zinsaufwendungen',
  transferaufwendungen: 'Transfers & Umlagen',
  sonstige_aufwendungen: 'Sonstige Aufwendungen',
};

/**
 * Farben für Diagramme
 */
export const chartColors = {
  einnahmen: '#38a169',
  ausgaben: '#e53e3e',
  neutral: '#4a5568',
};
