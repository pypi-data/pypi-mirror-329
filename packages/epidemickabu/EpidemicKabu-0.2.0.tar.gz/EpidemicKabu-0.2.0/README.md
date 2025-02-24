# EpidemicKabu a new method to identify epidemic waves and their peaks and valleys

***Kabu*** is a new methodology to identify waves, peaks, and valleys from epidemic curve. The algorithm in explain in **doi:..** as well as some examples.

## Description of files in this repository:

1. `epidemickabu/` contains the modules of the package:

   * `kabu.py` is the main module. It makes the necessary calculations for the subsequent identification of waves, and peaks and valleys. The main input is a dataset with two variables (i.e., **cases**, and **dates**) and the **kernels** to smooth both the epidemic curve and its first derivative with a Gaussian filter.

   * `kabuWaves.py` is a module to estimate the waves. You could set an optional **threshold** to filter the days delimiting the waves. There are some examples in **examples/** that give you and idea of the magnitude of this value. You can also filter the waves changing the **kernel**'s value.

   * `kabuPeaksValleys.py` is a module to estimate the Peaks and Valleys of each identified wave.
     
2. `examples/` contains the files to replicate examples of how to use the library. The examples are made with COVID-19 data for 15 countries:
   * `data/` is the input data used in all the research.
   * `dataframes/` is created to save the output dataframes.
   * `plots/` is created to save the output plots.
   * `exampleUseLibrary.ipynb` shows basic examples to use the library.
   * `exploringLibrary/.ipynb` explores attributes and methods from the classes in the library.
   * The other files show the steps for some analysis made with the results obtained with the library for COVID-19 data.

3. `test/` contains the files to test the code.

4. `additional/` contains some notebooks showing the step by step of the algorithm.

## Installation in Python

**NOTE:** *This project was made in* ***Python 3.10.6***

1. Install the library using `pip`
   ```sh 
   pip install epidemickabu
   ```
2. Import the library
   ```sh 
   import EpidemicKabu as ek
   ```

## Installation in R


1. Install and load the package `reticulate` which provides an interface between R and Python
   ```sh 
   install.packages("reticulate")
   ```
   and
   ```sh 
   library(reticulate)
   ```
2. Configure Python Environment
   ```sh 
   use_python("/path/to/python")
   ```
   or
   ```sh 
   use_virtualenv("/path/to/your/virtualenv")
   ```
3. Install and import the package `EpidemicKabu`
   ```sh 
   py_install("epidemickabu")
   ```
   and
   ```sh 
   ek <- import("EpidemicKabu")
   ```

## Contributing

This project is in progress and it requires some improvments. Therefore, if you have any suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/improvments`)
3. Commit your Changes (`git commit -m 'Adding some improvment`)
4. Push to the Branch (`git push origin feature/improvments`)
5. Open a Pull Request

## Contact

* [Lina M Ruiz G](https://co.linkedin.com/in/lina-marcela-ruiz-galvis-465896209) - lina.ruiz2@udea.edu.co

## Acknowledgments
* [Anderson Alexis Ruales Barbosa](https://co.linkedin.com/in/anderson-alexis-ruales-b27638199?original_referer=https%3A%2F%2Fwww.google.com%2F)
* [Oscar Ignacio Mendoza Cardozo](https://loop.frontiersin.org/people/2156647/overview)

    
    
    
    
   
