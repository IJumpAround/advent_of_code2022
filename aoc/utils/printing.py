def print_matrix(mtx, headers=True, row_range=None, col_range=None):
    if row_range is None:
        row_range = (0, len(mtx))
    if col_range is None:
        col_range = (0, len(mtx[0]))

    h = [str(_) for _ in range(max(len(mtx), len(mtx[0])))]
    w = max(map(len, h))

    h_str = "".join([f'{_:<{w}}  ' for _ in h[col_range[0]:col_range[1]]])

    if headers:
        print('   | ' + h_str)
    for i, row in enumerate(mtx):

        if row_range[0] <= i <= row_range[1]:
            line = "".join([f"{_:<{w}}  " for _ in row[col_range[0]:col_range[1]]])
            if headers:
                line = f'{i:<3}| ' + line
            print(line)