"use strict";

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const COLORS = {
    background: "#05080b",
    grid: "#1b252e",
    muted: "#687582",
    text: "#9aa8b3",
    gold: "#d6a550",
    blue: "#6f9eb5",
    blueBright: "#8bb8d0",
    line: "#5fa8d3",
};

const DAY_SECONDS = 86400;
const AU_METERS = 1.495978707e11;

const state = {
    playing: true,
    progress: 0,
    speed: 4,
    lastFrame: 0,
    elapsed: 0,
    simulationData: null,
    running: false,
};

const orbitCanvas = $("#orbit-canvas");
const trajectoryCanvas = $("#trajectory-chart");
const stateCanvas = $("#state-chart");

function setupCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    const width = Math.max(1, rect.width);
    const height = Math.max(1, rect.height);
    const ratio = Math.min(window.devicePixelRatio || 1, 2);

    const pixelWidth = Math.round(width * ratio);
    const pixelHeight = Math.round(height * ratio);

    if (canvas.width !== pixelWidth || canvas.height !== pixelHeight) {
        canvas.width = pixelWidth;
        canvas.height = pixelHeight;
    }

    const context = canvas.getContext("2d");
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    return { context, width, height };
}

function drawBackground(ctx, width, height) {
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, width, height);

    let seed = 42;
    const random = () => {
        seed = (seed * 16807) % 2147483647;
        return (seed - 1) / 2147483646;
    };

    for (let i = 0; i < 125; i++) {
        const x = random() * width;
        const y = random() * height;
        const radius = random() * 0.85 + 0.2;
        const alpha = random() * 0.35 + 0.08;

        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(155, 177, 196, ${alpha})`;
        ctx.fill();
    }
}

function drawGlow(ctx, x, y, radius, color, strength = 1) {
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);

    gradient.addColorStop(0, color.replace("ALPHA", `${0.25 * strength}`));
    gradient.addColorStop(0.35, color.replace("ALPHA", `${0.08 * strength}`));
    gradient.addColorStop(1, color.replace("ALPHA", "0"));

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}

function drawStar(ctx, x, y, radius) {
    drawGlow(ctx, x, y, radius * 3.2, "rgba(226, 163, 64, ALPHA)", 1.3);
    drawGlow(ctx, x, y, radius * 1.7, "rgba(255, 207, 112, ALPHA)", 1.2);

    const surface = ctx.createRadialGradient(
        x - radius * 0.3,
        y - radius * 0.35,
        radius * 0.05,
        x,
        y,
        radius
    );

    surface.addColorStop(0, "#fff8d9");
    surface.addColorStop(0.42, "#ffe8a1");
    surface.addColorStop(0.78, "#ffd36b");
    surface.addColorStop(1, "#d87925");

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = surface;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(
        x - radius * 0.25,
        y - radius * 0.3,
        radius * 0.13,
        0,
        Math.PI * 2
    );
    ctx.fillStyle = "rgba(255,255,255,0.7)";
    ctx.fill();
}

function drawPlanet(ctx, x, y, radius) {
    drawGlow(ctx, x, y, radius * 4.3, "rgba(70, 143, 191, ALPHA)", 1.5);
    drawGlow(ctx, x, y, radius * 2.0, "rgba(102, 173, 210, ALPHA)", 1);

    const surface = ctx.createRadialGradient(
        x - radius * 0.35,
        y - radius * 0.35,
        radius * 0.05,
        x,
        y,
        radius
    );

    surface.addColorStop(0, "#c1deeb");
    surface.addColorStop(0.35, "#8bb8d0");
    surface.addColorStop(0.75, "#47758e");
    surface.addColorStop(1, "#203846");

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = surface;
    ctx.fill();

    ctx.save();
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.clip();

    ctx.strokeStyle = "rgba(180, 215, 231, 0.24)";
    ctx.lineWidth = Math.max(1, radius * 0.18);

    for (let i = -2; i <= 2; i++) {
        ctx.beginPath();
        ctx.ellipse(
            x + i * radius * 0.18,
            y + i * radius * 0.12,
            radius * 0.75,
            radius * 0.18,
            -0.4,
            0,
            Math.PI * 2
        );
        ctx.stroke();
    }

    ctx.restore();
}

function drawCenterOfMass(ctx, x, y) {
    ctx.strokeStyle = "rgba(154, 168, 179, 0.75)";
    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.moveTo(x - 6, y);
    ctx.lineTo(x + 6, y);
    ctx.moveTo(x, y - 6);
    ctx.lineTo(x, y + 6);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.stroke();
}

function durationInDays() {
    const value = Math.max(0, Number($("#duration").value) || 1);
    const unit = $("#duration-unit").value;

    const multipliers = {
        YEAR: 365.25,
        MONTH: 30.4375,
        DAY: 1,
        HOUR: 1 / 24,
    };

    return value * (multipliers[unit] || 365.25);
}

function currentIndex() {
    const data = state.simulationData;
    if (!data?.trajectory_times?.length) return 0;

    return Math.min(
        data.trajectory_times.length - 1,
        Math.floor(state.progress * (data.trajectory_times.length - 1))
    );
}

function pointXY(point) {
    if (!Array.isArray(point)) return [0, 0];

    return [
        Number(point[0]) || 0,
        Number(point[1]) || 0,
    ];
}

function coordinatesInAU(trajectory) {
    if (!Array.isArray(trajectory)) return [];

    return trajectory.map((point) => {
        const [x, y] = pointXY(point);
        return [x / AU_METERS, y / AU_METERS];
    });
}

function getCoordinateBounds(series) {
    const points = series.flat().filter(
        (point) =>
            Array.isArray(point) &&
            Number.isFinite(point[0]) &&
            Number.isFinite(point[1])
    );

    if (!points.length) {
        return { minX: -1, maxX: 1, minY: -1, maxY: 1 };
    }

    let minX = Math.min(...points.map((point) => point[0]));
    let maxX = Math.max(...points.map((point) => point[0]));
    let minY = Math.min(...points.map((point) => point[1]));
    let maxY = Math.max(...points.map((point) => point[1]));

    if (maxX - minX < 1e-12) {
        minX -= 0.5;
        maxX += 0.5;
    }

    if (maxY - minY < 1e-12) {
        minY -= 0.5;
        maxY += 0.5;
    }

    const centerX = (minX + maxX) / 2;
    const centerY = (minY + maxY) / 2;
    const span = Math.max(maxX - minX, maxY - minY, 1e-12) * 1.15;

    return {
        minX: centerX - span / 2,
        maxX: centerX + span / 2,
        minY: centerY - span / 2,
        maxY: centerY + span / 2,
    };
}

function mapPosition(point, bounds, rect) {
    const x = rect.left +
        ((point[0] - bounds.minX) / (bounds.maxX - bounds.minX)) * rect.width;

    const y = rect.top +
        (1 - (point[1] - bounds.minY) / (bounds.maxY - bounds.minY)) * rect.height;

    return [x, y];
}

function drawPath(ctx, points, bounds, rect, color, lineWidth, endIndex = points.length - 1) {
    if (!points.length) return;

    const last = Math.min(endIndex, points.length - 1);
    if (last < 1) return;

    ctx.beginPath();

    for (let i = 0; i <= last; i++) {
        const [x, y] = mapPosition(points[i], bounds, rect);

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
}

function drawOrbitScene() {
    if (!orbitCanvas.isConnected) return;

    const { context: ctx, width, height } = setupCanvas(orbitCanvas);
    drawBackground(ctx, width, height);

    const data = state.simulationData;

    if (data?.trajectory_star?.length && data?.trajectory_planet?.length) {
        drawActualOrbitScene(ctx, width, height, data);
        return;
    }

    drawPreviewOrbitScene(ctx, width, height);
}

function drawPreviewOrbitScene(ctx, width, height) {
    const cx = width / 2;
    const cy = height / 2;
    const radius = Math.min(width * 0.34, height * 0.35, 170);
    const angle = state.progress * Math.PI * 2;

    ctx.save();
    ctx.setLineDash([2, 7]);
    ctx.strokeStyle = "rgba(110, 145, 175, 0.28)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.ellipse(cx, cy, radius, radius * 0.82, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();

    ctx.strokeStyle = "rgba(110, 145, 175, 0.9)";
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.ellipse(
        cx,
        cy,
        radius,
        radius * 0.82,
        0,
        -Math.PI / 2,
        -Math.PI / 2 + state.progress * Math.PI * 2
    );
    ctx.stroke();

    const starX = cx - Math.cos(angle) * radius * 0.015;
    const starY = cy - Math.sin(angle) * radius * 0.015;
    const planetX = cx + Math.cos(angle) * radius;
    const planetY = cy + Math.sin(angle) * radius * 0.82;

    drawCenterOfMass(ctx, cx, cy);
    drawStar(ctx, starX, starY, Math.max(8, Math.min(15, width * 0.018)));
    drawPlanet(ctx, planetX, planetY, Math.max(4, Math.min(7, width * 0.009)));

    drawLabels(ctx, starX, starY, planetX, planetY, cx, cy);

    const days = state.progress * durationInDays();
    $("#simulation-time").textContent =
        `${days.toFixed(2).padStart(6, "0")} DAYS`;

    $("#simulation-distance").textContent =
        `${getInputDistanceAU().toFixed(3)} AU`;

    updateTimeline();
}

function drawActualOrbitScene(ctx, width, height, data) {
    const star = coordinatesInAU(data.trajectory_star);
    const planet = coordinatesInAU(data.trajectory_planet);
    const count = Math.min(star.length, planet.length);

    if (!count) return;

    const index = Math.min(currentIndex(), count - 1);
    const bounds = getCoordinateBounds([star, planet]);

    const padding = Math.min(42, Math.max(18, Math.min(width, height) * 0.08));
    const rect = {
        left: padding,
        top: padding,
        width: Math.max(1, width - padding * 2),
        height: Math.max(1, height - padding * 2),
    };

    drawPath(ctx, star, bounds, rect, "rgba(214, 165, 80, 0.55)", 1.2, index);
    drawPath(ctx, planet, bounds, rect, "rgba(110, 170, 210, 0.55)", 1.3, index);

    const [cx, cy] = mapPosition([0, 0], bounds, rect);
    drawCenterOfMass(ctx, cx, cy);

    const [sx, sy] = mapPosition(star[index], bounds, rect);
    const [px, py] = mapPosition(planet[index], bounds, rect);

    drawStar(ctx, sx, sy, Math.max(8, Math.min(15, width * 0.018)));
    drawPlanet(ctx, px, py, Math.max(4, Math.min(7, width * 0.009)));

    drawLabels(ctx, sx, sy, px, py, cx, cy);

    const seconds = Number(data.trajectory_times?.[index]) || 0;
    $("#simulation-time").textContent =
        `${(seconds / DAY_SECONDS).toFixed(2).padStart(6, "0")} DAYS`;

    const distances = data.distance_history || [];
    const distance = Number(distances[index]);

    $("#simulation-distance").textContent = Number.isFinite(distance)
        ? `${(distance / AU_METERS).toFixed(3)} AU`
        : `${getInputDistanceAU().toFixed(3)} AU`;

    updateTimeline();
}

function drawLabels(ctx, sx, sy, px, py, cx, cy) {
    ctx.font = "10px Segoe UI, Arial";
    ctx.fillStyle = COLORS.gold;
    ctx.fillText("PRIMARY BODY", sx + 17, sy - 13);

    ctx.fillStyle = COLORS.blueBright;
    ctx.fillText("SECONDARY BODY", px + 12, py + 17);

    ctx.font = "9px Segoe UI, Arial";
    ctx.fillStyle = "#7f8c98";
    ctx.fillText("CENTER OF MASS", cx + 11, cy - 10);
}

function getInputDistanceAU() {
    const value = Math.max(0, Number($("#distance").value) || 1);
    const unit = $("#distance-unit").value;

    if (unit === "KM") return value * 1000 / AU_METERS;
    if (unit === "M") return value / AU_METERS;

    return value;
}

function updateTimeline() {
    $("#timeline-progress").style.width = `${state.progress * 100}%`;
    $("#timeline-percent").textContent =
        `${Math.round(state.progress * 100).toString().padStart(2, "0")}%`;
}

function drawChartGrid(ctx, width, height, options = {}) {
    const margin = {
        left: 54,
        right: 22,
        top: 24,
        bottom: 39,
    };

    const plotWidth = Math.max(1, width - margin.left - margin.right);
    const plotHeight = Math.max(1, height - margin.top - margin.bottom);

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, width, height);

    ctx.font = "10px Segoe UI, Arial";
    ctx.textBaseline = "middle";

    for (let i = 0; i <= 4; i++) {
        const y = margin.top + plotHeight * i / 4;

        ctx.beginPath();
        ctx.moveTo(margin.left, y);
        ctx.lineTo(width - margin.right, y);
        ctx.strokeStyle = COLORS.grid;
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.fillStyle = COLORS.muted;
        ctx.textAlign = "right";
        ctx.fillText((1 - i / 4).toFixed(2), margin.left - 10, y);
    }

    for (let i = 0; i <= 4; i++) {
        const x = margin.left + plotWidth * i / 4;

        ctx.beginPath();
        ctx.moveTo(x, margin.top);
        ctx.lineTo(x, height - margin.bottom);
        ctx.strokeStyle = COLORS.grid;
        ctx.stroke();

        ctx.fillStyle = COLORS.muted;
        ctx.textAlign = "center";
        ctx.fillText(String(i), x, height - margin.bottom + 18);
    }

    ctx.fillStyle = COLORS.text;
    ctx.textAlign = "center";
    ctx.fillText(options.xLabel || "TIME", margin.left + plotWidth / 2, height - 8);

    ctx.save();
    ctx.translate(13, margin.top + plotHeight / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillStyle = COLORS.muted;
    ctx.fillText(options.yLabel || "NORMALIZED VALUE", 0, 0);
    ctx.restore();

    return {
        left: margin.left,
        top: margin.top,
        width: plotWidth,
        height: plotHeight,
    };
}

function drawTrajectoryChart() {
    const { context: ctx, width, height } = setupCanvas(trajectoryCanvas);
    const plot = drawChartGrid(ctx, width, height, {
        xLabel: "X [AU]",
        yLabel: "Y [AU]",
    });

    const data = state.simulationData;

    if (data?.trajectory_star?.length && data?.trajectory_planet?.length) {
        drawActualTrajectoryChart(ctx, plot, data);
        return;
    }

    const cx = plot.left + plot.width / 2;
    const cy = plot.top + plot.height / 2;
    const radiusX = plot.width * 0.35;
    const radiusY = plot.height * 0.37;

    ctx.save();
    ctx.translate(cx, cy);

    ctx.strokeStyle = "rgba(214, 165, 80, 0.8)";
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.ellipse(0, 0, radiusX * 0.06, radiusY * 0.06, 0, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = COLORS.blue;
    ctx.lineWidth = 1.7;
    ctx.beginPath();

    for (let i = 0; i <= 220; i++) {
        const angle = (i / 220) * Math.PI * 2;
        const x = Math.cos(angle) * radiusX;
        const y = Math.sin(angle) * radiusY;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.stroke();

    ctx.fillStyle = COLORS.gold;
    ctx.beginPath();
    ctx.arc(0, 0, 4, 0, Math.PI * 2);
    ctx.fill();

    const angle = state.progress * Math.PI * 2;
    const px = Math.cos(angle) * radiusX;
    const py = Math.sin(angle) * radiusY;

    ctx.fillStyle = COLORS.blueBright;
    ctx.beginPath();
    ctx.arc(px, py, 4, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

function drawActualTrajectoryChart(ctx, plot, data) {
    const star = coordinatesInAU(data.trajectory_star);
    const planet = coordinatesInAU(data.trajectory_planet);
    const count = Math.min(star.length, planet.length);

    if (!count) return;

    const bounds = getCoordinateBounds([star, planet]);
    const rect = {
        left: plot.left,
        top: plot.top,
        width: plot.width,
        height: plot.height,
    };

    drawPath(ctx, star, bounds, rect, COLORS.gold, 1.6);
    drawPath(ctx, planet, bounds, rect, COLORS.blue, 1.7);

    const index = Math.min(currentIndex(), count - 1);
    const [sx, sy] = mapPosition(star[index], bounds, rect);
    const [px, py] = mapPosition(planet[index], bounds, rect);

    ctx.fillStyle = COLORS.gold;
    ctx.beginPath();
    ctx.arc(sx, sy, 3.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = COLORS.blueBright;
    ctx.beginPath();
    ctx.arc(px, py, 4, 0, Math.PI * 2);
    ctx.fill();
}

function scalarValue(value) {
    if (Array.isArray(value)) {
        return Math.sqrt(
            value.reduce((sum, item) => sum + Number(item) ** 2, 0)
        );
    }

    return Number(value);
}

function getChartSeries(selector, data) {
    if (!data) return null;

    const mapping = {
        distance: {
            values: data.distance_history,
            label: "DISTANCE [AU]",
            convert: (value) => value / AU_METERS,
        },
        velocity: {
            values: data.velocity_history,
            label: "VELOCITY [KM/S]",
            convert: (value) => value / 1000,
        },
        energy: {
            values: data.energy_history,
            label: "TOTAL ENERGY [J]",
            convert: (value) => value,
        },
        angular: {
            values: data.angular_momentum_history,
            label: "ANGULAR MOMENTUM [KG·M²/S]",
            convert: (value) => value,
        },
    };

    const config = mapping[selector];
    if (!config || !Array.isArray(config.values) || !config.values.length) {
        return null;
    }

    const values = config.values.map((value) => {
        const number = scalarValue(value);
        return config.convert(number);
    });

    if (!values.every(Number.isFinite)) return null;

    return { values, label: config.label };
}

function drawStateChart() {
    const { context: ctx, width, height } = setupCanvas(stateCanvas);
    const selector = $("#state-selector").value;

    const labels = {
        distance: "DISTANCE [AU]",
        velocity: "VELOCITY [KM/S]",
        energy: "TOTAL ENERGY [J]",
        angular: "ANGULAR MOMENTUM [KG·M²/S]",
    };

    $("#state-axis-label").textContent = labels[selector];

    const plot = drawChartGrid(ctx, width, height, {
        xLabel: "TIME",
        yLabel: labels[selector],
    });

    const series = getChartSeries(selector, state.simulationData);

    if (series && series.values.length > 1) {
        drawActualStateChart(ctx, plot, series.values);
        return;
    }

    drawPreviewStateChart(ctx, plot, selector);
}

function drawActualStateChart(ctx, plot, values) {
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min;
    const padding = range > 0 ? range * 0.08 : Math.max(Math.abs(max) * 0.01, 1);

    const low = min - padding;
    const high = max + padding;
    const span = high - low || 1;

    const normalized = values.map((value) => (value - low) / span);

    ctx.strokeStyle = COLORS.line;
    ctx.lineWidth = 1.8;
    ctx.beginPath();

    normalized.forEach((value, index) => {
        const t = index / Math.max(1, normalized.length - 1);
        const x = plot.left + t * plot.width;
        const y = plot.top + (1 - value) * plot.height;

        if (index === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });

    ctx.stroke();

    const index = Math.min(
        Math.floor(state.progress * (normalized.length - 1)),
        normalized.length - 1
    );

    const markerX =
        plot.left + index / Math.max(1, normalized.length - 1) * plot.width;
    const markerY = plot.top + (1 - normalized[index]) * plot.height;

    ctx.fillStyle = COLORS.blueBright;
    ctx.beginPath();
    ctx.arc(markerX, markerY, 3.5, 0, Math.PI * 2);
    ctx.fill();
}

function drawPreviewStateChart(ctx, plot, selector) {
    ctx.strokeStyle = COLORS.line;
    ctx.lineWidth = 1.8;
    ctx.beginPath();

    const getValue = (t) => {
        if (selector === "distance") {
            return 0.5 + 0.5 * Math.cos(t * Math.PI * 2);
        }

        if (selector === "velocity") {
            return 0.5 + 0.32 * Math.sin(t * Math.PI * 2);
        }

        if (selector === "energy") {
            return 0.5 + 0.015 * Math.sin(t * Math.PI * 8);
        }

        return 0.5 + 0.008 * Math.cos(t * Math.PI * 6);
    };

    for (let i = 0; i <= 180; i++) {
        const t = i / 180;
        const x = plot.left + t * plot.width;
        const y = plot.top + (1 - getValue(t)) * plot.height;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.stroke();

    const markerT = state.progress;
    const markerX = plot.left + markerT * plot.width;
    const markerY = plot.top + (1 - getValue(markerT)) * plot.height;

    ctx.fillStyle = COLORS.blueBright;
    ctx.beginPath();
    ctx.arc(markerX, markerY, 3.5, 0, Math.PI * 2);
    ctx.fill();
}

function updateMetrics(data) {
    const values = [
        Number(data.energy_error).toExponential(2),
        Number(data.angular_momentum_error).toExponential(2),
        Number(data.computation_time).toFixed(4),
        Number(data.steps).toLocaleString("en-US"),
    ];

    $$(".metrics-grid .metric-card strong").forEach((element, index) => {
        if (values[index] !== undefined) {
            element.textContent = values[index];
        }
    });
}

function setRunStatus(message, isError = false) {
    const note = $(".panel-note");
    note.textContent = message;
    note.style.color = isError ? "#e58d8d" : "";
}

const INSPECTOR_STYLE = `
    #orbital-data-inspector { margin-top: 22px; padding: 20px; border: 1px solid #26333d; border-radius: 10px; background: #080d12; color: #c7d1d9; }
    #orbital-data-inspector .inspector-heading { display:flex; gap:12px; align-items:center; justify-content:space-between; flex-wrap:wrap; margin-bottom:14px; }
    #orbital-data-inspector h3 { margin:0; font-size:12px; letter-spacing:1.5px; font-weight:600; color:#d6a550; }
    #orbital-data-inspector p { margin:7px 0 0; color:#82919d; font-size:12px; }
    #orbital-data-inspector button { background:#111b23; border:1px solid #354754; border-radius:5px; color:#c7d1d9; padding:8px 11px; cursor:pointer; font:inherit; font-size:11px; letter-spacing:.4px; }
    #orbital-data-inspector button:hover { border-color:#6f9eb5; color:#fff; }
    #orbital-data-inspector .inspector-table-wrap { overflow:auto; max-height:360px; border:1px solid #1b252e; }
    #orbital-data-inspector table { border-collapse:collapse; width:100%; min-width:700px; font-size:12px; font-variant-numeric:tabular-nums; }
    #orbital-data-inspector th, #orbital-data-inspector td { padding:9px 10px; border-bottom:1px solid #1b252e; text-align:right; white-space:nowrap; }
    #orbital-data-inspector th { position:sticky; top:0; background:#101820; color:#91a5b3; font-weight:600; }
    #orbital-data-inspector th:first-child, #orbital-data-inspector td:first-child { text-align:left; }
    #orbital-data-inspector .inspector-empty { padding:22px 10px; color:#82919d; text-align:center; font-size:12px; }
    #orbital-chart-tooltip { position:fixed; z-index:9999; display:none; pointer-events:none; padding:10px 12px; border:1px solid #3b5362; border-radius:6px; background:rgba(5,8,11,.97); color:#d7e0e6; box-shadow:0 8px 24px rgba(0,0,0,.35); font:12px/1.65 ui-monospace, SFMono-Regular, Consolas, monospace; white-space:nowrap; }
    #orbital-chart-tooltip strong { color:#d6a550; font-weight:600; }
`;

function formatExact(value, significantDigits = 10) {
    const number = Number(value);
    if (!Number.isFinite(number)) return "—";
    if (number === 0) return "0";
    return number.toExponential(significantDigits - 1);
}

function inspectorSeries(data) {
    const times = data?.trajectory_times || [];
    const count = times.length;
    const at = (values, index) => {
        if (!Array.isArray(values) || index >= values.length) return NaN;
        return scalarValue(values[index]);
    };
    const distance = data?.distance_history || [];
    const velocity = data?.velocity_history || [];
    const energy = data?.energy_history || [];
    const angular = data?.angular_momentum_history || [];

    return Array.from({ length: count }, (_, index) => ({
        index,
        time: Number(times[index]),
        distance: at(distance, index) / AU_METERS,
        velocity: at(velocity, index) / 1000,
        energy: at(energy, index),
        angular: at(angular, index),
        star: pointXY(data.trajectory_star?.[index]),
        planet: pointXY(data.trajectory_planet?.[index]),
    }));
}

function setupDataInspector() {
    if ($("#orbital-data-inspector")) return;

    const style = document.createElement("style");
    style.textContent = INSPECTOR_STYLE;
    document.head.appendChild(style);

    const analysisPage = $("#analysis");
    if (!analysisPage) return;

    const panel = document.createElement("section");
    panel.id = "orbital-data-inspector";
    panel.innerHTML = `
        <div class="inspector-heading">
            <div>
                <h3>NUMERICAL DATA</h3>
                <p id="inspector-description">Run an experiment to inspect the exact values returned by the physics engine.</p>
            </div>
            <button id="export-data-button" type="button" disabled>EXPORT CSV</button>
        </div>
        <div class="inspector-table-wrap">
            <table>
                <thead><tr>
                    <th>Step</th><th>Time [s]</th><th>Distance [AU]</th>
                    <th>Velocity [km/s]</th><th>Total energy [J]</th>
                    <th>Angular momentum [kg·m²/s]</th>
                </tr></thead>
                <tbody id="inspector-table-body">
                    <tr><td colspan="6" class="inspector-empty">No simulation data available.</td></tr>
                </tbody>
            </table>
        </div>
        <p id="inspector-table-note">Values are taken from the simulation response. Displayed rows are sampled for performance; CSV export includes every returned step.</p>
    `;
    analysisPage.appendChild(panel);

    const tooltip = document.createElement("div");
    tooltip.id = "orbital-chart-tooltip";
    document.body.appendChild(tooltip);

    $("#export-data-button").addEventListener("click", exportSimulationCSV);
}

function updateDataInspector(data) {
    setupDataInspector();
    const rows = inspectorSeries(data);
    const body = $("#inspector-table-body");
    const button = $("#export-data-button");
    const description = $("#inspector-description");

    if (!body) return;

    if (!rows.length) {
        body.innerHTML = '<tr><td colspan="6" class="inspector-empty">No simulation data available.</td></tr>';
        if (button) button.disabled = true;
        return;
    }

    const maxVisibleRows = 250;
    const stride = Math.max(1, Math.ceil(rows.length / maxVisibleRows));
    const visible = rows.filter(
        (row, index) => index % stride === 0 || index === rows.length - 1
    );

    body.innerHTML = visible.map((row) => `
        <tr>
            <td>${row.index}</td>
            <td>${formatExact(row.time)}</td>
            <td>${formatExact(row.distance)}</td>
            <td>${formatExact(row.velocity)}</td>
            <td>${formatExact(row.energy)}</td>
            <td>${formatExact(row.angular)}</td>
        </tr>
    `).join("");

    if (button) button.disabled = false;

    if (description) {
        description.textContent =
            `${rows.length.toLocaleString("en-US")} integration samples · showing ${visible.length.toLocaleString("en-US")} rows · full precision data available in CSV.`;
    }
}

function exportSimulationCSV() {
    const data = state.simulationData;
    if (!data?.trajectory_times?.length) return;

    const rows = inspectorSeries(data);

    const csvEscape = (value) => {
        if (Array.isArray(value)) return `"${value.join(";")}"`;

        const text = String(value ?? "");
        return /[",\r\n]/.test(text)
            ? `"${text.replace(/"/g, '""')}"`
            : text;
    };

    const header = [
        "step",
        "time_s",
        "distance_AU",
        "velocity_km_s",
        "total_energy_J",
        "angular_momentum_kg_m2_s",
        "star_x_m",
        "star_y_m",
        "planet_x_m",
        "planet_y_m",
    ];

    const lines = [header.join(",")];

    for (const row of rows) {
        const star = data.trajectory_star?.[row.index] || [];
        const planet = data.trajectory_planet?.[row.index] || [];

        lines.push([
            row.index,
            row.time,
            row.distance,
            row.velocity,
            row.energy,
            row.angular,
            star[0],
            star[1],
            planet[0],
            planet[1],
        ].map(csvEscape).join(","));
    }

    const blob = new Blob(["\uFEFF", lines.join("\r\n")], {
        type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "orbital-simulation-data.csv";

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

function showChartTooltip(canvas, event) {
    const data = state.simulationData;
    const tooltip = $("#orbital-chart-tooltip");

    if (!data || !tooltip) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const indexMax = Math.max(0, (data.trajectory_times?.length || 1) - 1);

    let index;

    if (canvas === stateCanvas) {
        const plotLeft = 54;
        const plotRight = 22;
        const plotWidth = Math.max(1, rect.width - plotLeft - plotRight);
        const t = Math.max(0, Math.min(1, (x - plotLeft) / plotWidth));

        index = Math.round(t * indexMax);
    } else {
        index = currentIndex();
    }

    const at = (values, sampleIndex) => {
        if (!Array.isArray(values) || sampleIndex >= values.length) {
            return NaN;
        }

        return scalarValue(values[sampleIndex]);
    };

    const row = {
        index,
        time: Number(data.trajectory_times?.[index]),
        distance: at(data.distance_history, index) / AU_METERS,
        velocity: at(data.velocity_history, index) / 1000,
        energy: at(data.energy_history, index),
        angular: at(data.angular_momentum_history, index),
    };

    if (!Number.isFinite(row.time)) return;

    let details = "";

    if (canvas === trajectoryCanvas || canvas === orbitCanvas) {
        const star = data.trajectory_star?.[index] || [];
        const planet = data.trajectory_planet?.[index] || [];

        details = `
            <div>Star X/Y: ${formatExact(star[0])} / ${formatExact(star[1])} m</div>
            <div>Planet X/Y: ${formatExact(planet[0])} / ${formatExact(planet[1])} m</div>`;
    } else {
        const selector = $("#state-selector")?.value || "distance";

        const labels = {
            distance: ["Distance", row.distance, "AU"],
            velocity: ["Velocity", row.velocity, "km/s"],
            energy: ["Total energy", row.energy, "J"],
            angular: ["Angular momentum", row.angular, "kg·m²/s"],
        };

        const selected = labels[selector] || labels.distance;
        details = `<div>${selected[0]}: ${formatExact(selected[1])} ${selected[2]}</div>`;
    }

    tooltip.innerHTML = `<strong>STEP ${row.index}</strong>
        <div>Time: ${formatExact(row.time)} s</div>
        <div>Distance: ${formatExact(row.distance)} AU</div>
        <div>Velocity: ${formatExact(row.velocity)} km/s</div>
        ${details}`;

    tooltip.style.display = "block";

    const left = Math.min(
        event.clientX + 14,
        window.innerWidth - tooltip.offsetWidth - 12
    );

    const top = Math.min(
        event.clientY + 14,
        window.innerHeight - tooltip.offsetHeight - 12
    );

    tooltip.style.left = `${Math.max(8, left)}px`;
    tooltip.style.top = `${Math.max(8, top)}px`;
}

function installChartTooltips() {
    [stateCanvas, orbitCanvas].forEach((canvas) => {
        canvas.addEventListener("pointermove", (event) => {
            showChartTooltip(canvas, event);
        });

        canvas.addEventListener("pointerleave", () => {
            const tooltip = $("#orbital-chart-tooltip");
            if (tooltip) tooltip.style.display = "none";
        });
    });
}

function renderAll() {
    drawOrbitScene();
    drawTrajectoryChart();
    drawStateChart();
}

function animationFrame(timestamp) {
    if (state.lastFrame === 0) state.lastFrame = timestamp;

    const delta = Math.min((timestamp - state.lastFrame) / 1000, 0.1);
    state.lastFrame = timestamp;

    if (state.playing) {
        state.progress += delta * state.speed / 50;

        if (state.progress >= 1) {
            state.progress = 0;
        }

        state.elapsed += delta;
        renderAll();
    }

    requestAnimationFrame(animationFrame);
}

function resetAnimation() {
    state.progress = 0;
    state.elapsed = 0;
    renderAll();
}

function selectTab(tabName) {
    $$(".tab").forEach((tab) => {
        const selected = tab.dataset.tab === tabName;

        tab.classList.toggle("active", selected);
        tab.setAttribute("aria-selected", String(selected));
    });

    $$(".page").forEach((page) => {
        page.classList.toggle("active", page.id === tabName);
    });

    requestAnimationFrame(renderAll);
}

async function runExperiment() {
    if (state.running) return;

    const button = $("#run-button");
    const buttonLabel = button.querySelector("span");
    const originalLabel = buttonLabel?.textContent || "RUN EXPERIMENT";

    const requestData = {
        star_mass: Number($("#star-mass").value),
        star_mass_unit: $("#star-mass-unit").value,
        planet_mass: Number($("#planet-mass").value),
        planet_mass_unit: $("#planet-mass-unit").value,
        distance: Number($("#distance").value),
        distance_unit: $("#distance-unit").value,
        velocity: Number($("#velocity").value),
        velocity_unit: $("#velocity-unit").value,
        duration: Number($("#duration").value),
        duration_unit: $("#duration-unit").value,
        precision: $("#precision").value,
    };

    if (
        !Number.isFinite(requestData.star_mass) ||
        requestData.star_mass <= 0 ||
        !Number.isFinite(requestData.planet_mass) ||
        requestData.planet_mass <= 0 ||
        !Number.isFinite(requestData.distance) ||
        requestData.distance <= 0 ||
        !Number.isFinite(requestData.velocity) ||
        requestData.velocity < 0 ||
        !Number.isFinite(requestData.duration) ||
        requestData.duration <= 0
    ) {
        setRunStatus("Check the experiment parameters and try again.", true);
        return;
    }

    state.running = true;
    button.disabled = true;

    if (buttonLabel) {
        buttonLabel.textContent = "RUNNING SIMULATION...";
    }

    setRunStatus("Computing gravitational trajectories...");

    try {
        const response = await fetch("/api/simulate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify(requestData),
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "The simulation request was rejected.";

            throw new Error(detail);
        }

        if (
            !Array.isArray(data.trajectory_star) ||
            !Array.isArray(data.trajectory_planet) ||
            !Array.isArray(data.trajectory_times) ||
            data.trajectory_times.length === 0
        ) {
            throw new Error("The backend returned incomplete trajectory data.");
        }

        state.simulationData = data;
        state.progress = 0;
        state.elapsed = 0;
        state.playing = true;

        $("#play-button").textContent = "Ⅱ";
        $("#play-button").setAttribute("aria-label", "Pause animation");

        updateMetrics(data);
        updateDataInspector(data);
        renderAll();

        const playButton = $("#play-button");
        if (playButton) playButton.disabled = false;

        setRunStatus(
            `SIMULATION COMPLETE · ${Number(data.steps).toLocaleString("en-US")} STEPS`
        );
    } catch (error) {
        console.error("ORBITAL simulation failed:", error);

        setRunStatus(
            error instanceof TypeError
                ? "Could not connect to the simulation server. Check that the backend is running."
                : `Simulation failed: ${error.message}`,
            true
        );
    } finally {
        state.running = false;
        button.disabled = false;

        if (buttonLabel) {
            buttonLabel.textContent = originalLabel;
        }
    }
}

$$(".tab").forEach((tab) => {
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-selected", String(tab.classList.contains("active")));

    tab.addEventListener("click", () => selectTab(tab.dataset.tab));
});

$("#play-button").addEventListener("click", () => {
    state.playing = !state.playing;
    $("#play-button").textContent = state.playing ? "Ⅱ" : "▶";

    $("#play-button").setAttribute(
        "aria-label",
        state.playing ? "Pause animation" : "Resume animation"
    );
});

$("#reset-button").addEventListener("click", resetAnimation);

$("#speed").addEventListener("change", (event) => {
    state.speed = Number(event.target.value) || 4;
    $("#speed-label").textContent = `${state.speed}× SPEED`;
});

$("#state-selector").addEventListener("change", drawStateChart);
$("#run-button").addEventListener("click", runExperiment);

[
    "#star-mass",
    "#star-mass-unit",
    "#planet-mass",
    "#planet-mass-unit",
    "#distance",
    "#distance-unit",
    "#velocity",
    "#velocity-unit",
    "#duration",
    "#duration-unit",
    "#precision",
].forEach((selector) => {
    $(selector).addEventListener("change", () => {
        if (!state.simulationData) renderAll();
    });
});

window.addEventListener("resize", renderAll);

if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(() => renderAll());

    [orbitCanvas, trajectoryCanvas, stateCanvas].forEach((canvas) => {
        observer.observe(canvas.parentElement);
    });
}

setupDataInspector();
installChartTooltips();
renderAll();
requestAnimationFrame(animationFrame);