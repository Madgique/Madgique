# CLAUDE.md — Madgique (GitHub Profile)

## Structure du projet

- `README.md` — Profil GitHub avec badges de téléchargements CurseForge et Modrinth
- `.github/workflows/snake.yml` — Génération quotidienne de la snake animation
- `.github/workflows/update-downloads.yml` — Mise à jour hebdomadaire des compteurs de téléchargements
- `.github/scripts/update_downloads.py` — Script de fetch des downloads CurseForge + Modrinth

## Badges de téléchargements

Les badges dans la section "Minecraft Mods" du README sont mis à jour automatiquement chaque lundi via GitHub Actions.

### Fonctionnement
- **Modrinth** : API publique `https://api.modrinth.com/v2/user/Madgique/projects` — retourne tous les projets avec leurs downloads individuels, sommation côté script
- **CurseForge** : Scraping du profil `https://www.curseforge.com/members/madgique/projects` — extraction du total "XX Downloads"

Le script gère les échecs indépendamment : si une plateforme est indisponible, l'autre est tout de même mise à jour.

### Lancement manuel
Aller dans GitHub → Actions → "Update Download Counts" → "Run workflow"
