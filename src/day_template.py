from itertools import combinations

from helpers import day, get_data, timed

today = day(2020, 1)

def part1(ns):
  return None

def part2(ns):
  return None

def main() -> None:
  input = list(map(int,get_data(today)))
  print(f'{today} ⭐️ = {part1(input)}')
  print(f'{today} ⭐️⭐️ = {part2(input)}')

if __name__ == '__main__':
  timed(main)
