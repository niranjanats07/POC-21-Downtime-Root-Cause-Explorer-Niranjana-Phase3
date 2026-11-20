"use client";

import ReactECharts from "echarts-for-react";

type Incident = {
  incident_id: string;
  machine_id: string;
  failure_frequency: number;
  downtime_minutes: number;
};

type ScatterTooltipParams = {
  data: unknown;
};

type Props = {
  data: Incident[];
};

export default function ScatterChart({ data }: Props) {
  if (!data.length) {
    return (
      <div
        className="flex min-h-[300px] items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-900/40 px-6 text-center text-sm text-slate-400"
        role="status"
      >
        No incident data is available for the selected filters.
      </div>
    );
  }

  const option = {
    animationDuration: 500,
    tooltip: {
      trigger: "item",
      confine: true,
      formatter: (params: ScatterTooltipParams) => {
        if (!Array.isArray(params.data)) {
          return "";
        }

        const item = params.data as [
          number,
          number,
          string,
          string
        ];

        return `
          <strong>${item[2]}</strong><br/>
          Machine: ${item[3]}<br/>
          Failure Frequency: ${item[0]}<br/>
          Downtime: ${item[1]} minutes
        `;
      },
    },
    grid: {
      left: "10%",
      right: "5%",
      top: "12%",
      bottom: "18%",
      containLabel: true,
    },
    xAxis: {
      type: "value",
      name: "Failure Frequency",
      nameLocation: "middle",
      nameGap: 35,
      axisLabel: {
        color: "#cbd5e1",
      },
      nameTextStyle: {
        color: "#94a3b8",
      },
      axisLine: {
        lineStyle: {
          color: "#475569",
        },
      },
      splitLine: {
        lineStyle: {
          color: "#334155",
        },
      },
    },
    yAxis: {
      type: "value",
      name: "Downtime (minutes)",
      nameLocation: "middle",
      nameGap: 50,
      axisLabel: {
        color: "#cbd5e1",
      },
      nameTextStyle: {
        color: "#94a3b8",
      },
      axisLine: {
        lineStyle: {
          color: "#475569",
        },
      },
      splitLine: {
        lineStyle: {
          color: "#334155",
        },
      },
    },
    series: [
      {
        name: "Downtime Incidents",
        type: "scatter",
        symbolSize: 14,
        data: data.map((item) => [
          Number(item.failure_frequency),
          Number(item.downtime_minutes),
          item.incident_id,
          item.machine_id,
        ]),
        itemStyle: {
          color: "#a78bfa",
          borderColor: "#c4b5fd",
          borderWidth: 1,
        },
        emphasis: {
          focus: "series",
          itemStyle: {
            borderColor: "#ffffff",
            borderWidth: 2,
          },
        },
      },
    ],
  };

  return (
    <div
      className="w-full min-w-0"
      role="img"
      aria-label="Scatter chart comparing incident failure frequency and downtime duration"
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
