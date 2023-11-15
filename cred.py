"""Implementations of the basic CRED scores.

For particular classifiers made with these function, see breadwinners.py.
"""

from collections import Counter
from typing import Callable, List, Union


ZIPF_ARGS = {
    'm_scale': 6.809072720465265,
    'm_offset': 2.7684855243401376,
    'm_exp': -1.487145194941155,
    'm_asymptote': 0.5267270772577696,
    'n_scale': 0.10735926073322274,
    'n_offset': 12.014486487513718,
    'n_exp': -12.653531461204041,
    'n_asymptote': 0.013873425087145296,
    'm0': -2.7279975090636936,
    'b0': 2.1480493853508404,
}


def get_ngram_cts(doc: str, n: int) -> List[int]:
  ngrams = Counter([doc[i : i + n] for i in range(0, len(doc) - n + 1)])
  return [ct for tok, ct in ngrams.most_common()]


def smooth_distribution(
    cts: List[str], topk: None, smooth: float, eps: float
) -> List[int]:
  """Convert raw ngram counts into (smoothed) distribution.

  Note: smoothing happens before epsilon thresholding but after topk sampling.
  """
  if topk:
    cts = cts[0:topk]
  smooth = smooth or 0
  z = sum(cts) + smooth * len(cts)
  freqs_smoothed = []
  for ct in cts:
    p = (ct + smooth) / z
    if eps and p < eps:
      break
    freqs_smoothed.append(p)
  return freqs_smoothed


def adjust_count_towards_asymptote(
    n: int, ngram_asymptote: Union[float, int]
) -> float:
  """See Section 4.1: Compensating for Length Dependency."""
  if not ngram_asymptote:
    return n
  return ngram_asymptote * (n / (n + ngram_asymptote))


def uniform_moment(freqs: List[int], exp: float, ngram_asymptote=None) -> float:
  """Get the value of the expth moment if this distribution were uniform.

  Used for normalizing by length.
  """
  n = adjust_count_towards_asymptote(len(freqs), ngram_asymptote)
  return pow(n, 1 - exp)


def zipf_estimator(ngram_size: int, token_idx: int) -> float:
  """Estimated freqency of token_idx'th most common ngram_size-gram in a corpus.

  Note: token_idx is 1-indexed.
  """
  if token_idx <= 0:
    raise ValueError(
        f'Zipf estimator uses 1-indexed tokens; got token_idx={token_idx}'
    )
  m = (
      ZIPF_ARGS['m_scale']
      * pow(token_idx + ZIPF_ARGS['m_offset'], ZIPF_ARGS['m_exp'])
      + ZIPF_ARGS['m_asymptote']
  )
  n_scale = (
      ZIPF_ARGS['n_scale']
      * pow(ngram_size + ZIPF_ARGS['n_offset'], ZIPF_ARGS['n_exp'])
      + ZIPF_ARGS['n_asymptote']
  )
  return n_scale / pow(token_idx, m)


def ttr_score_single(doc: str, n: int) -> float:
  """TTR score for a single n-gram length."""
  toks = [doc[i : i + n] for i in range(0, len(doc) - n)]
  return 1 - len(set(toks)) / len(toks)


def moment_score_single(
    doc: str,
    n: int,
    exp: float,
    topk: int = None,
    eps: float = None,
    smooth: float = None,
    ngram_asymptote: int = None,
) -> float:
  """Moment score for a single n-gram length."""
  cts = get_ngram_cts(doc, n)
  freqs = smooth_distribution(cts, topk=topk, eps=eps, smooth=smooth)
  transformed = [pow(p, exp) for p in freqs]
  uni = uniform_moment(freqs, exp, ngram_asymptote)
  return sum(transformed) / uni


def zipfianness_score_single(
    doc: str,
    n: int,
    distance_fn: Callable[[float, float], float],
    topk: int = None,
    eps: float = None,
    smooth: float = None,
    ngram_asymptote: int = None,
) -> float:
  """Zipfinanness score for a single n-gram length."""
  cts = get_ngram_cts(doc, n)
  freqs = smooth_distribution(cts, topk=topk, eps=eps, smooth=smooth)
  if not freqs:
    return 100
  uniform_p = 1 / adjust_count_towards_asymptote(len(freqs), ngram_asymptote)
  error = 0
  uniform_error = 0
  for i, p in enumerate(freqs):
    zipf_val = zipf_estimator(n, i + 1)
    error += distance_fn(p, zipf_val)
    uniform_error += distance_fn(uniform_p, zipf_val)
  return error / uniform_error


def ttr_score(
    doc: str, ngram_lengths: Union[int, List[int]], **kwargs
) -> float:
  scores = [ttr_score_single(doc, n, **kwargs) for n in ngram_lengths]
  return sum(scores) / len(scores)


def moment_score(
    doc: str, ngram_lengths: Union[int, List[int]], exp: float, **kwargs
) -> float:
  scores = [moment_score_single(doc, n, exp, **kwargs) for n in ngram_lengths]
  return sum(scores) / len(scores)


def zipfianness_score(
    doc: str,
    ngram_lengths: Union[int, List[int]],
    distance_fn: Callable[[float, float], float],
    **kwargs,
) -> float:
  scores = [
      zipfianness_score_single(doc, n, distance_fn, **kwargs)
      for n in ngram_lengths
  ]
  return sum(scores) / len(scores)
