import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  haushaltSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Haushalt 2025',
      items: [
        'haushalt-2025/uebersicht',
        'haushalt-2025/einnahmen',
        'haushalt-2025/ausgaben',
        'haushalt-2025/sankey',
      ],
    },
    {
      type: 'category',
      label: 'Haushalt 2024',
      items: [
        'haushalt-2024/uebersicht',
      ],
    },
    {
      type: 'category',
      label: 'Zeitreihen',
      items: [
        'zeitreihen/uebersicht',
      ],
    },
    {
      type: 'category',
      label: 'Datenquellen',
      items: [
        'datenquellen/uebersicht',
        'datenquellen/mcp-server',
        'datenquellen/lsn-datenbank',
      ],
    },
  ],
};

export default sidebars;
