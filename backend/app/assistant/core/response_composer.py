def _format_number(value):
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    return str(value)


def compose_answer(intent, payload):
    if intent == "get_summary":
        summary = payload["summary"]
        metrics = summary.get("overall_metrics", {})
        return (
            f"The approved synthetic dataset contains "
            f"{metrics.get('incident_count', 'N/A')} incidents and "
            f"{_format_number(metrics.get('total_downtime_minutes', 'N/A'))} "
            f"observed downtime minutes."
        )

    if intent == "list_priority_items":
        results = payload.get("results", [])
        if not results:
            return "No approved priority results were found."
        first = results[0]
        return (
            f"{first.get('group_key')} ranks first with "
            f"{_format_number(first.get('result_value'))} "
            f"{first.get('result_unit')} of observed downtime "
            f"({len(results)} ranked groups available)."
        )

    if intent in ("compare_groups", "describe_segment"):
        results = payload.get("results", [])
        dimension = payload.get("dimension", "selected")
        if not results:
            return f"No approved comparative results were found for {dimension}."

        ordered = sorted(
            results,
            key=lambda item: (
                item.get("priority_rank", 999999),
                item.get("result_id", ""),
            ),
        )
        lines = [
            f"{dimension.replace('_', ' ').title()} comparison by observed downtime:"
        ]
        for item in ordered:
            lines.append(
                f"#{item.get('priority_rank')} {item.get('group_key')}: "
                f"{_format_number(item.get('result_value'))} "
                f"{item.get('result_unit')} "
                f"({item.get('result_id')})."
            )
        return " ".join(lines)

    if intent == "explain_result":
        result = payload.get("result")
        return result.get("finding") if result else None

    if intent == "explain_method":
        return (
            f"Approved track: {payload.get('approved_track')}. "
            f"Method version: {payload.get('method_version')}. "
            f"{payload.get('primary_analytical_question') or ''}"
        ).strip()

    if intent == "explain_limitation":
        limitations = payload.get("limitations", [])
        if limitations:
            text = " ".join(str(item) for item in limitations)
            text = text.replace("rankingstability", "ranking stability")
            return "Approved analytical limitations: " + text
        return (
            "The results use synthetic data and are descriptive demonstration "
            "outputs. They do not establish causation, predict future failures, "
            "or demonstrate actual industrial performance."
        )

    if intent == "get_data_freshness":
        metadata = payload["metadata"]
        return (
            f"Data version {metadata.get('data_version')}; "
            f"method version {metadata.get('method_version')}; "
            f"generated at {metadata.get('generated_at')}."
        )

    return None
