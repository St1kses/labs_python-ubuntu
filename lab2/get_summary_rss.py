UNITS = ["B", "KiB", "MiB", "GiB", "TiB"]
def to_human_readable(num_bytes: float) -> str:
    unit_index = 0
    value = float(num_bytes)
    while value >= 1024 and unit_index < len(UNITS) - 1:
        value /= 1024
        unit_index += 1
    return f"{value:.2f} {UNITS[unit_index]}"
def get_summary_rss(ps_output_path: str) -> str:
    with open(ps_output_path, "r", encoding="utf-8") as output_file:
        lines = output_file.readlines()[1:]
    total_kib = 0
    for line in lines:
        columns = line.split()
        if len(columns) < 6:
            continue
        try:
            total_kib += int(columns[5])
        except ValueError:
            continue
    total_bytes = total_kib * 1024
    return to_human_readable(total_bytes)
if __name__ == "__main__":
    PS_OUTPUT_FILE = "output_file.txt"
    print(get_summary_rss(PS_OUTPUT_FILE))
