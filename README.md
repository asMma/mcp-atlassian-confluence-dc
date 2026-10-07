# Assistant Confluence & Jira pour GitHub Copilot

Ce projet connecte **GitHub Copilot** (dans VS Code) à **Confluence** et **Jira** de l'entreprise. Une fois installé, vous pouvez demander à Copilot en français, dans le chat, de créer ou modifier des pages Confluence et de créer des tickets Jira — sans jamais ouvrir Confluence ou Jira vous-même.

> Aucune connaissance en programmation n'est nécessaire pour l'utiliser au quotidien. L'installation (une seule fois) demande de suivre quelques étapes précises ci-dessous — si vous bloquez, demandez à votre équipe IT de les faire avec vous.

---

## 1. Installation (à faire une seule fois)

### Étape 1 — Installer les outils de base

1. Installez **VS Code** : https://code.visualstudio.com/
2. Ouvrez VS Code, allez dans l'onglet **Extensions** (icône de blocs sur la barre de gauche) et installez **GitHub Copilot** et **GitHub Copilot Chat**.
3. Installez `uv` (l'outil qui fait tourner ce projet, pas besoin de Docker ni Python préinstallé) :
   - **Mac/Linux** : ouvrez le Terminal et collez :
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - **Windows** : ouvrez PowerShell et collez :
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

### Étape 2 — Récupérer ce projet

Dans un Terminal, placez-vous dans un dossier de votre choix puis :

```bash
git clone https://github.com/asMma/mcp-atlassian-confluence-dc.git
cd mcp-atlassian-confluence-dc
uv sync --frozen --no-group dev
```

### Étape 3 — Obtenir vos jetons d'accès (Personal Access Token)

Un jeton d'accès remplace votre mot de passe pour que Copilot puisse se connecter à votre place, sans jamais connaître votre mot de passe réel.

**Pour Confluence :**
1. Connectez-vous à Confluence dans votre navigateur.
2. Cliquez sur votre photo de profil (en haut à droite) → **Paramètres du profil** (ou *Profile*).
3. Dans le menu de gauche, cliquez sur **Jetons d'accès personnels** (*Personal Access Tokens*).
4. Cliquez sur **Créer un jeton** (*Create token*), donnez-lui un nom (ex: "copilot"), puis copiez le jeton généré — vous ne pourrez plus le revoir après.

**Pour Jira :** même procédure, depuis votre profil Jira.

Gardez ces deux jetons de côté temporairement, vous en aurez besoin à l'étape suivante.

### Étape 4 — Configurer VS Code

1. Dans VS Code, ouvrez le dossier du projet cloné (**Fichier → Ouvrir le dossier...**).
2. Ouvrez le fichier `.vscode/mcp.json`.
3. Remplacez `/chemin/vers/mcp-atlassian` (aux deux endroits) par le chemin réel du dossier sur votre machine.
4. Remplacez `https://confluence.tonentreprise.com` et `https://jira.tonentreprise.com` par les vraies adresses de votre Confluence et Jira.
5. Enregistrez le fichier.

### Étape 5 — Se connecter

1. Ouvrez l'onglet **Copilot Chat** dans VS Code et passez en mode **Agent** (menu déroulant en haut du chat).
2. Cliquez sur l'icône outils (🔧) et vérifiez que `confluence-dc` et `jira-dc` apparaissent dans la liste.
3. La première fois que vous posez une question touchant Confluence ou Jira, VS Code vous demandera successivement :
   - de coller le jeton correspondant (celui de l'étape 3) ;
   - les **clés des espaces Confluence** (puis des **projets Jira**) que l'assistant a le droit d'utiliser, séparées par des virgules (ex: `DEV,TEAM`). **Vous pouvez laisser ce champ vide** pour ne poser aucune restriction, mais le renseigner est fortement recommandé : c'est ce qui empêche l'assistant de créer ou modifier quoi que ce soit en dehors des espaces/projets que vous avez listés, même en cas d'erreur de sa part (voir section 3 ci-dessous).

C'est prêt ! Passez à la section suivante pour l'utiliser.

> Pour changer cette liste plus tard, rouvrez la palette de commandes VS Code (**Cmd/Ctrl+Shift+P**) → *MCP: Reset Cached Inputs*, puis reposez une question à Copilot : il vous redemandera les valeurs.

---

## 2. Comment l'utiliser

Ouvrez le chat Copilot en **mode Agent**, et écrivez simplement ce que vous voulez en français. Voici des exemples que vous pouvez copier-coller et adapter.

### Créer une page Confluence

```
Crée une page Confluence dans l'espace "DEV" intitulée "Compte-rendu réunion du 15 mars".
Contenu : liste des présents (Alice, Bob, Claire), puis un résumé des décisions prises :
- Validation du nouveau design
- Report du déploiement à la semaine prochaine
```

```
Crée une page Confluence dans l'espace "RH" appelée "Procédure d'onboarding", comme
sous-page de la page "Ressources Humaines". Mets une checklist avec : créer le compte,
remettre le badge, planifier la formation.
```

### Mettre à jour une page Confluence existante

```
Trouve la page Confluence "Compte-rendu réunion du 15 mars" dans l'espace DEV
et ajoute une section "Actions à faire" avec : relancer le fournisseur, préparer la démo.
```

```
Ajoute un commentaire sur la page Confluence "Procédure d'onboarding" disant que
le document a été relu et validé.
```

### Créer un ticket Jira

```
Crée un ticket Jira dans le projet "SUPPORT" de type "Bug", avec le titre
"Le bouton d'export ne fonctionne plus" et la description : "Depuis la mise à jour
d'hier, cliquer sur Exporter ne fait rien. Testé sur Chrome et Firefox."
```

```
Crée un ticket Jira dans le projet "PROD" de type "Tâche" intitulé "Préparer la
présentation client", assigné à moi, avec une échéance à vendredi.
```

### Autres choses utiles à savoir demander

- *"Montre-moi les tickets Jira ouverts qui me sont assignés dans le projet SUPPORT"*
- *"Change le statut du ticket SUPPORT-42 en 'En cours'"*
- *"Ajoute un commentaire sur le ticket SUPPORT-42 pour dire que c'est en cours de traitement"*
- *"Cherche dans Confluence toutes les pages qui parlent de 'processus de recrutement'"*
- *"Résume-moi le contenu de la page Confluence 'Roadmap Q2'"*

> Astuce : Copilot vous montrera souvent ce qu'il va faire avant de l'exécuter réellement (surtout pour créer/modifier). Relisez et confirmez — c'est le seul moment où vous pouvez vérifier l'espace/le projet visé *avant* la création.

---

## 3. Se protéger des erreurs d'espace ou de projet

Ce MCP ne permet que de **créer et mettre à jour** du contenu — il n'y a pas de bouton "supprimer" un ticket, une page ou une pièce jointe, ce risque n'existe donc pas.

Le risque qui reste : que Copilot (ou vous) crée une page/un ticket dans le mauvais espace/projet, parmi tous ceux auxquels votre jeton a accès. Si vous avez renseigné les champs **"espaces Confluence autorisés"** et **"projets Jira autorisés"** à l'étape 5, c'est déjà réglé : toute tentative de création ou modification en dehors de cette liste est automatiquement rejetée, quoi que demande la conversation.

Si vous avez laissé ces champs vides et voulez les activer maintenant : rouvrez la palette de commandes de VS Code (**Cmd/Ctrl+Shift+P**) → *MCP: Reset Cached Inputs*, puis reposez une question à Copilot — il vous les redemandera.

---

## 4. En cas de problème

| Problème | Solution |
|---|---|
| `confluence-dc` ou `jira-dc` n'apparaît pas dans la liste d'outils | Vérifiez le chemin dans `.vscode/mcp.json` (étape 4) et relancez VS Code. |
| Copilot dit qu'il n'arrive pas à se connecter / erreur 401 | Votre jeton a peut-être expiré ou été mal collé — régénérez-en un (étape 3) et resaisissez-le. |
| "Je ne trouve pas Jetons d'accès personnels dans mon profil" | Cette option peut être désactivée par votre administrateur Confluence/Jira — contactez votre IT. |
| Copilot crée la page/le ticket dans le mauvais espace/projet | Précisez toujours la clé exacte de l'espace (ex: `DEV`) ou du projet (ex: `SUPPORT`) dans votre demande, et renseignez la liste des espaces/projets autorisés (section 3) pour bloquer toute tentative hors de cette liste. |
| Message d'erreur "is restricted by configuration" | Normal : l'espace/le projet demandé n'est pas dans votre liste d'espaces/projets autorisés (section 3). Si c'est une erreur, ajoutez-le à la liste via *MCP: Reset Cached Inputs*. |

---

## 5. Détails techniques (pour l'équipe IT)

Copie interne, auditée et corrigée, du serveur MCP [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) (licence MIT, voir `LICENSE`), figée sur le tag **v0.23.1**, pour connecter GitHub Copilot dans VS Code à notre Confluence et Jira Data Center (authentification par Personal Access Token, sans Docker).

Seuls les fichiers nécessaires à l'exécution ont été conservés (`src/`, `pyproject.toml`, `uv.lock`, `.env.example`, `LICENSE`). Pas de tests, docs, CI ni Dockerfile du projet amont.

### Audit et correctifs appliqués

- **Revue de code** : la faille SSRF historique du projet (CVE-2026-27826, corrigée en amont depuis la v0.17.0) est bien présente et même renforcée dans ce tag par une protection anti-DNS-rebinding (`src/mcp_atlassian/utils/ssrf_adapter.py`).
- **Bandit** (analyse statique) : 0 issue High, aucun secret en dur.
- **pip-audit** sur l'environnement réellement installé (121 paquets hors outils de dev) : 12 dépendances transitives avec des avis Medium (aucun Critical/High) — **corrigées** dans ce repo via un `uv.lock` mis à jour (`urllib3`, `idna`, `pyjwt`, `oauthlib`, `cryptography`, `pydantic-settings`, `soupsieve`, `pymdown-extensions`, `click`, `anyio`, `python-dotenv`, `pygments`). `pip-audit` ne remonte plus rien après coup.
- **Revue de sécurité complète du code applicatif** (audit manuel exhaustif, pas uniquement automatisé) : une faille de contournement des allowlists `JIRA_PROJECTS_FILTER`/`CONFLUENCE_SPACES_FILTER` a été trouvée et corrigée — ces filtres n'étaient appliqués que sur la recherche et `get_issue`, laissant ~70 autres outils (lecture et écriture) totalement non scopés dans un déploiement à identifiants partagés. Voir l'historique des commits pour le détail.
- Le code de `mcp-atlassian` lui-même n'a pas été modifié au-delà de ces correctifs : les dépendances tierces ont été relevées vers des versions corrigées, et deux failles d'allowlist applicative ont été comblées.
- `version` a été fixée en dur à `0.23.1` dans `pyproject.toml` (le versionnage dynamique basé sur git de l'amont ne s'applique pas à cette copie sans son historique).

### Configuration avancée

Voir `.env.example` pour la liste complète des variables supportées (OAuth, mTLS, proxy, filtrage par projet/espace `JIRA_PROJECTS_FILTER`/`CONFLUENCE_SPACES_FILTER`, mode lecture seule, etc.).

### Mettre à jour / re-auditer

Pour passer à un tag plus récent du projet amont, repartir du process complet (clone amont → revue de code → `uv lock --upgrade-package ...` si de nouvelles CVE sont publiées sur les dépendances → `uv sync --frozen --no-group dev` → tests). Ne jamais pointer sur la branche `main` de l'amont : toujours un tag de release précis.

### Licence

Ce projet reste sous licence MIT (`LICENSE`), identique à l'amont [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian).
