import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
import datetime
pd.set_option('mode.chained_assignment', None)

class curves:
    
    """curves is the class from kabu module in the EpidemicKabu library. The main workflow of this class is to normalize the epidemic curve, smooth it with a Gaussian kernel, and estimate the first and second derivative of the smoothed curve. The main workflow of this class is to normalize, smooth with a Gaussian kernel, and estimate the first and second derivative of the epidemic curve. A draw of this workflow in the research paper"""

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot = "./plots/",outFolderDF="./dataframes/"):

        """The arguments to make an instance are:
         1. dataframe: DataFrame with the dates and the number of cases by date
         2. datesName: Name of the column with the dates which are strings 
         3. casesName: Name of the column with the cases by each date
         4. kernel: value of the parameters to apply the Gaussian kernel.The kernel could be an int or it could be a list with [df,c1,v1,c2],where df is a dataframe with a column c1 with a values v1 and a column c2. In this way you could use a configuration file with the kernels as in https://github.com/LinaMRuizG/EpidemicKabuLibrary/blob/main/examples/data/configurationFile.csv
         5. plotName: The name for the output plot and file of the plot
         6. dfName: The name for the output dataframe. This dataframe has the inital dates and number of cases and it is added a column for the normalized values and smoothed values
         7. outFolderPlot: The directory to put the output plot. The default is ./plots/, be sure of create it
         8. outFolderDF: The directory to put the output dataframe. The default is ./dataframes/,be sure of create it""" 
        
        #database
        self.df = dataframe
        #column names 
        self.dN = datesName
        self.cN = casesName
        #parameters
        self.kernel = kernel
        #to customize
        self.plotName = plotName
        self.dfName = dfName
        self.outFolderPlot = outFolderPlot
        self.outFolderDF = outFolderDF

    
    def stansardizingDates(self):

        """It converts the dates of the column datesName in a Timestamp object with to_date() function from pandas"""

        #df = self.df
        #self.df["Date_reported"]= pd.to_datetime(self.df["Date_reported"])
        self.df.loc[:, self.dN] = pd.to_datetime(self.df[self.dN])

    
    def curveNormalization(self, inputNormalization, outputNormalization):

        """It normalizes (i.e., dividing by the maximum value) a column (i.e., inputNormalization) in the dataframe.
        The result is a new column (i.e., outputNormalization) in the dataframe"""

        df = self.df
        df.loc[:,outputNormalization] = df[inputNormalization]/df[inputNormalization].abs().max()
    


    def __gettingKernel(self,kernel):

        """It gets the kernel value. The kernel could be a int or it could be a list with [df,c1,v1,c2], where df is the dataframe with the kernels, c1 is the name of the column with the values from which filtering the kernel (it could have the countries names), v1 is the value to be selected from c1, c2 is the name of the column with the values of the kernels. In this way you could use a configuration file with the kernels as in https://github.com/LinaMRuizG/EpidemicKabuLibrary/blob/main/examples/data/configurationFile.csv"""

        
        if isinstance(kernel,(int,float)):
            k = kernel
            #in this case k is the number directly put in the instance of the object
        else:
            df = kernel[0]
            #df is the dataframe with the kernels
            c1 = kernel[1]
            #c1 is the name of the column with the values from which filtering the kernel.
            #It could have the countries names 
            v1 = kernel[2]
            #the value to be selected from the c1
            c2 = kernel[3]
           
            #c2 is the name of the column with the values of the kernels
            try:
                k = int(df[df[c1]==v1][c2].iloc[0])
            except:
                k = 18
                print(f"For {v1} it was used the default kernel equal to 18")
                
            
            #in this case k is the number selected from df
        return k/2

    def curveSmoothing(self,inputToSmooth,outputSmoothed,k):

        """It smooths any column (i.e.,inputToSmooth) in the dataframe using gaussian_filter function. The result is a new column (i.e., outputSmoothed) in the dataframe """

        kernel = self.__gettingKernel(k)
        df = self.df
        df.loc[:,outputSmoothed] = gaussian_filter(df[inputToSmooth], kernel)

    
    def curveSmoothing2(self,inputToSmooth,outputSmoothed,k):
        
        """It smooths any column (i.e.,inputToSmooth) in the dataframe using a Gaussian kernel function. The result is a new column (i.e., outputSmoothed) in the dataframe """

        kernel = self.__gettingKernel(k)
        smoothed_cases = []
        df = self.df
        
        for date in sorted(df[self.dN]):
            df.loc[:,'gaussian'] = np.exp( - (((df[self.dN] - date).apply(lambda x: x.days)) ** 2) / (2 * (kernel ** 2)))
            df.loc[:,'gaussian'] /= df['gaussian'].sum()
            smoothed_cases.append((df[inputToSmooth] * df['gaussian']).sum())     
        df.loc[:,outputSmoothed] = smoothed_cases
      
    
    def discreteDerivative(self,inputToDerivate,outputDerivate):
        
        """It makes a discrete derivate of any column (i.e., inputToDerivate) in the dataframe. The result is a new column (i.e., outputDerivate) in the dataframe"""
        
        df = self.df
        df.loc[:,outputDerivate] = df[inputToDerivate].rolling(2).agg(lambda x : x.iloc[1]-x.iloc[0])
    
    
    def plottingTheCurveNormalized(self):

        """It makes a temporal plot of the Normalized and Smoothed cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df["NormalizedCases"], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedNCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Normalized "+self.cN)
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()

    def plottingTheCurveNoNormalized(self):

        """It makes a temporal plot of the No-Normalized and Smoothed cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df[self.cN], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedCases"], color="red", label ="Smoothed Cases")
        plt.ylabel(self.cN)
        plt.xlabel("Time")
        plt.title(self.plotName)
        plt.legend()


    def confidenceInterval(self,dataFrame,kernel,cut="Waves",z=1.96):
        """z comes from confidence interval assuming a normal distribution"""

        casesName = self.cN
        datesName = self.dN
        dataFrame[datesName] = pd.to_datetime(dataFrame[datesName])
        
        if cut=="Waves":
            cutDates = "cutDatesW"
        elif cut == "Peaks":
            cutDates = "cutDatesPV"
        
        cutsIndex = dataFrame[dataFrame[cutDates]==1].index
        
        daily_cases = dataFrame.loc[cutsIndex, casesName]
        smoothed_cases = dataFrame.loc[cutsIndex, 'SmoothedCases']

        # Actualizar los valores de 'daily_cases' en los índices cutsIndex
        dataFrame.loc[cutsIndex, casesName] = daily_cases.where(daily_cases != 0, smoothed_cases)

        deltat = (kernel/2) / np.sqrt(np.abs(dataFrame.loc[cutsIndex, casesName].values))
        uncertanties = []
        
        for i in deltat:
            uncertanty = round(i * z)
            #print(uncertanty)
            if uncertanty == 0:
                uncertanties.append(1)
            else:
                uncertanties.append(uncertanty)

        data = {
            'cut_day': [dataFrame[datesName][cut] for cut in cutsIndex],
            "cases" : daily_cases,
            'CI(95%)': [f"{i} days" for i in uncertanties],
            }
        df = pd.DataFrame(data)

        return df

    def run(self):

        """It run all the class methods in the correct order to make the main workflow of this class. It creates the output variables that will be part of the a dataframe to be used in the kabuWaves and kabuPeakValleys modules"""

        self.stansardizingDates()

        self.curveNormalization(self.cN,"NormalizedCases")
        
        self.curveSmoothing2("NormalizedCases","SmoothedNCases",self.kernel)
        self.curveSmoothing2(self.cN,"SmoothedCases",self.kernel)
    
        
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed",self.kernel)
        
        
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")


    def runAndPlot(self):
        
        """If builds the plot and a dataframe of the plot"""

        self.run()
        
        self.plottingTheCurveNormalized()
        plt.savefig(self.outFolderPlot+self.plotName+"N.png")
        self.plottingTheCurveNoNormalized()
        plt.savefig(self.outFolderPlot+self.plotName+"NoN.png")
        
        df = self.df[[self.dN,self.cN,"NormalizedCases","SmoothedCases"]]
        df.to_csv(self.outFolderDF + self.dfName + ".csv")

















