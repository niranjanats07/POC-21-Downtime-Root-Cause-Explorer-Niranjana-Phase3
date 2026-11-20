"use client";

import ReactECharts from "echarts-for-react";

type Cause = {
  root_cause: string;
  downtime_minutes: number;
  cumulative_percentage: number;
};

type Props = {
  data: Cause[];
};

export default function ParetoChart({ data }: Props) {
  if (!data.length) {
    return (
      <div
        className="flex min-h-[300px] items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-900/40 px-6 text-center text-sm text-slate-400"
        role="status"
      >
        No cause data is available for the selected filters.
      </div>
    );
  }

  const option = {
    animationDuration: 500,
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    legend: {
      data: ["Downtime", "Cumulative Percentage"],
      bottom: 0,
      textStyle: {
        color: "#cbd5e1",
      },
    },
    grid: {
      left: "5%",
      right: "8%",
      top: "12%",
      bottom: "22%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: data.map((item) => item.root_cause),
      axisLabel: {
        color: "#cbd5e1",
        rotate: 20,
        interval: "auto",
        hideOverlap: true,
        width: 110,
        overflow: "truncate",
      },
      axisLine: {
        lineStyle: {
          color: "#475569",
        },
      },
    },
    yAxis: [
      {
        type: "value",
        name: "Downtime (minutes)",
        nameTextStyle: {
          color: "#94a3b8",
        },
        axisLabel: {
          color: "#cbd5e1",
        },
        splitLine: {
          lineStyle: {
            color: "#334155",
          },
        },
      },
      {
        type: "value",
        name: "Cumulative (%)",
        min: 0,
        max: 100,
        nameTextStyle: {
          color: "#94a3b8",
        },
        axisLabel: {
          color: "#cbd5e1",
          formatter: "{value}%",
        },
        splitLine: {
          show: false,
        },
      },
    ],
    series: [
      {
        name: "Downtime",
        type: "bar",
        data: data.map((item) => item.downtime_minutes),
        itemStyle: {
          color: "#22d3ee",
          borderRadius: [5, 5, 0, 0],
        },
        barMaxWidth: 48,
        emphasis: {
          focus: "series",
        },
      },
      {
        name: "Cumulative Percentage",
        type: "line",
        yAxisIndex: 1,
        data: data.map((item) => item.cumulative_percentage),
        smooth: true,
        symbolSize: 7,
        lineStyle: {
          width: 3,
          color: "#f59e0b",
        },
        itemStyle: {
          color: "#f59e0b",
        },
        emphasis: {
          focus: "series",
        },
      },
    ],
  };

  return (
    <div
      className="w-full min-w-0"
      role="img"
      aria-label="Pareto chart showing downtime by root cause and cumulative percentage"
    >
      <ReactECharts
        option={option}
        style={{ height: "350px", width: "100%" }}
        notMerge={true}
        lazyUpdate={true}
        opts={{ renderer: "canvas" }}
      />
    </div>
  );
}
