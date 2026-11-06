/* Renderização dos agregados incorporados pelo gerador Python. */
document.addEventListener("DOMContentLoaded", () => {
  const figuras = [...document.querySelectorAll(".visualizacao")];
  const aviso = document.querySelector(".aviso-graficos");
  if (typeof Chart === "undefined") {
    aviso.hidden = false;
    figuras.forEach(figura => { figura.querySelector(".dados-grafico").open = true; });
    return;
  }

  document.body.classList.add("graficos-prontos");
  Chart.defaults.color = "#655b4e";
  Chart.defaults.font.family = "system-ui, sans-serif";
  Chart.defaults.font.size = 12;
  const decimal = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 2 });
  const medida = (valor, tipo) => {
    if (valor === null) return "Sem observações";
    if (tipo === "decimal") return new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 4 }).format(valor);
    return decimal.format(valor) + (tipo === "percentual" ? "%" : "");
  };
  const quebrarRotulo = (rotulo, limite) => {
    const linhas = [""];
    for (const palavra of String(rotulo).split(" ")) {
      const atual = linhas.length - 1;
      if (linhas[atual] && linhas[atual].length + palavra.length > limite) linhas.push(palavra);
      else linhas[atual] += (linhas[atual] ? " " : "") + palavra;
    }
    return linhas;
  };

  const referencia = {
    id: "referencia",
    afterDraw(chart, args, options) {
      if (options.value === null || options.value === undefined) return;
      const { ctx, chartArea, scales } = chart;
      const horizontal = chart.options.indexAxis === "y";
      const posicao = (horizontal ? scales.x : scales.y).getPixelForValue(options.value);
      ctx.save();
      ctx.strokeStyle = "#655b4e";
      ctx.setLineDash([5, 4]);
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(horizontal ? posicao : chartArea.left, horizontal ? chartArea.top : posicao);
      ctx.lineTo(horizontal ? posicao : chartArea.right, horizontal ? chartArea.bottom : posicao);
      ctx.stroke();
      ctx.restore();
    },
  };

  function renderizar(figura) {
    const canvas = figura.querySelector("canvas");
    // Details fechados não têm dimensões. A criação ocorre quando forem abertos.
    if (figura.closest("details:not([open])") || !canvas.getClientRects().length) return;
    const existente = Chart.getChart(canvas);
    if (existente) {
      existente.resize();
      return;
    }
    const config = JSON.parse(figura.querySelector(".chart-data").textContent);
    const horizontal = config.horizontal ?? false;
    const valor = {
      beginAtZero: true,
      max: config.max,
      grid: { color: "#e8e1d5" },
      border: { display: false },
      ticks: { callback: v => medida(v, config.metric), maxTicksLimit: 6 },
    };
    const categoria = {
      grid: { display: false },
      border: { display: false },
      ticks: {
        autoSkip: !horizontal,
        maxTicksLimit: horizontal ? undefined : 7,
        maxRotation: 0,
        callback: function (v) {
          return quebrarRotulo(this.getLabelForValue(v), horizontal ? 18 : 12);
        },
      },
    };
    if (config.axisTitle) categoria.title = { display: true, text: config.axisTitle };
    const scales = horizontal ? { x: valor, y: categoria } : { x: categoria, y: valor };
    if (config.secondary) {
      scales.y.title = { display: true, text: "Clientes" };
      scales.y1 = {
        position: "right", min: 0, max: 100,
        grid: { drawOnChartArea: false }, border: { display: false },
        ticks: { callback: v => medida(v, "percentual"), maxTicksLimit: 6 },
      };
    }
    new Chart(canvas, {
      type: config.type,
      data: config.data,
      plugins: [referencia],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: horizontal ? "y" : "x",
        locale: "pt-BR",
        resizeDelay: 80,
        animation: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? false : { duration: 350 },
        interaction: { mode: config.type === "line" ? "index" : "nearest", intersect: false },
        plugins: {
          referencia: { value: config.reference },
          legend: {
            display: config.legend ?? false, position: "bottom",
            labels: { usePointStyle: true, boxWidth: 9, padding: 16 },
          },
          tooltip: {
            backgroundColor: "#171717", titleColor: "#F4F0E7", bodyColor: "#F4F0E7",
            padding: 12, displayColors: !!config.legend,
            callbacks: {
              title: items => quebrarRotulo(items[0]?.label ?? "", 32),
              label: context => {
                const tipo = context.dataset.yAxisID === "y1" ? "percentual" : config.metric;
                const numero = horizontal ? context.parsed.x : context.parsed.y;
                return context.dataset.label + " · " + medida(numero, tipo);
              },
              afterLabel: context => context.dataset.details?.[context.dataIndex] ?? "",
            },
          },
        },
        scales,
      },
    });
  }

  figuras.forEach(renderizar);
  document.querySelectorAll("details").forEach(detalhe => {
    detalhe.addEventListener("toggle", () => {
      if (detalhe.open) requestAnimationFrame(() => detalhe.querySelectorAll(".visualizacao").forEach(renderizar));
    });
  });
});
