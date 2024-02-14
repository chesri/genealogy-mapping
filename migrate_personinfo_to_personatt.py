import arcpy
        
arcpy.env.workspace = R"C:\Users\chrism\OneDrive\Geneaology\Studies and Projects\19_Data Modeling Attempts\Gen_DataModel_DEV\Gen_DataModel_DEV.gdb"

person_table = arcpy.ListTables("person")[0]
person_fields = [field.name for field in arcpy.ListFields(person_table)][1:]

person_attributes_table = arcpy.ListTables("person_attributes")[0]
person_att_fields = ['legacy_id','attribute_name','attribute_value']

persons = [row for row in arcpy.da.SearchCursor(person_table,person_fields) if row[0]]
person_att_list = []


for person in persons:
    print(f"Processing {person}")
    att_dict= {}
    
    for i,att in enumerate(person_fields):
        att_dict[att] = person[i]
    
    att_dict['legacy_id'] = att_dict.pop('person_id')
    person_att_list.append(att_dict)

with arcpy.da.InsertCursor(person_attributes_table, person_att_fields) as icursor:
    for person in person_att_list:
        print(person)
        for att in person:
            print(f"{person['legacy_id']},{att}, {person[att]}")
            icursor.insertRow((person['legacy_id'], att, person[att]))
        
print("done.")
