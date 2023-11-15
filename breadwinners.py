"""Implementations of the best CRED scores according to our gridsearch.
"""
import cred


class CredScore:
  """Abstract base class for CRED scores."""
  ngram_asymptote = None

  def signature(self) -> str:
    elements = [
        self.nickname,
        self.type_descriptor,
        f"n={self.ns}",
        f"ngram_asymptote={self.ngram_asymptote}",
        f"repeat_threshold={self.threshold_repeat}",
        f"noisy_threshold={self.threshold_noisy}",
    ]
    return ":".join(elements)

  def score(self, doc:str) -> float:
    raise ValueError("Abstract class; score is not implemented")

  def clf_repeat(self, doc:str) -> bool:
    """Classify whether the doc is repetitive.
    True means the doc is OK; False means that it is redundant."""
    return self.score(doc) < self.threshold_repeat

  def clf_noisy(self, doc:str) -> bool:
    """Classify whether the doc is noisy.
    True means the doc is OK; False means that it is noisy."""
    return self.score(doc) < self.threshold_noisy


class Pumpernickel(CredScore):
  """A hearty score that fares excellently on noisy text."""

  threshold_repeat = 0.5095067282
  threshold_noisy = 0.5095067282
  ns = [4, 5]
  ngram_asymptote = 2000
  distance_fn = lambda self, x, y: (x - y) ** 2
  nickname = "pumpernickel"
  type_descriptor = "zipfianness_(x-y)^2"

  def score(self, doc:str) -> float:
    return cred.zipfianness_score(
        doc,
        ngram_lengths=self.ns,
        distance_fn=self.distance_fn,
        ngram_asymptote=self.ngram_asymptote,
    )


class Vollkorn(CredScore):
  """A lighter version of Pumpernickel with almost equivalent performance."""

  threshold_repeat = 0.7414957191
  threshold_noisy = 0.5723524719
  ns = [4]
  ngram_asymptote = 2000
  distance_fn = lambda self, x, y: (x - y) ** 2
  nickname = "vollkorn"
  type_descriptor = "zipfianness_(x-y)^2"

  def score(self, doc:str) -> float:
    return cred.zipfianness_score(
        doc,
        ngram_lengths=self.ns,
        distance_fn=self.distance_fn,
        ngram_asymptote=self.ngram_asymptote,
    )


class Sodabread(CredScore):
  """A light and versatile score, performing well on both noise and repeat."""

  threshold_repeat = 1.060987194
  threshold_noisy = 0.8452993116
  ns = [8]
  ngram_asymptote = 2000
  exp = 2
  nickname = "sodabread"
  type_descriptor = "moment_x^2"

  def score(self, doc:str) -> float:
    return cred.moment_score(
        doc,
        ngram_lengths=self.ns,
        exp=self.exp,
        ngram_asymptote=self.ngram_asymptote,
    )


class Crouton(CredScore):
  """Best TTR score with perfectly OK performance."""

  threshold_repeat = 0.2233798512
  threshold_noisy = 0.2225532769
  ns = [10]
  nickname = "crouton"
  type_descriptor = "ttr"

  def score(self, doc:str) -> float:
    return cred.ttr_score(doc, ngram_lengths=self.ns)
