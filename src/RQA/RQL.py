import src.RQA.CustomPythonModules.DynamicalSystemsModule as RecurrenceFunctions;
import src.RQA.CustomPythonModules.SpatioTemporalEyeTrackingModule as ReoccurrenceFunctions;
import os
import sys
import math

class RQA:
    
    def __init__(self,fixations):
        self.fixations = fixations
        self.TimeSeriesData = []
        self.loadFileInfo()


    def loadTimeSeriesData(self):
        for i in range( 0, self.numFixations, 1 ):
            self.TimeSeriesData.append((self.fixationPositionsX[i], self.fixationPositionsY[i]))
            self.TimeSeriesDimensions = len( self.TimeSeriesData[0])

    def loadFileInfo(self):

        self.numFixations = len(self.fixations)
        self.fixationPositionsX = []
        self.fixationPositionsY = []
        self.fixationDurations = []
        for fixation in self.fixations:
            self.fixationPositionsX.append( float(fixation[0]))
            self.fixationPositionsY.append( float(fixation[1]))
            self.fixationDurations.append( float(fixation[2]))

            #rof
        self.fixationDurationsScaled = []
        maxFixationDuration = max( self.fixationDurations )
        for i in range( 0, self.numFixations, 1 ):
            scaledFixation = ( ( float( self.fixationDurations[i] ) / float( maxFixationDuration ) ))

            self.fixationDurationsScaled.append( scaledFixation)
        
        return ( None )
        #fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        ## FUNCTION FOR CALCULATING AND PLOTTING THE RECURRENCE DATA AND STATS
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def CalculateRecurrenceFunction( self, timeDelayValue, numTimeDelaySample, phaseSpaceClusteringThreshold ):

        result = {}
        self.TimeDelayValue = timeDelayValue
        self.loadTimeSeriesData()
        

        self.minEmbeddingSequenceLength = int(math.ceil(((2.0 * self.TimeSeriesDimensions) + 1.0 ) / float(self.TimeSeriesDimensions)))
        self.NumTimeDelaySamples = numTimeDelaySample
        self.PhaseSpaceClusteringThreshold = phaseSpaceClusteringThreshold

        self.FixationsXYPhaseSpaceData = RecurrenceFunctions.TimeDelayEmbedding(timeSeriesObservations=self.TimeSeriesData,delayStep=self.TimeDelayValue,delaySamples=self.NumTimeDelaySamples )
        self.RecurrenceMatrixData = RecurrenceFunctions.CreateRecurrenceMatrix(phaseSpaceData=self.FixationsXYPhaseSpaceData,clusteringDistanceThreshold=self.PhaseSpaceClusteringThreshold )

        self.Recurrence = RecurrenceFunctions.getRecurrence(self.RecurrenceMatrixData,self.NumTimeDelaySamples )
        
        self.RecurrenceRate = RecurrenceFunctions.getRecurrenceRate( self.RecurrenceMatrixData, self.NumTimeDelaySamples )
        ( self.RecurrenceMeanX, self.RecurrenceMeanY ) = RecurrenceFunctions.getRecurrenceMean( self.RecurrenceMatrixData, self.NumTimeDelaySamples )
        ( self.RecurrenceStandardDeviationX, self.RecurrenceStandardDeviationY ) = RecurrenceFunctions.getRecurrenceStandardDeviation( self.RecurrenceMatrixData, self.NumTimeDelaySamples )
    
        result['recurrence'] = self.Recurrence
        result['recurrenceRate'] = self.RecurrenceRate
        result['recurrenceMeanX'] = self.RecurrenceMeanX
        result['recurrenceMeanY'] = self.RecurrenceMeanY
        result['recurrenceStandartDeviationX'] = self.RecurrenceStandardDeviationX
        result['recurrenceStandartDeviationY'] = self.RecurrenceStandardDeviationY

            # valueNames= [ r'\rho', r'\bar{\rho}', r'\mu_{x}', r'\mu_{y}', r'\sigma_{x}', r'\sigma_{y}' ],
        return result
        #fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        ## FUNCTION FOR CALCULATING AND PLOTTING THE REOCCURRENCE DATA AND STATS
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def CalculateReoccurrenceFunction( self, fixationSpaceDistanceRadius):

        if not self.TimeSeriesData:
            self.loadTimeSeriesData()

        result = {}
        self.FixationSpaceDistanceRadius = fixationSpaceDistanceRadius
        self.ReoccurrenceMatrixData = ReoccurrenceFunctions.CreateReoccurrenceMatrix( positionData=self.TimeSeriesData,clusteringDistanceThreshold=self.FixationSpaceDistanceRadius )
        self.Reoccurrence = ReoccurrenceFunctions.getReoccurrence( self.ReoccurrenceMatrixData )
        self.ReoccurrenceRate = ReoccurrenceFunctions.getReoccurrenceRate( self.ReoccurrenceMatrixData )
        self.ReoccurrenceDeterminism = ReoccurrenceFunctions.getDeterminism( self.ReoccurrenceMatrixData )
        self.ReoccurrenceLaminarity = ReoccurrenceFunctions.getLaminarity( self.ReoccurrenceMatrixData )
        self.ReoccurrenceCORM = ReoccurrenceFunctions.getCORM( self.ReoccurrenceMatrixData )

        result['reoccurence'] = self.Reoccurrence
        result['reoccurenceRate'] = self.ReoccurrenceRate
        result['reoccurenceDeterminism'] = self.ReoccurrenceDeterminism
        result['reoccurenceLaminarity'] = self.ReoccurrenceLaminarity
        result['reoccurenceCORM'] = self.ReoccurrenceCORM
        
        return result