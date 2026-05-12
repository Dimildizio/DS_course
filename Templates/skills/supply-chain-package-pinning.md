---
name: supply-chain package pinning policy
description: Никогда не ставим latest версию пакета (supply-chain risk, минимум 1-3 месяца возраста). Всегда фиксируем версии в pyproject.toml и requirements.txt — никаких open-ended deps.
type: feedback
originSessionId: 
---

## Правило

**Минимальный возраст релиза = 1-3 месяца** перед добавлением в `pyproject.toml`. Идеально — предпредпоследняя стабильная версия.

## Почему

Типовые supply-chain инциденты:
- event-stream (2018) — malicious code в npm-пакете под прикрытием maintenance transfer
- ua-parser-js (2021) — three-day window от компрометации до обнаружения
- colors.js / faker.js (2022) — author-sabotage
- 3CX (2023) — supply chain через dependency
- xz-utils (2024) — двухлетняя социальная инженерия

### 2026 incidents — особенно показательны

- **axios (npm) — 30–31 марта 2026**: maintainer-аккаунт `jasonsaayman` скомпрометирован, email переведён на атакера (`ifstap@proton.me`); опубликованы `axios@1.14.1` (latest) и `axios@0.30.4` (legacy) с phantom dep `plain-crypto-js@4.2.1` → obfuscated dropper → **WAVESHAPER.V2 RAT** (Windows/macOS/Linux). 100M+ weekly downloads. Атрибуция: UNC1069 (North Korea-nexus). Версии сняли через ~3 часа — окна хватило для массового заражения. Подтверждает правило «60 дней минимум»: если бы пользователи не брали `latest` сразу, ущерб был бы 0.
- **Bitwarden CLI impersonation (npm) — апрель 2026**: фальшивый пакет `@bitwarden/cli` v2026.4.0 (typosquat на легитимный Bitwarden), часть кампании **TeamPCP** — крадёт креды cloud-провайдеров, CI/CD-токены, файлы с dev-машин. Защита: всегда смотреть source/maintainer, а не имя.
- **Shai-Hulud campaigns (npm) — 22 и 29 апреля 2026**: «Shai-Hulud: The Third Coming» (22.04) + «Mini Shai-Hulud» (29.04) — серия скомпрометированных npm-пакетов. Одна из ветвей пришла через **SAP-related npm packages** (29.04, окно 09:55–12:14 UTC).
- **🚨 SAP npm + Claude Code hook abuse — 29 апреля 2026**: malicious payload собирает GitHub-токены, npm-токены, GitHub Actions secrets, cloud-секреты (AWS/Azure/GCP/Kubernetes) **и инжектит `.claude/settings.json` с `SessionStart` хуком в каждый доступный GitHub-репозиторий**. Это **первый известный supply-chain attack нацеленный на конфигурацию AI coding agent'а** как канал персистентности и propagation.
  1. После любого `npm install` — `git status` смотрит на изменения в `.claude/`.
  2. Pre-commit hook должен валидировать `.claude/settings.json` — никаких внезапных `SessionStart` хуков.
  3. Не доверяем коммитам в `.claude/` которые мы лично не сделали — даже если pre-commit пропустил.
- **DevTap typosquat-кампания (npm) — 1 апреля – 3 мая 2026**: один publisher выкатил 6 пакетов с «инфраструктурными» именами, специально похожими на привычные dev-deps: `centralogger`, `dom-utils-lite`, `node-fetch-lite`, `connector-agent`, `node-gyp-runtime`, `node-env-resolve`. `node-env-resolve@{1.0.7, 1.0.8}` помечены malicious 2 мая, подтверждено 3 мая. Payload (Windows): HKCU Run-key persistence через `wscript.exe` + VBS-stub → detached Node-agent с mic capture, browser-history theft, screenshot, keyboard/mouse simulation. **Урок**: имя пакета само по себе не доказывает легитимность; ищем maintainer + историю + downloads.
- **🚨 TanStack npm — 11 мая 2026, 19:20–19:26 UTC**: атакующий выложил **84 malicious версии в 42 `@tanstack/*` пакетах** (включая `@tanstack/react-router` с 12M+ weekly downloads) за 6 минут. Tradecraft: `pull_request_target` «Pwn Request» pattern + GitHub Actions cache poisoning через fork↔base trust boundary + runtime extraction OIDC-токена из GitHub Actions runner. Обнаружено внешним researcher'ом (Ashish Kurmi, StepSecurity) за ~20 минут; npm security удаляет tarball'ы. Severity HIGH. Payload крадёт: AWS, GCP, Kubernetes, HashiCorp Vault credentials, GitHub tokens, SSH keys, содержимое `.npmrc`. **Recommended action для всех затронутых**: ротировать все ↑ креды на install host.
- **🚨 Mini Shai-Hulud npm worm — 12 мая 2026**: SlowMist issued Critical alert о **self-propagating worm**, скомпрометировано **169+ JavaScript-пакетов** — включая TanStack, UiPath, **Mistral AI**, DraftLab. Цели: crypto wallets, cloud credentials, CI/CD secrets. Принципиальное отличие: **не typosquat**, worm hijack'ает легитимный build pipeline и распространяется через зависимости. Любой `npm install` 12 мая — потенциальный risk. AI/ML экосистема явно зацеплена (Mistral AI пакет).

**Pattern**: в 2026 атаки массово ушли от ad-hoc obfuscated payload'ов к **умному targeting инфраструктуры разработчика** — CI/CD-секреты, AI-agent-конфиги, IDE-hooks, OIDC-токены, GitHub Actions cache. Latest-installation остаётся главным attack vector. **Self-propagating worms** (Mini Shai-Hulud) поднимают ставки: одна compromised dep → каскад через граф зависимостей.

**Дополнительные защитные практики (выведено из 2026-кейсов)**:
- `npm ci` / `pip install -r requirements.lock` вместо `npm install` / `pip install` — никакого resolution на install-стороне.
- Если в проекте есть GitHub Actions: не использовать `pull_request_target` без чёткого whitelist'а; не доверять PR-source code на base-branch trust level; кэш Actions должен быть scoped to ref, не share между fork и base.
- Любой workflow читает секреты — secrets идут только в reviewed-PRs, не в forked PRs.
- В наш `.gitignore` / CI: после любого install-step — `git diff --exit-code .claude/ .github/ pyproject.toml uv.lock` чтоб поймать инжект.

Latest = окно когда коммьюнити ещё не успело отреветь malware / backdoor.

## Что делать при `uv add` или bump зависимости

1. **Стоп до выполнения**. Проверить:
   ```bash
   uv pip index versions <package>           # список доступных версий
   pip show <package> | grep Released-Date   # дата релиза
   ```
2. Целевая версия — **минимум 60 дней** в публичном доступе, идеально 90+.
3. Перед добавлением — посмотреть CHANGELOG / release notes на предмет sus коммитов maintainer'а; быстрый взгляд на GitHub Issues (есть ли «something weird in v X.Y.Z»).
4. **Pin обязательно** — никаких open-ended `package`, `package>=X` без верхней границы, `package*`.
5. `uv.lock` **всегда коммитим** (это даёт reproducibility и protection от silent upgrade'а).
6. После добавления — `uv pip audit` (или `pip-audit`) на предмет известных CVE.
7. **Никогда `uv lock --upgrade-all` без явной причины** — это автообновит всё до latest, включая свежак.

## Форматы pin'а

### `pyproject.toml` (PEP 621 / `[project.dependencies]`)

Диапазон с обеими границами: нижняя — конкретная проверенная версия, верхняя — следующий major (или next-next minor для conservative).

```toml
[project]
dependencies = [
    "fastapi>=0.115.6,<0.116",       # минор-pin: один minor шаг вверх
    "pydantic>=2.10.4,<3",           # major-pin: до следующего major
    "lightgbm>=4.5.0,<4.7",          # narrow: 1-2 minor вверх
    "mlflow>=2.18.0,<3",
]
```

Запрещено:
- `"fastapi"` (open-ended, latest при resolve)
- `"fastapi>=0.115.6"` (без верхней границы)
- `"fastapi==*"` или `"fastapi~=0.115"` без явного pin'а
- `"fastapi @ git+https://..."` без commit SHA

### `requirements.txt` (если придётся писать)

Полная фиксация **точной версии + hash** (PEP 665 / pip-compile стиль):

```
fastapi==0.115.6 \
    --hash=sha256:9abf9a1...
```

Минимум — `package==X.Y.Z` (точно), без диапазонов. `requirements.txt` — это уже артефакт после resolve, не должен оставлять воли solver'у.

Запрещено в requirements.txt:
- `fastapi>=0.115` (диапазон — это для pyproject)
- `fastapi` (open-ended)
- комментарий-only без версии

### Lock-файлы

Любой lock (`uv.lock`, `poetry.lock`, `pip-compile.txt`, `requirements.lock`) — **всегда коммитим** и не редактируем руками. `uv sync --frozen` / `pip install -r requirements.lock` — единственный production install path.

## Исключения (когда можно ставить новое)

- Security advisory с CVE в текущей версии — патч ставить надо, но **проверить что патч пришёл с того же maintainer'а** что и предыдущие релизы (signed commits, два-факторная аутентификация).
- Pre-release / beta — никогда в production deps; только в dev-deps если есть конкретная нужда.

## Что записать в pyproject.toml на старте

Когда впервые добавим фреймворк или библиотеку:

- Проверить latest на PyPI → отступить минимум на ОДНУ minor version → pin диапазон.
- На каждый из этих пакетов делать заметку в DEVLOG: какая версия зафиксирована и почему.

**How to apply:** при любом упоминании добавить/обновить зависимость — **остановиться, проверить возраст**, обсудить с пользователем если возраст < 60 дней. Никогда не молча тянуть `@latest`. Любой написанный руками `pyproject.toml`/`requirements.txt` обязан проходить чеклист:
1. У каждой строки есть точная версия (requirements) или диапазон с обеими границами (pyproject).
2. Возраст нижней границы ≥ 60 дней (идеально 90+).
3. Нет `@latest`, `*`, открытых `>=X`.
4. Lock-файл закоммичен в той же ревизии.
