#This is the app/OPENFDA_data file


import requests
import pandas
import plotly.express as px


pandas.options.mode.copy_on_write = True

company = input("Please input your desired company (try 'Abbott Laboratories', 'Medtronic', or 'Boston Scientfic' as a example): ")
company.replace(" ", "+")
pmadevices_query = f'https://api.fda.gov/device/pma.json?search=applicant:"{company}"&sort=decision_date:desc&limit=1000'
devicerecall_query = f'https://api.fda.gov/device/recall.json?search=recalling_firm:"{company}"&sort=event_date_posted:desc&limit=1000'

p = requests.get(pmadevices_query)
pmadevicedata = p.json()

r = requests.get(devicerecall_query)
recalldata = r.json()

if "error" not in pmadevicedata:
    #
    # Medical Devices seeking premarket approval
    #

    numDevices = pmadevicedata["meta"]["results"]["total"]
    print(numDevices, "devices seeking premarket approval found, showing the 1000 most recent results") # 1000 result limit for API
    pmadevicedata = pmadevicedata["results"]
    df = pandas.DataFrame(pmadevicedata)

    apprdf = df[df.decision_code == "APPR"]
    apprdf['decision_date'] = apprdf['decision_date'].astype("string")
    apprdf['decision_date'] = pandas.to_datetime(apprdf['decision_date'])

    # Plotting approvals over time
    approvals_by_date = df.groupby(apprdf['decision_date'].dt.date).size().reset_index(name='count')

    fig = px.line(approvals_by_date, x='decision_date', y='count',
              title='Premarket Device Approvals Over Time',
              labels={'decision_date': 'Date', 'count': 'Number of Approvals'})
    fig.show()

    #
    # Medical Device Recalls
    #

    numRecalls = recalldata["meta"]["results"]["total"]
    print(numRecalls, "Recalls Found, showing the 1000 most recent results")
    recalldata = recalldata["results"]
    rdf = pandas.DataFrame(recalldata)

    rdf['event_date_posted'] = rdf['event_date_posted'].astype("string")
    rdf['event_date_posted'] = pandas.to_datetime(rdf['event_date_posted'])

    # Plotting recalls over time
    recalls_by_date = rdf.groupby(rdf['event_date_posted'].dt.date).size().reset_index(name='count')

    fig = px.line(recalls_by_date, x='event_date_posted', y='count',
              title='Device Recalls Over Time',
              labels={'event_date_posted': 'Date', 'count': 'Number of Recalls'})
    fig.show()

else:
    print("company not found")