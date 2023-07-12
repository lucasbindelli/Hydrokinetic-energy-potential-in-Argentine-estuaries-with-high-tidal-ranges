# Hydrokinetic-energy-potential-in-Argentine-estuaries-with-high-tidal-ranges
Paper codes and simulations for Bindelli et al., 2023 (IEEE).

![ID-8048_GraphicalAbstract-PatagonianEstuaries-Reviewed_v02](https://github.com/lucasbindelli/Hydrokinetic-energy-potential-in-Argentine-estuaries-with-high-tidal-ranges/assets/94264268/8d7fe4fb-7eb9-423b-8bf2-fc29c1c5366c)

Instructions:

Run Delft3D models following the established order. For advancing into a Rank "i+1", it is necessary to Nest the Rank "i+1" into Rank "i" model, generating boundary conditions. Modelling scheme should be: Run Rank 0 -> Nest Rank 1 -> Run Rank 1 -> etc.

Once all models have been run, go to the Post-Processing tab and execute the python codes, also in the established order. For this, Python 3 is needed and all the libraries used are described within the first lines of each code.

Note: Paths for python codes should be adjusted.

End of Readme File.

ACKNOWLEDGMENTS

The authors would like to thank de National Water Institute authorities (INA, Argentina) for providing the facilities, and to the CONICET and the YPF Foundation for funding.
