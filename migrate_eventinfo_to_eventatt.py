# Cmac, 2/14/2024
import arcpy
        
arcpy.env.workspace = R"C:\Users\chrism\OneDrive\Geneaology\Studies and Projects\19_Data Modeling Attempts\Gen_DataModel_DEV\Gen_DataModel_DEV.gdb"

event_table = arcpy.ListFeatureClasses("event")[0]
event_fields = [field.name for field in arcpy.ListFields(event_table)]



events = [row for row in arcpy.da.SearchCursor(event_table,event_fields) if row[0]]
event_att_list = []

for event in events:
    print(f"Processing {event}")
    att_dict= {}
    
    for i,att in enumerate(event_fields):
        att_dict[att] = event[i]
    
    att_dict['event_fk'] = att_dict.pop('OBJECTID')
    event_att_list.append(att_dict)

# Prepare and write destination
arcpy.env.workspace = R"C:\Users\chrism\OneDrive\Geneaology\Studies and Projects\19_Data Modeling Attempts\Gen_DataModel_DEV\genDB_v2.geodatabase"
event_attributes_table = arcpy.ListTables("*event_attributes")[0]
event_att_fields = ['attribute_name','attribute_value','person_fk', 'event_fk']

with arcpy.da.InsertCursor(event_attributes_table, event_att_fields) as icursor:
    for event in event_att_list:
        print(event)
        for att in event:
            if att != 'Shape':
                print(f"{att}, {event[att]}, {event['person_fk']},{event['event_fk']}")
                icursor.insertRow((att, event[att], event['person_fk'], event['event_fk']))
        
print("done.")
