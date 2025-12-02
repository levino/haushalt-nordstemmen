import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs">
            Zum Haushalt 2025
          </Link>
        </div>
      </div>
    </header>
  );
}

function Feature({title, description, link}: {title: string; description: string; link: string}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
        <Link to={link}>Mehr erfahren</Link>
      </div>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <Feature
            title="Einnahmen"
            description="Woher kommt das Geld? Steuern, Zuweisungen, Gebühren - alle Einnahmequellen auf einen Blick."
            link="/docs/haushalt-2025/einnahmen"
          />
          <Feature
            title="Ausgaben"
            description="Wofür wird das Geld verwendet? Personal, Sachkosten, Transfers - die größten Ausgabenposten."
            link="/docs/haushalt-2025/ausgaben"
          />
          <Feature
            title="Sankey-Diagramme"
            description="Visualisierung des Geldflusses: Von den Einnahmen zu den Ausgaben in interaktiven Diagrammen."
            link="/docs/haushalt-2025/sankey"
          />
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Startseite"
      description="Transparente Visualisierung des Gemeindehaushalts Nordstemmen mit Sankey-Diagrammen">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <section className="container margin-vert--xl">
          <div className="row">
            <div className="col col--8 col--offset-2">
              <Heading as="h2">Aktuelle Haushaltslage</Heading>
              <p>
                Die Gemeinde Nordstemmen befindet sich seit 2024 in der <strong>Haushaltssicherung</strong>.
                Der Haushaltsplan 2025 weist einen <strong>Fehlbetrag von 4,9 Mio. EUR</strong> aus.
              </p>
              <table>
                <thead>
                  <tr>
                    <th>Kennzahl</th>
                    <th>2024</th>
                    <th>2025</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Ordentliche Erträge</td>
                    <td>24,7 Mio. EUR</td>
                    <td>24,1 Mio. EUR</td>
                  </tr>
                  <tr>
                    <td>Ordentliche Aufwendungen</td>
                    <td>25,4 Mio. EUR</td>
                    <td>29,0 Mio. EUR</td>
                  </tr>
                  <tr>
                    <td>Jahresergebnis</td>
                    <td>-0,7 Mio. EUR</td>
                    <td>-4,9 Mio. EUR</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
