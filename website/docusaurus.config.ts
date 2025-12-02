import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Haushalt Nordstemmen',
  tagline: 'Transparente Visualisierung des Gemeindehaushalts',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://levino.github.io',
  baseUrl: '/haushalt-nordstemmen/',

  organizationName: 'levino',
  projectName: 'haushalt-nordstemmen',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'de',
    locales: ['de'],
  },

  // Mermaid aktivieren
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/levino/haushalt-nordstemmen/tree/main/website/',
        },
        blog: false, // Blog deaktivieren
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    // Mermaid Konfiguration
    mermaid: {
      theme: {
        light: 'default',
        dark: 'dark',
      },
    },
    navbar: {
      title: 'Haushalt Nordstemmen',
      logo: {
        alt: 'Gemeinde Nordstemmen',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'haushaltSidebar',
          position: 'left',
          label: 'Haushalt',
        },
        {
          to: '/docs/einnahmen',
          label: 'Einnahmen',
          position: 'left',
        },
        {
          to: '/docs/ausgaben',
          label: 'Ausgaben',
          position: 'left',
        },
        {
          href: 'https://github.com/levino/haushalt-nordstemmen',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Haushalt',
          items: [
            {
              label: 'Übersicht',
              to: '/docs/intro',
            },
            {
              label: 'Einnahmen',
              to: '/docs/einnahmen',
            },
            {
              label: 'Ausgaben',
              to: '/docs/ausgaben',
            },
          ],
        },
        {
          title: 'Quellen',
          items: [
            {
              label: 'Gemeinde Nordstemmen',
              href: 'https://www.nordstemmen.de/',
            },
            {
              label: 'Ratsinformationssystem',
              href: 'https://nordstemmen.ratsinfomanagement.net/',
            },
            {
              label: 'LSN-Online Datenbank',
              href: 'https://www1.nls.niedersachsen.de/statistik/',
            },
          ],
        },
        {
          title: 'Mehr',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/levino/haushalt-nordstemmen',
            },
            {
              label: 'Daten (YAML)',
              href: 'https://github.com/levino/haushalt-nordstemmen/tree/main/data',
            },
          ],
        },
      ],
      copyright: `Datenstand: Dezember 2024. Alle Daten aus öffentlichen Quellen. Erstellt mit Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['yaml', 'python', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
