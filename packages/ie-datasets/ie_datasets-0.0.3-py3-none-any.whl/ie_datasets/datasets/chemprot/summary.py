from ie_datasets.datasets.chemprot.load import load_units


def get_summary() -> str:
    lines: list[str] = []

    for split in ("sample", "train", "validation", "test"):
        units = list(load_units(split=split))

        lines.append("=" * 80)
        lines.append(f"{split.upper()}: {len(units)} units")

        L = max(len(str(unit.pmid)) for unit in units)
        for unit in units:
            lines.append(f"  {str(unit.pmid).rjust(L)}: {unit.num_chars:4d} chars, {unit.num_entity_mentions:3d} entity mentions, {unit.num_relations:2d} relations")

    return "\n".join(lines)


__all__ = [
    "get_summary"
]
