###############################################################################
# 03. March 2018, Johannes Römpp --GitHub: johannesmichael/ifc-python
# https://github.com/johannesmichael/ifc-python
#                                                                               #
# This file depends on psets.py                                                 #
# It was developed to help analyze ifc property data with pandas and            #
# excel.                                                                        #
#                                                                               #
#                                                                               #
# It uses the IfcOpenshell-python package                                       #
# https://github.com/IfcOpenShell/IfcOpenShell/tree/master/src/ifcopenshell-python/ifcopenshell
# Thanks to the IfcOpenshell-team!!!                                            #
#                                                                               #
# This script and its functions is distributed in the hope that                 #
# it will be useful, when working with ifc data.	                            #
#                                                                               #
# For help with ifc data, take a look at                                        #
# http://www.buildingsmart-tech.org/ifc/IFC2x3/TC1/html/index.htm				#
###############################################################################







"""
Thanks to ifcopenshell-python https://github.com/IfcOpenShell/IfcOpenShell/tree/master/src/ifcopenshell-python/ifcopenshell

This script is used to extract all pset-information of an ifc-file and save it to an excel-workbook.
In the analyze part one can define attributes the pivo-table is grouped by
"""




import ifcopenshell as ifc
import psets
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from pandas import DataFrame, Series, ExcelWriter
import pandas as pd
import os

#-------File Functions-----------------
def OpenFile(_extension, _filetypes):
	
    filename = askopenfilename(defaultextension = _extension, filetypes=[_filetypes])
    print(filename)
    return filename

def SaveFileAs(_extension):
	
    filename = asksaveasfilename(defaultextension = _extension)
    print(filename)
    return filename

def extract_instances(instances, source_file):

        for inst in instances:
            pset_dict = {"Source_File":source_file}
           
            pset_dict.update({"IFC_Name":inst.Name, \
                              "IFC_GlobalId":inst.GlobalId,\
                              "IFC_Entity":inst.is_a(),\
                              "IFC_Description":inst.Description, \
                              "IfcBuildingStorey": [x.RelatingStructure.Name for x in inst.ContainedInStructure][0]})
            if inst.Tag:
                pset_dict.update({"IFC_Tag":inst.Tag})
            if hasattr(inst, "Longname"):
                pset_dict.update({"IFC_Longname":inst.Longname})
            
            try:
                pset_dict.update({"IfcSystem":inst.HasAssignments[0].RelatingGroup.Name})
            except:
                pass

            pset_dict.update(IFC_Psets.get_all_pset_data(inst))
            #print(pset_dict)
            pset_instances_list.append(pset_dict)
            


#----------Read Ifc-File----------
#ifc_file_path1="B:\DEV_Temp\HA.ifc"
ifc_file_path = OpenFile(".ifc", ("IFC-Files","*.ifc"))
ifc_file= ifc.open(ifc_file_path)

source_file = os.path.split(ifc_file_path)[1]
#extract data from Ifc-File

#------IfcElement-------------------
instances = ifc_file.by_type("IfcElement") #better be more precise, like IfcBuildingElement, IfcDistributionElement...

print(len(instances))

instance_info_list = []
pset_instances_list = []

extract_instances(instances,source_file)

#---------Data to DataFrame--------------
#all instances and attributes to DataFrame
df=DataFrame(pset_instances_list)
pivot1 = df.pivot_table(index=["IFC_Name", "IFC_Entity"],values=["IfcGlobalId"],aggfunc=[len])

#-----------Analyze
#Names and IFCClassification
df_analyze = df

attr_names=Series(list(df))
unique_names = Series(df.IFC_Name.unique())


outfile = SaveFileAs(".xlsx")

writer = ExcelWriter(outfile)
df.to_excel(writer,"All")
attr_names.to_excel(writer,"AttributeNames")
unique_names.to_excel(writer,"IFC_Name")
pivot1.to_excel(writer,"Analyze")

writer.save()
