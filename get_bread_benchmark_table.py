"""Evaluate noise classification functions on BREAD; print markdown table."""

from collections import defaultdict
import os
from typing import Callable, Dict, List, Tuple

import breadwinners as bw


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

BREAD_FILEPATH = f"{__location__}/bread.tsv"
BREAD_SPLITS = ["tune", "test"]
BREAD_LABELS = ["ok", "repeat", "boil"]
BREAD_SLICES = ["repeat", "noisy"]


def f1(fp: int, fn: int, tp: int, tn: int) -> float:
  return 2 * tp / (2 * tp + fp + fn)


def f2(fp: int, fn: int, tp: int, tn: int) -> float:
  return 5 * tp / (5 * tp + 4 * fp + fn)


def p44(fp: int, fn: int, tp: int, tn: int) -> float:
  """P4 score where we upweight positive examples by 4.

  (simulating behavior on cleaner data)
  """
  tp *= 4
  fn *= 4
  return (4 * tp * tn) / ((4 * tp * tn) + (tp + tn) * (fp + fn))


def slice_bread(
    bread: Dict[str, Dict[str, List[str]]], split: str, bread_slice: str
) -> Tuple[List[str], List[str]]:
  """Get tune/test splits of the BREAD data."""
  assert bread_slice in BREAD_SLICES
  assert split in BREAD_SPLITS
  if bread_slice == "repeat":
    return bread[split]["ok"], bread[split]["repeat"]
  else:
    return bread[split]["ok"], bread[split]["repeat"] + bread[split]["boil"]


def load_bread(fname: str) -> Dict[str, Dict[str, List[str]]]:
  all_docs = {"tune": defaultdict(list), "test": defaultdict(list)}
  with open(fname, "r") as f:
    for i, line in enumerate(f):
      parts = line.strip().split("\t")
      if len(parts) != 3:
        continue
      split, label, doc = parts
      if label not in BREAD_LABELS:
        continue
      all_docs[split][label].append(doc)
    return all_docs


def score_bread_slice(
    bread: Dict[str, Dict[str, List[str]]],
    clf: Callable[[str], bool],
    bread_slice: str,
    split: str,
    metric: Callable[[int, int, int, int], float],
) -> float:
  ok_docs, bad_docs = slice_bread(bread, split, bread_slice)
  fp, fn, tp, tn = error_classes_from_slices(clf, ok_docs, bad_docs)
  return metric(fp, fn, tp, tn)


def score_all_bread(
    bread: Dict[str, Dict[str, List[str]]],
    clf: bw.CredScore,
    metric: Callable[[int, int, int, int], float],
):
  result = []
  for split in BREAD_SPLITS:
    score = score_bread_slice(bread, clf.clf_repeat, "repeat", split, metric)
    result.append((clf.nickname, split, "repeat", score))
    score = score_bread_slice(bread, clf.clf_noisy, "noisy", split, metric)
    result.append((clf.nickname, split, "noisy", score))
  return result


def error_classes_from_slices(
    clf: Callable[[str], bool],
    positive_examples: List[str],
    negative_examples: List[str],
) -> Tuple[int, int, int, int]:
  fp, fn, tp, tn = 0, 0, 0, 0
  for x in negative_examples:
    if clf(x):
      fp += 1
    else:
      tn += 1
  for x in positive_examples:
    if clf(x):
      tp += 1
    else:
      fn += 1
  return fp, fn, tp, tn


if __name__ == "__main__":
  BREAD = load_bread(BREAD_FILEPATH)

  def print_readme_table(classifiers):
    print("classifier | split | bread slice | score")
    print("-----------|-------|-------------|------")
    for clf in classifiers:
      result = score_all_bread(BREAD, clf, f1)
      for tup in result:
        print("{} | {} | {} | {:.2%}".format(*tup))

  print_readme_table(
      [bw.Pumpernickel(), bw.Vollkorn(), bw.Sodabread(), bw.Crouton()]
  )
