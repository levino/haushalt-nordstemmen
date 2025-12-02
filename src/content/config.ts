import { defineCollection, z } from 'astro:content';

// Schema für Haushaltsdaten
const haushalteCollection = defineCollection({
  type: 'data',
  schema: z.object({
    jahr: z.number(),
    typ: z.enum(['plan', 'ist']),
    quelle: z.string(),
    // Optionale detaillierte Steueraufschlüsselung (aus LSN-Datenbank)
    steuern_detail: z.object({
      grundsteuer_a: z.number(),
      grundsteuer_b: z.number(),
      gewerbesteuer_netto: z.number(),
      einkommensteueranteil: z.number(),
      umsatzsteueranteil: z.number(),
      sonstige_steuern: z.number(),
    }).optional(),
    ertraege: z.object({
      steuern_und_abgaben: z.number(),
      zuwendungen_und_umlagen: z.number(),
      aufloesungsertraege_sonderposten: z.number(),
      oeffentlich_rechtliche_entgelte: z.number(),
      privatrechtliche_entgelte: z.number(),
      kostenerstattungen: z.number(),
      zinsen_finanzertraege: z.number(),
      sonstige_ertraege: z.number(),
    }),
    aufwendungen: z.object({
      personalaufwendungen: z.number(),
      sach_und_dienstleistungen: z.number(),
      abschreibungen: z.number(),
      zinsen_aufwendungen: z.number(),
      transferaufwendungen: z.number(),
      sonstige_aufwendungen: z.number(),
    }),
    summen: z.object({
      gesamtertraege: z.number(),
      gesamtaufwendungen: z.number(),
      jahresergebnis: z.number(),
    }),
  }),
});

export const collections = {
  'haushalte': haushalteCollection,
};
