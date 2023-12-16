import streamlit as st
from deta import Deta
import pandas as pd
from twilio.rest import Client

custId = 0

DETA_KEY = "d0bequc3wix_Lanp9LHeo8QFYQwHcUn3bz9CdZ1iZbRy"
#initialize project key
deta = Deta(DETA_KEY)
#connect and create to db
db = deta.Base("users_db")

def clear_state():
    return {}

def insert_user(customerId,name,phoneNumber):
  return db.put({"key":customerId,"name":name,"phoneNumber":phoneNumber})

#insert_user("1","Abinaya","9876523456")

def fetch_all_users():
  res = db.fetch()
  return res.items

def get_user(customerId):
  return db.get(customerId)

users = fetch_all_users()

customerIds = [user["key"] for user in users]
names = [user["name"] for user in users]
phoneNumbers = [user["phoneNumber"] for user in users]

#-----------------------------------------------------------------------------------------------------------------------
db2 = deta.Base("courier_db")

def insert_courier(c,c_,w,s,d,dp,p,date,status,slat,slong,dlat,dlong):
  return db2.put({"key":c,"customerId":c_,"Weight(kgs)":w,"Source":s,"Destination":d,"Description":dp,"Price":p,"Date":date,"Status":status,"slat":slat,"slong":slong,"dlat":dlat,"dlong":dlong})

#insert_courier("1","1","59","Chennai","Bangalore","Fragile Items","70",'6/2/2023',"1","13.0827","80.2707","12.9716","77.5946")

def fetch_all_courier():
  res = db2.fetch()
  return res.items

def get_courier(courierId):
  return db2.get(courierId)
#-----------------------------------------------------------------------------------------------------------------------
import folium
couriers = fetch_all_courier()
slat = [c["slat"] for c in couriers]
slong = [c["slong"] for c in couriers]
dlat = [c["dlat"] for c in couriers]
dlong = [c["dlong"] for c in couriers]
source = [c["Source"] for c in couriers]
destination = [c["Destination"] for c in couriers]
key = [c["key"] for c in couriers]
date = [c["Date"] for c in couriers]
description = [c["Description"] for c in couriers]
price = [c["Price"] for c in couriers]
status = [c["Status"] for c in couriers]
weight = [c["Weight(kgs)"] for c in couriers]
customerId = [c["customerId"] for c in couriers]


db3 = deta.Base("queries")

def insert_query(name,email,message):
    return db3.put({"Name":name,"Email":email,"Message":message})
def fetch_all_queries():
    res = db3.fetch()
    return res.items

queries = fetch_all_queries()

name_ = [user["Name"] for user in queries]
email_ = [user["Email"] for user in queries]
message_ = [user["Message"] for user in queries]
#-----------------------------------------------------------------------------------------------------------------------

def insertCustomerRecord():
    customerId = st.text_input("Customer ID")
    customerName = st.text_input("Customer Name")
    phoneNumber = st.text_input("Phone Number")
    if st.checkbox("Submit"):
        insert_user(customerId,customerName,phoneNumber)
        st.success("Inserted Successfully")
    st.write("<hr>", unsafe_allow_html=True)

def insertCourierRecord():
    key = st.text_input("Courier ID")
    date = st.text_input("Date")
    desp = st.text_input("Description")
    dest = st.text_input("Destination")
    price = ""
    weight = st.text_input("Weight")
    source = st.text_input("Source")
    status = st.text_input("Status")
    custId = st.text_input("Customer ID")
    dlat = st.text_input("dlat")
    dlong = st.text_input("dlong")
    slat = st.text_input("slat")
    slong = st.text_input("slong")
    if st.checkbox("Submit"):
        w = int(weight)
        if (w<=30 and w>0):
            price = "30"
        elif (w<=50 and w>30):
            price = "50"
        elif (w<=70 and w>50):
            price = "70"
        else:
            price = "100"
        insert_courier(key,custId,weight,source,dest,desp,price,date,status,slat,slong,dlat,dlong)
        st.success("Inserted Successfully")

    st.write("<hr>", unsafe_allow_html=True)

# Define a function to check login credentials
def authenticate(username, password):
    if username == "admin" and password == "password":
        return True
    else:
        return False

# Define your Streamlit app
def login():
    st.write("<h1 style ='color:#ffbf00'>Sign In<h1>",unsafe_allow_html=True)
    st.subheader("Please enter your credentials to log in.")

    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a login button to submit the credentials
    if st.checkbox("Login"):
        if authenticate(username, password):
            st.success("Logged in as {}".format(username))
            st.write("<hr>",unsafe_allow_html=True)
            if st.checkbox("Insert Customer Record"):
                insertCustomerRecord()
            if st.checkbox("Insert Courier Records"):
                insertCourierRecord()
            if st.checkbox("Fetch all Customers"):

                data={}
                data["CustomerID"] = customerIds
                data["Name"] = names
                data["Phone Numbers"] = phoneNumbers
                df = pd.DataFrame(data)

                # Display the DataFrame as a table
                st.table(df)
            if st.checkbox("Fetch all Couriers"):

                data = {}
                data["CourierID"] = key
                data["CustomerID"] = customerId
                data["Source"] = source
                data["Destination"] = destination
                data["Date"] = date
                data["Description"] = description
                data["Price"] = price
                data["Status"] = status
                data["Weight"] = weight

                df = pd.DataFrame(data)

                # Display the DataFrame as a table
                st.table(df)
            if st.checkbox("Update Status"):
                id = st.text_input("Courier ID")
                if st.checkbox("Submit"):
                    record = db2.get(id)
                    if (len(record)==0):
                        st.error("Invalid Courier ID")
                    elif(record["Status"]=="1"):
                        st.success("Status Updated Already")
                    else:
                        record["Status"] = "1"
                        db2.put(record,id)
                        st.success("Status Updated Successfully")
                        # Your Twilio account SID and auth token
                        account_sid = "AC1f31f4290992152707ab1a0515d45d10"
                        auth_token = "b7448da728232da2f69c2fed686ae4e6"

                        # Create a Twilio client instance
                        client = Client(account_sid, auth_token)

                        # The phone number you want to send the SMS to (must be verified with Twilio)
                        c_id = record["customerId"]
                        record2 = db.get(c_id)
                        #st.write(record2["phoneNumber"])
                        to_phone_number = "+91"+record2["phoneNumber"]

                        message = client.messages.create(
                            from_='+15074311784',
                            body='Your Courier with Courier id : '+record["key"]+' is Delivered',
                            to=to_phone_number
                        )
                        print(message.sid)
                        print("SMS sent successfully!")
        else:
            st.error("Incorrect username or password")

def phoneOrTrack():
    if st.checkbox("Phone Number"):
        phoneNo()
    if st.checkbox("Track ID"):
        trackId()

    # Add other content to the page as needed
def trackId():
    st.write('<hr>', unsafe_allow_html=True)
    st.write("Please enter your track Id to track.")
    trackId_ = st.text_input("Track ID")
    st.write('<hr>', unsafe_allow_html=True)
    if st.checkbox("Submit "):
        couriers = fetch_all_courier()
        recordToTrack = [c for c in couriers if(c["key"]==str(trackId_))]
        if (len(recordToTrack)!=0):
            st.success("Valid Track ID")
            st.write(recordToTrack)
            if (recordToTrack[0]["Status"]=="1"):
                st.write('<p style="font-size: 20px; font-weight: bold; text-align: center;">STATUS</p>',unsafe_allow_html=True)
                st.write('<p style="color: green; font-size: 24px; font-weight: bold; text-align: center; text-decoration: underline;">DELIVERED</p>',
                    unsafe_allow_html=True)

            else:
                st.write("STATUS")
                st.write(
                    '<p style="color: red; font-size: 24px; font-weight: bold; text-align: center; text-decoration: underline;">PENDING</p>',
                    unsafe_allow_html=True)

            TRAIL = [[float(slat[0]), float(slong[0])], [float(dlat[0]), float(dlong[0])]]
            print(TRAIL)
            print(source[0],destination[0])

            map = folium.Map(LOCATION=TRAIL[0], zoom_start=7)
            map.add_child(folium.Marker(location=[TRAIL[0][0], TRAIL[0][1]], popup=source[0],
                                        icon=folium.Icon(color='red', icon='map-marker')))
            map.add_child(folium.Marker(location=[TRAIL[1][0], TRAIL[1][1]], popup=destination[0],
                                        icon=folium.Icon(color='red', icon='map-marker')))
            # SIMPLY TRYING TO MARK THE LINE THROUGH SOME SPECIFIED LATITUDES AND LONGITUDES
            folium.PolyLine(TRAIL, tooltip="HOTELS").add_to(map)
            map.save("map.png")
            st.image("map.png")

        else:
            st.error("Invalid Track ID")

def verifyPhoneNumber(phNo):
    print(phNo,phoneNumbers)
    if (phNo in phoneNumbers):
        global custId
        custId = phoneNumbers.index(phNo)+1
        return True
    return False

def phoneNo():
    st.write('<hr>', unsafe_allow_html=True)
    st.write("Please enter your phone Number to log in.")
    phNo = st.text_input("Phone Number")

    if st.checkbox("Submit"):
        print(phNo)
        if verifyPhoneNumber(phNo):
            st.success("An otp is generated to this Number")
            otp()
        else:
            st.error("No user with this phone Number")
    st.write('<hr>', unsafe_allow_html=True)

def history():


    courierId2 = [c for c in couriers if (c["customerId"]==str(custId))]
    #st.write(courierId2)
    num_sections = len(courierId2)

    # Create a for loop to create n number of sections
    for i in range(num_sections):
        # Create a container for the section
        with st.container():
            # Add content to the section
            st.write('<div class ="st-bd"> '+
                    "Date             "+"<span class = "r">"+courierId2[0]["Date"]+"</span>"+"<br>"+
                    "Description      "+"<span class = "r">"+courierId2[0]["Description"]+"</span>"+"<br>"+
                    "Destination      "+"<span class = "r">"+courierId2[0]["Destination"]+"</span>"+"<br>"+
                    "Price            "+"<span class = "r">"+courierId2[0]["Price"]+"</span>"+"<br>"+
                    "Source           "+"<span class = "r">"+courierId2[0]["Source"]+"</span>"+"<br>"+
                    "Status           "+"<span class = "r">"+courierId2[0]["Status"]+"</span>"+"<br>"+
                    "Weight(kgs)      "+"<span class = "r">"+courierId2[0]["Weight(kgs)"]+"</span>"+"<br>"+
                    "customer ID      "+"<span class = "r">"+courierId2[0]["customerId"]+"</span>"+"<br>"+
                    "Courier ID       "+"<span class = "r">"+courierId2[0]["key"]+"</span>"+"<br>"+
                     '</div>', unsafe_allow_html=True)
        st.markdown("""
            <style>
            .st-bd {
                
                border: 2px solid black;
                border-radius: 5px;
                padding: 20px;
                width:50%
            }
            .r{
                text-align: right;
            }
            </style>
        """, unsafe_allow_html=True)

def HistoryOrTrack():
    if st.checkbox("History"):
        history()
    if st.checkbox("TrackOrder"):
        trackId()

def otp():
    st.write('<hr>', unsafe_allow_html=True)
    st.write("Please enter OTP to log in.")
    otp_ = st.text_input("OTP")
    if st.checkbox("Submit OTP"):
        if (otp_=="9876"):
            st.success("Logged In successfully!")
            st.write("Now You can access History and Track your Order")
            HistoryOrTrack()
        else:
            st.error("Invalid OTP")
    st.write('<hr>', unsafe_allow_html=True)

# Define another Streamlit app for the About page
def contacts():
    st.write("<h1 style ='color:#ffbf00;text-align:center'>Queries<h1>",unsafe_allow_html=True)
    data = {}
    data["Name"] = name_
    data["Email"] = email_
    data["Message"] = message_
    df = pd.DataFrame(data)

    # Display the DataFrame as a table
    st.table(df)

def inference():
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
        ["Count Analysis", "Price Analysis", "Source&Dest Analysis", "Delivery status", "Weight Analysis",
         "Amount Collected", "Profit Analysis", "Customer Analysis", "Forecasting"])
    with tab1:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=77b47764-b95d-4ceb-8e45-38785fa1acde&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab2:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=8e781fad-911e-410b-8fde-c6bc5cbef20f&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab3:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=e1ddaacd-0d4b-4d88-8228-f36248712fa7&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab4:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=368b7528-15bb-4002-961c-f930bf2717b3&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab5:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=66d78e22-8ddc-48e2-a3de-93e92e6ee0ca&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab6:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=09d2d77e-8409-4656-84ac-e13c83037360&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab7:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=05012dbf-8847-4a63-813f-abbf3cb7e7bf&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab8:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=956a67cf-6520-4f04-b381-85a9a084c3a0&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    with tab9:
        # st.markdown("""<iframe title="PB_page1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=5b7274ea-a37b-43db-aeab-2f9ba76ce24b&autoAuth=true&ctid=da780102-affb-4105-8d1a-34ddb1b9fe7c" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
        power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=579bfa49-8370-4594-b6af-77982713de29&autoAuth=true&ctid=b971d3ed-dcd1-4105-985a-d3ab51447fa4"

        embedded_url = power_bi_url + "&toolbarHidden=true&navContentPaneEnabled=false&filterPaneEnabled=false"

        st.markdown(
            f'<div style="display: flex; justify-content: center;"><iframe width="1000" height="541.25" src="{embedded_url}" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(
        "<h25 style='text-align: right; color:white;font-size: 8px; font-family: Comic Sans MS;'>Made with ❤️</h25>",
        unsafe_allow_html=True)


# Run your Streamlit app
if __name__ == "__main__":
    pages = {"Login":login,"Queries":contacts,"Inferences":inference}
    st.set_page_config(page_title="Manager", page_icon=":guardsman:", layout="wide")

    st.sidebar.title("Navigation")
    page_options = list(pages.keys())
    selected_page = st.sidebar.selectbox("", page_options)
    page = pages[selected_page]
    page()



#"home": main, "about": about,"services":services,"Contacts":contacts,"getPhNo":phoneNo,"getTrackId":trackId,"otp":otp
