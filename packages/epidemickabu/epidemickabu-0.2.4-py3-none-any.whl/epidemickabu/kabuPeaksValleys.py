from .kabuWaves import *
#from kabuWaves import *

class peaksValleys(waves):

    """peaksValleys is the class from kabuPeaksValleys module in the EpidemicKabu library. It is a child class of 
    curves and waves classes from module kabu and kabuWaves, respectively. Its workflow is to identify the cut points
    that delimites the start and the end of a peak and valley. And filter those cut points according to a threshold.
    A draw of this workflow in the research paper
     """

    def __init__(self,dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot = "./plots/",outFolderDF="./dataframes/",fbi=0):
        
        """The arguments to make an instance are:
         1. dataframe: DataFrame with the dates and the number of cases by date
         2. datesName: Name of the column with the dates which are strings 
         3. casesName: Name of the column with the cases by each date
         4. kernel: value of the parameters to apply the Gaussian kernel.The kernel could be an int or it could be a list with [df,c1,v1,c2],where df is a dataframe with a column c1 with a values v1 and a column c2. In this way you could use a configuration file with the kernels as in https://github.com/LinaMRuizG/EpidemicKabuLibrary/blob/main/examples/data/configurationFile.csv
         5. plotName: The name for the output plot and file of the plot
         6. dfName: The name for the output dataframe. This dataframe has the inital dates and number of cases and it is added a column for the normalized values and smoothed values
         7. outFolderPlot: The directory to put the output plot. The default is ./plots/, be sure of create it
         8. outFolderDF: The directory to put the output dataframe. The default is ./dataframes/, be sure of create it"""
        
        super().__init__(dataframe,datesName,casesName,kernel,plotName,dfName,outFolderPlot,outFolderDF,fbi)
        

    def idenCutPointsPV(self,inputToFindCuts,outputName): 

        """For a column (i.e.,inputToFindCuts), it identifies the positions (i.e., rows) with a positive value for each consecutive pair of positive-negative values (+/-) and negative value for each consecutive pair of negative-positive values (-/+)"""

        df = self.df

        df[outputName] = (df[inputToFindCuts].rolling(2).agg(lambda x : True if (x.iloc[0]<0 and x.iloc[1]>0) or (x.iloc[0]>0 and x.iloc[1]<0) else False)).fillna(False)
        #puts True to each positive value in inputToFindCuts that is predated by a negative value and also to each negative value in inputToFindCuts that is predated by a positive value



    def idenPreviousDatesPV(self,inputCuts,inputToFindCuts):

        """
        Using the columns (i.e.,inputCuts and inputToFindCuts) from the dataframe, it identifies 
        the positions (i.e., rows) with a negative value for each consecutive pair of positive-negative values (+/-)
        or a positive value for each consecutive pair of negative-positive values (-/+). It filters with these positions
        the dates and the values of inputToFindCuts (i.e., the column used to indentify the cut points). 
        Then, it selects the dates associated to the lowest absolute value of each consecutive pair of positive-negative or 
        negative-positive (i.e., ensuring to select the date associate to the value closest to zero or when the values
        of the column cut the axis in the temporal plot)
        Notice that this is exactly the same method as idenPreviousDatesW() from kabuWaves, the only
        difference is the name of the final variable (new attribute) "self.cutDatesPV"  """

        df = self.df
       
        positions1 = df[df[inputCuts]==True][[self.dN,inputToFindCuts]].reset_index(drop=True)
        #gets the dates and the values in inputToFindCuts which are True in inputCuts (positive values predated by negative and negative values predated by positive)
       
        positions2 = df[df[self.dN].isin(list(positions1[self.dN] - datetime.timedelta(days=1)))][[self.dN,inputToFindCuts]].reset_index(drop=True)
        #gets the previous dates of dates in position1 (which are the dates of the negative values followed by positive and positive values followed by negative). Then, it gets their dates and the values in inputToFindCuts 
        positions2.rename(columns={self.dN:self.dN+"1",inputToFindCuts:inputToFindCuts+"1"},inplace=True)
        
        positions = pd.concat([positions1, positions2], axis=1)

        self.cutDatesPV = list(positions.agg(lambda x : x[self.dN] if abs(x[inputToFindCuts])<abs(x[inputToFindCuts+"1"])  else x[self.dN+"1"], axis=1))
        #selects the dates associated to the value of inputToFindCuts (in positions) closest to zero

        self.df["cutDatesPV0"] = self.df[self.dN].isin(self.cutDatesPV).astype(int)
        #creates a new column with 1 in the dates selected
        
    
    def __subtraction__(self,serie,timestamp):
                
        """It gets the dates in a 'serie' which are closet to an specific date (TimeStamp format). The closest pass the date and before the date """
        
        subtraction = serie-timestamp
        #gets the difference in days between each date of the serie and a the TimeStamp date
        subtraction2 = [td.days for td in subtraction]
        #gets the days of the differences

        zipping = list(zip(serie,subtraction2))
    
        pos = [i for i in zipping if i[1]>0]
        neg = [i for i in zipping if i[1]<0]
        #separates positive differences from negative ones

        if len(pos)==0:
            minPos = [[],[]]
            #a format to avoid mistakes if the are not positive differences 
        
        elif len(pos)==1:
            minPos = pos[0]
            #if there is only one positive
        
        else:
            minPos = min(pos, key = lambda x: x[1])
            #returns the lowest positive and the original date associated
            
        if len(neg)==0:
            maxNeg = [[],[]]
            #a format to avoid mistakes if the are not negative differences 
        
        elif len(neg)==1:
            maxNeg = neg[0]
            #if there is only one negative
        
        else:
            maxNeg = max(neg, key = lambda x: x[1])
            #returns the biggest positive and the original date associated

        return [minPos[0],maxNeg[0]]
        #returns the dates associated to the lowest positive and the biggest negative differences

    
    def filteringCutDatePV(self):
        
        """it selects the cutDatesPV0 which are closest to rigth and left of each peak (i.e., the maximum value or height of the wave-the smoothed curve) inside a wave"""
        
        df = self.df
        
        df.loc[:,"cutDatesW2"]=df["cutDatesW"].cumsum()
        #builds the groups of waves
        
        peaksDates = df.groupby(df["cutDatesW2"]).apply(
            lambda x : x[x["SmoothedCases"]==max(x["SmoothedCases"])][self.dN])
        #gets the dates of the maximum value in each wave
        
        df["peaksDates"] = df[self.dN].isin(peaksDates).astype(int)
        #creates the peaksDates column in the df
        
        filteredPVCutDates = df.groupby(df["cutDatesW2"]).apply(
            lambda x:
            self.__subtraction__(
            x[x["cutDatesPV0"]==1][self.dN],
            x[x["peaksDates"]==1][self.dN].iloc[0]))
        #selects the dates in cutDatesPV that are closest to the rigth and left of each one of the peaksDates
        
        self.cutDatesPV = [item for sublist in filteredPVCutDates for item in sublist if item]
        self.df["cutDatesPV"] = self.df[self.dN].isin(self.cutDatesPV).astype(int)
 
    
    def run(self):
       
        """It run all the class methods in the correct order and builds the plot and a dataframe of the plot"""
        
        #those are the methods of curves class
        self.stansardizingDates()
        self.curveNormalization(self.cN,"NormalizedCases")
        self.curveSmoothing2("NormalizedCases","SmoothedNCases",self.kernel)
        self.curveSmoothing2(self.cN,"SmoothedCases",self.kernel)
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed",self.kernel)
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")

        #those are the methods from this class
        self.idenCutPointsPV("SecondDerivate","rollingSD")
        self.idenPreviousDatesPV("rollingSD","SecondDerivate")

        #those are the methods from detecting waves class
        self.idenCutPointsW("FirstDerivateSmoothed","rollingFDS")
        self.idenPreviousDatesW("rollingFDS","FirstDerivateSmoothed")
        self.filteOnInfectionItself()
        
        #those are the methods from this class
        self.filteringCutDatePV()

        #creating and saving the output dataframe
        df = self.df[[self.dN,self.cN,"SmoothedCases","cutDatesPV"]]
        df.to_csv(self.outFolderDF + self.dfName + ".csv")
        
        self.plottingTheCurveNormalized(self.cutDatesPV)
        self.plottingTheCurveNoNormalized(self.cutDatesPV)
    





