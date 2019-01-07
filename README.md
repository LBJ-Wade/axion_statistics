# Axion Statistics
Fourier and machine learning tools for constraining axion-like-particles in astrophysical observations as described in https://arxiv.org/abs/1808.05916 

# Requirements

Python 2.7, PyXspec 2

for Fourier Analysis: https://github.com/NFFT/nfft

for Machine Learning: tensorflow 1.5

# Usage

1. Use mathematica notebook PhotonAxionConversionCluster.nb to generate output: survivalProbs_*Bfield.txt

2. Delete all survivalProbs_*Bfield.mod files

3. Use python ALPmod.py to generate survivalProbs_*Bfield.mod table models as input for PyXspec.

4. Run python PyXspec_*instrument.py to perform PyXspec scan over all .mod files. Output: g_chisq.txt 

5. Run python Analyze_*instrument.py to analyze g_chsiq.txt. Outputs: histo_*.pdf and g_deltachi2.pdf
