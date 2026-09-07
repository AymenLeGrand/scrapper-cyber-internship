/**
 * France Cyber & Cryptology Internship Tracker
 * Client-side Controller
 */

let allJobs = [];
let appliedJobs = new Set(JSON.parse(localStorage.getItem('applied_jobs') || '[]'));
let activeCategory = 'all';
let activeSpontaneousCategory = 'all';

const SPONTANEOUS_COMPANIES = [
  // =========================================================================
  // 1. SÉCURITÉ EMBARQUÉE, MATÉRIELLE & CESTI
  // =========================================================================
  {
    name: "SERMA Safety & Security",
    group: "hardware",
    sector: "CESTI ANSSI, Canaux Auxiliaires & Puces",
    url: "https://www.serma-safety-security.com/nous-rejoindre/"
  },
  {
    name: "eShard",
    group: "hardware",
    sector: "Attaques physiques SCA & FIA, Crypto Puces & Mobile",
    url: "https://eshard.com/careers",
    email: "jobs@eshard.com"
  },
  {
    name: "Secure-IC",
    group: "hardware",
    sector: "Sécurité Matérielle, IP Crypto & Post-Quantique",
    url: "https://www.secure-ic.com/company/careers/",
    email: "contact@secure-ic.com"
  },
  {
    name: "NinjaLab",
    group: "hardware",
    sector: "Cryptanalyse & Attaques Physiques sur Cartes à Puce / HSM",
    url: "https://ninjalab.io",
    email: "contact@ninjalab.io"
  },
  {
    name: "Oppida (Groupe Apave)",
    group: "hardware",
    sector: "CESTI ANSSI, Évaluation Sécuritaire & Crypto",
    url: "https://www.oppida.fr/rejoignez-nous/"
  },
  {
    name: "Idemia",
    group: "hardware",
    sector: "Composants Sécurisés, Crypto Embarquée & Cartes à Puce",
    url: "https://careers.idemia.com/search/?q=&locationsearch=France"
  },

  // =========================================================================
  // 2. CRYPTOLOGIE DE POINTE & R&D
  // =========================================================================
  {
    name: "CryptoExperts",
    group: "crypto",
    sector: "Cryptologie Théorique & Appliquée, White-box",
    url: "https://www.cryptoexperts.com/contact/",
    email: "contact@cryptoexperts.com"
  },
  {
    name: "Zama",
    group: "crypto",
    sector: "Cryptographie Homomorphe (FHE) & Confidentialité",
    url: "https://jobs.zama.org"
  },
  {
    name: "Quarkslab",
    group: "crypto",
    sector: "R&D, Recherche de Vulnérabilités & Reverse",
    url: "https://blog.quarkslab.com/tag/internship.html",
    label: "Blog Stages &rarr;",
    email: "jobs@quarkslab.com"
  },
  {
    name: "CEA (Leti / List)",
    group: "crypto",
    sector: "Recherche Crypto Matérielle & Architectures Sécurisées",
    url: "https://www.emploi.cea.fr/accueil.aspx?LCID=1036"
  },
  {
    name: "Inria",
    group: "crypto",
    sector: "Recherche Fondamentale & Appliquée en Cryptologie",
    url: "https://www.inria.fr/fr/nous-rejoindre"
  },

  // =========================================================================
  // 3. OFFENSIVE, PENTEST & ÉDITEURS
  // =========================================================================
  {
    name: "Synacktiv",
    group: "offensive",
    sector: "Pentest, Audit & R&D Offensive",
    url: "https://www.synacktiv.com/nous-rejoindre",
    email: "apply@synacktiv.com"
  },
  {
    name: "Stormshield",
    group: "offensive",
    sector: "Éditeur Firewall, UTM & Endpoint (Airbus)",
    url: "https://careers.stormshield.eu/"
  },
  {
    name: "Sekoia.io",
    group: "offensive",
    sector: "Éditeur SOC, CTI & XDR",
    url: "https://careers.sekoia.com/"
  },
  {
    name: "Gatewatcher",
    group: "offensive",
    sector: "Éditeur NDR & Détection Réseau",
    url: "https://www.gatewatcher.com/carrieres/"
  },
  {
    name: "OCTO Technology",
    group: "offensive",
    sector: "Architecture & DevSecOps",
    url: "https://jobs.smartrecruiters.com/OctoTechnology"
  },

  // =========================================================================
  // 4. CONSEIL, DÉFENSE & ÉTAT
  // =========================================================================
  {
    name: "ANSSI",
    group: "consulting_defense",
    sector: "Agence Nationale de Sécurité de l'État",
    url: "https://cyber.gouv.fr/nous-rejoindre"
  },
  {
    name: "Wavestone",
    group: "consulting_defense",
    sector: "Conseil Cyber & Digital Trust",
    url: "https://jobs.smartrecruiters.com/Wavestone1"
  },
  {
    name: "Devoteam Cyber Trust",
    group: "consulting_defense",
    sector: "Conseil & Intégration Sécurité",
    url: "https://jobs.smartrecruiters.com/Devoteam"
  },
  {
    name: "Sopra Steria",
    group: "consulting_defense",
    sector: "Cyberdéfense & Conseil",
    url: "https://jobs.smartrecruiters.com/SopraSteria1"
  },
  {
    name: "HeadMind Partners",
    group: "consulting_defense",
    sector: "Cyber Risk & Sécurité",
    url: "https://join.headmind.com"
  },
  {
    name: "Sia Partners",
    group: "consulting_defense",
    sector: "Conseil Cybersécurité & IA",
    url: "https://jobs.smartrecruiters.com/Sia"
  },
  {
    name: "Forvis Mazars",
    group: "consulting_defense",
    sector: "Audit IT & Cybersécurité",
    url: "https://jobs.smartrecruiters.com/MAZARS"
  },
  {
    name: "Orange Cyberdefense",
    group: "consulting_defense",
    sector: "Leader MSSP, SOC & Détection",
    url: "https://orange.jobs/jobs/v3/search?keyword=Orange%20Cyberdefense"
  },
  {
    name: "Thales",
    group: "consulting_defense",
    sector: "Défense, Cyber & Spatial",
    url: "https://thales.wd3.myworkdayjobs.com/Careers"
  },
  {
    name: "Airbus Protect",
    group: "consulting_defense",
    sector: "Cybersécurité Industrielle, Défense & Sûreté de Fonctionnement",
    url: "https://www.protect.airbus.com/careers/job-offers/"
  },
  {
    name: "VINCI / Axians",
    group: "consulting_defense",
    sector: "Infrastructures Cyber & Réseaux",
    url: "https://jobs.vinci.com/fr/"
  }
];

document.addEventListener('DOMContentLoaded', async () => {
  renderSpontaneousGrid();
  setupSpontaneousToggle();
  await loadJobs();
  setupEventListeners();
});

function renderSpontaneousGrid() {
  const grid = document.getElementById('spontaneousGrid');
  if (!grid) return;

  const filtered = SPONTANEOUS_COMPANIES.filter(c => {
    if (activeSpontaneousCategory === 'all') return true;
    return c.group === activeSpontaneousCategory;
  });

  grid.innerHTML = filtered.map(c => `
    <div class="p-3 bg-zinc-950/80 rounded-md border border-zinc-800/80 flex flex-col justify-between gap-2.5 hover:border-zinc-700 transition">
      <div>
        <div class="font-medium text-xs text-zinc-100">${escapeHtml(c.name)}</div>
        <div class="text-[11px] text-zinc-400 mt-0.5">${escapeHtml(c.sector)}</div>
      </div>
      <div class="flex items-center gap-3 pt-1 text-xs">
        <a href="${c.url}" target="_blank" rel="noopener noreferrer" class="font-medium text-indigo-400 hover:text-indigo-300 transition">
          ${c.label || 'Portail &rarr;'}
        </a>
        ${c.email ? `<a href="mailto:${c.email}" class="text-zinc-400 hover:text-zinc-200 transition">Email direct</a>` : ''}
      </div>
    </div>
  `).join('');
}

function setupSpontaneousToggle() {
  const toggleBtn = document.getElementById('toggleSpontaneousBtn');
  const headerBtn = document.getElementById('headerSpontaneousBtn');
  const content = document.getElementById('spontaneousContent');
  const toggleText = document.getElementById('spontaneousToggleText');
  const section = document.getElementById('spontaneousSection');
  const spontChips = document.querySelectorAll('#spontaneousCategoryChips .category-chip');

  function toggle() {
    const isHidden = content.classList.contains('hidden');
    if (isHidden) {
      content.classList.remove('hidden');
      toggleText.textContent = 'Masquer';
    } else {
      content.classList.add('hidden');
      toggleText.textContent = 'Afficher';
    }
  }

  if (toggleBtn) toggleBtn.addEventListener('click', toggle);
  if (headerBtn) {
    headerBtn.addEventListener('click', () => {
      if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        toggleText.textContent = 'Masquer';
      }
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  spontChips.forEach(chip => {
    chip.addEventListener('click', () => {
      spontChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeSpontaneousCategory = chip.getAttribute('data-spont-cat');
      renderSpontaneousGrid();
    });
  });
}

async function loadJobs() {
  const container = document.getElementById('jobsContainer');
  try {
    const res = await fetch('./data/jobs.json?t=' + Date.now());
    if (!res.ok) throw new Error('Impossible de charger data/jobs.json');
    allJobs = await res.json();
    
    updateStats();
    populateLocationFilter();
    renderJobs();
  } catch (err) {
    console.error(err);
    container.innerHTML = `
      <div class="p-4 bg-rose-950/30 border border-rose-900/60 rounded text-rose-300 text-xs">
        <p class="font-semibold">Erreur de chargement</p>
        <p class="text-xs mt-1 text-rose-400">Impossible de lire data/jobs.json.</p>
      </div>
    `;
  }
}

const FRENCH_HUBS = [
  { label: 'Paris / IDF', keywords: ['paris', 'idf', 'courbevoie', 'nanterre', 'puteaux', 'levallois', 'défense', 'defense', 'saint-ouen', 'vélizy', 'massy', 'saclay'] },
  { label: 'Nantes', keywords: ['nantes', 'herblain'] },
  { label: 'Toulouse', keywords: ['toulouse', 'colomiers', 'blagnac'] },
  { label: 'Rennes', keywords: ['rennes', 'cesson'] },
  { label: 'Lyon', keywords: ['lyon', 'villeurbanne', 'grenoble'] },
  { label: 'Lille', keywords: ['lille', 'villeneuve'] },
  { label: 'Bordeaux', keywords: ['bordeaux', 'mérignac', 'pessac'] },
  { label: 'Aix-Marseille', keywords: ['aix', 'marseille'] },
  { label: 'Sophia Antipolis / Nice', keywords: ['sophia', 'nice', 'antibes'] },
  { label: 'Brest', keywords: ['brest'] },
  { label: 'Strasbourg', keywords: ['strasbourg'] }
];

function populateLocationFilter() {
  const select = document.getElementById('locationFilter');
  if (!select) return;

  const activeJobs = allJobs.filter(j => j.status === 'active');
  const counts = {};
  const matchedJobIds = new Set();

  FRENCH_HUBS.forEach(hub => {
    let count = 0;
    activeJobs.forEach(job => {
      const loc = (job.location || '').toLowerCase();
      if (hub.keywords.some(k => loc.includes(k))) {
        count++;
        matchedJobIds.add(job.id);
      }
    });
    if (count > 0) {
      counts[hub.label] = { count, keywords: hub.keywords };
    }
  });

  // Catch any unexpected new locations from newly scraped announcements
  activeJobs.forEach(job => {
    if (!matchedJobIds.has(job.id) && job.location) {
      let clean = job.location.split(',')[0].trim().replace(/\(.*?\)/, '').trim();
      if (clean && clean.length > 2) {
        if (!counts[clean]) {
          counts[clean] = { count: 0, keywords: [clean.toLowerCase()] };
        }
        counts[clean].count++;
      }
    }
  });

  const prevSelected = select.value;
  let html = `<option value="all">Toutes les villes (${activeJobs.length})</option>`;
  
  const sortedHubs = Object.entries(counts).sort((a, b) => b[1].count - a[1].count);
  sortedHubs.forEach(([label, data]) => {
    html += `<option value="${label}">${label} (${data.count})</option>`;
  });

  select.innerHTML = html;
  if (prevSelected && counts[prevSelected]) {
    select.value = prevSelected;
  } else {
    select.value = 'all';
  }
}

function updateStats() {
  const activeJobs = allJobs.filter(j => j.status === 'active');
  const cryptoJobs = activeJobs.filter(j => j.is_crypto);
  const cyberJobs = activeJobs.filter(j => !j.is_crypto);

  document.getElementById('statTotal').textContent = activeJobs.length;
  document.getElementById('statCrypto').textContent = cryptoJobs.length;
  document.getElementById('statCyber').textContent = cyberJobs.length;
  document.getElementById('countAll').textContent = activeJobs.length;
}

function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  const locationFilter = document.getElementById('locationFilter');
  const hideAppliedToggle = document.getElementById('hideAppliedToggle');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const chips = document.querySelectorAll('#categoryChips .category-chip');

  searchInput.addEventListener('input', () => renderJobs());
  locationFilter.addEventListener('change', () => renderJobs());
  hideAppliedToggle.addEventListener('change', () => renderJobs());

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-category');
      renderJobs();
    });
  });

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      searchInput.value = '';
      locationFilter.value = 'all';
      hideAppliedToggle.checked = false;
      chips.forEach(c => c.classList.remove('active'));
      chips[0].classList.add('active');
      activeCategory = 'all';
      renderJobs();
    });
  }

  if (exportCsvBtn) {
    exportCsvBtn.addEventListener('click', exportToCsv);
  }
}

function getFilteredJobs() {
  const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
  const selectedLocation = document.getElementById('locationFilter').value;
  const hideApplied = document.getElementById('hideAppliedToggle').checked;

  return allJobs.filter(job => {
    if (job.status !== 'active') return false;

    if (hideApplied && appliedJobs.has(job.id)) return false;

    if (activeCategory === 'crypto' && !job.is_crypto) return false;
    if (activeCategory === 'offensive') {
      const isOff = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('offensive') || dl.includes('pentest') || dl.includes('reverse') || dl.includes('red team') || dl.includes('exploit') || dl.includes('vulnérabilit') || dl.includes('hardening');
      });
      if (!isOff && !(job.domain || '').includes('Offensive')) return false;
    }
    if (activeCategory === 'defensive') {
      const isDef = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('défensive') || dl.includes('soc') || dl.includes('incident') || dl.includes('detection') || dl.includes('forensic') || dl.includes('cert') || dl.includes('csirt') || dl.includes('threat');
      });
      if (!isDef && !(job.domain || '').includes('SOC') && !(job.domain || '').includes('Defensive')) return false;
    }
    if (activeCategory === 'cloud_devsecops') {
      const isCloud = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('cloud') || dl.includes('devsecops') || dl.includes('ci/cd') || dl.includes('container') || dl.includes('kubernetes') || dl.includes('infrastructure');
      });
      if (!isCloud && !(job.domain || '').includes('Cloud')) return false;
    }
    if (activeCategory === 'ai_cyber') {
      const isAi = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('ia') || dl.includes('intelligence artificielle') || dl.includes('machine learning') || dl.includes('llm');
      });
      if (!isAi && !(job.domain || '').includes('IA')) return false;
    }

    // Dynamic Location filter
    if (selectedLocation !== 'all') {
      const hub = FRENCH_HUBS.find(h => h.label === selectedLocation);
      const loc = (job.location || '').toLowerCase();
      if (hub) {
        if (!hub.keywords.some(k => loc.includes(k))) return false;
      } else {
        if (!loc.includes(selectedLocation.toLowerCase())) return false;
      }
    }

    if (query) {
      const searchTarget = [
        job.title,
        job.company_name,
        job.location,
        job.domain,
        job.description || '',
        (job.all_domains || []).join(' ')
      ].join(' ').toLowerCase();

      const terms = query.split(/\s+/);
      const matchesAll = terms.every(term => searchTarget.includes(term));
      if (!matchesAll) return false;
    }

    return true;
  });
}

function renderJobs() {
  const container = document.getElementById('jobsContainer');
  const emptyState = document.getElementById('emptyState');
  const resultsCount = document.getElementById('resultsCount');

  const filtered = getFilteredJobs();
  resultsCount.textContent = `${filtered.length} offres`;

  if (filtered.length === 0) {
    container.innerHTML = '';
    emptyState.classList.remove('hidden');
    return;
  }

  emptyState.classList.add('hidden');
  container.innerHTML = filtered.map(job => createJobCardHtml(job)).join('');

  attachCardEvents();
}

function createJobCardHtml(job) {
  const isApplied = appliedJobs.has(job.id);
  const isCrypto = job.is_crypto;
  
  let badgeStyle = 'bg-zinc-800 text-zinc-300';
  if (isCrypto) {
    badgeStyle = 'bg-indigo-950 text-indigo-300 border border-indigo-800/60';
  } else if ((job.domain || '').includes('Offensive')) {
    badgeStyle = 'bg-rose-950/70 text-rose-300 border border-rose-900/60';
  } else if ((job.domain || '').includes('SOC') || (job.domain || '').includes('Defensive')) {
    badgeStyle = 'bg-sky-950/70 text-sky-300 border border-sky-900/60';
  } else if ((job.domain || '').includes('Cloud')) {
    badgeStyle = 'bg-purple-950/70 text-purple-300 border border-purple-900/60';
  }

  return `
    <article class="job-card bg-zinc-900/40 rounded-lg border border-zinc-800/70 p-4 hover:border-zinc-700 transition ${isApplied ? 'opacity-50' : ''}">
      <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        
        <div class="space-y-2 flex-1">
          <div>
            <span class="text-[11px] font-medium px-2 py-0.5 rounded ${badgeStyle}">
              ${escapeHtml(job.domain || 'Cybersécurité')}
            </span>
          </div>

          <h2 class="text-sm font-semibold text-zinc-100 hover:text-indigo-400 transition tracking-tight">
            <a href="${job.direct_url}" target="_blank" rel="noopener noreferrer">
              ${escapeHtml(job.title)}
            </a>
          </h2>

          <div class="flex flex-wrap items-center gap-x-2 text-xs text-zinc-400">
            <span class="font-medium text-zinc-200">${escapeHtml(job.company_name)}</span>
            <span class="text-zinc-600">•</span>
            <span>${escapeHtml(job.location || 'France')}</span>
          </div>

          ${job.description ? `
            <p class="text-xs text-zinc-400 pt-0.5 line-clamp-2 leading-relaxed">
              ${escapeHtml(job.description)}
            </p>
          ` : ''}
        </div>

        <div class="flex flex-col sm:items-end gap-2.5 shrink-0 pt-2 sm:pt-0">
          <a 
            href="${job.direct_url}" 
            target="_blank" 
            rel="noopener noreferrer"
            class="inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 text-xs font-medium rounded-md bg-zinc-100 text-zinc-950 hover:bg-white transition"
          >
            <span>Postuler</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </a>

          <div class="flex items-center gap-3 text-xs">
            <button class="copy-link-btn text-xs text-zinc-500 hover:text-zinc-300 transition" data-url="${job.direct_url}">
              Copier le lien
            </button>
            <label class="inline-flex items-center gap-1.5 text-xs text-zinc-400 cursor-pointer select-none">
              <input type="checkbox" class="toggle-applied rounded bg-zinc-900 border-zinc-700 text-indigo-500 focus:ring-0 w-3.5 h-3.5" data-id="${job.id}" ${isApplied ? 'checked' : ''}>
              <span>Postulé</span>
            </label>
          </div>
        </div>

      </div>
    </article>
  `;
}

function attachCardEvents() {
  document.querySelectorAll('.copy-link-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = btn.getAttribute('data-url');
      navigator.clipboard.writeText(url).then(() => {
        const original = btn.textContent;
        btn.textContent = 'Copié !';
        btn.classList.add('text-emerald-400');
        setTimeout(() => {
          btn.textContent = original;
          btn.classList.remove('text-emerald-400');
        }, 1500);
      });
    });
  });

  document.querySelectorAll('.toggle-applied').forEach(chk => {
    chk.addEventListener('change', (e) => {
      const id = e.target.getAttribute('data-id');
      if (e.target.checked) {
        appliedJobs.add(id);
      } else {
        appliedJobs.delete(id);
      }
      localStorage.setItem('applied_jobs', JSON.stringify(Array.from(appliedJobs)));
      
      const card = e.target.closest('.job-card');
      if (card) {
        card.classList.toggle('opacity-50', e.target.checked);
      }

      if (document.getElementById('hideAppliedToggle').checked) {
        renderJobs();
      }
    });
  });
}

function exportToCsv() {
  const filtered = getFilteredJobs();
  if (filtered.length === 0) {
    alert('Aucune offre à exporter.');
    return;
  }

  const headers = ['Titre', 'Entreprise', 'Lieu', 'Domaine', 'Lien Direct'];
  const rows = filtered.map(j => [
    `"${(j.title || '').replace(/"/g, '""')}"`,
    `"${(j.company_name || '').replace(/"/g, '""')}"`,
    `"${(j.location || '').replace(/"/g, '""')}"`,
    `"${(j.domain || '').replace(/"/g, '""')}"`,
    `"${(j.direct_url || '').replace(/"/g, '""')}"`
  ]);

  const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `stages_cyber_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
