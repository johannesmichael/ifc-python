#Attributes with Pset-Name, like {"BaseQUantities,Lenght":2.03}


###############################################################################
# This file contains functions to retrieve ifc property set information.        #
# It was developed to help analyze ifc property data with pandas and            #   
# excel. See IfcAnalyze.py for example
# 
# 
# It uses the IfcOpenshell-python package 
# https://github.com/IfcOpenShell/IfcOpenShell/tree/master/src/ifcopenshell-python/ifcopenshell
# Thanks to the IfcOpenshell-team!!!                                            #
#                                                                               #
# This module and its functions is distributed in the hope that                 #
# it will be useful, when working with ifc data.	
# 
# For help with ifc data, take a look at 
# http://www.buildingsmart-tech.org/ifc/IFC2x3/TC1/html/index.htm												  #
###############################################################################


"""
Module with function to retrieve pset information of an IFC file with
the IfcOpenshell Package

Covers:
instance Information
Standard and userdefined psets
BaseQuantitites
IfcSingleValues

Type Information not working well yet


"""


#TODO: IfcPropertyEnumeratedValue, IfcPropertyBoundedValue, IfcPropertyTableValue, IfcPropertyReferenceValue, IfcPropertyListValue


def get_all_pset_data(ifc_instance):
    """
    Get all (non-geometrical) data of an instance
    from Pset (default and user-defined)
    argument: instance from ifc file
    return: dict of dictionaries (attribute_name:attribute_value)
    """
    pset_dict= {}
    #getting type
    #getting pset single values
    {pset_dict.update(get_property_single_value(x))\
         for x in get_related_property_sets(ifc_instance)}
    return pset_dict
	
def get_related_property_sets(ifc_instance):
    """
    Returns a list of IfcPropertySets for given ifc_instance
    argument: ifc_instance
    return: list of property sets
    """
    properties_list = []
    for x in ifc_instance.IsDefinedBy:
        if x.is_a("IfcRelDefinesByProperties"):
            if x.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                properties_list.append(x.RelatingPropertyDefinition)
    return properties_list    


def get_property_single_value(x):
    """
    Returns a dict of dicts of IfcSingleValues, even from IfcComplexProperties. Returning a dictionary of dictionaries
    is used, because it is easy to transform to pandas.DataFrame 
    argument: IFC Element as contained in list from get_related_property_sets()
    return: dict of property single values like {"IfcName":"xx", "IfcGlobalId": "klkhlkh", ......}

    """
    attributes_dicts={}
   
    for y in x.HasProperties:
        if y.is_a("IfcPropertySingleValue") and y.NominalValue is not None:
            attributes_dicts.update({(x.Name,y.Name):y.NominalValue.wrappedValue})
        if y.is_a("IfcComplexProperty"):
            for z in y.HasProperties:
                if z.NominalValue is not None:
                    attributes_dicts.update({(x.Name,z.Name): z.NominalValue.wrappedValue})

    return attributes_dicts   
	
def get_related_properties(ifc_instance):
    defined_by_properties_list=[x.RelatingPropertyDefinition \
                                for x in ifc_instance.IsDefinedBy \
                                if x.is_a("IfcRelDefinesByProperties")]
    return defined_by_properties_list

def get_related_type_definition(ifc_instance):
    """
    Returns the related type definitions for a given ifc_instance
    argument: ifc_instance
    return: list of IfcElementType
    """
    defined_by_type_list=[x.RelatingType for x in ifc_instance.IsDefinedBy \
                          if x.is_a("IfcRelDefinesByType")]
    return defined_by_type_list

            

def get_related_quantities(ifc_instance):
    """
    Returns a list of IfcElementQuantity for given IFC ID
    argument: ifc_instance
    return: list of property sets
    """
    quantities_list =[]
    for x in ifc_instance.IsDefinedBy:
        if x.is_a("IfcRelDefinesByProperties"):
            if x.RelatingPropertyDefinition.is_a("IfcElementQuantity"):
                quantities_list.append(x.RelatingPropertyDefinition)
    return quantities_list     

  
        

def get_type_single_value(x):
    """
    Returns a dict of dicts of IfcXXTYpe single values (like "IfcWallType"). Returning a dictionary of dictionaries
    is used, because it is easy to transform to pandas.DataFrame 
    argument: IFC Element as contained in list from get_related_property_sets()
    return: dict of property single values like {"IfcName":"xx", "IfcGlobalId": "klkhlkh", ......}

    """
    type_attr_dicts={}
    if x.HasPropertySets:
        try:
            {type_attr_dicts.update({"TypeDefinition_" + x.Name:y.Name}) for y in x.HasPropertySets if y.Name is not None}
            #for y in x.HasPropertySets:
            #    if y.Name is not None:
            #        type_attr_dicts.update({"TypeDefinition_" + x.Name:y.Name})
        except:
            print("Type Value Exception for IfcGlobalID "+ x.GlobalId)

    return type_attr_dicts

def get_quantity_single_value(x):
    """
    Returns a dict of dicts of IfcElementQuantity single values.
    Returning a dictionary of dictionaries
    is used, because it is easy to transform to pandas.DataFrame 
    argument: IFC Element as contained in list from get_related_property_sets()
    return: dict of property single values like {"IfcName":"xx", "IfcGlobalId": "klkhlkh", ......}

    """
    quantities_dicts = {}
    for y in x.Quantities:
        if y.is_a('IfcQuantityArea'):
            quantities_dicts.update({(x.Name,y.Name):y.AreaValue})
        if y.is_a('IfcQuantityLength'):
            quantities_dicts.update({(x.Name,y.Name):y.LengthValue})
        if y.is_a('IfcQuantityVolume'):
            quantities_dicts.update({(x.Name,y.Name):y.VolumeValue})
        if y.is_a('IfcQuantityCount'):
            quantities_dicts.update({(x.Name,y.Name):y.CountValue})
        if y.is_a('IfcQuantityWeight'):
            quantities_dicts.update({(x.Name,y.Name):y.WeightValue})
        
    return quantities_dicts 

def get_all_instance_data(ifc_instance):
    """
    Get all (non-geometrical) data of an instance
    from Pset (default and user-defined), BaseQuantities and Type
    argument: instance from ifc file
    return: dict of dictionaries (attribute_name:attribute_value)
    """
    pset_dict= {}
    
    #getting pset single values
    {pset_dict.update(get_property_single_value(x))\
     for x in get_related_property_sets(ifc_instance)}

    #getting basequantities single values
    {pset_dict.update(get_quantity_single_value(x)) \
     for x in get_related_quantities(ifc_instance)}

    #getting type
    {pset_dict.update(get_type_single_value(x)) \
     for x in get_related_type_definition(ifc_instance)}

    return pset_dict

def get_all_quantity_data(ifc_instance):
    """
    Get all (non-geometrical) data of an instance
    from BaseQuantities 
    argument: instance from ifc file
    return: dict of dictionaries (attribute_name:attribute_value)
    """
    pset_dict= {}
    #getting basequantities single values
    {pset_dict.update(get_quantity_single_value(x)) \
        for x in get_related_quantities(ifc_instance)}
    return pset_dict


def get_all_type_data(ifc_instance):
    """
    Get all (non-geometrical) data of an instance
    from Type
    argument: instance from ifc file
    return: dict of dictionaries (attribute_name:attribute_value)
    """
    pset_dict= {}
    #getting type
    {pset_dict.update(get_type_single_value(x)) \
        for x in get_related_type_definition(ifc_instance)}
    return pset_dict



def get_space_boundaries(ifc_instance):
	""" Get all SpaceBoundaries of an IFC  instance 
		param _id: Ifc Instance
		return: dict of attributes
	"""
	dict_space_relations = {}
	list_spaces = []
	try:
		relating_spaces=[x.RelatingSpace for x in ifc_instance.ProvidesBoundaries]
		
	except:
		dict_space_relations.update({ifc_instance.GlobalId: "No Spaces found"})
	else:
		for rel in relating_spaces:
			list_spaces.append(rel.id())
			
	finally:
		#dict_space_relations[ifc_file[_id].GlobalId]= list_spaces
		return list_spaces

def get_pset_single_value_by_args(ifc_instance, pset_name, pset_attribute):
	""" Return a specific single value from a space pset
		param _id: ifc instance
		param pset_name: Name of Pset
		param pset_attribute: Name of Pset attribute
		return: Nominal value 
	"""
	try:
		defined_by= ifc_instance.IsDefinedBy
		
	except:
		print("Type Value Exception for IfcGlobalID "+ ifc_instance.GlobalId)
	else:
		for defin in defined_by:
			if defin.is_a("IfcRelDefinesByProperties"):
				psets = defin.RelatingPropertyDefinition
				if psets.Name == _pset_name:
					single_values = psets.HasProperties
					for value in single_values:
						if value.Name == _pset_attribute:
							_nominal_value = value.NominalValue.wrappedValue
							return _nominal_value



def get_space_relation(ifc_instance):
	""" Get all SpaceBoundaries of an ifc instance by given Ifc-instance

		args:
        ifc_instance: id of instance
	    returns:
        list of related spaces as ifc-instance
	"""
	spaces_list = []
	try:
		relating_spaces=[x.RelatingSpace for x in ifc_instance.ProvidesBoundaries]
		
	except:
		print(ifc_instance.GlobalId + ": No Spaces found")
	else:
		for rel in relating_spaces:
			spaces_list.append(rel)
			
	finally:
		return spaces_list