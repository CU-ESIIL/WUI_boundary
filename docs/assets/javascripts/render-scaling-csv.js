(function () {
  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let cell = "";
    let inQuotes = false;

    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      const next = text[i + 1];

      if (ch === '"') {
        if (inQuotes && next === '"') {
          cell += '"';
          i += 1;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === "," && !inQuotes) {
        row.push(cell);
        cell = "";
      } else if ((ch === "\n" || ch === "\r") && !inQuotes) {
        if (ch === "\r" && next === "\n") {
          i += 1;
        }
        row.push(cell);
        if (row.some((value) => value.length > 0)) {
          rows.push(row);
        }
        row = [];
        cell = "";
      } else {
        cell += ch;
      }
    }

    row.push(cell);
    if (row.some((value) => value.length > 0)) {
      rows.push(row);
    }

    return rows;
  }

  function resolveCsvUrl(src) {
    if (!src) {
      return "";
    }
    return new URL(src, window.location.href).toString();
  }

  function renderTable(container, parsedRows, sourceLabel) {
    const [header, ...body] = parsedRows;
    if (!header || header.length === 0) {
      container.innerHTML = '<p class="scaling-table-message">Summary table is empty.</p>';
      return;
    }

    const thead = `<thead><tr>${header
      .map((col) => `<th scope="col">${escapeHtml(col)}</th>`)
      .join("")}</tr></thead>`;
    const tbody = `<tbody>${body
      .map(
        (cells) =>
          `<tr>${header
            .map((_, i) => `<td>${escapeHtml(cells[i] ?? "")}</td>`)
            .join("")}</tr>`
      )
      .join("")}</tbody>`;

    container.innerHTML = `
      <table class="scaling-results-table">
        ${thead}
        ${tbody}
      </table>
      <p class="scaling-table-caption">Rendered from <code>${escapeHtml(sourceLabel)}</code>.</p>
    `;
  }

  function renderPlot(container, parsedRows) {
    const [header, ...body] = parsedRows;
    if (!header || body.length === 0) {
      container.innerHTML = '<p class="scaling-table-message">Plot data is empty.</p>';
      return;
    }

    const epsilonIdx = header.indexOf("epsilon");
    const perimeterIdx = header.indexOf("perimeter");
    if (epsilonIdx < 0 || perimeterIdx < 0) {
      container.innerHTML = '<p class="scaling-table-message">Plot columns are missing in CSV.</p>';
      return;
    }

    const points = body
      .map((cells) => ({
        x: Number(cells[epsilonIdx]),
        y: Number(cells[perimeterIdx]),
      }))
      .filter((point) => Number.isFinite(point.x) && Number.isFinite(point.y));

    if (points.length < 2) {
      container.innerHTML = '<p class="scaling-table-message">Not enough rows to draw the plot.</p>';
      return;
    }

    const width = 960;
    const height = 420;
    const margin = { top: 30, right: 20, bottom: 48, left: 70 };
    const xmin = Math.min(...points.map((point) => point.x));
    const xmax = Math.max(...points.map((point) => point.x));
    const ymin = Math.min(...points.map((point) => point.y));
    const ymax = Math.max(...points.map((point) => point.y));

    const scaleX = (x) => {
      if (xmax === xmin) {
        return margin.left;
      }
      return margin.left + ((x - xmin) / (xmax - xmin)) * (width - margin.left - margin.right);
    };

    const scaleY = (y) => {
      if (ymax === ymin) {
        return height - margin.bottom;
      }
      return (
        height -
        margin.bottom -
        ((y - ymin) / (ymax - ymin)) * (height - margin.top - margin.bottom)
      );
    };

    const pathData = points
      .map((point, index) => `${index === 0 ? "M" : "L"}${scaleX(point.x)},${scaleY(point.y)}`)
      .join(" ");

    const circles = points
      .map(
        (point) =>
          `<circle cx="${scaleX(point.x)}" cy="${scaleY(point.y)}" r="4" class="scaling-plot-point" />`
      )
      .join("");

    container.innerHTML = `
      <svg class="scaling-results-plot" viewBox="0 0 ${width} ${height}" role="img" aria-label="Synthetic WUI boundary scaling relationship">
        <line x1="${margin.left}" y1="${height - margin.bottom}" x2="${width - margin.right}" y2="${height - margin.bottom}" class="scaling-plot-axis" />
        <line x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${height - margin.bottom}" class="scaling-plot-axis" />
        <path d="${pathData}" class="scaling-plot-line" />
        ${circles}
      </svg>
      <p class="scaling-table-caption">Synthetic perimeter across epsilon values.</p>
    `;
  }

  async function fetchParsedRows(container) {
    const source = container.dataset.csvSrc;
    const fallback =
      container.dataset.csvFallback ||
      "Summary output is unavailable right now. Please use the CSV download link.";

    if (!source) {
      throw new Error(fallback);
    }

    const csvUrl = resolveCsvUrl(source);
    const response = await fetch(csvUrl, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(fallback);
    }

    const csvText = await response.text();
    const rows = parseCsv(csvText);
    if (rows.length === 0) {
      throw new Error(fallback);
    }

    return { rows, sourceLabel: source };
  }

  async function initialize() {
    const tableContainer = document.querySelector("[data-csv-table='true']");
    const plotContainer = document.querySelector("[data-csv-plot='true']");

    const targets = [tableContainer, plotContainer].filter(Boolean);
    if (targets.length === 0) {
      return;
    }

    const sourceContainer = tableContainer || plotContainer;
    const fallback =
      sourceContainer.dataset.csvFallback ||
      "Summary output is unavailable right now. Please use the CSV download link.";

    try {
      const { rows, sourceLabel } = await fetchParsedRows(sourceContainer);
      if (tableContainer) {
        renderTable(tableContainer, rows, sourceLabel);
      }
      if (plotContainer) {
        renderPlot(plotContainer, rows);
      }
    } catch (error) {
      targets.forEach((target) => {
        target.innerHTML = `<p class="scaling-table-message">${escapeHtml(fallback)}</p>`;
      });
    }
  }

  document.addEventListener("DOMContentLoaded", initialize);
})();
