def get_results_for_dimension(package, dimension):
    results = package["results"]
    selected = [
        item for item in results
        if item.get("result_type") == "comparative_group_ranking"
        and item.get("result_category") == dimension
        and item.get("metric_name") == "total_downtime_minutes"
    ]
    selected.sort(key=lambda item: (item["priority_rank"], -item["result_value"]))
    return selected[:25]


def get_result_by_id(package, result_id):
    for item in package["results"]:
        if item.get("result_id") == result_id:
            return item
    return None


def get_priority_items(package):
    summary = package["summary"]
    return summary.get("priority_items", [])[:25]
