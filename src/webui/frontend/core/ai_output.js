const THINK_RE = /<think>([\s\S]*?)<\/think>/gi;

export function parseAiMessage(input) {
  const text = String(input || "").replace(/\r\n/g, "\n");
  const parts = [];
  let cursor = 0;
  let match;
  while ((match = THINK_RE.exec(text)) !== null) {
    if (match.index > cursor) {
      parts.push({ type: "answer", content: text.slice(cursor, match.index).trim() });
    }
    parts.push({ type: "think", content: match[1].trim() });
    cursor = match.index + match[0].length;
  }
  if (cursor < text.length) {
    parts.push({ type: "answer", content: text.slice(cursor).trim() });
  }
  return parts.filter((part) => part.content);
}

export function renderAiMessage(host, input, options = {}) {
  host.innerHTML = "";
  host.classList.add("ai-output");
  const meta = options.meta || "";
  if (meta) {
    const metaEl = document.createElement("div");
    metaEl.className = "ai-output__meta";
    metaEl.textContent = meta;
    host.append(metaEl);
  }

  const parts = parseAiMessage(input);
  if (!parts.length) {
    const empty = document.createElement("p");
    empty.className = "ai-output__empty";
    empty.textContent = "模型没有返回内容。";
    host.append(empty);
    return;
  }

  for (const part of parts) {
    if (part.type === "think") {
      host.append(renderThink(part.content));
    } else {
      const body = document.createElement("div");
      body.className = "ai-output__answer";
      renderBlocks(body, part.content);
      host.append(body);
    }
  }
}

function renderThink(content) {
  const details = document.createElement("details");
  details.className = "ai-output__think";
  const summary = document.createElement("summary");
  summary.textContent = "模型思考过程";
  details.append(summary);
  const body = document.createElement("div");
  body.className = "ai-output__think-body";
  renderBlocks(body, content);
  details.append(body);
  return details;
}

function renderBlocks(host, content) {
  const lines = content.split("\n");
  let paragraph = [];
  let list = null;

  function flushParagraph() {
    if (!paragraph.length) return;
    const p = document.createElement("p");
    renderInline(p, paragraph.join("\n"));
    host.append(p);
    paragraph = [];
  }

  function flushList() {
    if (!list) return;
    host.append(list);
    list = null;
  }

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      flushList();
      const level = String(Math.min(heading[1].length + 3, 6));
      const h = document.createElement(`h${level}`);
      renderInline(h, heading[2]);
      host.append(h);
      continue;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    const ordered = line.match(/^\d+[.)]\s+(.+)$/);
    if (bullet || ordered) {
      flushParagraph();
      const kind = ordered ? "ol" : "ul";
      if (!list || list.tagName.toLowerCase() !== kind) {
        flushList();
        list = document.createElement(kind);
      }
      const item = document.createElement("li");
      renderInline(item, (bullet || ordered)[1]);
      list.append(item);
      continue;
    }

    flushList();
    paragraph.push(rawLine.trimEnd());
  }

  flushParagraph();
  flushList();
}

function renderInline(host, text) {
  const pattern = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let cursor = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    appendText(host, text.slice(cursor, match.index));
    const token = match[0];
    if (token.startsWith("**")) {
      const strong = document.createElement("strong");
      strong.textContent = token.slice(2, -2);
      host.append(strong);
    } else {
      const code = document.createElement("code");
      code.textContent = token.slice(1, -1);
      host.append(code);
    }
    cursor = match.index + token.length;
  }
  appendText(host, text.slice(cursor));
}

function appendText(host, text) {
  if (!text) return;
  const chunks = text.split("\n");
  chunks.forEach((chunk, index) => {
    if (index > 0) host.append(document.createElement("br"));
    if (chunk) host.append(document.createTextNode(chunk));
  });
}
