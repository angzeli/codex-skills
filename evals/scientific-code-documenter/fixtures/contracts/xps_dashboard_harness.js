#!/usr/bin/env node

const fs = require("fs");
const vm = require("vm");


function requireCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}


class ClassList {
  constructor(element) {
    this.element = element;
    this.values = new Set();
  }

  setFromString(value) {
    this.values = new Set(String(value).split(/\s+/).filter(Boolean));
  }

  contains(value) {
    return this.values.has(value);
  }

  toggle(value, force) {
    const enabled = force === undefined ? !this.values.has(value) : Boolean(force);
    if (enabled) this.values.add(value);
    else this.values.delete(value);
    this.element._className = Array.from(this.values).join(" ");
    return enabled;
  }
}


class Element {
  constructor(document, tagName, id = "") {
    this.ownerDocument = document;
    this.tagName = tagName.toUpperCase();
    this.id = id;
    this.children = [];
    this.parentNode = null;
    this.attributes = {};
    this.listeners = {};
    this.value = "";
    this.checked = false;
    this._textContent = "";
    this._className = "";
    this.classList = new ClassList(this);
    document.elements.push(this);
    if (id) document.byId.set(id, this);
  }

  get className() {
    return this._className;
  }

  set className(value) {
    this._className = String(value);
    this.classList.setFromString(value);
  }

  get textContent() {
    return this._textContent;
  }

  set textContent(value) {
    this._textContent = String(value);
  }

  get innerHTML() {
    return "";
  }

  set innerHTML(value) {
    requireCondition(value === "", "harness supports only clearing innerHTML");
    this.children.forEach((child) => {
      child.parentNode = null;
    });
    this.children = [];
  }

  get firstChild() {
    return this.children[0] || null;
  }

  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }

  append(...children) {
    children.forEach((child) => this.appendChild(child));
  }

  replaceChildren(...children) {
    this.children = [];
    this.append(...children);
  }

  removeChild(child) {
    const index = this.children.indexOf(child);
    requireCondition(index >= 0, "attempted to remove a non-child node");
    this.children.splice(index, 1);
    child.parentNode = null;
    return child;
  }

  remove() {
    if (this.parentNode) this.parentNode.removeChild(this);
  }

  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === "class") this.className = value;
  }

  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name]
      : null;
  }

  addEventListener(type, callback) {
    if (!this.listeners[type]) this.listeners[type] = [];
    this.listeners[type].push(callback);
  }

  dispatch(type) {
    (this.listeners[type] || []).forEach((callback) => callback({ target: this }));
  }

  click() {
    this.dispatch("click");
    if (this.tagName === "A") this.ownerDocument.recordDownload(this);
  }
}


class FakeDocument {
  constructor() {
    this.byId = new Map();
    this.elements = [];
    this.downloads = [];
    this.body = new Element(this, "body");
  }

  add(tagName, id, initial = {}) {
    const element = new Element(this, tagName, id);
    Object.assign(element, initial);
    return element;
  }

  getElementById(id) {
    return this.byId.get(id) || null;
  }

  createElement(tagName) {
    return new Element(this, tagName);
  }

  createElementNS(_namespace, tagName) {
    return new Element(this, tagName);
  }

  createTextNode(value) {
    const node = new Element(this, "#text");
    node.textContent = value;
    return node;
  }

  querySelectorAll(selector) {
    if (selector.startsWith(".")) {
      const className = selector.slice(1);
      return this.elements.filter((element) => element.classList.contains(className));
    }
    if (selector.startsWith("#")) {
      const element = this.getElementById(selector.slice(1));
      return element ? [element] : [];
    }
    return this.elements.filter((element) => element.tagName.toLowerCase() === selector.toLowerCase());
  }

  querySelector(selector) {
    return this.querySelectorAll(selector)[0] || null;
  }

  recordDownload(anchor) {
    const blob = fakeUrl.blobs.get(anchor.href);
    requireCondition(blob, "download anchor does not reference a captured blob");
    this.downloads.push({ filename: anchor.download, text: blob.parts.join("") });
  }
}


class FakeBlob {
  constructor(parts, options) {
    this.parts = parts.map(String);
    this.type = options && options.type;
  }
}


const fakeUrl = {
  nextId: 1,
  blobs: new Map(),
  createObjectURL(blob) {
    const value = `blob:fixture-${this.nextId++}`;
    this.blobs.set(value, blob);
    return value;
  },
  revokeObjectURL() {},
};


function tableRows(document) {
  return document.getElementById("results-body").children.map((row) =>
    row.children.map((cell) => cell.textContent),
  );
}


function svgOrders(document) {
  return document
    .getElementById("profile-plot")
    .children.filter((element) => element.tagName === "CIRCLE")
    .map((element) => element.getAttribute("data-order"));
}


function runFixture(path) {
  const html = fs.readFileSync(path, "utf8");
  const scripts = [];
  const pattern = /<script([^>]*)>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = pattern.exec(html)) !== null) {
    if (!/type\s*=\s*["']application\/json["']/i.test(match[1])) scripts.push(match[2]);
  }
  requireCondition(scripts.length > 0, "no executable inline script found");

  const document = new FakeDocument();
  document.add("select", "sample-filter", { value: "all" });
  document.add("select", "region-filter", { value: "all" });
  document.add("input", "show-components", { checked: true });
  document.add("tbody", "results-body");
  document.add("div", "row-count");
  document.add("div", "mean-intensity");
  document.add("div", "max-energy");
  document.add("svg", "profile-plot");
  document.add("span", "plot-status");
  document.add("button", "reset-button");
  document.add("button", "export-button");
  const componentHeader = document.add("th", "");
  componentHeader.className = "component-column";

  const window = {};
  window.window = window;
  window.document = document;
  const context = vm.createContext({
    window,
    document,
    Blob: FakeBlob,
    URL: fakeUrl,
    console,
  });
  scripts.forEach((script) => vm.runInContext(script, context, { filename: path }));

  const exported = window.__XPS_EXPORT__;
  requireCondition(exported && typeof exported === "object", "window.__XPS_EXPORT__ is missing");
  requireCondition(
    JSON.stringify(Object.keys(exported).sort()) === JSON.stringify(["rows", "schemaVersion", "toCsv"]),
    "window.__XPS_EXPORT__ public shape changed",
  );
  requireCondition(exported.schemaVersion === 3, "schemaVersion changed");
  requireCondition(typeof exported.toCsv === "function", "toCsv is not callable");

  const expectedRows = [
    ["PDI-Me-COOH", "C1s", 284.8, 12640, "aromatic_C", 0],
    ["PDI-Me-COOH", "C1s", 286.35, 5240, "imide_C", 1],
    ["PDI-Me-COOH", "N1s", 399.72, 7340, "imide_N", 2],
    ["PDI-H-COOH", "C1s", 284.76, 11880, "aromatic_C", 3],
    ["PDI-H-COOH", "O1s", 531.82, 4160, "carbonyl_O", 4],
    ["PDI-OMe-COOH", "C1s", 286.68, 6040, "methoxy_C", 5],
    ["PDI-OMe-COOH", "O1s", 533.16, 4720, "methoxy_O", 6],
  ];
  const actualRows = exported.rows.map((row) => [
    row.sample,
    row.region,
    row.binding_energy_ev,
    row.intensity_cps,
    row.component,
    row.order,
  ]);
  requireCondition(JSON.stringify(actualRows) === JSON.stringify(expectedRows), "raw export rows changed");

  const expectedCsv =
    "sample,region,binding_energy_ev,intensity_cps,component\n" +
    expectedRows
      .map((row) => `${row[0]},${row[1]},${row[2].toFixed(2)},${row[3]},${row[4]}`)
      .join("\n") +
    "\n";
  requireCondition(exported.toCsv(exported.rows) === expectedCsv, "full CSV export changed");
  requireCondition(document.getElementById("row-count").textContent === "7", "initial row count changed");
  requireCondition(document.getElementById("mean-intensity").textContent === "7.431", "display scaling or mean formatting changed");
  requireCondition(document.getElementById("max-energy").textContent === "533.16", "binding-energy formatting changed");
  requireCondition(tableRows(document).length === 7, "initial table row count changed");
  requireCondition(JSON.stringify(svgOrders(document)) === JSON.stringify(["0", "1", "2", "3", "4", "5", "6"]), "initial SVG point order changed");

  const sample = document.getElementById("sample-filter");
  const region = document.getElementById("region-filter");
  sample.value = "PDI-Me-COOH";
  sample.dispatch("change");
  requireCondition(document.getElementById("row-count").textContent === "3", "sample filter row count changed");
  requireCondition(document.getElementById("mean-intensity").textContent === "8.407", "filtered mean changed");
  requireCondition(document.getElementById("max-energy").textContent === "399.72", "filtered maximum changed");
  requireCondition(JSON.stringify(svgOrders(document)) === JSON.stringify(["0", "1", "2"]), "sample filter reordered SVG data");

  region.value = "C1s";
  region.dispatch("change");
  requireCondition(JSON.stringify(svgOrders(document)) === JSON.stringify(["0", "1"]), "combined filters changed order")

  const components = document.getElementById("show-components");
  components.checked = false;
  components.dispatch("change");
  requireCondition(
    document.querySelectorAll(".component-column").every((element) => element.classList.contains("hidden")),
    "component visibility toggle changed",
  );

  document.getElementById("reset-button").click();
  requireCondition(sample.value === "all" && region.value === "all" && components.checked, "reset control state changed");
  requireCondition(document.getElementById("row-count").textContent === "7", "reset row count changed");
  requireCondition(
    document.querySelectorAll(".component-column").every((element) => !element.classList.contains("hidden")),
    "reset no longer restores component visibility",
  );

  sample.value = "PDI-H-COOH";
  sample.dispatch("change");
  document.getElementById("export-button").click();
  requireCondition(document.downloads.length === 1, "export did not produce one download");
  requireCondition(document.downloads[0].filename === "xps_visible_rows.csv", "export filename changed");
  requireCondition(
    document.downloads[0].text ===
      "sample,region,binding_energy_ev,intensity_cps,component\n" +
        "PDI-H-COOH,C1s,284.76,11880,aromatic_C\n" +
        "PDI-H-COOH,O1s,531.82,4160,carbonyl_O\n",
    "filtered CSV values, formatting, order, raw intensity, or trailing newline changed",
  );

  console.log("PASS HTML dashboard behaviour contract");
}


if (process.argv.length !== 3) {
  throw new Error("usage: xps_dashboard_harness.js HTML_FILE");
}
runFixture(process.argv[2]);
