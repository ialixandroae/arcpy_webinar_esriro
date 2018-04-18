// 1.Citire layere din ArcGIS Pro

//Se obtine obiectul proiect
arcpy.mp.ArcGISProject('CURRENT')

// Se obtine harta activa din proiect
proiectArcGIS = arcpy.mp.ArcGISProject('CURRENT').activeMap
proiectArcGIS

//Se arata tipul hartii
proiectArcGIS.mapType

// Se arata numele hartii
proiectArcGIS.name

//Apoi se schimba numele hartii si se arata din nou
proiectArcGIS.name

// Se obtine variabila cu layere
layere = proiectArcGIS.listLayers()
layere

//Se printeaza numarul de layere
len(layere)

// Se itereaza layere si se printeaza
for layer in layere:
    print(layer) 
	
	
// Se creeaza o variabila cu primul layer
layerUAT = layere[0]
layerUAT

// Se printeaza numele layer
layerUAT.name

// Se face zoom in pe bucuresti, si se activeaza labels
layerUAT.showLabels = True

// Se dezactiveaza labels
layerUAT.showLabels = False

// Se dezactiveaza layerul
layerUAT.visible = False

//Se activeaza layerul
layerUAT.visible = True

// Se creeaza o variabila cu campuri
fields = arcpy.ListFields(layerUAT)
fields

// Se printeaza nr de campuri si se arata in ArcGIS Pro campurile
len(fields)

// Se printeaza numele fiecarui camp 
for field in fields:
    print(field.name) 
	
// Se printeaza mesaj customizat cu nume si tip camp 
for field in fields:
    print("Nume camp: {0}, tip: {1}".format(field.name, field.type))

// Se adauga camp nou
campNou = arcpy.AddField_management(layerUAT, "UNIT_BUFFER", 'TEXT')

// Se foloseste SearchCursor pentru a printa informatii din atribute
with arcpy.da.SearchCursor(layerUAT, ["DEN_UAT", "DEN_JUD", "SIRUTA", "CENS_2011"]) as cursor:
    for row in cursor:
        print("Localitatea {0} din judetul {1} cu SIRUTA {2} avea in 2011 o populatie de: {3}".format(row[0], row[1], row[2], row[3])) 
		
// Se foloseste UpdateCursor pentru a insera valori intr-un camp in functie de alte campuri
with arcpy.da.UpdateCursor(layerUAT, ["CENS_2011", "UNIT_BUFFER"]) as cursor:
    for row in cursor:
        if(row[0] < 50000):
            row[1] = '1 Kilometers'
        elif(row[0] > 50000 and row[0] < 100000):
            row[1] = '2 Kilometers'
        elif(row[0] > 100000 and row[0] < 500000):
            row[1] = '3 Kilometers'
        elif(row[0] > 500000 and row[0] < 1000000):
            row[1] = '4 Kilometers'
        elif(row[0] > 1000000):
            row[1] = '5 Kilometers'
        cursor.updateRow(row) 
		
// Se realizeaza un buffer
bufferUAT = arcpy.Buffer_analysis(layerUAT, "layerBuffer", "UNIT_BUFFER")


// Salvare feature class
arcpy.FeatureClassToFeatureClass_conversion(bufferUAT, "path_locatie_geodatabase", "BUFFER_UAT")

// Flux de lucru in PyCharm

import arcpy, shutil

numeGDB = "GDB_Webinar"
locatieGDB = r"path_locatie_geodatabase"

print("Creare geodatabase {0}".format(numeGDB))
gdb = arcpy.CreateFileGDB_management(locatieGDB, numeGDB)

date = ["POINT", "POLYLINE", "POLYGON"]
campuri = ["CAMP1", "CAMP2", "CAMP3"]
format = ['TEXT', "SHORT", "DOUBLE"]

for fc in date:
    outName = "FEATURE_CLASS_" + fc
    sr = arcpy.SpatialReference(4326)
    print("Se creeaza feature class-ul: {}".format(outName))
    createdFc = arcpy.CreateFeatureclass_management(out_path=gdb,
                                        out_name=outName,
                                        geometry_type=fc,
                                        spatial_reference=sr)
    for index, camp in enumerate(campuri):
        print("Se adauga campul {0} cu formatul {1}".format(camp, format[index]))
        arcpy.AddField_management(createdFc,camp,format[index])


print("Creare arhiva baza de date: {0}".format(numeGDB))
shutil.make_archive(locatieGDB + "\\" + "backup_GDB","zip",locatieGDB + "\\" + numeGDB + ".gdb")



