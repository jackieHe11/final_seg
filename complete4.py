

feature_name="Blocks"  # "Boundary", "Blocks" or "Roads"

ref_layer_name = ('' + city + '_Locales_Polygons')
upd_layer_name = '' + city + '_Complete'

for layer in root.findLayers():
    #print layer.name()
    if layer.name() == ref_layer_name:
        ref_layer = layer.layer()
    elif layer.name() == upd_layer_name:
        upd_layer = layer.layer()

if ref_layer is None or upd_layer is None:
    raise ValueError('Was not able to find appropriately named layers')

locale_dict = {}
lat_dict = {}
long_dict = {}
for ref_feat in ref_layer.getFeatures():
    geom = ref_feat.geometry()
    attrs = ref_feat.attributes()
    locale_id = ref_feat['ID_string']
    locale_no = ref_feat['Locale_No']
    lat = ref_feat['Lat']
    long = ref_feat['Long']

    print(locale_id, locale_no)
    locale_dict[locale_id] = locale_no
    lat_dict[locale_id] = lat
    long_dict[locale_id] = long

index_land_use = -1
index_id_string = -1
index_locale_no = -1
index_lat = -1
index_long = -1

for i, field in enumerate(upd_layer.fields()):
    # print(i, field.name(), field.type(), field.typeName())
    if field.name().lower() == 'land_use':
        index_land_use = i
    elif field.name().lower() == 'id_string':
        index_id_string = i
    elif field.name().lower() == 'locale_no':
        index_locale_no = i
    elif field.name().lower() == 'lat':
        index_lat = i
    elif field.name().lower() == 'long':
        index_long = i
    else:
        print(field.name())
        raise Exception('Unexpected field in layer to be updated')


assert index_land_use != -1
assert index_id_string != -1
assert index_locale_no != -1
assert index_lat != -1
assert index_long != -1

# we have a dictionary mapping locale identifiers to locale_no values
# we have layer/features to be updated
# cycle through features
#   lookup locale_id, ie ID_string minus last character, in dictionary
#   retain value as appropriate locale_no for that feature
#   change attribute value for that feature
# commit all changes at end
upd_layer.startEditing()
for upd_feat in upd_layer.getFeatures():
    attrs = upd_feat.attributes()
    identifier = attrs[index_id_string]
    locale_id = identifier[:-1]
    locale_no = locale_dict[locale_id]
    lat = lat_dict[locale_id]
    long = long_dict[locale_id]
    if upd_feat.id() < 100:
        print(upd_feat.id(), index_locale_no, locale_no)
    upd_layer.changeAttributeValue(upd_feat.id(), index_locale_no, locale_no)
    upd_layer.changeAttributeValue(upd_feat.id(), index_id_string, locale_id)
    upd_layer.changeAttributeValue(upd_feat.id(), index_lat, lat)
    upd_layer.changeAttributeValue(upd_feat.id(), index_long, long)
    
upd_layer.commitChanges()
for upd_feat in upd_layer.getFeatures():
    if upd_feat.id() < 100:
        print(upd_feat.attributes())

