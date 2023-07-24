import pandas
import sys
sys.path.insert(1, '/scripts')
from automation_utils import AutomationUtils
from atr_sdk import ATRConsul, ATRApi
import datetime
import csv
import os
import requests
import json

utils = AutomationUtils()
configuration = utils.load_configuration()
uniqueTaskIDs = sys.argv[1]
print(uniqueTaskIDs)
Diff_Task_IDs = uniqueTaskIDs.split(', ')
print(Diff_Task_IDs)



# for fields in configuration['Consider ticket fields']:
print(configuration['Consider ticket fields']['Caller and Affected contact details'])

file_path = "WorkflowMonitoringWithoutAgent/TaskNumber_AssignmentGrp.csv"
file_path_shortName = "WorkflowMonitoringWithoutAgent/ShortNameOfResolverGroups.csv"
TaskIncidentFilePath = "WorkflowMonitoringWithoutAgent/testappend.csv"

df = pandas.read_csv(file_path)
df_shortName = pandas.read_csv(file_path_shortName)

dicts = df.to_dict('records')
dicts_shortName = df_shortName.to_dict('records')

# print("Weekday: ", datetime.datetime.now().weekday())


#defining all field values for the ticket
def main():
    
    # Diff_Task_IDs = ["TS99000692", "TS99000691", "TS99000926", "TS00008316", "TS99001106", "TS99001360", "TS99000783", "TS99000241", "TS99000231", "TS99001030"]



    dict_list = {}
    
    i = 0 
    
    try:
            
        for key in dicts:
            csvdata = dicts[i]
            TaskID = csvdata.get('Task ID')
            Assignment_group = csvdata.get('Assignment')
            dict_var = {
                TaskID : Assignment_group
            }
            i += 1
            
            print(dict_var)
            dict_list.update(dict_var)
            
        print(dict_list)
        print("$$$$$$$$$$$$$$$$$$$$$$")
        
        ticket_assignment_dict  = {}
        
        weekday_int = datetime.datetime.now().weekday() #Get the current day of the week as an integer (0 = Monday, 6 = Sunday)
        print(weekday_int)
        
        if weekday_int == 0:
            print("Only Monday...")
            for item in Diff_Task_IDs:
                if item in dict_list:
                    
                    print(dict_list[item])
                    print(item)
                    ticket_assignment_dict.update({item: dict_list[item]})
                    # payload(item, dict_list[item])
                    # Incident_Number = Create_Ticket(item, dict_list[item])
                    # print(Incident_Number)
                    if not is_value_present_in_csv(TaskIncidentFilePath, item):
                        Incident_Number = Create_Ticket(item, dict_list[item])
                        print(Incident_Number)
                        append_to_csv(TaskIncidentFilePath, item, Incident_Number)
                    else:
                        print("Value already present in the CSV file.")
                 
            
                else:
                    print(dict_list["Other"])
                    ticket_assignment_dict.update({item: dict_list["Other"]})
                    # payload(item, dict_list["Other"])
                    # print(ticket_assignment_dict)
                    # Create_Ticket(item, dict_list["Other"])
                    print("Testing")
                    # Incident_Number = Create_Ticket(item, dict_list["Other"])
                    # print(Incident_Number)
                    if not is_value_present_in_csv(TaskIncidentFilePath, item):
                        Incident_Number = Create_Ticket(item, dict_list["Other"])
                        print(Incident_Number)
                        append_to_csv(TaskIncidentFilePath, item, Incident_Number)
                    else:
                        print("Value already present in the CSV file.")
                
        else:
            print("except Monday...")
            for item in Diff_Task_IDs:
                if item in dict_list:
                    
                    print(dict_list[item])
                    ticket_assignment_dict.update({item: dict_list[item]})
                    
                    # Incident_Number = Create_Ticket(item, dict_list[item])
                    # print(Incident_Number)
                    if not is_value_present_in_csv(TaskIncidentFilePath, item):
                        Incident_Number = Create_Ticket(item, dict_list[item])
                        print(Incident_Number)
                        append_to_csv(TaskIncidentFilePath, item, Incident_Number)
                    else:
                        print("Value already present in the CSV file.")
                    
                    
                else:
                    print(dict_list["Other"])
                    ticket_assignment_dict.update({item: dict_list["Other"]})
                    # Incident_Number = Create_Ticket(item, dict_list["Other"])
                    # print(Incident_Number)
                    if not is_value_present_in_csv(TaskIncidentFilePath, item):
                        Incident_Number = Create_Ticket(item, dict_list["Other"])
                        print(Incident_Number)
                        append_to_csv(TaskIncidentFilePath, item, Incident_Number)
                    else:
                        print("Value already present in the CSV file.")
        
        print("ticket_assignment_dict: ", ticket_assignment_dict)
    except Exception as e:
        print(e)   


# Ticket_Type, Assignment_Group, Short_Description, Description, Business_Service, Configuration_item, Caller, Affected_Contact, Priority_level, Urgency_level, Diff_TaskID
def Create_Ticket(Task_number, Assignment_Group):
    
    # def payload(Task_number, Assignment_Group):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    print(current_date)
        
    # Diff_TASKID = Task_number
    tickettype = "Incident"
    print(tickettype)
    assignmentgroup = Assignment_Group
    print(assignmentgroup)
    
    if assignmentgroup == "IST RTBS Functional Support MP PY":
        prioritylevel = "3- Medium"
        urgencylevel = "3 - Medium"
        
    else:
        prioritylevel = "4- Low"
        urgencylevel = "4 - Low"
    print(prioritylevel)
    print(urgencylevel)
    S_name = ""
    j = 0
    for key_shortName in dicts_shortName:
        
        csvData_shortName = key_shortName
        resolverGroup = csvData_shortName.get('Resolver Group')
        short_resolverGroup = csvData_shortName.get('Short Name')
        
        if resolverGroup == assignmentgroup:
            S_name = short_resolverGroup
            # shortdescription = "Workflow without agent- " + S_name + " - "+ current_date + " - " +Diff_TASKID
            
    j += 1
    shortdescription = "Workflow without agent- " + S_name + " - "+ current_date + " - " +Task_number    
    description = "Workflow without agent- " + S_name + " - "+ current_date + " - " +Task_number 
    print(shortdescription)
    print(description)
    
    businessservice = "RTBS/Workflow"
    print(businessservice)
    configurationitem = "RTBS/Workflow"
    print(configurationitem)
    callername = "Agarwal, Anshul (IST-ACCENTURE)"
    print(callername)
    affected = "Agarwal, Anshul (IST-ACCENTURE)"
    print(affected)
    
    # return current_date, tickettype, Assignment_Group, shortdescription, description, businessservice, configurationitem, callername, affected

    atr_consul = ATRConsul()
    
    admin_password = atr_consul.get('configuration/aaam-atr-v3-identity-management/admin.password')
    atr = ATRApi('admin', admin_password)
    token = atr.token
    # print(token)
    # print(atr.im_url)
    # print(atr.atr_user)
    # print(atr.atr_password)
    postPayload = {
        "type": tickettype,
        "assignmentGroupATR": assignmentgroup,
        "priority": prioritylevel,
        "urgency": urgencylevel,
        "shortDescription":shortdescription,
        "description":description,
        "business_service": businessservice,
        "cmdb_ci":configurationitem,
        "caller_id": callername,
        "contact_type": affected,
        
    }



    apiBaseUrl = "http://ticket-management:8080/api/v1/tickets"
    try:
            
        res = requests.request("POST", apiBaseUrl, headers=atr.headers, data=json.dumps(postPayload), verify = False)
        Ticket_Incident = res.json()['coreData']['number']
        print(Ticket_Incident)
        return Ticket_Incident
        code = res.status_code
        print(code)
    # try: 
            
    #     if res.status_code == 201:
            
    #         Ticket_Incident = res.json()['coreData']['number']
    #         print(Ticket_Incident)
    #         return Ticket_Incident
    #     else:
    #         return "Ticket not created..."
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)
        return None, None
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
        return None, res.status_code
    # print(res.text['coreData']['number'])

    # print(res.std_err)



# Create_Ticket(tickettype, assignmentgroup, shortdescription, description, businessservice, configurationitem, callername, affected, prioritylevel, urgencylevel)
def is_value_present_in_csv(TaskIncidentFilePath, search_value):
    with open(TaskIncidentFilePath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Assuming the value to be checked is in the first column (index 0)
            if row and row[0] == search_value:
                return True
    return False
            
def append_to_csv(TaskIncidentFilePath, task_id, incident):
    fieldnames = ['Task ID', 'Incidents']
    
    if not os.path.isfile(TaskIncidentFilePath):
        with open(TaskIncidentFilePath, 'w', newline='') as TaskIncidentCSVFile:
            # fieldnames = ['Task ID', 'Incidents']
            writer = csv.DictWriter(TaskIncidentCSVFile, fieldnames=fieldnames)
            # if csvfile.tell() == 0:
            writer.writeheader()
            
        
    with open(TaskIncidentFilePath, 'a', newline='') as appendTaskIncidentCSVFile:
        writer = csv.DictWriter(appendTaskIncidentCSVFile, fieldnames=fieldnames)
        writer.writerow({'Task ID': task_id, 'Incidents': incident})
    
    return "Successfully appended"

# append_to_csv(path, 'task...ID', "incidentnumber")
    
        
if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(str.join(" ", str(e).splitlines())) 
    
