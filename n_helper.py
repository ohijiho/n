from itertools import count


def fetch_problem(n):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    url = f'https://www.acmicpc.net/problem/{n}'
    import requests
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


def cmd_make_tcs_cat(n, in_file, out_file):
    with open(in_file, "w") as in_file, open(out_file, "w") as out_file:
        make_tcs_cat(n, in_file, out_file)


def main(cmd, *argv):
    cmds = {
        'make_tcs_cat': cmd_make_tcs_cat,
    }
    cmds[cmd](*argv)


import sys
main(*sys.argv[1:])
