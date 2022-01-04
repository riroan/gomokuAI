def index2coordinate(index, size):
    row = index // size
    col = index % size
    return int(row), int(col)