import sys
def get_mean_size(lines) -> float:
    file_sizes = []
    for line in lines[1:]:
        columns = line.split()
        if len(columns) < 9:
            continue
        try:
            size = int(columns[4])
            file_sizes.append(size)
        except ValueError:
            continue
    if not file_sizes:
        return 0.0
    return sum(file_sizes) / len(file_sizes)
if __name__ == "__main__":
    input_lines = sys.stdin.readlines()
    mean_size = get_mean_size(input_lines)
    print(f"{mean_size:.2f}")
