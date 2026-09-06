# 🛡️ France Cyber & Cryptology M2 Internship Tracker & Auto-Notifier

Application web légère hébergée sur **GitHub Pages**, dotée d'un **scénario de scraping et de validation automatisé via GitHub Actions**, conçue spécialement pour les étudiants en **Master 2 / PFE** en **Cybersécurité** et **Cryptologie** partout en France.

---

## 🌟 Points Forts du Projet

1. **Liens 100% Directs sur les Sites Officiels des Entreprises (Zéro Agrégateur)** :
   - Aucun lien mort vers Indeed, Jooble ou autres fermes de clics.
   - Les liens pointent **exclusivement** vers les plateformes carrières officielles des employeurs : portails Workday officiels (Thales, Airbus), sites carrières (SERMA, eShard, Secure-IC, Synacktiv, Quarkslab, Inria), ou portails ATS directs d'entreprises (Lever, Greenhouse, SmartRecruiters, WTTJ).
2. **Filtrage Silencieux des Restrictions Défense & Habilitations Exclusives** :
   - Exclusion automatique en arrière-plan des offres imposant une *nationalité française obligatoire* ou une habilitation secret défense exclusive (DGSE/DGSI/unités militaires).
   - Ciblage prioritaire des grands éditeurs logiciels, cabinets de conseil, banques et laboratoires civils (SERMA, eShard, Secure-IC, Ledger, Zama, Sekoia, TEHTRIS, Gatewatcher, Wavestone, Advens, BNP, Société Générale) qui recrutent massivement les étudiants internationaux en M2 en France.
3. **Vérification Continue de la Disponibilité des Offres** :
   - Le validateur HTTP vérifie avant chaque mise à jour si les pages d'offres sont toujours actives et écarte automatiquement les annonces closes ou expirées.
4. **Alertes Email Automatiques par GitHub Actions** :
   - Dès qu'une nouvelle offre de stage M2 active est détectée, un email récapitulatif formaté en HTML vous est envoyé avec les liens directs pour postuler immédiatement.
5. **Interface Web Épurée & Suivi des Candidatures** :
   - Recherche instantanée par mot-clé, filtre par spécialité (Cryptologie, Pentest/Offensif, SOC/DFIR, DevSecOps/Cloud), filtre géographique, case à cocher « Postulé » enregistrée dans le navigateur, et export CSV.

---

## 🏢 Entreprises Couvertes (Répertoire de plus de 70 Organisations)

- **Sécurité Matérielle, CESTI & Cryptologie Embarquée** :
  SERMA Safety & Security / SERMA NES, eShard, Secure-IC, NinjaLab, Oppida, STMicroelectronics France, NXP France, Idemia.
- **R&D Cryptologie & Boutiques d'Excellence** :
  CryptoExperts, Quarkslab, Zama (FHE), Cosmian, Ledger (Donjon), Inria (COSMIQ, CASCADE, PRIVATICS), CEA-List/Leti, Moabi.
- **Éditeurs Pure-Players Cybersécurité** :
  Synacktiv, Stormshield, Sekoia.io, Gatewatcher, TEHTRIS, HarfangLab, GitGuardian, YesWeHack, Yogosha, Patrowl, WALLIX, ChapsVision, Amossys, Lexfo, XMCO, Intrinsec, I-Tracing.
- **Grands Groupes Industriels & Aéronautique** :
  Thales (Thales Cyber Solutions, Thales DIS, SIX GTS), Airbus CyberSecurity, Safran, Naval Group, Dassault Systèmes, Schneider Electric, Alstom.
- **Cabinets de Conseil & Grands MSSP** :
  Orange Cyberdefense, Advens, Wavestone, Capgemini / Sogeti Cyber, Sopra Steria, Eviden (Atos BDS), Devoteam, Accenture Security, Big 4 (Deloitte, PwC, EY, KPMG).
- **Opérateurs d'Importance Vitale (OIV) & Banques** :
  BNP Paribas (CERT-BNP), Société Générale (CERT-SG), Crédit Agricole, BPCE, EDF (CERT-EDF), TotalEnergies, SNCF, Docaposte.

---

## 🚀 Déploiement Rapide sur GitHub (en 5 minutes)

### 1. Pousser le projet sur votre compte GitHub

Ouvrez un terminal dans ce dossier et exécutez :

```bash
git init
git add .
git commit -m "Initial commit: France Cyber & Crypto Internship Tracker"
git branch -M main
git remote add origin https://github.com/<VOTRE_PSEUDO_GITHUB>/france-cyber-crypto-internships.git
git push -u origin main
```

### 2. Activer GitHub Pages (Hébergement Gratuit)

1. Rendez-vous sur votre dépôt GitHub.
2. Allez dans l'onglet **Settings** > **Pages** (dans le menu de gauche).
3. Dans **Build and deployment** > **Source**, sélectionnez **Deploy from a branch**.
4. Choisissez la branche `main` et le dossier `/ (root)`, puis cliquez sur **Save**.
5. Votre site sera accessible en ligne en moins de 2 minutes à l'adresse :
   `https://<VOTRE_PSEUDO_GITHUB>.github.io/france-cyber-crypto-internships/`

### 3. Autoriser GitHub Actions à mettre à jour les données

Pour que le bot puisse sauvegarder les nouvelles offres dans `data/jobs.json` :
1. Allez dans **Settings** > **Actions** > **General**.
2. Descendez jusqu'à la section **Workflow permissions**.
3. Cochez **Read and write permissions**.
4. Cliquez sur **Save**.

### 4. Configurer les Alertes Email Automatiques (GitHub Secrets)

Pour recevoir les alertes dès qu'un nouveau stage apparaît :
1. Allez dans **Settings** > **Secrets and variables** > **Actions**.
2. Cliquez sur **New repository secret** et ajoutez les variables suivantes :

| Nom du Secret | Description | Exemple |
| :--- | :--- | :--- |
| `EMAIL_HOST` | Serveur SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Port SMTP (TLS) | `587` |
| `EMAIL_USER` | Votre adresse email d'envoi | `votre.email@gmail.com` |
| `EMAIL_PASSWORD` | Mot de passe d'application | `abcd efgh ijkl mnop` *(voir note ci-dessous)* |
| `NOTIFY_EMAIL_TO` | Votre adresse email de réception | `votre.email@gmail.com` |

> [!TIP]
> **Si vous utilisez Gmail** : Utilisez un **Mot de passe d'application** (App Password).
> Activez la validation en 2 étapes sur votre compte Google, puis générez un mot de passe d'application sur [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

---

## 💻 Exécution Locale (Optionnelle)

Si vous souhaitez exécuter le scraper ou tester l'interface sur votre machine :

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer une recherche et validation manuelle
python -m scraper.main --dry-run

# 3. Lancer le scraper automatique en boucle locale (toutes les 1 heure)
python scripts/run_hourly.py

# 4. Lancer le serveur web localement
python -m http.server 8000
```
Ouvrez ensuite [http://localhost:8000](http://localhost:8000) dans votre navigateur.

---

## ⚙️ Structure du Projet

```text
├── .github/
│   └── workflows/
│       └── scrape_and_notify.yml   # Workflow Cron (toutes les 1h) et envoi d'emails
├── scripts/
│   └── run_hourly.py               # Démon de scraping local toutes les 1h
├── data/
│   ├── jobs.json                   # Base active des offres vérifiées en direct
│   └── seen_jobs.json              # Historique des offres notifiées (anti-doublons)
├── scraper/
│   ├── companies.py                # Répertoire de 70+ entreprises cibles en France
│   ├── filters.py                  # Filtrage M2, taxonomie Cyber/Crypto, éligibilité nationalité
│   ├── ats_scrapers.py             # Scrapers officiels (Workday, SmartRecruiters, Lever, Greenhouse, etc.)
│   ├── validator.py                # Vérification liveness HTTP et détection offres closes
│   ├── notifier.py                 # Moteur d'alerte email SMTP HTML
│   └── main.py                     # Script d'orchestration global
├── index.html                      # Interface web minimaliste et responsive
├── app.js                          # Moteur client (recherche, filtres, suivi candidatures, CSV)
├── style.css                       # Styles visuels et animations
├── requirements.txt                # Dépendances Python (requests, beautifulsoup4, python-dotenv)
└── README.md                       # Guide de documentation complet
```
