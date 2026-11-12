// World of Codecraft: French and English, picked automatically.
// The language is detected once per start from the system (WOCC_LANG if set, else macOS
// AppleLanguages, else LC_ALL / LC_MESSAGES / LANG): French when it starts with "fr", English
// otherwise. It is shared with every copy of the mod (shared "wocc.lang"), so the header, the board,
// the pane headers and the village all speak the same language. Force it with WOCC_LANG=fr|en in the
// environment Herdr starts from, or with "lang": "fr" | "en" in a block's props.

import { exec, shared, setShared, props } from "herdr";

const KEY = "wocc.lang";
let asked = false;

/** "fr" or "en". */
export function lang() {
  const p = props()?.lang;
  if (p === "fr" || p === "en") return p;
  return shared(KEY) === "fr" ? "fr" : "en";
}

/** Detects the system language once per start (call it from init). */
export function detectLang(cx) {
  if (asked) return;
  asked = true;
  cx.spawn(async () => {
    try {
      const r = await exec("sh", ["-c",
        'if [ -n "$WOCC_LANG" ]; then echo "$WOCC_LANG"; exit; fi; ' +
        '(defaults read -g AppleLanguages 2>/dev/null | sed -n 2p | tr -d " \\"(),"); ' +
        'echo "${LC_ALL:-${LC_MESSAGES:-$LANG}}"']);
      const first = (r.stdout ?? "").split("\n").map((s) => s.trim()).find(Boolean) ?? "";
      const l = /^fr/i.test(first) ? "fr" : "en";
      if (shared(KEY) !== l) setShared(KEY, l);
    } catch {}
  });
}

/** Every visible string, by key. A function takes the values it needs. */
const S = {
  en: {
    village: "Hobbiton",
    villageOf: (v) => `village of ${v}`,
    pct: (n) => `${n}%`,
    // races and classes
    race: { elfe: "Elf", orque: "Orc", humain: "Hobbit", "mort-vivant": "Barrow-wight", nain: "Dwarf" },
    cls: { mage: "wizard", artificier: "smith", guerrier: "shirriff", pretre: "loremaster", rodeur: "ranger", voleur: "burglar" },
    hero: (race, cls) => `${race} ${cls}`,
    // states
    quest: {
      working: { mot: "On the road", fr: "sets out on the road" },
      blocked: { mot: "Aid needed!", fr: "calls for aid" },
      done: { mot: "Tale to tell", fr: "is back with a tale to tell" },
      idle: { mot: "Resting by the fire", fr: "rests by the fire" },
    },
    board: { blocked: "aid needed", done: "tale to tell", working: "on the road", idle: "resting" },
    hours: ["Night", "Breakfast", "Elevenses", "Luncheon", "Tea", "Dinner", "Supper"],
    days: "d",
    home: "Home",
    district: (n, name) => `Realm ${n} · ${name}`,
    // header
    accountNone: (label, acc) => `${label}: no reading for Claude account ${acc}`,
    account: (acc) => `account ${acc}`,
    five: (p) => `5h: ${p}%`,
    quotaTip: (label, acc, rem, fair, five, fiveLeft, stale) =>
      `${label} = Claude account ${acc}\n${rem}% left this week (the Party in ${fair})${five != null ? `\n5-hour window: ${five}% left${fiveLeft ? ` (${fiveLeft})` : ""}` : ""}${stale ? "\nReading older than 30 min" : ""}`,
    gold: "Mithril", wood: "Lembas",
    waitingMany: (n, blocked) => `${n} ${blocked ? "waiting" : "tales to tell"}`,
    waitingOne: (name, blocked) => `${name} ${blocked ? "is waiting" : "is done"}`,
    waitingTip: (title, blocked) => `${title} ${blocked ? "awaits your orders" : "is back from the road"} (click: go there)`,
    questTab: (name) => `Quest: ${name}`,
    hourTip: (hour, night) => `${hour} (hobbit mealtime) · ${night ? "night" : "day"}`,
    heroesAtWork: "heroes at work",
    heroesTip: (busy, all) => `${busy} heroes at work, ${all} agents in Hobbiton`,
    untilFair: "until the Party",
    fairTip: "The long-expected Party: the weekly reset of the Claude quotas",
    immersion: "Immersion", workshop: "Workshop",
    immersionTip: "Immersive mode: the village fills the window, the terminal goes below (ctrl-shift-i)",
    workshopTip: "Back to the workshop: the terminal fills the window, the village goes below (ctrl-shift-i)",
    // board
    questN: (n) => `Quest #${n}`,
    questTip: (n, name, panes) => `Quest ${n}: ${name}${panes > 1 ? ` (${panes} sessions)` : ""} (click: show it)`,
    goThere: "(click: go there)",
    sessions: (n) => `${n} ${n === 1 ? "session" : "sessions"}`,
    heroes: (n) => `${n} ${n === 1 ? "hero" : "heroes"}`,
    sessionsHere: (s) => `${s} in this realm`,
    districts: "Realms",
    newQuest: "Quest", newQuestTip: "Start a new quest (a new tab in this realm)",
    newDistrict: "Realm", newDistrictTip: "Found a new realm (a new space)",
    // command panel
    map: "Map of the Shire",
    selected: "Selected unit",
    noUnit: "No unit selected",
    clickHero: "Click a hero in Hobbiton",
    onGuard: "On guard",
    go: "Go", goTip: "Go to this hero",
    next: "Next", nextTip: "Next hero",
    animations: "Animations", yes: "on", no: "off",
    animOnTip: "Animations, scenes and enemies: on.\nClick: still images (saves CPU)",
    animOffTip: "Still images.\nClick: animate the village (scenes, enemies)",
    // pane header
    scroll: "Scroll",
    splitR: "Split right", splitD: "Split down", zoom: "Zoom", close: "Close",
    // places
    building: { grange: "Farmstead and fields", tour: "Wizard's Tower", atelier: "Smithy", hotel: "Mayor's Hall", taverne: "The Green Dragon", temple: "Mathom-house", caserne: "Shirriff-house" },
    market: "Market",
    campfire: "Campfire",
    gate: "Bywater Road",
    crier: "Quick Post",
    recruit: { tour: "a wizard (Claude)", atelier: "a smith (Codex)", caserne: "a shirriff (terminal)" },
    recruitTip: (name, what) => `${name}\nDouble-click: recruit ${what}`,
    mapTip: "Village map (click: move the view there)",
    // chronicle
    arrives: (title, prog) => `${title} (${prog}) arrives in Hobbiton`,
    leaves: (title) => `${title} leaves Hobbiton`,
    hearYe: (n, b) => `Hear now! ${n} ${n === 1 ? "hero" : "heroes"} in Hobbiton${b ? `, ${b} awaiting your orders` : ""}`,
    quoted: (s) => ` "${s}"`,
    unitTip: (title, prog, where, word) => `${title} · ${prog}\n${where}\n${word} (click: go there)`,
    onGuardTerm: "On guard (terminal)",
    help: ["Aid!", "Aid!", "What news?", "To me!"],
    demoTabs: ["PR review", "tests", "migration", "docs", "rest", "map", "triage", "build", "refactor", "fix"],
    // scenes
    ouch: "Ouch!", sealed: "Sealed!", sent: "Message sent!", testsOk: "Tests passed!", testsKo: "Tests failing",
    // village life
    treasury: (p) => `Mathom-hoard of Hobbiton: ${p}% of account A left this week`,
    fair: (t) => `The long-expected Party: reset in ${t}`,
  },
  fr: {
    village: "Hobbitebourg",
    villageOf: (v) => `village de ${v}`,
    pct: (n) => `${n} %`,
    race: { elfe: "elfe", orque: "orque", humain: "hobbit", "mort-vivant": "des Galgals", nain: "nain" },
    cls: { mage: "magicien", artificier: "forgeron", guerrier: "shiriff", pretre: "maître du savoir", rodeur: "rôdeur", voleur: "cambrioleur" },
    hero: (race, cls) => `${cls} ${race}`,
    quest: {
      working: { mot: "Sur la route", fr: "prend la route" },
      blocked: { mot: "À l'aide !", fr: "appelle à l'aide" },
      done: { mot: "Un récit à conter", fr: "revient avec un récit à conter" },
      idle: { mot: "Au coin du feu", fr: "se repose au coin du feu" },
    },
    board: { blocked: "aide", done: "récit", working: "en route", idle: "repos" },
    hours: ["Nuit", "Petit-déj.", "Onze-heures", "Déjeuner", "Thé", "Dîner", "Souper"],
    days: "j",
    home: "Logis",
    district: (n, name) => `Royaume ${n} · ${name}`,
    accountNone: (label, acc) => `${label} : pas de relevé du compte Claude ${acc}`,
    account: (acc) => `compte ${acc}`,
    five: (p) => `5 h : ${p} %`,
    quotaTip: (label, acc, rem, fair, five, fiveLeft, stale) =>
      `${label} = compte Claude ${acc}\nIl reste ${rem} % cette semaine (la Fête dans ${fair})${five != null ? `\nFenêtre 5 h : ${five} % restants${fiveLeft ? ` (${fiveLeft})` : ""}` : ""}${stale ? "\nRelevé de plus de 30 min" : ""}`,
    gold: "Mithril", wood: "Lembas",
    waitingMany: (n, blocked) => `${n} ${blocked ? "attendent" : "récits à conter"}`,
    waitingOne: (name, blocked) => `${name} ${blocked ? "attend" : "a fini"}`,
    waitingTip: (title, blocked) => `${title} ${blocked ? "attend tes ordres" : "revient de la route"} — clic : y aller`,
    questTab: (name) => `Quête : ${name}`,
    hourTip: (hour, night) => `${hour} (repas hobbit) · ${night ? "nuit" : "jour"}`,
    heroesAtWork: "héros à l'œuvre",
    heroesTip: (busy, all) => `${busy} héros travaillent, ${all} agents à Hobbitebourg`,
    untilFair: "avant la Fête",
    fairTip: "La Fête longuement attendue : réinitialisation hebdomadaire des quotas Claude",
    immersion: "Immersion", workshop: "Atelier",
    immersionTip: "Mode immersif : le village occupe la fenêtre, le terminal passe en bas (ctrl-shift-i)",
    workshopTip: "Retour à l'atelier : le terminal occupe la fenêtre, le village passe en bas (ctrl-shift-i)",
    questN: (n) => `Quête n° ${n}`,
    questTip: (n, name, panes) => `Quête ${n} : ${name}${panes > 1 ? ` (${panes} sessions)` : ""} — clic : l'afficher`,
    goThere: "— clic : y aller",
    sessions: (n) => `${n} ${n === 1 ? "session" : "sessions"}`,
    heroes: (n) => `${n} héros`,
    sessionsHere: (s) => `${s} dans ce royaume`,
    districts: "Royaumes",
    newQuest: "Quête", newQuestTip: "Afficher une nouvelle quête (nouvel onglet dans ce royaume)",
    newDistrict: "Royaume", newDistrictTip: "Fonder un nouveau royaume (nouvel espace)",
    map: "Carte de la Comté",
    selected: "Unité choisie",
    noUnit: "Aucune unité choisie",
    clickHero: "Clic sur un héros de Hobbitebourg",
    onGuard: "De garde",
    go: "Aller", goTip: "Aller à ce héros",
    next: "Suivant", nextTip: "Héros suivant",
    animations: "Animations", yes: "oui", no: "non",
    animOnTip: "Animations, scènes et ennemis : activés.\nClic : images fixes (économise le processeur)",
    animOffTip: "Images fixes.\nClic : animer le village (scènes, ennemis)",
    scroll: "Parchemin",
    splitR: "Fendre à droite", splitD: "Fendre en bas", zoom: "Agrandir", close: "Fermer",
    building: { grange: "Ferme et champs", tour: "Tour du magicien", atelier: "Forge", hotel: "Hôtel du Maire", taverne: "Le Dragon Vert", temple: "Maison des Mathoms", caserne: "Poste des Shiriffs" },
    market: "Marché",
    campfire: "Feu de camp",
    gate: "Route de Lèzeau",
    crier: "Poste rapide",
    recruit: { tour: "un magicien (Claude)", atelier: "un forgeron (Codex)", caserne: "un shiriff (terminal)" },
    recruitTip: (name, what) => `${name}\nDouble-clic : recruter ${what}`,
    mapTip: "Carte du village — clic : y déplacer la vue",
    arrives: (title, prog) => `${title} (${prog}) arrive à Hobbitebourg`,
    leaves: (title) => `${title} quitte Hobbitebourg`,
    hearYe: (n, b) => `Oyez ! ${n} héros à Hobbitebourg${b ? `, ${b} attendent tes ordres` : ""}`,
    quoted: (s) => ` « ${s} »`,
    unitTip: (title, prog, where, word) => `${title} · ${prog}\n${where}\n${word} — clic : y aller`,
    onGuardTerm: "De garde (terminal)",
    help: ["À l'aide !", "À l'aide !", "Quelles nouvelles ?", "Par ici !"],
    demoTabs: ["revue PR", "tests", "migration", "doc", "repos", "carte", "tri", "build", "refonte", "correctif"],
    ouch: "Aïe !", sealed: "Scellé !", sent: "Message envoyé !", testsOk: "Tests réussis !", testsKo: "Tests en échec",
    treasury: (p) => `Trésor des Mathoms : ${p} % du compte A cette semaine`,
    fair: (t) => `La Fête longuement attendue : réinitialisation dans ${t}`,
  },
};

/** The string (or the function's result) for a key in the current language. */
export function t(key, ...args) {
  const v = S[lang()][key] ?? S.en[key];
  return typeof v === "function" ? v(...args) : v;
}

/** A live view of a table (race, cls, quest, board, building, recruit): `tbl("race").elfe`. */
export const tbl = (key) => new Proxy({}, { get: (_o, k) => (S[lang()][key] ?? S.en[key])?.[k] });
