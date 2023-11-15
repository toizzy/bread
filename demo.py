"""Usage example. Just run the following:

>>> python3 demo.py
"""
import breadwinners as bw

loaf = bw.Vollkorn()

print("""The following examples show scores on increasingly repetitive / noisy inputs.
the score should increase for each one; higher scores mean more noise.
This is for demonstration porpoises; CRED scores are more reliable for longer inputs.

""")

print(loaf.score(
"Once upon a time, there was a customer named Akshay who was very particular about"
"his coffee. He always ordered the same thing: a venti, two-pump, nonfat,"
"extra-hot latte with no foam. However, what the patrons and indeed the baristas"
"did not know was that he didn't drink them; instead he went home and analyzed"
"them in his coffee lab. Akshay loved coffee, but not this type."))

print(loaf.score(
"Once upon a time, there was a customer named Akshay who was very particular "
"about his coffee. He always ordered the same thing: a venti, two-pump, "
"a venti, two-pump, a venti, two-pump, a venti, two-pump, a venti, "
"two-pump, a venti, two-pump, extra-hot latte with no foam. However, what "
"the patrons did not know was that he didn't drink them."))

print(loaf.score(
"Once upon a time, there was a venti named Akshay who was very particular "
"about his pumps. He always ordered a venti, two-pump, a venti, two-pump, "
"a venti, two-pump, a venti, two-pump, a venti, two-pump, a venti, "
"two-pump, a venti, two-pump, extra-extra-extra-extra-extra-extra-hot "
"with no foam or no foam or no ventis or no foam or no coffee."))

print(loaf.score(
"Once upon a foam, there was an extra venti named Pump who was extra "
"about his foam. He extra pumped a venti, two-pump, a venti, two-pump, "
"a venti, two-pump, a venti, two-pump, a venti, two-pump, a venti, "
"two-pump, a venti, two-pump, extra-extra-extra-extra-extra-extra-hot "
"with no foam or no foam or no extra-extra-extra-extra-extra-extra-foam."))

print(loaf.score(
"Once foam a foam there foam an foam venti foam Pump foam was foam "
"about foam foam. foam extra foam a foam two-pump, foam venti, foam "
"a foam two-pump, foam venti, foam a foam two-pump, foam venti, "
"two-pump, foam venti, foam extra-extra-extra-extra-extra-extra-hot "
"no foam no foam or foam extra-extra-extra-extra-extra-extra-foam."))


print(loaf.score(
"FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMM"
"VEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEENNNNNNNNNNNNNNNNNNNNNTTTTTTTTIIIII"
"COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOVFEEEEEEEEEEEEEEEEEEEEFE"
"PUMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEXXXXXXXXXXXXXTRRRRRRRAAA"))



print("""


Now let's use these same scores to classify text:

""")


print("Non-repetitive; classifier output should be 'True': ", end="\t")
print(loaf.clf_repeat(
"Once upon a time, there was a customer named Akshay who was very particular about"
"his coffee. He always ordered the same thing: a venti, two-pump, nonfat,"
"extra-hot latte with no foam. However, what the patrons and indeed the baristas"
"did not know was that he didn't drink them; instead he went home and analyzed"
"them in his coffee lab. Akshay loved coffee, but not this type."))

print("Repetitive; classifier output should be 'False': ", end="\t")
print(loaf.clf_repeat(
"Once upon a time, there was a customer named Akshay who was very particular "
"about his coffee. He always ordered the same thing: a venti, two-pump, "
"a venti, two-pump, a venti, two-pump, a venti, two-pump, a venti, "
"two-pump, a venti, two-pump, extra-hot latte with no foam. However, what "
"the patrons did not know was that he didn't drink them."))

