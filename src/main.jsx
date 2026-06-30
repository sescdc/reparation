import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowUpRight,
  BookOpen,
  Download,
  FileText,
  Filter,
  Landmark,
  MapPinned,
  Search,
  ShieldCheck,
} from "lucide-react";
import data from "./data/reports.json";
import "./styles.css";

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

function Header() {
  return (
    <header className="site-header">
      <a className="brand" href="#top" aria-label="NEGRO RESEARCH INSTITUTE home">
        <span className="brand-mark">NRI</span>
        <span>{data.agency}</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="#national">National</a>
        <a href="#cities">Cities</a>
        <a href="#method">Method</a>
      </nav>
      <a className="header-action" href={data.nationalReportPath} target="_blank" rel="noreferrer">
        <FileText size={17} />
        National PDF
      </a>
    </header>
  );
}

function Hero() {
  return (
    <section id="top" className="hero">
      <div className="hero-copy">
        <h1>NEGRO RESEARCH INSTITUTE</h1>
        <p className="hero-lede">
          United States Reparations Dossier for Black people: a city-by-city evidence library
          paired with a national-facing summary of the reports in this archive.
        </p>
        <div className="hero-actions">
          <a className="primary-button" href="#cities">
            <BookOpen size={19} />
            Read the Reports
          </a>
          <a className="secondary-button" href={data.nationalReportPath} target="_blank" rel="noreferrer">
            <Download size={18} />
            Download PDF
          </a>
        </div>
      </div>
      <div className="hero-panel" aria-label="Archive summary">
        <img
          className="hero-archive-image"
          src="/assets/reparations-archive-hero.png"
          alt="Archival reparations research documents and city dossiers"
        />
        <div className="panel-topline">
          <MapPinned size={19} />
          United States Reparations Dossier
        </div>
        <div className="hero-total">{data.aggregateTotalLabel}</div>
        <p>{data.methodologyNote}</p>
        <div className="mini-grid">
          <span>
            <strong>{data.cityCount}</strong>
            City Reports
          </span>
          <span>
            <strong>{data.categories.length}</strong>
            Damage Categories
          </span>
          <span>
            <strong>PDF</strong>
            Public Archive
          </span>
        </div>
      </div>
    </section>
  );
}

function NationalBreakdown() {
  const topCities = [...data.cities].sort((a, b) => b.total - a.total).slice(0, 6);
  return (
    <section id="national" className="national section-band">
      <div className="section-heading">
        <h2>National Breakdown</h2>
        <p>
          A disciplined aggregate view of the 36 local and regional briefs, with the original
          source PDFs preserved for city-level inspection.
        </p>
      </div>
      <div className="national-layout">
        <div className="total-block">
          <span>Archive aggregate</span>
          <strong>{formatCurrency(data.aggregateTotal)}</strong>
          <p>
            Sum of headline liability estimates across the reports in the source folder. This is
            not labeled as a complete national reparations total.
          </p>
        </div>
        <div className="rank-list">
          {topCities.map((city, index) => (
            <a href={`#${city.slug}`} className="rank-row" key={city.slug}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{city.name}</strong>
              <em>{city.totalLabel}</em>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

function MethodBand() {
  return (
    <section id="method" className="method">
      <div>
        <h2>Evidence Architecture</h2>
        <p>
          The archive centers the documents themselves. Each local brief can be opened directly,
          while the national dossier states the aggregate limits in plain language.
        </p>
      </div>
      <ul>
        {data.categories.map((category) => (
          <li key={category}>
            <ShieldCheck size={18} />
            {category}
          </li>
        ))}
      </ul>
    </section>
  );
}

function CityArchive() {
  const [query, setQuery] = useState("");
  const [stateFilter, setStateFilter] = useState("All");
  const states = useMemo(
    () => ["All", ...Array.from(new Set(data.cities.map((city) => city.state))).sort()],
    []
  );
  const filtered = data.cities.filter((city) => {
    const haystack = `${city.name} ${city.state} ${city.jurisdiction}`.toLowerCase();
    return (
      haystack.includes(query.toLowerCase()) &&
      (stateFilter === "All" || city.state === stateFilter)
    );
  });

  return (
    <section id="cities" className="cities">
      <div className="section-heading">
        <h2>City Evidence Library</h2>
        <p>
          Every city section includes the source PDF from the Desktop reparations folder, with
          headline figures surfaced for scanning.
        </p>
      </div>
      <div className="archive-controls">
        <label className="search-field">
          <Search size={18} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search city, county, or state"
          />
        </label>
        <label className="select-field">
          <Filter size={18} />
          <select value={stateFilter} onChange={(event) => setStateFilter(event.target.value)}>
            {states.map((state) => (
              <option key={state}>{state}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="city-grid">
        {filtered.map((city) => (
          <article className="city-card" id={city.slug} key={city.slug}>
            <div className="city-card-head">
              <Landmark size={20} />
              <span>{city.state}</span>
            </div>
            <h3>{city.name}</h3>
            <p>{city.jurisdiction}</p>
            <div className="city-total">{city.totalLabel}</div>
            <div className="city-meta">
              <span>{city.pageCount || "PDF"} pages</span>
              <span>{city.sourcePageNote}</span>
            </div>
            <div className="city-actions">
              <a href={city.pdfPath} target="_blank" rel="noreferrer">
                <FileText size={17} />
                View
              </a>
              <a href={city.pdfPath} download>
                <Download size={17} />
                Download PDF
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <NationalBreakdown />
        <MethodBand />
        <CityArchive />
        <section className="closing">
          <h2>Read the Reports</h2>
          <p>
            The public archive is built to make the claim auditable: national summary first, city
            evidence always one click away.
          </p>
          <a className="primary-button" href={data.nationalReportPath} target="_blank" rel="noreferrer">
            <ArrowUpRight size={19} />
            Open National Dossier
          </a>
        </section>
      </main>
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
