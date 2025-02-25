import copy
from bs4 import BeautifulSoup


def table_span_normalize(html):
    if isinstance(html, str):
        soup = BeautifulSoup(html, 'html.parser')
        if soup is None:
            raise ValueError('Can\'t build DOM tree')
    elif not isinstance(html, BeautifulSoup):
        raise ValueError(f'Unsupported input type {type(html)}')
    else:
        soup = html

    for table in reversed(soup('table')):
        rows = []
        for thead in table('thead', recursive=False):
            rows.extend(thead('tr', recursive=False))
        for tbody_tr in table(['tbody', 'tr'], recursive=False):
            if 'tr' == tbody_tr.name:
                rows.append(tbody_tr)
            else:
                rows.extend(tbody_tr('tr', recursive=False))
        for tfoot in table('tfoot', recursive=False):
            rows.extend(tfoot('tr', recursive=False))

        rows_ = [[] for _ in range(len(rows))]
        for r, row in enumerate(rows):
            for cell in row(['th', 'td'], recursive=False):
                rowspan = int(cell.get('rowspan', 1))
                rowspan = len(rows) if 0 == rowspan else rowspan
                rowspan = min(rowspan, len(rows) - r)
                del cell['rowspan']

                colspan = int(cell.get('colspan', 1))
                colspan = 1 if 0 == r and len(rows) == rowspan else colspan
                colspan = max(colspan, 1)
                del cell['colspan']

                for rs in range(r, len(rows)):
                    rows_[rs].extend([None] * colspan)

                ix = rows_[r].index(None)

                for rs in range(r, r + rowspan):
                    for cs in range(ix, ix + colspan):
                        if rows_[rs][cs] is not None:
                            colspan = min(colspan, cs - ix)

                for rs in range(r, r + rowspan):
                    for cs in range(ix, ix + colspan):
                        cell_ = copy.deepcopy(cell)
                        rows_[rs][cs] = cell_

        maxcol = 1
        for row in rows_:
            for i, cell in enumerate(row):
                if cell is None:
                    continue
                maxcol = max(maxcol, i + 1)
        for r, row_ in enumerate(rows_):
            row_ = row_[:maxcol] + [None] * (maxcol - len(row_))
            row_ = [soup.new_tag('td') if c is None else c for c in row_]
            rows_[r] = row_

        drop = []
        for i in range(maxcol - 1):
            same = []
            for row_ in rows_:
                same.append(str(row_[i]) == str(row_[i + 1]))
            if same and all(same):
                drop.append(i + 1)
        for row_ in rows_:
            for i in drop[::-1]:
                del row_[i]


        for row, row_ in zip(rows, rows_):
            row.clear()
            for cell_ in row_:
                row.append(cell_)

    if isinstance(html, str):
        html = str(soup).strip()
    else:
        html = soup

    return html
