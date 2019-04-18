#!/usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RecurrenceReoccurrenceViewer.py
#
# Project Webpage:
# http://geovis.cis.rit.edu
#
# Multidisciplinary Vision Research Laboratory (MVRL)
# Chester F. Carlson Center for Imaging Science (CIS)
# Rochester Institute of Technology (RIT)
#
# Tommy P. Keane
# tommy@tommypkeane.com
# http://www.tommypkeane.com
#
# Lab Co-Director and Project Co-Manager:
# Jeff B. Pelz
# pelz@cis.rit.edu
# Wiedman Professor
# Chester F. Carlson Center for Imaging Science
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## STANDARD PYTHON MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os;
import sys;
import math;
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## MATPLOTLIB (MATLAB-STYLE PLOTTING) MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import matplotlib;

matplotlib.use( 'Qt4Agg' );
matplotlib.rcParams[ 'backend.qt4' ] = 'PySide';

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as matplotlibFigureCanvas;
from matplotlib.figure import Figure as matplotlibFigure;

import matplotlib.pyplot as matplotlibplotting;
# matplotlibplotting.rc( 'text', usetex= True );
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## PYSIDE Qt GRAPHICAL USER INTERFACE MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from PySide import QtCore;
from PySide import QtGui;
from PySide import QtSvg;
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## PYTHON IMAGE LIBRARY MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import Image;
import ImageFilter;
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## CUSTOM MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from CustomPythonModules import *;
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## PLOTTING CANVAS WIDGET (INHERITS FROM matplotlibFigureCanvas AND QWidget)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PlotWidgetClass( matplotlibFigureCanvas, QtGui.QWidget ):

	
	## CLASS INITIALIZATION FUNCTION
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__( self, figureDPI= 72, parent= None, mainWindow= None ):
		
		matplotlibFigureCanvas.__init__( self, matplotlibFigure() );
		
		self.setParent( parent );

		self.mainWindowReference = mainWindow;
		
		# DEFINE FIGURE (SIZE IN INCHES)
		self.figure = matplotlibFigure( figsize=      ( 11, 8.5 ),
										dpi=          figureDPI,
										facecolor=    ( 1, 1, 1 ),
										edgecolor=    ( 0, 0, 0 ) );


		## P - Plot, S - Scatter, 3 - 3D, I - Image, C - Contour
		self.contentType = 'P';

		self.canvas = matplotlibFigureCanvas( self.figure )
		
		self.currentAxes = self.figure.add_subplot( 1, 1, 1 );
		
		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
	
	## HELPER FUNCTION TO GET THE CURRENT POSITION WITHIN THE CURRENT PLOT
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def getPlotPosition(self, x, y ):

		CurrentAxesObject = self.figure.gca();

		percentageXY = CurrentAxesObject.transAxes.inverted().transform( [ x, y ] );

		axisX = ( (CurrentAxesObject.get_xlim()[1] - CurrentAxesObject.get_xlim()[0]) * percentageXY[0] ) + CurrentAxesObject.get_xlim()[0];
		axisY = ( (CurrentAxesObject.get_ylim()[1] - CurrentAxesObject.get_ylim()[0]) * (1 - percentageXY[1]) ) + CurrentAxesObject.get_ylim()[0];

		return ( [axisX, axisY] );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	

	## CALLBACK FUNCTION FOR ANY TIME THE MOUSE MOVES
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def mouseMoveEvent(self, event):

		CurrentAxesObject = self.figure.gca();

		positionXY = self.getPlotPosition( event.x(), event.y() );

		if ( (positionXY[0] >= CurrentAxesObject.get_xlim()[0]) and (positionXY[1] >= CurrentAxesObject.get_ylim()[0]) and
			 (positionXY[0] <= CurrentAxesObject.get_xlim()[1]) and (positionXY[1] <= CurrentAxesObject.get_ylim()[1]) ):

			self.mainWindowReference.statusBar().showMessage( "Current Position " +
															  "| X: " +
															  ( "%.3f" % positionXY[0] ) +
															  ", Y: " +
															  ( "%.3f" % positionXY[1] ) );

			QtGui.QApplication.setOverrideCursor( QtGui.QCursor( QtCore.Qt.CrossCursor ) );

		else:

			self.mainWindowReference.refreshStatus();

			QtGui.QApplication.setOverrideCursor( QtGui.QCursor( QtCore.Qt.ArrowCursor ) );

		#fi
		
		return None;
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	
	## CREATE A NEW IMAGE PLOT WITH SCATTER DATA ON IT FOR A GIVEN AXES
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def newImageScatterPlot( self, imageObject, xData, yData, markerSizeData ):

		self.currentAxes.clear();

		self.currentAxes.imshow( imageObject );

		self.currentAxes.scatter(  x=  		xData,
								   y= 		yData,
								   s= 		markerSizeData,
								   marker= 	'D',
								   c= 		'm' );
		
		self.currentAxes.set_xlim( 0, imageObject.size[0] );
		self.currentAxes.set_ylim( imageObject.size[1], 0 );
		
		self.currentAxes.get_xaxis().set_visible( False );
		self.currentAxes.get_yaxis().set_visible( False );

		self.currentAxes.set_title( "Fixations Plotted with Duration [ms] by Size" );
		
		self.figure.tight_layout();

		self.figure.canvas.draw();
		QtCore.QCoreApplication.processEvents();
		matplotlibplotting.show();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	
	## CREATE A NEW BAR PLOT FOR A GIVEN AXES
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def newBarPlot( self, valueNames, barHeights, plotTitle, barTitles ):

		self.currentAxes.clear();

		self.currentAxes.grid( color= ( (0.5, 0.5, 0.5, 0.25) ), linestyle= '-.', linewidth= 1 );

		numValues = len( valueNames );

		barPosition = map( float, list( range( 0, numValues - 1, 1 ) ) );

		self.currentAxes.bar( left= 	barPosition,
							  height=	barHeights[1::1],
							  width= 	0.75,
							  color= 	'blue' );

		for i in range( 1, numValues, 1 ):

			self.currentAxes.text( x= 					(barPosition[i-1] + 0.375),
								   y= 					(float(barHeights[i]) * 1.05),
								   text= 				( "{0:.2f}".format(barHeights[i]) + " " + barTitles[i] ),
								   ha= 					'center',
								   va= 					'center',
								   backgroundcolor= 	'white' );

		#rof

		self.currentAxes.set_xticks( map( lambda x: x + 0.375, barPosition ) );
		self.currentAxes.set_xticklabels( valueNames[1::1]);

		self.currentAxes.set_ylim( (  0.0 ), (float(max( barHeights[1::1] )) * 1.1) );
		self.currentAxes.set_xlim( ( -0.5 ), (float(numValues - 1) + 0.25) );

		self.currentAxes.set_xlabel( ("R: " + "{0:.2f}".format(barHeights[0])) );

		self.currentAxes.set_title( plotTitle );
		
		self.figure.canvas.draw();
		QtCore.QCoreApplication.processEvents();
		matplotlibplotting.show();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



	## CREATE A NEW DOT PLOT FOR A GIVEN AXES
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def newDotPlot( self, dotMatrix, plotTitle, offset= 0 ):

		self.currentAxes.clear();

		self.currentAxes.grid( color= ( (0.5, 0.5, 0.5, 0.05) ), linestyle= '-.', linewidth= 1 );

		for i in range( 0, len( dotMatrix ), 1 ):

			for j in range( 0, len( dotMatrix[i] ), 1 ):
				
				self.currentAxes.scatter( x= 		( i + (offset - 1) ),
										  y= 		( ( dotMatrix[i] )[j] + (offset - 1) ),
										  marker= 	's',
										  s= 		max( [10, 200 / len(dotMatrix)] ),
										  color= 	( (1.0, 0.0, 0.0, 1.00) ) );

				self.currentAxes.scatter( x= 		( dotMatrix[i] )[j] + (offset - 1),
										  y= 		i + (offset - 1),
										  marker= 	's',
										  s= 		max( [10, 200 / len(dotMatrix)] ),
										  color= 	( (1.0, 0.0, 0.0, 0.25) ) );

			#rof

		#rof

		self.currentAxes.set_ylabel( 'Fixation' );
		self.currentAxes.set_ylabel( 'Fixation' );
		
		self.currentAxes.set_title( plotTitle );
		
		self.figure.canvas.draw();
		QtCore.QCoreApplication.processEvents();
		QtCore.QCoreApplication.processEvents();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#ssalc -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## MAIN WINDOW CLASS FOR THE GUI (INHERITS FROM QMainWindowReference)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class MainWindowClass( QtGui.QMainWindow ):

	
	## CLASS INITIALIZATION FUNCTION
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__( self, parent= None ):

		QtGui.QMainWindow.__init__( self, parent );

		self.centralWidget = DialogWidgetClass( mainWindow= self );

		self.setCentralWidget( self.centralWidget );

		self.statusBarMessage = ( "Application Ready..." );


		self.setWindowTitle( "Testing Recurrence and Reoccurrence Statistics" );
		self.refreshStatus();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
	## REFRESH THE STATUS BAR'S MESSAGE
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def refreshStatus( self ):

		self.statusBar().showMessage( self.statusBarMessage );

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	## REFRESH THE STATUS BAR'S MESSAGE
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def refreshGUI( self ):

		QtCore.QCoreApplication.processEvents();
		QtCore.QCoreApplication.processEvents();
		QtCore.QCoreApplication.processEvents();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#ssalc -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




## THE CENTRAL CONTAINER WIDGET (INHERITS FROM QDialog) FOR THE GUI ELEMENTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class DialogWidgetClass( QtGui.QDialog ):

	
	## THE CLASS INITIALIZATION FUNCTION
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__( self, mainWindow= None, parent= None ):

		# Initialize the QDialog Class that this Class Inherits from
		QtGui.QDialog.__init__( self, parent );

		# Create a Local Copy of the Main Window's self Object to Modify/Call the Containing Main Window Instance
		self.mainWindowReference = mainWindow;

		
		## CREATE THE PLOT OBJECTS
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		self.ImagePlotObject       			= PlotWidgetClass( mainWindow= self.mainWindowReference );
		
		self.RecurrencePlotObject     		= PlotWidgetClass( mainWindow= self.mainWindowReference );
		self.RecurrenceStatsPlotObject		= PlotWidgetClass( mainWindow= self.mainWindowReference );
		
		self.ReoccurrencePlotObject   		= PlotWidgetClass( mainWindow= self.mainWindowReference );
		self.ReoccurrenceStatsPlotObject	= PlotWidgetClass( mainWindow= self.mainWindowReference );
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		
		

		## CREATE THE BUTTON OBJECTS
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		self.buttOpenImageFile = QtGui.QPushButton( "Open Files..." );
		
		self.buttOpenImageFile.pressed.connect( self.OpenImageFileFunction );
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		


		## SETUP AND APPLY THE LAYOUT FOR THE OBJECTS
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		MainWindowLayoutObject = QtGui.QHBoxLayout();

		InputButtsLayoutObject = QtGui.QHBoxLayout();
		InputButtsLayoutObject.addWidget( self.buttOpenImageFile );
		
		InputDataLayoutObject = QtGui.QVBoxLayout();
		InputDataLayoutObject.addLayout( InputButtsLayoutObject );
		InputDataLayoutObject.addStretch( 1 );
		InputDataLayoutObject.addWidget( self.ImagePlotObject );

		RecurrencePlotsLayoutObject = QtGui.QVBoxLayout();
		RecurrencePlotsLayoutObject.addWidget( self.RecurrencePlotObject );
		RecurrencePlotsLayoutObject.addWidget( self.RecurrenceStatsPlotObject );

		ReoccurrencePlotsLayoutObject = QtGui.QVBoxLayout();
		ReoccurrencePlotsLayoutObject.addWidget( self.ReoccurrencePlotObject );
		ReoccurrencePlotsLayoutObject.addWidget( self.ReoccurrenceStatsPlotObject );

		MainWindowLayoutObject.addLayout( InputDataLayoutObject );
		MainWindowLayoutObject.addLayout( RecurrencePlotsLayoutObject );
		MainWindowLayoutObject.addLayout( ReoccurrencePlotsLayoutObject );

		self.setLayout( MainWindowLayoutObject );
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



	## FUNCTION FOR OPENING AND PARSING THE IMAGE FILE TO PLOT
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OpenImageFileFunction( self ):

		( self.openedImageFileName, _ ) = QtGui.QFileDialog.getOpenFileName( self,
																	  		 caption= 	"Open Image File...",
																	  		 dir=		"./",
																	  		 filter=	"*.png;*.jpeg;*.jpg;*.tiff;*.tif;*.pdf;*.svg" );


		self.ImageObject = Image.open( self.openedImageFileName );

		self.OpenDataFileFunction();

		self.mainWindowReference.resize( self.screenSize[0], self.screenSize[1] );
		self.mainWindowReference.move( 0, 0 );
		QtCore.QCoreApplication.processEvents();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



	## FUNCTION FOR OPENING AND PARSING THE DATA FILE TO PLOT
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OpenDataFileFunction( self ):

		( self.openedDataFileName, _ ) = QtGui.QFileDialog.getOpenFileName( self,
																	  		caption= 	"Open Eye-Tracking Data File...",
																	  		dir=		"./",
																	  		filter=		"*.txt;*.csv" );

		dataFileObject = open( self.openedDataFileName, 'r' );

		dataFileRowStringsList = dataFileObject.readlines();

		numHeaderLines = 1;

		self.numFixations = ( len( dataFileRowStringsList ) - numHeaderLines );

		self.fixationPositionsX = [];
		self.fixationPositionsY = [];

		self.fixationDurations = [];

		for currentRowString in ( dataFileRowStringsList[ numHeaderLines : : 1 ] ):

			currentRowDataList = ( currentRowString[ 0 : -1 : 1 ] ).split( ',' );

			self.fixationPositionsX.append( float(currentRowDataList[0]) );
			self.fixationPositionsY.append( float(currentRowDataList[1]) );

			self.fixationDurations.append( float(currentRowDataList[2]) );

		#rof


		self.fixationDurationsScaled = [];

		maxFixationDuration = max( self.fixationDurations );

		for i in range( 0, self.numFixations, 1 ):

			scaledFixation = ( ( float( self.fixationDurations[i] ) / float( maxFixationDuration ) ) * self.ImageObject.size[1] );

			self.fixationDurationsScaled.append( scaledFixation );

		#rof


		self.ImagePlotObject.newImageScatterPlot( imageObject= 		self.ImageObject,
												  xData= 			self.fixationPositionsX,
												  yData= 			self.fixationPositionsY,
												  markerSizeData= 	self.fixationDurationsScaled );

		QtCore.QCoreApplication.processEvents();

		self.screenSize = ( QtGui.QApplication.desktop().screen().rect().width(),
							QtGui.QApplication.desktop().screen().rect().height() );
		
		self.CalculateAndPlotRecurrenceFunction();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



	## FUNCTION FOR CALCULATING AND PLOTTING THE RECURRENCE DATA AND STATS
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def CalculateAndPlotRecurrenceFunction( self ):

		( self.TimeDelayValue, _ ) = QtGui.QInputDialog.getText( self,
															 	 "User's Choice",
															 	 "Enter the desired Time-Delay Value\n(Step-Size Between Sequence Samples)" );


		self.TimeDelayValue = int( self.TimeDelayValue );

		self.TimeSeriesData = [];

		for i in range( 0, self.numFixations, 1 ):

			self.TimeSeriesData.append( ( self.fixationPositionsX[i], self.fixationPositionsY[i] ) );

		#rof

		self.TimeSeriesDimensions = len( self.TimeSeriesData[0] );

		self.minEmbeddingSequenceLength = int( math.ceil( ( (2.0 * self.TimeSeriesDimensions) + 1.0 ) / float(self.TimeSeriesDimensions) ) );

		( self.NumTimeDelaySamples, _ ) = QtGui.QInputDialog.getText( self,
																  	  "User's Choice",
																  	  "Enter the desired Time-Delay Sequence Length\n(Number of Sequence Samples; Minimum: " +
																  	  str( self.minEmbeddingSequenceLength )  + ")" );


		( self.PhaseSpaceClusteringThreshold, _ ) = QtGui.QInputDialog.getText( self,
																				"User's Choice",
																				"Enter the desired Threshold on Phase-Space Distance\n(Clustering Threshold in Range [0,1])" );


		self.NumTimeDelaySamples = int( self.NumTimeDelaySamples );
		self.PhaseSpaceClusteringThreshold = float( self.PhaseSpaceClusteringThreshold );


		self.FixationsXYPhaseSpaceData = RecurrenceFunctions.TimeDelayEmbedding( timeSeriesObservations= 	self.TimeSeriesData,
																			  	 delayStep= 				self.TimeDelayValue,
																			  	 delaySamples= 				self.NumTimeDelaySamples );

		self.RecurrenceMatrixData = RecurrenceFunctions.CreateRecurrenceMatrix( phaseSpaceData= 				self.FixationsXYPhaseSpaceData,
													   							clusteringDistanceThreshold= 	self.PhaseSpaceClusteringThreshold );

		self.Recurrence = RecurrenceFunctions.getRecurrence( self.RecurrenceMatrixData, self.NumTimeDelaySamples );
		
		self.RecurrenceRate = RecurrenceFunctions.getRecurrenceRate( self.RecurrenceMatrixData, self.NumTimeDelaySamples );
		
		( self.RecurrenceMeanX, self.RecurrenceMeanY ) = RecurrenceFunctions.getRecurrenceMean( self.RecurrenceMatrixData, self.NumTimeDelaySamples );

		( self.RecurrenceStandardDeviationX, self.RecurrenceStandardDeviationY ) = RecurrenceFunctions.getRecurrenceStandardDeviation( self.RecurrenceMatrixData, self.NumTimeDelaySamples );

		
		self.RecurrencePlotObject.newDotPlot( dotMatrix= self.RecurrenceMatrixData,
											  plotTitle= "Recurrence Plot",
											  offset=	   self.NumTimeDelaySamples );


		# valueNames= [ r'\rho', r'\bar{\rho}', r'\mu_{x}', r'\mu_{y}', r'\sigma_{x}', r'\sigma_{y}' ],
		self.RecurrenceStatsPlotObject.newBarPlot( valueNames= [ 'r', 'rAvg', 'u-x', 'u-y', 's-x', 's-y' ],
												   barHeights= [ self.Recurrence,
												   			   	 self.RecurrenceRate,
												   			   	 self.RecurrenceMeanX,
												   			   	 self.RecurrenceMeanY,
												   			   	 self.RecurrenceStandardDeviationX,
												   			   	 self.RecurrenceStandardDeviationY ],
												   plotTitle=  "Recurrence Quantification Measures (Statistics)",
												   barTitles=  [ '', '', '', '', '', '' ] );

		QtCore.QCoreApplication.processEvents();
		self.mainWindowReference.refreshGUI();
		QtCore.QCoreApplication.processEvents();
		self.CalculateAndPlotReoccurrenceFunction();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



	## FUNCTION FOR CALCULATING AND PLOTTING THE REOCCURRENCE DATA AND STATS
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def CalculateAndPlotReoccurrenceFunction( self ):

		( self.FixationSpaceDistanceRadius, _ ) = QtGui.QInputDialog.getText( self,
																			  "User's Choice",
																			  "Enter the desired Pixel Radius\n(For Fixation Clustering)" );


		self.FixationSpaceDistanceRadius = int( self.FixationSpaceDistanceRadius );

		self.ReoccurrenceMatrixData = ReoccurrenceFunctions.CreateReoccurrenceMatrix( positionData= 				self.TimeSeriesData,
																					  clusteringDistanceThreshold= 	self.FixationSpaceDistanceRadius );

		self.Reoccurrence = ReoccurrenceFunctions.getReoccurrence( self.ReoccurrenceMatrixData );
		
		self.ReoccurrenceRate = ReoccurrenceFunctions.getReoccurrenceRate( self.ReoccurrenceMatrixData );
		
		self.ReoccurrenceDeterminism = ReoccurrenceFunctions.getDeterminism( self.ReoccurrenceMatrixData );

		self.ReoccurrenceLaminarity = ReoccurrenceFunctions.getLaminarity( self.ReoccurrenceMatrixData );

		self.ReoccurrenceCORM = ReoccurrenceFunctions.getCORM( self.ReoccurrenceMatrixData );

		
		self.ReoccurrencePlotObject.newDotPlot( dotMatrix= self.ReoccurrenceMatrixData,
												plotTitle= "Reoccurrence Plot" );

		self.ReoccurrenceStatsPlotObject.newBarPlot( valueNames= [ 'R', 'REC', 'DET', 'LAM', 'CORM' ],
													 barHeights= [ self.Reoccurrence,
													 			   self.ReoccurrenceRate,
													 			   self.ReoccurrenceDeterminism,
													 			   self.ReoccurrenceLaminarity,
													 			   self.ReoccurrenceCORM ],
													 plotTitle=  "Reoccurrence Quantification Measures",
													 barTitles=	 [ '[#]', '[%]', '[%]', '[%]', '[%]' ] );

		QtCore.QCoreApplication.processEvents();
		self.mainWindowReference.refreshGUI();
		QtCore.QCoreApplication.processEvents();

		return ( None );
	#fed -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#ssalc -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	

## THE MAIN APPLICATION CALL
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if ( __name__ == '__main__' ):
	
	# CREATE AN INSTANCE OF A QT APPLICATION (OUR PLOTTING GUI)
	CurrentQtApplication = QtGui.QApplication( [] );

   
	# CREATE AN INSTANCE OF THE GUI CLASS
	NewRecurrencePlottingWindow = MainWindowClass();

	
	# DISPLAY THE WINDOW AND BRING IT TO THE FRONT OF ALL THE OTHER WINDOWS
	NewRecurrencePlottingWindow.show();
	NewRecurrencePlottingWindow.activateWindow();
	NewRecurrencePlottingWindow.raise_();
	

	# SET THE Qt APPLICATION TO CALL ITSELF TO CLOSE WHEN THIS PYTHON APPLICATION CLOSES
	sys.exit( CurrentQtApplication.exec_() );
#fi ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
