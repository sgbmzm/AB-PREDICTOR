The code is for personal use only - not for profit

# AB Group Predictor

Finds the closest Avotaynu (AB) groups for a person, by the first 37 Y-STR markers (FTDNA order).
It can also give the distance between the markers of two people.

**MAIN-CODE_FILE = ab_predictor.py**

| File | What it is |
|---|---|
| `ab_predictor.py` | the window (tkinter) |
| `abp_core.py` | the calculation |
| `required_files/2data37+A.csv` | the STR models of the AB groups |
| `additions/` | older versions |

To run the python code (recommended through https://thonny.org/): download the files above and keep them together
(with the folder `required_files`). No extra library is needed.

## The calculation
For each group: the sum of the differences (in steps) between the person's markers and the model of the group.
- A marker that was not tested (0 / null / empty), or is missing in the model, is not counted.
- A marker with several values (DYS385, DYS464 ...): the difference of each value. If the number of values differs
  (for example DYS464 with 4 values against a model with 6), the marker counts 2 steps.
- The distance is scaled to the number of markers the person has, so a model with a missing marker gets no advantage.
- The 10 closest groups are shown, with the gap between the 1st and 2nd. A small gap means that the 2nd or 3rd group
  may be the right one; an SNP test decides.

## Data source
The STR models of the AB groups: [JewishDNA](https://jewishdna.net/ModalsAB.html), in collaboration with
[Avotaynu Online](https://avotaynuonline.com/avotaynu-foundation-dna-project/). All rights to these data belong to them.

## Credit
Written by Yehudit Bohrer and Dr. Simcha Gershon Bohrer.

## Terms of use
The results are estimates only, and may be wrong. They do not prove Jewish (or any other) ancestry, and must not be
used alone for any decision. All use is at your own responsibility.

## Versions
`APP_VERSION` in `ab_predictor.py` (MAJOR.MINOR.PATCH). 2.0.0 - the new calculation (above), English/Hebrew display,
terms of use. Build: Actions -> "Build ab_predictor for all systems" (Windows x64, Linux x64, Mac).
