from ie_datasets.datasets.scierc.load import load_units


def get_summary() -> str:
    lines: list[str] = []

    for split in ("train", "dev", "test"):
        units = list(load_units(split=split))

        lines.append("=" * 80)
        lines.append(f"{split.upper()}: {len(units)} units")

        L = max(len(unit.doc_key) for unit in units)
        for unit in units:
            lines.append(f"  {unit.doc_key.rjust(L)}: {unit.num_tokens:3d} tokens, {unit.num_sentences:2d} sentences, {unit.num_entity_mentions:2d} entity mentions, {unit.num_relations:2d} relations")

    return "\n".join(lines)
