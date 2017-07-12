#Script to train neural network to play 2048
#Qlearning Neural Network Adapted from code by Arthur Juliani 
"""https://medium.com/emergent-future/simple-reinforcement
-learning-with-tensorflow-part-0-q-learning-with-tables
-and-neural-networks-d195264329d0"""

#for 2048
import random as rand
import time as time
import math 

#Argument parsing
import sys 

#for reinforcement training
import numpy as np
import tensorflow as tf

#Constants for 2048 
DIMEN      = 4
QUIT       = 'q'
EMPTY      = -1
BORDER     = "-----------------"
SPACE      = "____"
EMPTY_ROW  = "|                 |"
UP         = 'w'
DOWN       = 's'
LEFT       = 'a'
RIGHT      = 'd'

#Instance Variables
board     = np.array([[0 for x in range(DIMEN)] for y in range(DIMEN)], np.int32)
highestScore = np.array([0 for x in range(1)], np.int32)
lastTenScores = np.array([0 for x in range(10)], np.int32)
lastHundredScores = np.array([0 for x in range(100)], np.int32)
lastTenTotals = np.array([0 for x in range(10)], np.int32)
lastHundredTotals = np.array([0 for x in range(100)], np.int32)
rand.seed(time.time())
xPlot = list()
yPlot = list()
xPlot2 = list()
yPlot2 = list()
scores = {} 
scores["prevHigh"] = 0 
scores["prevTotal"] = 0 
scores["currHigh"] = 0 
scores["currTotal"] = 0 
rateOfDecrease = 50 #Rate of decrease in random choice (Higher = slower rate)

#Formatting information for cmbl file (For viewing results in Logger Pro)
cmblFmt1 = """<Document>
  <FileCoherence>1</FileCoherence>
  <Version>3.10.1</Version>
  <charset>utf-8</charset>
  <ApplicationBuildDateTime>Aug 27 2015 10:30:01</ApplicationBuildDateTime>
  <FileName>test.cmbl</FileName>
  <FileIDString>7/8/17 23:31CBass4232452451016993851</FileIDString>
  <CreatorOS>1</CreatorOS>
  <CreatorApp>1</CreatorApp>
  <AbsoluteVersion>1</AbsoluteVersion>
  <Radians>1</Radians>
  <NumDerivativePoints>7</NumDerivativePoints>
  <NumSmoothingPoints>7</NumSmoothingPoints>
  <ShowZeroOnToolbar>0</ShowZeroOnToolbar>
  <ShowDataMarkOnToolbar>0</ShowDataMarkOnToolbar>
  <ShowGraphMatchOnToolbar>0</ShowGraphMatchOnToolbar>
  <GraphMatchUseConstant>1</GraphMatchUseConstant>
  <GraphMatchUseLinear>1</GraphMatchUseLinear>
  <GraphMatchUseQuadratic>1</GraphMatchUseQuadratic>
  <GraphMatchNumSections>0</GraphMatchNumSections>
  <Stationery>0</Stationery>
  <CreationDateTime>7/8/17 23:31</CreationDateTime>
  <ModifiedDateTime>7/8/17 23:53</ModifiedDateTime>
  <PageBounds>0 0 19.7777777778 10.8472222222</PageBounds>
  <ScreenResolution>0 0 1440 900</ScreenResolution>
  <MathType>0</MathType>
  <AllowOptionsDialogs>1</AllowOptionsDialogs>
  <AllowAutoCurveFit>1</AllowAutoCurveFit>
  <ReplayWindowPosition>0 68 389 466 570 1</ReplayWindowPosition>
  <ReplayWindowSpeed>1</ReplayWindowSpeed>
  <ReplayWindowRepeat>0</ReplayWindowRepeat>
  <SensorConflictEnabled>1</SensorConflictEnabled>
  <MathConstantValue>3.141592653590</MathConstantValue>
  <MathConstantNumPlaces>3</MathConstantNumPlaces>
  <MathConstantIncrement>1.000000000000</MathConstantIncrement>
  <MathConstantEditable>0</MathConstantEditable>
  <MathConstantUnits></MathConstantUnits>
  <MathConstantName>pi</MathConstantName>
  <Page>
    <ID>100 </ID>
    <BroadcastTo>0 </BroadcastTo>
    <Visible>1</Visible>
    <PageTitle></PageTitle>
    <PageColor>0xcccc 0xcccc 0xffff| 0xffff 0x1d</PageColor>
    <PageDisplayPageInfo>0 </PageDisplayPageInfo>
    <PagePageInfo></PagePageInfo>
    <PageGraphPaper>0 </PageGraphPaper>
    <PageGraphPaperLineSpacing>0.25 </PageGraphPaperLineSpacing>
    <PageGraphPaperLineColor>0x8484 0x7070 0xffff| 0xffff 0x1e</PageGraphPaperLineColor>
    <PageReplayWindowPosition>0 68 389 466 570</PageReplayWindowPosition>
    <PageTable>
      <ID>107 </ID>
      <BroadcastTo>0 </BroadcastTo>
      <Visible>1</Visible>
      <Bounds>0.015 0.015 2.44387586806 10.8322222222 </Bounds>
      <SubordinateToID>0</SubordinateToID>
      <SubordinateOffset>0 0</SubordinateOffset>
      <BackgroundTransparent>0</BackgroundTransparent>
      <BackgroundColor>0x0 0x0 0x0| 0xffff 0xfffffffb</BackgroundColor>
      <AddNewData>1</AddNewData>
      <Locked>0</Locked>
      <AutoCreated>0</AutoCreated>
      <GraphLinkedIDs>0 </GraphLinkedIDs>
      <YLinkedIDs>0 </YLinkedIDs>
      <Font>
        <Size> 12 </Size>
        <Justification> 2 </Justification>
        <VerticalJustification> 0 </VerticalJustification>
        <Styles> 0 0 0 0 0 0 </Styles>
        <Family> 3 </Family>
        <Color>0x0 0x0 0x0| 0xffff 0x0</Color>
        <Name>System Font Regular</Name>
        <Rotation>0</Rotation>
      </Font>
      <TableColumn> 102 0.8 </TableColumn>
      <TableColumn> 104 0.8 </TableColumn>
      <StartIndex> 24 </StartIndex>
      <DisplayBlackAndWhite> 0 </DisplayBlackAndWhite>
    </PageTable>
    <PageGraphCartesian>
      <ID>106 </ID>
      <BroadcastTo>1 108 </BroadcastTo>
      <Visible>1</Visible>
      <Bounds>2.47887586806 0.02 19.7577777778 10.8272222222 </Bounds>
      <SubordinateToID>0</SubordinateToID>
      <SubordinateOffset>0 0</SubordinateOffset>
      <BackgroundTransparent>0</BackgroundTransparent>
      <BackgroundColor>0xffff 0xffff 0xffff| 0xffff 0x0</BackgroundColor>
      <AddNewData>0</AddNewData>
      <Locked>0</Locked>
      <AutoCreated>1</AutoCreated>
      <GraphLinkedIDs>0 </GraphLinkedIDs>
      <YLinkedIDs>0 </YLinkedIDs>
      <Font>
        <Size> 12 </Size>
        <Justification> 0 </Justification>
        <VerticalJustification> 0 </VerticalJustification>
        <Styles> 0 0 0 0 0 0 </Styles>
        <Family> 3 </Family>
        <Color>0x0 0x0 0x0| 0xffff 0x0</Color>
        <Name>System Font Regular</Name>
        <Rotation>0</Rotation>
      </Font>
      <GraphTitle></GraphTitle>
      <GraphTitleColor>0x0 0x0 0x0| 0xffff 0x2e</GraphTitleColor>
      <GraphShowPoints>0</GraphShowPoints>
      <GraphInterpolate>0</GraphInterpolate>
      <GraphShowTangent>0</GraphShowTangent>
      <GraphShowLegend>0</GraphShowLegend>
      <GraphShowCursorStatus>1</GraphShowCursorStatus>
      <GraphShowCursorDelta>1</GraphShowCursorDelta>
      <GraphPlotBaseColumnID>102 </GraphPlotBaseColumnID>
      <GraphPlotTraceIDPairs>2 102 104 102 110 </GraphPlotTraceIDPairs>
      <LogXAxis>0</LogXAxis>
      <LogYAxis>0</LogYAxis>
      <LogRightYAxis>0</LogRightYAxis>
      <GraphShowTraceErrorBars>1</GraphShowTraceErrorBars>
      <GraphShowBaseErrorBars>1</GraphShowBaseErrorBars>
      <GraphShowUncertaintyBoxes>0</GraphShowUncertaintyBoxes>
      <GraphConnectLines>0</GraphConnectLines>
      <GraphBarGraph>0</GraphBarGraph>
      <BinGraphStackColumns>0</BinGraphStackColumns>
      <GraphShowPointProtectors>1</GraphShowPointProtectors>
      <GraphMajorTickStyle>1</GraphMajorTickStyle>
      <GraphMajorTickColor>0xc0c0 0xc0c0 0xc0c0| 0xffff 0x2b</GraphMajorTickColor>
      <GraphMinorTickStyle>0</GraphMinorTickStyle>
      <GraphMinorTickColor>0xc0c0 0xc0c0 0xc0c0| 0xffff 0x2b</GraphMinorTickColor>
      <GraphPlotXAutoscale>2</GraphPlotXAutoscale>
      <GraphPlotYAutoscale>3</GraphPlotYAutoscale>
      <GraphPlotDoubleYAutoscale>3</GraphPlotDoubleYAutoscale>
      <GraphPlotXAutoscaleOnFirstData>0</GraphPlotXAutoscaleOnFirstData>
      <GraphPlotYAutoscaleOnFirstData>0</GraphPlotYAutoscaleOnFirstData>
      <GraphPlotDoubleYAutoscaleOnFirstData>0</GraphPlotDoubleYAutoscaleOnFirstData>
      <GraphPlotXAutoscaleHint>0</GraphPlotXAutoscaleHint>
      <GraphPlotYAutoscaleHint>0</GraphPlotYAutoscaleHint>
      <GraphPlotDoubleYAutoscaleHint>0</GraphPlotDoubleYAutoscaleHint>
      <GraphPlotXMin>0</GraphPlotXMin>
      <GraphPlotXMax>60</GraphPlotXMax>
      <GraphPlotXTicksRotatedAngle>0</GraphPlotXTicksRotatedAngle>
      <ShowAllValuesAsMajorTicks>0</ShowAllValuesAsMajorTicks>
      <GraphPlotYMin>0</GraphPlotYMin>
      <GraphPlotYMax>120</GraphPlotYMax>
      <GraphPlotDefaultXMin>0</GraphPlotDefaultXMin>
      <GraphPlotDefaultXMax>60</GraphPlotDefaultXMax>
      <GraphPlotDefaultYMin>0</GraphPlotDefaultYMin>
      <GraphPlotDefaultYMax>100</GraphPlotDefaultYMax>
      <GraphPlotXLabel></GraphPlotXLabel>
      <GraphPlotYLabel></GraphPlotYLabel>
      <GraphDrawRainbow>0</GraphDrawRainbow>
      <AudioTraceIDs>2 104 110 </AudioTraceIDs>
      <GraphPlotDoubleYAxis>0</GraphPlotDoubleYAxis>
    </PageGraphCartesian>
    <PageHelperDataCurveFit>
      <ID>108 </ID>
      <BroadcastTo>0 </BroadcastTo>
      <Visible>1</Visible>
      <Bounds>9.52797526042 3.80949652778 11.3010397135 5.63282986111 </Bounds>
      <SubordinateToID>106</SubordinateToID>
      <SubordinateOffset>7.04909939236 3.78949652778</SubordinateOffset>
      <BackgroundTransparent>0</BackgroundTransparent>
      <BackgroundColor>0xffff 0xffff 0xffff| 0xffff 0x0</BackgroundColor>
      <AddNewData>0</AddNewData>
      <Locked>0</Locked>
      <AutoCreated>0</AutoCreated>
      <GraphLinkedIDs>0 </GraphLinkedIDs>
      <YLinkedIDs>0 </YLinkedIDs>
      <Font>
        <Size> 10 </Size>
        <Justification> 0 </Justification>
        <VerticalJustification> 0 </VerticalJustification>
        <Styles> 0 0 0 0 0 0 </Styles>
        <Family> 3 </Family>
        <Color>0x0 0x0 0x0| 0xffff 0x0</Color>
        <Name>System Font Regular</Name>
        <Rotation>0</Rotation>
      </Font>
      <GUIHelperRangeMin>0</GUIHelperRangeMin>
      <GUIHelperRangeMax>60</GUIHelperRangeMax>
      <GUIHelperTraceColumnID>104</GUIHelperTraceColumnID>
      <GUIHelperBaseColumnID>102</GUIHelperBaseColumnID>
      <GUIHelperPrecision>4</GUIHelperPrecision>
      <GUIHelperPrecisionDecimal>0</GUIHelperPrecisionDecimal>
      <GUIHelperMinimized>0</GUIHelperMinimized>
      <GUIHelperUseEntireRange>0</GUIHelperUseEntireRange>
      <GUIHelperUnderlyingHistogramFFTColumnID>0</GUIHelperUnderlyingHistogramFFTColumnID>
      <CurveFitFunctionID>110</CurveFitFunctionID>
      <CurveFitColumnID>0</CurveFitColumnID>
      <CurveFitError>7.99204014504</CurveFitError>
      <CurveFitMethod>1</CurveFitMethod>
      <CurveFitUncertainty>0</CurveFitUncertainty>
      <ManualCurveFitIncrements>0 </ManualCurveFitIncrements>
      <ManualCurveFitShowRMSE>1</ManualCurveFitShowRMSE>
      <ManualCurveFitWeightColumnId>4294967295</ManualCurveFitWeightColumnId>
      <CurveFitCorrelation>0.206432441322</CurveFitCorrelation>
    </PageHelperDataCurveFit>
  </Page>
  <CurrentPageIndex>0</CurrentPageIndex>
  <DataSet>
    <ID>101 </ID>
    <BroadcastTo>1 107 </BroadcastTo>
    <Visible>1</Visible>
    <DataSetName>Data Set</DataSetName>
    <DataSetComments></DataSetComments>
    <DataSetPosition>0</DataSetPosition>
    <DataSetSourceName></DataSetSourceName>
    <DataSetShowInDataBrowser>1</DataSetShowInDataBrowser>
    <DataSetHistogram>0</DataSetHistogram>
    <DataSetFFT>0</DataSetFFT>
    <DataSetLatest>0</DataSetLatest>
    <DataSetAutoCreated>1</DataSetAutoCreated>
    <DataSetStoredRun>0</DataSetStoredRun>
    <DataSetPrediction>0</DataSetPrediction>
    <DataSetVideoAnalysis>0</DataSetVideoAnalysis>
    <DataSetGraphMatch>0</DataSetGraphMatch>
    <Metadata>
      <DataMark>
      </DataMark>
      <DataTag>
      </DataTag>
    </Metadata>
    <DataColumn>
      <ID>102 </ID>
      <BroadcastTo>3 17 106 107 </BroadcastTo>
      <Visible>1</Visible>
      <DataObjectName>X</DataObjectName>
      <DataObjectShortName>x</DataObjectShortName>
      <DataObjectColor>0x0 0x0 0x0| 0xffff 0x0</DataObjectColor>
      <DataObjectDataSource>0</DataObjectDataSource>
      <DataObjectPrecisionDecimal>1</DataObjectPrecisionDecimal>
      <DataObjectPrecision>0</DataObjectPrecision>
      <DataObjectAutomaticDecimal>1</DataObjectAutomaticDecimal>
      <DataObjectThickLines>0</DataObjectThickLines>
      <ColumnUnits></ColumnUnits>
      <ColumnProtected>0</ColumnProtected>
      <ColumnUserEditable>1</ColumnUserEditable>
      <ColumnTreatAsText>0</ColumnTreatAsText>
      <ColumnDataType>0</ColumnDataType>
      <StartTime>1499571093</StartTime>
      <TimeOfDayFormat>hh:mm:ss</TimeOfDayFormat>
      <ColumnGeoRole>n-a</ColumnGeoRole>
      <ColumnGeoDisplay>DD</ColumnGeoDisplay>
      <ColumnUserCreated>1</ColumnUserCreated>
      <ColumnPPStyle>9</ColumnPPStyle>
      <ColumnPPSize>2</ColumnPPSize>
      <ColumnDisplayPPInterval>1</ColumnDisplayPPInterval>
      <ColumnDisplayPPIntervalAuto>0</ColumnDisplayPPIntervalAuto>
      <ColumnDisplayPPFromColumn>0</ColumnDisplayPPFromColumn>
      <ColumnDisplayPPColumnID>0</ColumnDisplayPPColumnID>
      <ColumnUseErrorCalculations>0</ColumnUseErrorCalculations>
      <ColumnErrorFixed>1</ColumnErrorFixed>
      <ColumnErrorConstant>1</ColumnErrorConstant>
      <ColumnErrorValue>0</ColumnErrorValue>
      <ColumnErrorColumnID>0</ColumnErrorColumnID>
      <ColumnForceScientific>0</ColumnForceScientific>
      <ColumnSensorColumn>0</ColumnSensorColumn>
      <ColumnSensorInputColumn>0</ColumnSensorInputColumn>
      <ColumnAllowUserDelete>1</ColumnAllowUserDelete>
      <ColumnMatchTag></ColumnMatchTag>
      <ColumnStartCollectTime>0</ColumnStartCollectTime>
      <ColumnGenerateValues>0</ColumnGenerateValues>
      <ColumnGenerateType>0</ColumnGenerateType>
      <ColumnStart>1</ColumnStart>
      <ColumnEnd>100</ColumnEnd>
      <ColumnIncrement>1</ColumnIncrement>
      <ColumnNameStart>0</ColumnNameStart>
      <ColumnNumber>10</ColumnNumber>
      <ColumnShowLiveReadout>0</ColumnShowLiveReadout>
      <ColumnLastDataCollectedMode>0</ColumnLastDataCollectedMode>
      <ColumnGroupID>103</ColumnGroupID>
      <ColumnCells>"""

cmblFmt2 = """</ColumnCells>
    </DataColumn>
    <DataColumn>
      <ID>104 </ID>
      <BroadcastTo>3 17 106 107 </BroadcastTo>
      <Visible>1</Visible>
      <DataObjectName>Y</DataObjectName>
      <DataObjectShortName>y</DataObjectShortName>
      <DataObjectColor>0xffff 0x0 0x3333| 0xffff 0x0</DataObjectColor>
      <DataObjectDataSource>0</DataObjectDataSource>
      <DataObjectPrecisionDecimal>1</DataObjectPrecisionDecimal>
      <DataObjectPrecision>0</DataObjectPrecision>
      <DataObjectAutomaticDecimal>1</DataObjectAutomaticDecimal>
      <DataObjectThickLines>0</DataObjectThickLines>
      <ColumnUnits></ColumnUnits>
      <ColumnProtected>0</ColumnProtected>
      <ColumnUserEditable>1</ColumnUserEditable>
      <ColumnTreatAsText>0</ColumnTreatAsText>
      <ColumnDataType>0</ColumnDataType>
      <StartTime>1499571093</StartTime>
      <TimeOfDayFormat>hh:mm:ss</TimeOfDayFormat>
      <ColumnGeoRole>n-a</ColumnGeoRole>
      <ColumnGeoDisplay>DD</ColumnGeoDisplay>
      <ColumnUserCreated>1</ColumnUserCreated>
      <ColumnPPStyle>8</ColumnPPStyle>
      <ColumnPPSize>2</ColumnPPSize>
      <ColumnDisplayPPInterval>1</ColumnDisplayPPInterval>
      <ColumnDisplayPPIntervalAuto>0</ColumnDisplayPPIntervalAuto>
      <ColumnDisplayPPFromColumn>0</ColumnDisplayPPFromColumn>
      <ColumnDisplayPPColumnID>0</ColumnDisplayPPColumnID>
      <ColumnUseErrorCalculations>0</ColumnUseErrorCalculations>
      <ColumnErrorFixed>1</ColumnErrorFixed>
      <ColumnErrorConstant>1</ColumnErrorConstant>
      <ColumnErrorValue>0</ColumnErrorValue>
      <ColumnErrorColumnID>0</ColumnErrorColumnID>
      <ColumnForceScientific>0</ColumnForceScientific>
      <ColumnSensorColumn>0</ColumnSensorColumn>
      <ColumnSensorInputColumn>0</ColumnSensorInputColumn>
      <ColumnAllowUserDelete>1</ColumnAllowUserDelete>
      <ColumnMatchTag></ColumnMatchTag>
      <ColumnStartCollectTime>0</ColumnStartCollectTime>
      <ColumnGenerateValues>0</ColumnGenerateValues>
      <ColumnGenerateType>0</ColumnGenerateType>
      <ColumnStart>1</ColumnStart>
      <ColumnEnd>100</ColumnEnd>
      <ColumnIncrement>1</ColumnIncrement>
      <ColumnNameStart>0</ColumnNameStart>
      <ColumnNumber>10</ColumnNumber>
      <ColumnShowLiveReadout>0</ColumnShowLiveReadout>
      <ColumnLastDataCollectedMode>0</ColumnLastDataCollectedMode>
      <ColumnGroupID>105</ColumnGroupID>
      <ColumnCells>"""

cmblFmt3 = """</ColumnCells>
    </DataColumn>
  </DataSet>
  <DataSet>
    <ID>109 </ID>
    <BroadcastTo>0 </BroadcastTo>
    <Visible>1</Visible>
    <DataSetName>&#38;&#38;^% CurveFitFunctions %^&#38;&#38;</DataSetName>
    <DataSetComments></DataSetComments>
    <DataSetPosition>1</DataSetPosition>
    <DataSetSourceName></DataSetSourceName>
    <DataSetShowInDataBrowser>0</DataSetShowInDataBrowser>
    <DataSetHistogram>0</DataSetHistogram>
    <DataSetFFT>0</DataSetFFT>
    <DataSetLatest>0</DataSetLatest>
    <DataSetAutoCreated>0</DataSetAutoCreated>
    <DataSetStoredRun>0</DataSetStoredRun>
    <DataSetPrediction>0</DataSetPrediction>
    <DataSetVideoAnalysis>0</DataSetVideoAnalysis>
    <DataSetGraphMatch>0</DataSetGraphMatch>
    <Metadata>
      <DataMark>
      </DataMark>
      <DataTag>
      </DataTag>
    </Metadata>
    <FunctionModel>
      <ID>110 </ID>
      <BroadcastTo>1 106 </BroadcastTo>
      <Visible>1</Visible>
      <DataObjectName>mx+b</DataObjectName>
      <DataObjectShortName>mx+b</DataObjectShortName>
      <DataObjectColor>0x0 0x0 0x0| 0xffff 0x2e</DataObjectColor>
      <DataObjectDataSource>0</DataObjectDataSource>
      <DataObjectPrecisionDecimal>0</DataObjectPrecisionDecimal>
      <DataObjectPrecision>4</DataObjectPrecision>
      <DataObjectAutomaticDecimal>0</DataObjectAutomaticDecimal>
      <DataObjectThickLines>0</DataObjectThickLines>
      <FunctionModelPower>1</FunctionModelPower>
      <FunctionModelString>m*x+b</FunctionModelString>
      <FunctionModelLinear>1</FunctionModelLinear>
      <FunctionModelType>1</FunctionModelType>
      <FunctionCoefficientArray>2 0.0941829719725 102.387625595 </FunctionCoefficientArray>
      <FunctionCoefficientUncertaintyArray>2 0.0581181648284 2.02164351715 </FunctionCoefficientUncertaintyArray>
      <FunctionModelParameterNames>m
b
</FunctionModelParameterNames>
      <FunctionModelTimeOffset>0</FunctionModelTimeOffset>
      <FunctionModelTimeOffsetValue>0</FunctionModelTimeOffsetValue>
    </FunctionModel>
  </DataSet>
  <DataSourceServer>
    <ID>13 </ID>
    <BroadcastTo>0 </BroadcastTo>
    <Visible>1</Visible>
  </DataSourceServer>
  <MBLBrain>
    <MBLCollectionUserCollectMode>0</MBLCollectionUserCollectMode>
    <MBLCollectionDropCounterMode>0</MBLCollectionDropCounterMode>
    <MBLCollectionTimeUnit>1</MBLCollectionTimeUnit>
    <MBLCollectionSampleAtZero>1</MBLCollectionSampleAtZero>
    <MBLCollectionRepeat>0</MBLCollectionRepeat>
    <MBLCollectionEnhancedTiming>0</MBLCollectionEnhancedTiming>
    <MBLFastStart>0</MBLFastStart>
    <MBLCollectionDeltaT>1</MBLCollectionDeltaT>
    <MBLCollectionNumSamples>11</MBLCollectionNumSamples>
    <MBLCollectionMaxDuration>10</MBLCollectionMaxDuration>
    <MBLCollectionOversampling>1</MBLCollectionOversampling>
    <MBLCollectionNumEWEColumns>1</MBLCollectionNumEWEColumns>
    <MBLColumnHeader>
      <MBLColumnHeaderName>Entry</MBLColumnHeaderName>
      <MBLColumnHeaderShortName>Entry</MBLColumnHeaderShortName>
      <MBLColumnHeaderUnits></MBLColumnHeaderUnits>
    </MBLColumnHeader>
    <MBLColumnHeader>
      <MBLColumnHeaderName></MBLColumnHeaderName>
      <MBLColumnHeaderShortName></MBLColumnHeaderShortName>
      <MBLColumnHeaderUnits></MBLColumnHeaderUnits>
    </MBLColumnHeader>
    <MBLColumnHeader>
      <MBLColumnHeaderName></MBLColumnHeaderName>
      <MBLColumnHeaderShortName></MBLColumnHeaderShortName>
      <MBLColumnHeaderUnits></MBLColumnHeaderUnits>
    </MBLColumnHeader>
    <MBLCollectionSelectedEventTime>0</MBLCollectionSelectedEventTime>
    <MBLCollectionSelectedEventName>Event Number</MBLCollectionSelectedEventName>
    <MBLCollectionSelectedEventShortName>Event</MBLCollectionSelectedEventShortName>
    <MBLCollectionSelectedEventUnits></MBLCollectionSelectedEventUnits>
    <MBLCollectionEndDigitalAfterNum>0</MBLCollectionEndDigitalAfterNum>
    <MBLCollectionNumDigitalEvents>10</MBLCollectionNumDigitalEvents>
    <MBLCollectionTriggerEnabled>0</MBLCollectionTriggerEnabled>
    <MBLTriggerType>0</MBLTriggerType>
    <MBLTriggerValue>0</MBLTriggerValue>
    <MBLTriggerUseConstant>0</MBLTriggerUseConstant>
    <MBLTriggerConstant></MBLTriggerConstant>
    <MBLTriggerPreTriggerData>0</MBLTriggerPreTriggerData>
    <MBLRadiationInterval>5</MBLRadiationInterval>
    <MBLRadiationIntervalTimeUnit>1</MBLRadiationIntervalTimeUnit>
    <MBLStoreLatestMax>0</MBLStoreLatestMax>
    <MBLEWEAverageData>0</MBLEWEAverageData>
    <MBLSEAverageData>0</MBLSEAverageData>
    <MBLContinuous>0</MBLContinuous>
    <MBLCollectionMiniGCStartTemp>35</MBLCollectionMiniGCStartTemp>
    <MBLCollectionMiniGCHoldTime>2</MBLCollectionMiniGCHoldTime>
    <MBLCollectionMiniGCRampRate>5</MBLCollectionMiniGCRampRate>
    <MBLCollectionMiniGCFinalTemp>65</MBLCollectionMiniGCFinalTemp>
    <MBLCollectionMiniGCFinalHoldTime>12</MBLCollectionMiniGCFinalHoldTime>
    <MBLCollectionMiniGCTotalLength>20</MBLCollectionMiniGCTotalLength>
    <MBLCollectionMiniGCPressure>7</MBLCollectionMiniGCPressure>
    <MBLGoogleMapsMarkerOptions>0</MBLGoogleMapsMarkerOptions>
    <MBLGoogleMapsOpenAnnotations>0</MBLGoogleMapsOpenAnnotations>
    <GoogleMapsSettings>
      <GoogleMapsLatitudeColumnID>0</GoogleMapsLatitudeColumnID>
      <GoogleMapsLongitudeColumnID>0</GoogleMapsLongitudeColumnID>
      <GoogleMapsShowMarkers>1</GoogleMapsShowMarkers>
      <GoogleMapsMarkerOptions>0</GoogleMapsMarkerOptions>
      <GoogleMapsValueColumnID>0</GoogleMapsValueColumnID>
      <GoogleMapsOpenAnnotations>0</GoogleMapsOpenAnnotations>
      <GoogleMapsDrawLine>0</GoogleMapsDrawLine>
      <GoogleMapsDrawLineSingleColor>0</GoogleMapsDrawLineSingleColor>
      <GoogleMapsingleColor>0x0 0x0 0x0| 0xffff 0x0</GoogleMapsingleColor>
      <GoogleMapsDrawLineColumnID>0</GoogleMapsDrawLineColumnID>
      <GoogleMapsDrawLineAutoScale>0</GoogleMapsDrawLineAutoScale>
      <GoogleMapsDrawLineSmooth>1</GoogleMapsDrawLineSmooth>
      <GoogleMapsDrawLineMin>0</GoogleMapsDrawLineMin>
      <GoogleMapsDrawLineMax>0</GoogleMapsDrawLineMax>
    </GoogleMapsSettings>
  </MBLBrain>
  <FileCoherence>1</FileCoherence>
</Document>"""

#FUNCTIONS FOR 2048 GAME

#Populate board array with empty spaces and initial tiles
def initializeBoard() :
	scores["currTotal"] = 0
	for r in range(DIMEN):
		for c in range(DIMEN):
			board[r][c] = EMPTY

	#Choose two distinct coordinate pairs
	x1, x2, y1, y2 = 0, 0, 0, 0
	x1 = rand.randint(0, DIMEN - 1)
	x2 = rand.randint(0, DIMEN - 1)
	y1 = rand.randint(0, DIMEN - 1)
	y2 = rand.randint(0, DIMEN - 1)

	while (y1 == y2) :
		y2 = rand.randint(0, DIMEN - 1)

	if chooseFour():
		board[y1][x1] = 2
	else: 
		board[y1][x1] = 1

	if chooseFour():
		board[y2][x2] = 2 
	else:
		board[y2][x2] = 1

#Add new random tile to board (more likely 2 than 4)  IF POSSIBLE!
def addRandomVals():
	if boardIsFull():
		return

	x1, y1 = rand.randint(0, DIMEN - 1), rand.randint(0, DIMEN - 1)
	while (board[y1][x1] != EMPTY) :
		x1 = rand.randint(0, DIMEN - 1)
		y1 = rand.randint(0, DIMEN - 1)

	if chooseFour():
		board[y1][x1] = 2
	else:
		board[y1][x1] = 1

#Determine if the board is full (no empty tiles)
def boardIsFull():
	fullnessCounter = 0
	for r in range(DIMEN):
		for c in range(DIMEN):
			if (board[r][c] == EMPTY): 
				fullnessCounter += 1

	if (fullnessCounter == 0):
		return True

	return False

#Probability of adding a 4 instead of a 2 to the board after a move
def chooseFour():
	#10 percent chance to be a 4
	return (rand.randint(0,9) == 0)

#Filter input for valid characters, q + wasd
def chooseMove():
	#TODO
	#Replace with machine learning algorithm !!

	#time.sleep(.5) #sleep for x seconds

	if (rand.randint(0, 1) == 0):
		return 'a'
	elif (rand.randint(0, 2) > 0):
		return 's'
	elif (rand.randint(0, 1) == 1):
		return 'w'
	else:
		return 'd'

#Convert byte to lowercase
def toLowerCase(input):
	if (input >= 65 and input <= 90):
		input += 32

	return input

#Shift board in direction specified by user
def updateBoard(command):

	if (command == UP or command == 0) :
		shiftUp()
	elif (command == LEFT or command == 1) :
		shiftLeft()
	elif (command == DOWN or command == 2) :
		shiftDown()
	else :
		shiftRight()

#Shifts tiles up in grid according to 2048 rules
def shiftUp():
	for r in range(DIMEN - 1):
		for c in range(DIMEN): 
			if (board[r][c] == EMPTY):
				for k in range(1, 4 - r, 1):
					if (board[r+k][c] != EMPTY):
						board[r][c] = board[r+k][c]
						board[r+k][c] = EMPTY
						c -= 1
						break
			else:
				for k in range(1, 4 - r, 1):
					if (board[k+r][c] == board[r][c]):
						board[r][c] += 1
						scores["currTotal"] += math.pow(2, board[r][c])
						board[k+r][c] = EMPTY
						break
					if (board[k+r][c] != EMPTY):
						break


#Shifts tiles down in grid according to 2048 rules
def shiftDown():
	for r in range(DIMEN - 1, 0, -1):
		for c in range(DIMEN): 
			if (board[r][c] == EMPTY): 
				for k in range(1, r + 1, 1):
					if (board[r-k][c] != EMPTY): 
						board[r][c] = board[r-k][c]
						board[r-k][c] = EMPTY
						c -= 1
						break
			else:
				for k in (1, r + 1, 1):
					if (board[r-k][c] == board[r][c]): 
						board[r][c] += 1
						scores["currTotal"] += math.pow(2, board[r][c])
						board[r-k][c] = EMPTY
						break
					if (board[r-k][c] != EMPTY):
						break

#Shifts tiles to left in grid according to 2048 rules
def shiftLeft():
	for r in range(DIMEN):
		for c in range (DIMEN - 1):
			if (board[r][c] == EMPTY):
				for k in range(1, 4 - c, 1): 
					if (board[r][c+k] != EMPTY):
						board[r][c] = board[r][c+k]
						board[r][c+k] = EMPTY
						c -= 1
						break
					
				
			else: 
				for k in range(1, 4 - c, 1):
					if (board[r][c+k] == board[r][c]): 
						board[r][c] += 1
						scores["currTotal"] += math.pow(2, board[r][c])
						board[r][c+k] = EMPTY
						break
					
					if (board[r][c+k] != EMPTY): 
						break
					
				
			
		
	


#Shifts tiles to right in grid according to 2048 rules
def shiftRight():
	for r in range(DIMEN): 
		for c in range(DIMEN - 1, 0, -1):
			if (board[r][c] == EMPTY):
				for k in range(1, c + 1, 1):
					if (board[r][c-k] != EMPTY): 
						board[r][c] = board[r][c-k]
						board[r][c-k] = EMPTY
						c += 1
						break
					
				
			else:
				for k in range(1, c + 1, 1):
					if (board[r][c-k] == board[r][c]):
						board[r][c] += 1
						scores["currTotal"] += math.pow(2, board[r][c])
						board[r][c-k] = EMPTY
						break
					
					if (board[r][c-k] != EMPTY): 
						break

#Prints board in nice format to console
def printBoard():
	print(" %s\n" % BORDER, end='')
	for r in range(DIMEN):
		print("%s" % EMPTY_ROW)
		print("| ", end='')

		for c in range(DIMEN):
			if (board[r][c] == EMPTY):
				print("%s" % SPACE , end='')
			else:
				print("%d" % board[r][c] , end='')
				printSpacing(board[r][c])

		print("|")
	print(" %s" % BORDER)

##Print spacing based on length of number (assumes 4 digits max number)
def printSpacing(printedInt):
	if (printedInt > 99) :
		print(" ", end='')
	elif (printedInt > 9) :
		print("  ", end='')
	else :
		print("   ", end='')

#Checks if no valid moves are left in board, signifies end of game
def gameOver():
	for r in range(DIMEN): 
		for c in range(DIMEN):
			if (board[r][c] == EMPTY): 
				return False
			
			if (r-1 >= 0): 
				if (board[r-1][c] == board[r][c]): 
					return False
				
			
			if (r+1 < 4): 
				if (board[r+1][c] == board[r][c]): 
					return False
				
			
			if (c-1 >= 0): 
				if (board[r][c-1] == board[r][c]): 
					return False
				
			
			if (c+1 < 4): 
				if (board[r][c+1] == board[r][c]): 
					return False
	return True


#Returns int value of highest tile value in board
def highestTileValue():
	highestTile = 0

	for r in range(DIMEN):
		for c in range(DIMEN):
			if (board[r][c] > highestTile):
				highestTile = board[r][c]
	return highestTile

def updateState(command):
	updateBoard(command)
	addRandomVals()

	reward = 0
	scores["currHigh"] = highestTileValue();
	if (scores["currHigh"] > scores["prevHigh"]):
		reward = scores["currHigh"]

	scores["prevHigh"] = scores["currHigh"]
	
	if (scores["currTotal"] > scores["prevTotal"]):
		#POTENTIALLY OVEREMPHASIZES HIGH SCORE
		reward += math.log(scores["currTotal"] - scores["prevTotal"],2)# emphasizes high score over high tile

	scores["prevTotal"] = scores["currTotal"]

	if gameOver():
		if (scores["currHigh"] > highestScore[0]):
			highestScore[0] = scores["currHigh"]
		return (-10, True)
	else:
		return (reward, False)

def main(): #FIX REWARD RETURN  - SCALE DOWN BY LOG
	tf.reset_default_graph()
	sess = tf.Session()

	numArgs = len(sys.argv) #parse command line arguments
	if (numArgs > 1):
		for arg in sys.argv:
			if (arg == "2048Trainer.py"):
				continue
			else: #load network from command line
				saver = tf.train.import_meta_graph(arg)
				saver.restore(sess,tf.train.latest_checkpoint('./'))
				graph = tf.get_default_graph()
				W = graph.get_tensor_by_name("W:0")
				break; 
	else: #initialize network
		W = tf.Variable(tf.random_uniform([4,4],0,0.01), name="W")

	#These lines establish the feed-forward part of the network used to choose actions
	inputs1 = tf.placeholder(shape=[4,4],dtype=tf.float32)
	Qout = tf.matmul(inputs1,W)
	predict = tf.argmax(Qout,1)

	#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
	nextQ = tf.placeholder(shape=[4,4],dtype=tf.float32)
	loss = tf.reduce_sum(tf.square(nextQ - Qout))
	trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
	updateModel = trainer.minimize(loss)

	saver = tf.train.Saver([W])

	y = .99
	e = 0.1
	numGames = 100000
	with sess:
		sess.run(tf.global_variables_initializer())
		gameCounter = 0
		avgScore = 0
		for i in range(numGames):
			initializeBoard() #resets board to beginning state
			s = np.copy(board)
			#print(s)
			rAll = 0
			done = False
			j = 0
			while (True):
				#Choose an action by greedily (with e chance of random action) from the Q-network
				#print(s)
				#print(np.nanmax(s))
				#print(s/np.nanmax(s))
				a,allQ = sess.run([predict,Qout],feed_dict={inputs1:s/4096}) #np.nanmax(s)
				#allQ /= np.nanmax(allQ)
				#print(allQ)
				#BUG: allQ = NAN

				if np.random.rand(1) < e:
					a[0] = rand.randint(0,3)
				
				#Get new state and reward from environment
				r,done = updateState(a[0])
				#print(r)
				s1 = board
				#print(s1)

				#Obtain the Q' values by feeding the new state through our network
				Q1 = sess.run(Qout,feed_dict={inputs1:s1/4096})

				#Obtain maxQ' and set our target value for chosen action.
				maxQ1 = np.max(Q1)
				targetQ = allQ
				targetQ[0,a[0]] = r + y*maxQ1

				#Train our network using target and predicted Q values
				_,W1 = sess.run( [updateModel,W], feed_dict={inputs1:s/4096,nextQ:targetQ} )
				rAll += r
				s = s1

				if done:
				#Reduce chance of random action as we train the model.
					e = 1./((i/rateOfDecrease) + 10)
					gameCounter += 1
					break
			#print("Final Score: %d" % scores["currTotal"])
			lastTenScores[gameCounter % 10] = scores["currHigh"]
			lastHundredScores[gameCounter % 100] = scores["currHigh"]
			lastTenTotals[gameCounter % 10] = scores["currTotal"]
			lastHundredTotals[gameCounter % 100] = scores["currTotal"]

			if (gameCounter % 10 == 0):
				print("%d Games Completed" % gameCounter)
				#print("Last 10 average high = %d" % np.average(lastTenScores))

			#print("Curr score = %d" % highestTileValue())
			if (gameCounter % 100  == 0):
				print(allQ)
				avg = np.average(lastHundredScores)
				avg2 = np.average(lastHundredTotals)
				#print("Last 100 average = %d" % avg)
				print("Highest score = %d" % math.pow(2,highestScore[0]))
				xPlot.append(gameCounter/100 - 1)
				yPlot.append(avg)
				xPlot2.append(gameCounter/100 - 1)
				yPlot2.append(avg2)
				

			if (gameCounter % 1000 == 0):
				saver.save(sess, "2048Training", global_step=gameCounter)

				fileOut = open("HighAVG.cmbl", 'w')
				fileOut.write(cmblFmt1)
				fileOut.write("\n")
				for i in range(len(xPlot)):
					fileOut.write(str(xPlot[i]))
					fileOut.write("\n")
				fileOut.write(cmblFmt2)
				fileOut.write("\n")
				for i in range(len(yPlot)):	
					fileOut.write(str(yPlot[i]))
					fileOut.write("\n")
				fileOut.write(cmblFmt3)
				fileOut.write("\n")
				fileOut.close()


				fileOut = open("ScoreAVG.cmbl", 'w')
				fileOut.write(cmblFmt1)
				fileOut.write("\n")
				for i in range(len(xPlot2)):
					fileOut.write(str(xPlot2[i]))
					fileOut.write("\n")
				fileOut.write(cmblFmt2)
				fileOut.write("\n")
				for i in range(len(yPlot2)):	
					fileOut.write(str(yPlot2[i]))
					fileOut.write("\n")
				fileOut.write(cmblFmt3)
				fileOut.write("\n")
				fileOut.close()
	
#Call main function on execution 
if __name__ == "__main__":
    main()

#network = tf.contrib.rnn.BasicLSTMCell(16)
#state = tf.zeros([1, 16*16])
#probabilities = []
#loss = 0.0
