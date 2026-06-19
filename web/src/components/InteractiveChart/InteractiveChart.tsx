import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js-basic-dist-min";
import type { Data, Layout } from "plotly.js";
import type { DerivativeModel } from "../../domain/derivativeModel";
import styles from "./InteractiveChart.module.scss";

const Plot = createPlotlyComponent(Plotly);

type Props = {
  model: DerivativeModel;
};

export function InteractiveChart({ model }: Props) {
  const xRange = [model.xs[0], model.xs[model.xs.length - 1]];
  const data: Data[] = model.series.map((series) => ({
    x: model.xs,
    y: series.values.map((value) => (Number.isFinite(value) ? value : null)),
    type: "scatter",
    mode: "lines",
    name: series.name,
    line: {
      color: series.color,
      width: series.strokeWidth ?? 2,
      dash: series.dashed ? "dash" : "solid",
    },
    hovertemplate: "x=%{x:.4f}<br>y=%{y:.6f}<extra>%{fullData.name}</extra>",
  }));

  const layout: Partial<Layout> = {
    autosize: true,
    dragmode: "zoom",
    hovermode: "x unified",
    margin: { l: 58, r: 24, t: 10, b: 54 },
    paper_bgcolor: "rgba(255,255,255,0)",
    plot_bgcolor: "rgba(247,250,250,0.72)",
    font: {
      family: "Inter, system-ui, sans-serif",
      color: "#47575e",
      size: 12,
    },
    xaxis: {
      range: xRange,
      zeroline: false,
      gridcolor: "#e4ecee",
      linecolor: "#d8e0e2",
      tickformat: ".3~f",
      title: { text: "x" },
    },
    yaxis: {
      zeroline: false,
      gridcolor: "#dfe8ea",
      linecolor: "#d8e0e2",
      tickformat: ".3~f",
      title: { text: "значение" },
    },
    legend: {
      orientation: "h",
      x: 0,
      y: -0.18,
      xanchor: "left",
      yanchor: "top",
      font: { size: 12 },
    },
  };

  return (
    <div className={styles.chart}>
      <Plot
        data={data}
        layout={layout}
        config={{
          displaylogo: false,
          responsive: true,
          scrollZoom: true,
          modeBarButtonsToRemove: ["lasso2d", "select2d"],
          toImageButtonOptions: {
            format: "png",
            filename: "fractional-derivative-chart",
            height: 900,
            width: 1400,
            scale: 1,
          },
        }}
        className={styles.plot}
        useResizeHandler
      />
    </div>
  );
}
