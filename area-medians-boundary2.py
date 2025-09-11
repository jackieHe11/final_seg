#add arterials

feature_name="Blocks"  # "Boundary", "Blocks" or "Roads" or "Areas"
group="Arterial" # "T0" or "T1_T3" or "Arterial"
dir_prefix='/Users/jackiehe/Desktop/Materials/research/Segmentation_Research/qgis_project/'
# Set the directory where the input files are stored
directory=dir_prefix+city+'/'+city+'_'+feature_name+'/'+city+'_'+group+'/'
#directory='C:/Users/'+user+'/World Resources Institute/Urban Land Use - Documents/AUE Data and Maps/WRI-NGS custom data from NYU/#WRI_Mexican_cities_submission'+'/'+city+'/'+city+'_'+feature_name+'/'+city+'_'+group+'/'

file = ''+city+'_Master_AR_Medians.shp'

# create vector layer object
vlayer = QgsVectorLayer(directory +file , file , "ogr")
print(file)

# add the layer to the registry
QgsProject.instance().addMapLayer(vlayer, False)

# add the layer to the group
QgsProject.instance().layerTreeRoot().addLayer(vlayer)

#add study area

feature_name="Areas" 

# Set the directory where the input files are stored
directory=dir_prefix+city+'/'+city+'_'+feature_name+'/'
#directory='C:/Users/'+user+'/World Resources Institute/Urban Land Use - Documents/AUE Data and Maps/WRI-NGS custom data from NYU/#WRI_Mexican_cities_submission'+'/'+city+'/'+city+'_'+feature_name+'/'+city+'_'+group+'/'

file = ''+city+'_studyArea.shp'

# create vector layer object
vlayer = QgsVectorLayer(directory +file , file , "ogr")
print(file)

# add the layer to the registry
QgsProject.instance().addMapLayer(vlayer, False)

# add the layer to the group
QgsProject.instance().layerTreeRoot().addLayer(vlayer)

feature_name="Boundary"  # "Boundary", "Blocks" or "Roads" or "Areas"

if feature_name=='Boundary':
    feature_num='0' 
elif feature_name=='Blocks':
   feature_num='1'
print(feature_num)


group="T0" # "T0" or "T1_T3" or "Arterial"

# Set the directory where the input files are stored
group_name = f"{city}_{feature_name}_{group}"
root = QgsProject.instance().layerTreeRoot()

# Create group in the layer tree
mygroup = root.addGroup(group_name)

# load vector layers
for files in os.listdir(directory):

    # load only the shapefiles
    if files.endswith(''+feature_num+'.shp'):

        # create vector layer object
        vlayer = QgsVectorLayer(directory + files, files , "ogr")
        print(files)

        # add the layer to the registry
        QgsProject.instance().addMapLayer(vlayer, False)
        
        # add the layer to the group
        mygroup.addLayer(vlayer)

# Get the list of input files
fileList = os.listdir(directory)
 
# Copy the features from all the files in a new list
feats = []
feats_stored = []
for file in fileList:
    if file.endswith(''+feature_num+'.shp'):
        layer = QgsVectorLayer(directory + file, file, 'ogr')
        for feat in layer.getFeatures():
            geom = feat.geometry()
            attrs = feat.attributes()
            feature = QgsFeature()
            feature.setGeometry(geom)
            feature.setAttributes(attrs)
            feats.append(feature)
            feats_stored.append(feature)

# Get the Coordinate Reference System and the list of fields from the last input file
crs = layer.crs().toWkt()
field_list = [field for field in layer.fields()] 
# Create the merged layer by checking the geometry type of  the input files (for other types, please see the API documentation)
# if layer.wkbType()==QGis.WKBPoint:
#     v_layer = QgsVectorLayer('Point?crs=' + crs, "Boundary T0 Merged", "memory")
# if layer.wkbType()==QGis.WKBLineString:
#     v_layer = QgsVectorLayer('LineString?crs=' + crs, "Boundary T0 Merged", "memory")
# if layer.wkbType()==QGis.WKBPolygon:
#     v_layer = QgsVectorLayer('Polygon?crs=' + crs, "Boundary T0 Merged", "memory")
from qgis.core import QgsWkbTypes, QgsVectorLayer
wkb_type = layer.wkbType()
merge_tag="Boundary T0 Merged"
if wkb_type == QgsWkbTypes.Point:
    v_layer = QgsVectorLayer(f'Point?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.LineString:
    v_layer = QgsVectorLayer(f'LineString?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.Polygon:
    v_layer = QgsVectorLayer(f'Polygon?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.MultiLineString:
    v_layer = QgsVectorLayer(f'MultiLineString?crs={crs}', merge_tag, "memory")
    print('T')
# Add the features to the merged layer
prov = v_layer.dataProvider()
prov.addAttributes(field_list)
v_layer.updateFields()
v_layer.startEditing()
prov.addFeatures(feats)
v_layer.commitChanges()
 
QgsProject.instance().addMapLayer(v_layer)

group="T1_T3" # "T0" or "T1_T3" or "Arterial"

# Set the directory where the input files are stored
directory=dir_prefix+city+'/'+city+'_Blocks/'+city+'_'+group+'/'
#directory='C:/Users/'+user+'/World Resources Institute/Urban Land Use - Documents/AUE Data and Maps/WRI-NGS custom data from NYU/#WRI_Mexican_cities_submission'+'/'+city+'/'+city+'_Blocks'+'/'+city+'_'+group+'/'

# Add group for layers
group_name = f"{city}_{feature_name}_{group}"

# Access the layer tree root
root = QgsProject.instance().layerTreeRoot()

mygroup = root.findGroup(group_name)
if mygroup is None:
    mygroup = root.addGroup(group_name)

# load vector layers
for files in os.listdir(directory):

    # load only the shapefiles
    if files.endswith(''+feature_num+'.shp'):

        # create vector layer object
        vlayer = QgsVectorLayer(directory + files, files , "ogr")
        print(files)

        # add the layer to the registry
        QgsProject.instance().addMapLayer(vlayer, False)
        # fix for QGIS 3
        # QgsProject.instance().addMapLayer(vlayer, False)
        
        # add the layer to the group
        mygroup.addLayer(vlayer)

# Get the list of input files
fileList = os.listdir(directory)
 
# Copy the features from all the files in a new list
feats = []
for file in fileList:
    if file.endswith(''+feature_num+'.shp'):
        layer = QgsVectorLayer(directory + file, file, 'ogr')
        for feat in layer.getFeatures():
            geom = feat.geometry()
            attrs = feat.attributes()
            feature = QgsFeature()
            feature.setGeometry(geom)
            feature.setAttributes(attrs)
            feats.append(feature)
            feats_stored.append(feature)

# Get the Coordinate Reference System and the list of fields from the last input file
crs = layer.crs().toWkt()
field_list = [field for field in layer.fields()] 
 
# Create the merged layer by checking the geometry type of  the input files (for other types, please see the API documentation)
merge_tag="Boundary T1_T3 Merged"
if wkb_type == QgsWkbTypes.Point:
    v_layer = QgsVectorLayer(f'Point?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.LineString:
    v_layer = QgsVectorLayer(f'LineString?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.Polygon:
    v_layer = QgsVectorLayer(f'Polygon?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.MultiLineString:
    v_layer = QgsVectorLayer(f'MultiLineString?crs={crs}', merge_tag, "memory")
# Add the features to the merged layer
prov = v_layer.dataProvider()
prov.addAttributes(field_list)
v_layer.updateFields()
v_layer.startEditing()
prov.addFeatures(feats)
v_layer.commitChanges()
 
QgsProject.instance().addMapLayer(v_layer)

# Merge T0 and T1_T3 boundaries
merge_tag=city+'_Locales_Merged'
if wkb_type == QgsWkbTypes.Point:
    v_layer = QgsVectorLayer(f'Point?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.LineString:
    v_layer = QgsVectorLayer(f'LineString?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.Polygon:
    v_layer = QgsVectorLayer(f'Polygon?crs={crs}', merge_tag, "memory")
elif wkb_type == QgsWkbTypes.MultiLineString:
    v_layer = QgsVectorLayer(f'MultiLineString?crs={crs}', merge_tag, "memory")  
# Add the features to the merged layer
prov = v_layer.dataProvider()
prov.addAttributes(field_list)
v_layer.updateFields()
v_layer.startEditing()
prov.addFeatures(feats_stored)
v_layer.commitChanges()

QgsProject.instance().addMapLayer(v_layer)

# add centroid coordinates to Locales_Merged file
from PyQt5.QtCore import QVariant

# add centroid coordinates to Locales_Merged file
layerName = city+'_Locales_Merged'
layer = QgsProject.instance().mapLayersByName(layerName)[0]

fields = layer.fields()
#for field in fields:
    #print field.displayName()

layer.startEditing()
layer.dataProvider().addAttributes([QgsField('lat', QVariant.Double),QgsField('long', QVariant.Double)])
layer.commitChanges()

index_lat = layer.dataProvider().fieldNameIndex('lat')
index_long = layer.dataProvider().fieldNameIndex('long')
print (index_lat, index_long)
assert index_lat != -1
assert index_long != -1

layer.startEditing()
for f in layer.getFeatures():
    cent_pt = f.geometry().centroid().asPoint()
    #print cent_pt.x(), cent_pt.y()
    layer.changeAttributeValue(f.id(), index_lat, cent_pt.y())
    layer.changeAttributeValue(f.id(), index_long, cent_pt.x())

layer.commitChanges()
