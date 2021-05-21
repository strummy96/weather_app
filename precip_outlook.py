# Precipitation Outlook PNG Generation
#
# Created By Seth Strumwasser
# Created: 03.24.21
# Updated: 03.24.21

print("Importing modules...")
import arcpy, sys, traceback, requests, datetime
import zipfile

# variables
current_date = datetime.date.today().strftime('%m.%d.%Y')
plocation = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\products\\"
dlocation = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\data\\"
aprx = arcpy.mp.ArcGISProject("C:\\Users\\seths\\Documents\\ArcGIS\\Projects\\precip_generation.aprx")
maplist = aprx.listMaps("Map")[0]

# precipitation
precip_url = "https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/814prcp_latest.zip"
precip_filename = "814prcp_latest.zip"
path = dlocation + precip_filename
precip_shp = dlocation + "814prcp_latest.shp"
precip_layer = "precip_layer.lyrx"
precip_fl = "Precip FL"
out_PNG = "precip_outlook" + str(current_date) + ".png"
layout = aprx.listLayouts("Layout")[0]

try:
    # download file
    print("Downloading file...")

    # check for existing data
    print("Checking for existing data...")
    if arcpy.Exists(path):
        arcpy.Delete_management(path)


    def download_url(url, location, chunk_size=128):
        r = requests.get(url, stream=True)
        with open(location, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)


    download_url(precip_url, path)
    print("...done.")

    # extratct zip contents
    print("Extracting zip contents...")
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(dlocation)
    print("...done.")

    # create feature layer from shapefile
    print("Creating layer from shapefile...")
    arcpy.MakeFeatureLayer_management(precip_shp, precip_fl)

    # create layer file from feature layer (check for existence)
    if arcpy.Exists(dlocation + precip_layer):
        arcpy.Delete_management(dlocation + precip_layer)

    arcpy.SaveToLayerFile_management(precip_fl, dlocation + precip_layer)

    print("...done.")

    # add layer to the map
    print("Adding layer to map...")
    precip_layer_file = arcpy.mp.LayerFile(dlocation + precip_layer)
    maplist.addLayer(precip_layer_file)

    print("...done.")

    # add symbology to layer
    print("Applying symbology...")
    arcpy.management.ApplySymbologyFromLayer(maplist.listLayers(precip_fl)[0],
                                             dlocation + "precip_layer_default_symbo.lyrx")
    print("...done.")

    # update text on layout
    print("Updating layout text...")
    tElements = layout.listElements("TEXT_ELEMENT")
    for tElement in tElements:
        if tElement.name == 'updated date':
            tElement.text = 'Updated: ' + str(current_date)
    print("...done.")

    # export layout to png
    print("Exporting layout to PNG...")

    if arcpy.Exists(plocation + out_PNG):
        arcpy.Delete_management(plocation + out_PNG)

    layout.exportToPNG(plocation + out_PNG)

    print("...done.")
    print("Process complete!")

    #print("Opening pdf...")
    #webbrowser.open(location + out_PDF)




except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    arcpy.AddError(msgs)
    arcpy.AddError(pymsg)

    print(msgs)
    print(pymsg)

    arcpy.AddMessage(arcpy.GetMessages(1))
    print(arcpy.GetMessages(1))
