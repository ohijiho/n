import sys
import os
from itertools import count


def fetch_problem(n):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    url = f'https://www.acmicpc.net/problem/{n}'

    stderr = sys.stderr
    devnull = open(os.devnull, 'w')
    sys.stderr = devnull

    import requests

    sys.stderr = stderr
    devnull.close()

    res = requests.get(url, headers={'User-Agent': ua})
    if not res.ok:
        raise Error('fetching {url} failed: {res.status_code} {res.reason}')
    return res.text


def extract_sample_ios(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    res = []
    for i in count(1):
        e = soup.find(id=f'sample-input-{i}')
        if e is None:
            break
        res.append((e.text, soup.find(id=f'sample-output-{i}').text))
    return res


def normalize_linebreaks(x):
    return x.replace('\r\n', '\n').replace('\r', '\n')


def make_tcs_cat(n, in_file, out_file):
    ios = extract_sample_ios(fetch_problem(n))
    if not ios:
        return
    sin, sout = zip(*ios)
    in_file.write(normalize_linebreaks(''.join(sin)))
    out_file.write(normalize_linebreaks(''.join(sout)))


def problem_title(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id='problem_title').text


def is_forbidden_char(c):
    if c <= ' ': return True
    if c in '|&;<>()$`\\"\'': return True
    if c in '*?[#~=%': return True
    return False


def to_filename(x):
    return ''.join('_' if is_forbidden_char(c) else c for c in x)


def cmd_make_tcs_cat(n, in_file, out_file):
    with open(in_file, "w") as in_file, open(out_file, "w") as out_file:
        make_tcs_cat(n, in_file, out_file)


def cmd_problem_title(n):
    print(problem_title(fetch_problem(n)))


def cmd_problem_filename(n):
    print(f'{n}_{to_filename(problem_title(fetch_problem(n)))}')


def main(cmd, *argv):
    cmds = {
        'make_tcs_cat': cmd_make_tcs_cat,
        'problem_title': cmd_problem_title,
    }
    cmds[cmd](*argv)



main(*sys.argv[1:])
