import importlib
import json
import os
import re
import sys
from datetime import date
from functools import lru_cache, reduce
from itertools import product
from pathlib import Path
from time import time
from typing import Callable, Iterator, List, Tuple

setup_start = time()

aoc_root = Path('../')
aoc_data = aoc_root / 'data'

with (aoc_root / 'config.json').open('r') as f:
  config = json.load(f)

def day(year: int, theday: int) -> date:
  global setup_start
  setup_start = time()
  return date(year, 12, theday)

def get_data(today: date = date.today()) -> Iterator:
  if not aoc_data.exists():
    aoc_data.mkdir()

  def save_daily_input(today: date) -> None:
    request, status_codes = import_requests()
    url = f'https://adventofcode.com/{today.year}/day/{today.day}/input'
    res = request('GET', url, cookies=config)
    if res.status_code != status_codes.ok:
      print(f'Day {today.day} not available yet')
      sys.exit(0)
    with file_path.open('wb') as f:
      for chunk in res.iter_content(chunk_size=128):
        f.write(chunk)
        print(chunk.decode('utf-8'), end='')
      print()

  file_path = aoc_data / f'day{today.day:02}.txt'
  if not file_path.exists():
    print(f'Data for day {today.day} not available, downloading!')
    save_daily_input(today)

  with file_path.open() as f:
    lines = f.read().strip().split('\n')
    for line in lines:
      yield line


def submit_answer(today: date, answer: str, level: int = 1) -> None:
  from bs4 import BeautifulSoup
  request, status_codes = import_requests()
  url = f'https://adventofcode.com/{today.year}/day/{today.day}/answer'
  payload = {'level': level, 'answer': answer}
  res = request('POST', url, cookies=config, data=payload)
  soup = BeautifulSoup(res.content, 'html.parser')
  for content in soup.find_all('article'):
    print(content.text)


def import_requests():
  from requests import codes, request
  return request, codes

def time_fmt(delta: float) -> Tuple[float, str]:
  if delta < 1e-6:
    return 1e9, 'ns'
  elif delta < 1e-3:
    return 1e6, 'µs'
  elif delta < 1:
    return 1e3, 'ms'
  return 1, 'seconds'

def execute(func: Callable) -> float:
  start = time()
  func()
  return time() - start

def timed(func: Callable, start=None) -> None:
  if setup_start is not None:
    setup = time() - setup_start
  if start is not None:
    setup = time() - start
  delta = execute(func)
  print_result(delta + setup)

def print_result(delta: List[float], prefix: str = '', suffix: str = ''):
  multiplier, unit = time_fmt(delta)
  divider = ''
  if prefix != '':
    divider = ': '
  if suffix != '':
    suffix = ' ' + suffix
  print(f'--- {prefix}{divider}{delta*multiplier:.2f} {unit}{suffix} ---')

def run_all():
  for file in sorted(Path('.').glob('day*-*.py')):
    print(f'Running \'{file.name}\':')
    import_start = time()
    day = importlib.import_module(file.name[:-3])
    timed(day.main, import_start)
    print()

if __name__ == '__main__':
  timed(run_all)
