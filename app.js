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
      <div class="p-4 bg-rose-950/30 border border-rose-900/60 rounded text-rose-300 text-xs font-mono">
        <p class="font-semibold">Erreur de chargement</p>
        <p class="text-[11px] mt-1 text-rose-400">Impossible de lire data/jobs.json.</p>
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
  
  // Minimal Badge styling
  let badgeBg = 'bg-zinc-800/80 text-zinc-300 border-zinc-700/60';
  if (isCrypto) {
    badgeBg = 'bg-indigo-950/60 text-indigo-300 border-indigo-800/80';
  } else if ((job.domain || '').includes('Offensive')) {
    badgeBg = 'bg-rose-950/60 text-rose-300 border-rose-800/80';
  } else if ((job.domain || '').includes('Defensive') || (job.domain || '').includes('SOC')) {
    badgeBg = 'bg-sky-950/60 text-sky-300 border-sky-800/80';
  } else if ((job.domain || '').includes('Cloud')) {
    badgeBg = 'bg-purple-950/60 text-purple-300 border-purple-800/80';
  }

  return `
    <article class="job-card bg-zinc-900/40 rounded-lg border border-zinc-800/80 p-4 sm:p-5 hover:border-zinc-700 transition ${isApplied ? 'opacity-60 bg-zinc-950/40' : ''}">
      <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        
        <div class="space-y-2 flex-1">
          <!-- Badges Bar -->
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800/90 text-zinc-300 border border-zinc-700/60">
              PFE (6 mois)
            </span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${badgeBg}">
              ${escapeHtml(job.domain || 'Cybersécurité')}
            </span>
            <span class="text-[10px] font-mono text-emerald-400 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
              Vérifié live
            </span>
          </div>

          <!-- Job Title & Company -->
          <h2 class="text-sm sm:text-base font-semibold text-zinc-100 hover:text-indigo-400 transition tracking-tight">
            <a href="${job.direct_url}" target="_blank" rel="noopener noreferrer" class="focus:outline-none">
              ${escapeHtml(job.title)}
            </a>
          </h2>

          <div class="flex flex-wrap items-center gap-y-1 gap-x-4 text-xs font-mono text-zinc-400">
            <span class="font-medium text-zinc-200">${escapeHtml(job.company_name)}</span>
            <span>${escapeHtml(job.location || 'France')}</span>
            <span class="text-zinc-500">Source: ${escapeHtml(job.source || 'Officiel')}</span>
          </div>

          <!-- Description Excerpt -->
          ${job.description ? `
            <p class="text-xs text-zinc-400 pt-1 line-clamp-2 leading-relaxed font-sans">
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
            class="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 text-xs font-mono font-medium rounded bg-zinc-100 text-zinc-950 hover:bg-white transition shadow-sm"
          >
            <span>Postuler</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </a>

          <div class="flex items-center gap-3 text-xs pt-1">
            <button class="copy-link-btn text-[11px] font-mono text-zinc-500 hover:text-zinc-300 transition" data-url="${job.direct_url}">
              Copier lien
            </button>
            <label class="inline-flex items-center gap-1.5 text-[11px] font-mono text-zinc-400 cursor-pointer select-none">
              <input type="checkbox" class="toggle-applied rounded bg-zinc-900 border-zinc-700 text-indigo-500 focus:ring-0 w-3.5 h-3.5" data-id="${job.id}" ${isApplied ? 'checked' : ''}>
              <span>${isApplied ? 'Postulé' : 'À postuler'}</span>
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
        btn.textContent = 'Copié';
        btn.classList.add('text-emerald-400');
        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('text-emerald-400');
        }, 1500);
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
