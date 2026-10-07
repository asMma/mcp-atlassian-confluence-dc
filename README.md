# mcp-atlassian (Confluence/Jira Data Center — build interne)

Copie interne, auditée et corrigée, du serveur MCP [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) (licence MIT, voir `LICENSE`), figée sur le tag **v0.23.1**, pour connecter **GitHub Copilot dans VS Code** à notre **Confluence et Jira Data Center** (authentification par Personal Access Token, sans Docker).

Seuls les fichiers nécessaires à l'exécution ont été conservés (`src/`, `pyproject.toml`, `uv.lock`, `.env.example`, `LICENSE`). Pas de tests, docs, CI ni Dockerfile du projet amont.

## Ce qui a été vérifié et corrigé (2026-10-07)

- **Revue de code** : la faille SSRF historique du projet (CVE-2026-27826, corrigée en amont depuis la v0.17.0) est bien présente et même renforcée dans ce tag par une protection anti-DNS-rebinding (`src/mcp_atlassian/utils/ssrf_adapter.py`).
- **Bandit** (analyse statique) : 0 issue High, aucun secret en dur.
- **pip-audit** sur l'environnement réellement installé (121 paquets hors outils de dev) : 12 dépendances transitives avec des avis Medium (aucun Critical/High) — **corrigées** dans ce repo via un `uv.lock` mis à jour (`urllib3`, `idna`, `pyjwt`, `oauthlib`, `cryptography`, `pydantic-settings`, `soupsieve`, `pymdown-extensions`, `click`, `anyio`, `python-dotenv`, `pygments`). `pip-audit` ne remonte plus rien après coup.
- Le code de `mcp-atlassian` lui-même n'a pas été modifié : seules les dépendances tierces ont été relevées vers des versions corrigées.
- `version` a été fixée en dur à `0.23.1` dans `pyproject.toml` (le versionnage dynamique basé sur git de l'amont ne s'applique pas à cette copie sans son historique).

## Installer

Prérequis : [`uv`](https://docs.astral.sh/uv/) (aucun Docker nécessaire).

```bash
git clone <url-de-ce-repo>
cd mcp-atlassian
uv sync --frozen --no-group dev
```

## Configurer VS Code / GitHub Copilot

Éditer `.vscode/mcp.json` (fourni dans ce repo) : remplacer `/chemin/vers/mcp-atlassian` par le chemin réel de ce clone sur votre machine, et renseigner l'URL de votre instance Confluence/Jira Data Center.

Dans VS Code : Copilot Chat → mode Agent → icône outils (🔧) → vérifier que `confluence-dc` apparaît → saisir votre Personal Access Token Confluence au premier lancement (généré depuis votre profil Confluence Data Center, menu *Personal Access Tokens*).

Pour Jira, dupliquer le même principe dans `mcp.json` avec `JIRA_URL` / `JIRA_PERSONAL_TOKEN` (voir `.env.example` pour la liste complète des variables supportées).

## Mettre à jour / re-auditer

Pour passer à un tag plus récent du projet amont, repartir du process complet (clone amont → revue de code → `uv lock --upgrade-package ...` si de nouvelles CVE sont publiées sur les dépendances → `uv sync --frozen --no-group dev` → tests). Ne jamais pointer sur la branche `main` de l'amont : toujours un tag de release précis.

## Licence

Ce projet reste sous licence MIT (`LICENSE`), identique à l'amont [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian).
