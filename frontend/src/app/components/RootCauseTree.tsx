"use client";

import ReactECharts from "echarts-for-react";

type RootCause = {
  root_cause: string;
  sub_cause: string;
  downtime_minutes: number;
};

type Props = {
  data: RootCause[];
};

export default function RootCauseTree({ data }: Props) {
  if (!data.length) {
    return (
      <div
        className="flex min-h-[300px] items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-900/40 px-6 text-center text-sm text-slate-400"
        role="status"
      >
        No root-cause evidence is available for the selected filters.
      </div>
    );
  }

  const groupedData = new Map<string, RootCause[]>();

  data.forEach((item) => {
    if (!groupedData.has(item.root_cause)) {
      groupedData.set(item.root_cause, []);
    }

    groupedData.get(item.root_cause)!.push(item);
  });

  const treeData = Array.from(groupedData.entries()).map(
    ([rootCause, subCauses]) => ({
      name: rootCause,
      children: subCauses.map((item) => ({
        name: `${item.sub_cause} (${item.downtime_minutes} min)`,
        value: item.downtime_minutes,
      })),
    })
  );

  const option = {
    animationDuration: 500,
    tooltip: {
      trigger: "item",
      triggerOn: "mousemove",
      confine: true,
      formatter: (params: { data?: { name?: string; value?: number } }) => {
        const name = params.data?.name ?? "Root cause";
        const value = params.data?.value;

        return value === undefined
          ? `<strong>${name}</strong>`
          : `<strong>${name}</strong><br/>Downtime: ${value} minutes`;
      },
    },
    series: [
      {
        type: "tree",
        data: treeData,
        top: "5%",
        left: "14%",
        bottom: "5%",
        right: "22%",
        layout: "orthogonal",
        orient: "LR",
        symbol: "roundRect",
        symbolSize: 10,
        edgeShape: "polyline",
        edgeForkPosition: "50%",
        expandAndCollapse: true,
        initialTreeDepth: -1,
        animationDuration: 500,
        animationDurationUpdate: 750,
        roam: true,
        label: {
          position: "left",
          verticalAlign: "middle",
          align: "right",
          color: "#e2e8f0",
          fontSize: 12,
          width: 150,
          overflow: "truncate",
        },
        leaves: {
          label: {
            position: "right",
            verticalAlign: "middle",
            align: "left",
            color: "#67e8f9",
            fontSize: 11,
            width: 190,
            overflow: "truncate",
          },
        },
        lineStyle: {
          color: "#64748b",
          width: 2,
        },
        itemStyle: {
          color: "#6366f1",
          borderColor: "#a5b4fc",
        },
        emphasis: {
          focus: "descendant",
        },
      },
    ],
  };

  return (
    <div
      className="w-full min-w-0 overflow-hidden"
      role="img"
      aria-label="Root-cause tree grouping contributing sub-causes and their observed downtime"
    >
      <ReactECharts
        option={option}
        style={{ height: "480px", width: "100%" }}
        notMerge={true}
        lazyUpdate={true}
        opts={{ renderer: "canvas" }}
      />
    </div>
  );
}
