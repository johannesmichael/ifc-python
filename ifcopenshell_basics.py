#Collection of basic methods to get ifc information
#Test for inverse attributes and related Spaces/elements

import ifcopenshell as ifc



file = ifc.open(filepath)
#types = file.types()
#supertypes= file.types_with_super()

walls = file.by_type("IfcWall")
spaces = file.by_type("IfcSpace")
space = spaces[1]
wall = walls[1]

buildingstorey = wall.ContainedInStructure[0].RelatingStructure
buildingstorey_name = buildingstorey.RelatingStructure.Name
print(buildingstorey)
print(buildingstorey_name)

#Get all inverse attribute names
inversAttrNames = wall.wrapped_data.get_inverse_attribute_names()
print(inversAttrNames)

#Get IfcRelDefinesProperties, starting point for all Psets
rel_properties= wall.IsDefinedBy
print(rel_properties)

#Get psets of the IfcPropertySets
for rel in rel_properties:
	pset = rel.RelatingPropertyDefinition
	print(pset)

#Get IfcPropertySingleValue
rel_single_values = pset.HasProperties
print(rel_single_values)

#Name of IfcPropertySingleValue
for single in rel_single_values:
	name_of_single_value = single.Name
	print(name_of_single_value)

#Get IfcRelSpaceBoundary of wall
rel_boundary = wall.ProvidesBoundaries
print(rel_boundary)

for rel in rel_boundary:
    rel_element = rel.RelatedBuildingElement
    print(rel_element)
    rel_space = rel.RelatingSpace
    print(rel_space)

#spaceBoundaries of space
space_bound = space.BoundedBy
print(space_bound)

#building elements related to space
for rel in space_bound:
	rel_space_element = rel.RelatedBuildingElement
	print(rel_space_element)

#Function, to get all attributes of property sets (IfcRelDefinedByProperties) and base quantities
def get_attr_of_pset(_id):
	""" Get all attributes of an instance by given Id
		param _id: id of instance
		return: dict of dicts of attributes
	"""
	dict_psets = {}
	
	try:
		defined_by=[x.RelatingPropertyDefinition for x in ifc_file[_id].IsDefinedBy if x.is_a("IfcRelDefinesByProperties")]
		
	except:
		dict_psets.update({ifc_file[_id].GlobalId: "No Attributes found"})
	else:
		for x in defined_by:
			if x.is_a("IfcPropertySet"):
				for y in x.HasProperties:
					if y.is_a("IfcPropertySingleValue"):
						dict_psets.update({y.Name: y.NominalValue.wrappedValue})
						
					if y.is_a("IfcComplexProperty"):
						for z in y.HasProperties:
							dict_psets.update({z.Name: z.NominalValue.wrappedValue})
							
			if x.is_a("IfcElementQuantity"):
				for y in x.Quantities:
					dict_psets.update({y[0]: y[3]})
					
	finally:
		dict_psets.update({"IfcGlobalId":ifc_file[_id].GlobalId})
		
		return dict_psets
