/**
 * France Cyber & Cryptology M2 Internship Tracker
 * Client-side Controller for GitHub Pages
 */

let allJobs = [];
let appliedJobs = new Set(JSON.parse(localStorage.getItem('applied_jobs') || '[]'));
let activeCategory = 'all';

document.addEventListener('DOMContentLoaded', async () => {
  await loadJobs();
  setupEventListeners();
});

async function loadJobs() {
  const container = document.getElementById('jobsContainer');
  try {
    const res = await fetch('./data/jobs.json?t=' + Date.now());
    if (!res.ok) throw new Error('Impossible de charger data/jobs.json');
    allJobs = await res.json();
    
    updateStats();
    renderJobs();
  } catch (err) {
    console.error(err);
    container.innerHTML = `
      <div class="p-6 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-sm">
        <p class="font-semibold">Erreur de chargement des données</p>
        <p class="text-xs mt-1 text-rose-600">Impossible de lire data/jobs.json. Vérifiez que le scraper a bien tourné.</p>
      </div>
    `;
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
  const chips = document.querySelectorAll('.category-chip');

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

    // Filter by applied status
    if (hideApplied && appliedJobs.has(job.id)) return false;

    // Category filter
    if (activeCategory === 'crypto' && !job.is_crypto) return false;
    if (activeCategory === 'offensive') {
      const isOff = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('offensive') || dl.includes('pentest') || dl.includes('reverse') || dl.includes('red team') || dl.includes('exploit') || dl.includes('vulnérabilit') || dl.includes('hardening');
      });
      if (!isOff) return false;
    }
    if (activeCategory === 'defensive') {
      const isDef = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('defensive') || dl.includes('cyberdéfense') || dl.includes('soc') || dl.includes('mdr') || dl.includes('dfir') || dl.includes('csirt') || dl.includes('forensic') || dl.includes('détection') || dl.includes('cti') || dl.includes('veille');
      });
      if (!isDef) return false;
    }
    if (activeCategory === 'cloud_devsecops') {
      const isCld = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('cloud') || dl.includes('devsecops') || dl.includes('ot') || dl.includes('scada') || dl.includes('iot') || dl.includes('workplace') || dl.includes('hardware');
      });
      if (!isCld) return false;
    }
    if (activeCategory === 'ai_cyber') {
      const isAI = (job.all_domains || []).some(d => {
        const dl = d.toLowerCase();
        return dl.includes('ia') || dl.includes('ai') || dl.includes('llm') || dl.includes('data');
      });
      if (!isAI) return false;
    }

    // Location filter
    const loc = (job.location || '').toLowerCase();
    if (selectedLocation === 'paris' && !loc.includes('paris') && !loc.includes('nanterre') && !loc.includes('courbevoie') && !loc.includes('puteaux') && !loc.includes('levallois')) return false;
    if (selectedLocation === 'rennes' && !loc.includes('rennes') && !loc.includes('cesson') && !loc.includes('bretagne')) return false;
    if (selectedLocation === 'nantes' && !loc.includes('nantes') && !loc.includes('herblain')) return false;
    if (selectedLocation === 'toulouse' && !loc.includes('toulouse') && !loc.includes('colomiers')) return false;
    if (selectedLocation === 'lyon_grenoble' && !loc.includes('lyon') && !loc.includes('villeurbanne')) return false;
    if (selectedLocation === 'remote' && !loc.includes('télétravail') && !loc.includes('remote') && !loc.includes('partiel')) return false;

    // Text Search query
    if (query) {
      const searchTarget = [
        job.title,
        job.company_name,
        job.location,
        job.domain,
        job.description || '',
        (job.all_domains || []).join(' ')
      ].join(' ').toLowerCase();

      // Support multi-word queries
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
  resultsCount.innerHTML = `Affichage de <strong>${filtered.length}</strong> offre(s) de stage vérifiée(s)`;

  if (filtered.length === 0) {
    container.innerHTML = '';
    emptyState.classList.remove('hidden');
    return;
  }

  emptyState.classList.add('hidden');
  container.innerHTML = filtered.map(job => createJobCardHtml(job)).join('');

  // Attach event handlers to buttons inside cards
  attachCardEvents();
}

function createJobCardHtml(job) {
  const isApplied = appliedJobs.has(job.id);
  const isCrypto = job.is_crypto;
  
  // Badge styling
  let badgeBg = 'bg-slate-100 text-slate-700 border-slate-200';
  if (isCrypto) {
    badgeBg = 'bg-indigo-50 text-indigo-700 border-indigo-200';
  } else if ((job.domain || '').includes('Offensive')) {
    badgeBg = 'bg-rose-50 text-rose-700 border-rose-200';
  } else if ((job.domain || '').includes('Defensive') || (job.domain || '').includes('SOC')) {
    badgeBg = 'bg-sky-50 text-sky-700 border-sky-200';
  } else if ((job.domain || '').includes('Cloud') || (job.domain || '').includes('GRC')) {
    badgeBg = 'bg-purple-50 text-purple-700 border-purple-200';
  }

  return `
    <article class="job-card bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm hover:shadow-md transition ${isApplied ? 'opacity-70 bg-slate-50/70' : ''}">
      <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        
        <div class="space-y-1.5 flex-1">
          <!-- Badges Bar -->
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
              🎓 Stage M2 / PFE (6 mois)
            </span>
            <span class="text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${badgeBg}">
              ${escapeHtml(job.domain || 'Cybersécurité')}
            </span>
            <span class="text-[11px] text-emerald-600 font-medium flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"></span>
              Vérifié actif
            </span>
          </div>

          <!-- Job Title & Company -->
          <h2 class="text-base sm:text-lg font-bold text-slate-900 hover:text-indigo-600 transition">
            <a href="${job.direct_url}" target="_blank" rel="noopener noreferrer" class="focus:outline-none">
              ${escapeHtml(job.title)}
            </a>
          </h2>

          <div class="flex flex-wrap items-center gap-y-1 gap-x-3 text-xs text-slate-600">
            <span class="font-semibold text-slate-900">🏢 ${escapeHtml(job.company_name)}</span>
            <span>📍 ${escapeHtml(job.location || 'France')}</span>
            <span class="text-slate-500">Source: ${escapeHtml(job.source || 'Site Officiel')}</span>
          </div>

          <!-- Description Excerpt -->
          ${job.description ? `
            <p class="text-xs text-slate-600 pt-1.5 line-clamp-2 leading-relaxed">
              ${escapeHtml(job.description)}
            </p>
          ` : ''}
        </div>

        <!-- Action Column -->
        <div class="flex flex-col sm:items-end gap-2 shrink-0 pt-2 sm:pt-0">
          <a 
            href="${job.direct_url}" 
            target="_blank" 
            rel="noopener noreferrer"
            class="inline-flex items-center justify-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-lg bg-slate-900 text-white hover:bg-indigo-600 shadow-sm transition"
          >
            <span>Postuler sur le site officiel</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
            </svg>
          </a>

          <div class="flex items-center gap-3 text-xs pt-1">
            <button class="copy-link-btn text-slate-500 hover:text-slate-800 transition" data-url="${job.direct_url}">
              📋 Copier lien
            </button>
            <label class="inline-flex items-center gap-1 text-slate-600 cursor-pointer select-none">
              <input type="checkbox" class="toggle-applied rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5 border-slate-300" data-id="${job.id}" ${isApplied ? 'checked' : ''}>
              <span>${isApplied ? 'Postulé ✓' : 'Postulé ?'}</span>
            </label>
          </div>
        </div>

      </div>
    </article>
  `;
}

function attachCardEvents() {
  // Copy Link button
  document.querySelectorAll('.copy-link-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const url = btn.getAttribute('data-url');
      navigator.clipboard.writeText(url).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Lien copié ! ✓';
        btn.classList.add('text-emerald-600');
        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('text-emerald-600');
        }, 1800);
      });
    });
  });

  // Toggle Applied status
  document.querySelectorAll('.toggle-applied').forEach(chk => {
    chk.addEventListener('change', (e) => {
      const id = chk.getAttribute('data-id');
      if (chk.checked) {
        appliedJobs.add(id);
      } else {
        appliedJobs.delete(id);
      }
      localStorage.setItem('applied_jobs', JSON.stringify(Array.from(appliedJobs)));
      renderJobs();
    });
  });
}

function exportToCsv() {
  const filtered = getFilteredJobs();
  if (filtered.length === 0) {
    alert('Aucune offre à exporter.');
    return;
  }

  const headers = ['Entreprise', 'Intitulé du Poste', 'Domaine', 'Localisation', 'Lien Direct Officiel', 'Statut'];
  const rows = filtered.map(j => [
    `"${(j.company_name || '').replace(/"/g, '""')}"`,
    `"${(j.title || '').replace(/"/g, '""')}"`,
    `"${(j.domain || '').replace(/"/g, '""')}"`,
    `"${(j.location || '').replace(/"/g, '""')}"`,
    `"${(j.direct_url || '').replace(/"/g, '""')}"`,
    `"${appliedJobs.has(j.id) ? 'Postulé' : 'À postuler'}"`
  ]);

  const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `stages_cyber_crypto_m2_france_${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
