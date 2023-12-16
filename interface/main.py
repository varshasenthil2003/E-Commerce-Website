import streamlit as st
from deta import Deta
import streamlit as st
import streamlit.components.v1 as components
import io
from PIL import Image
from twilio.rest import Client
import random

flag=0

account_sid = 'AC1f31f4290992152707ab1a0515d45d10'
auth_token = 'b7448da728232da2f69c2fed686ae4e6'

verify_sid = "VA25045aeae5d3593f6fc88e4796b50431"


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
db3 = deta.Base("queries")

def insert_query(name,email,message):
    return db3.put({"Name":name,"Email":email,"Message":message})
def fetch_all_queries():
    res = db3.fetch()
    return res.items



import folium
couriers = fetch_all_courier()
slat = [c["slat"] for c in couriers]
slong = [c["slong"] for c in couriers]
dlat = [c["dlat"] for c in couriers]
dlong = [c["dlong"] for c in couriers]
source = [c["Source"] for c in couriers]
destination = [c["Destination"] for c in couriers]


#-----------------------------------------------------------------------------------------------------------------------

# Define a function to check login credentials
def authenticate(username, password):
    if username == "admin" and password == "password":
        return True
    else:
        return False
# Define your Streamlit app
def main():
    st.write("<h1 style = 'text-align:center;color:#f73645'>Courier Express<h1>",unsafe_allow_html=True)
    st.subheader("View your order by")
    phoneOrTrack()

    #st.write("<hr style='color=#f73645;width:40%;margin-left:auto;margin-right:auto;'><h2 style = 'text-align:center;color:#f73645'>Who are we?<h2>", unsafe_allow_html=True)
    #st.markdown("""<p style = 'width:50%;text-align:center;margin-left:auto;margin-right:auto;'>Hello and welcome to our delivery service! We are committed to providing you with prompt and dependable transportation services for all of your requirements. Our professional team is dedicated to ensuring that your packages and parcels arrive securely and on time. With years of experience in the courier industry, we understand the significance of timely and efficient deliveries.</p><hr style='color=#ffbf00;width:40%;margin-left:auto;margin-right:auto;'>""", unsafe_allow_html=True)
    # Create a button to redirect to another page

def phoneOrTrack():

    if st.checkbox("Phone Number"):
        phoneNo()
    if st.checkbox("Track ID"):
        trackId()

    # Add other content to the page as needed
def trackId():
    st.subheader("Please enter your track Id to track.")
    trackId_ = st.text_input("Courier ID")
    if st.checkbox("Submit "):
        couriers = fetch_all_courier()
        recordToTrack = [c for c in couriers if(c["key"]==str(trackId_))]
        if (len(recordToTrack)!=0):
            st.success("Valid Track ID")
            #st.write(recordToTrack)
            if (recordToTrack[0]["Status"]=="1"):
                st.write('<p style="font-size: 20px; font-weight: bold; text-align: center;">STATUS</p>',unsafe_allow_html=True)
                st.write('<p style="color: green; font-size: 24px; font-weight: bold; text-align: center; text-decoration: underline;">DELIVERED</p>',
                    unsafe_allow_html=True)

            else:
                st.write('<p style="font-size: 20px; font-weight: bold; text-align: center;">STATUS</p>',unsafe_allow_html=True)
                st.write(
                    '<p style="color: red; font-size: 24px; font-weight: bold; text-align: center; text-decoration: underline;">PENDING</p>',
                    unsafe_allow_html=True)

            TRAIL = [[float(slat[0]), float(slong[0])], [float(dlat[0]), float(dlong[0])]]
            print(TRAIL)
            print(source[0],destination[0])

            # Create a Folium map object centered at the location with zoom level of 7
            map = folium.Map(location=TRAIL[0], zoom_start=7)

            # Add red markers for source and destination on the map
            map.add_child(folium.Marker(location=[TRAIL[0][0], TRAIL[0][1]], popup=source[0],
                                        icon=folium.Icon(color='red', icon='map-marker')))
            map.add_child(folium.Marker(location=[TRAIL[1][0], TRAIL[1][1]], popup=destination[0],
                                        icon=folium.Icon(color='red', icon='map-marker')))

            # Draw a polyline connecting the source and destination
            folium.PolyLine(TRAIL, tooltip="HOTELS").add_to(map)

            # Save the map as a PNG file named "map.png"
            map.save("map.html")

            # Define the HTML tag with a meta refresh tag to redirect to the target page
            html = f"""
                    <html>
                    <head>
                        
                    </head>
                    <body>
                        <a href="map.html">click</a>
                    </body>
                    </html>
                    """

            # Display the HTML tag using the 'html' function
            #components.html(html)
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
    st.write('<br>', unsafe_allow_html=True)
    st.subheader("Please enter your phone Number to log in.")
    phNo = st.text_input("Phone Number")

    if st.checkbox("Submit"):
        print(phNo)
        if verifyPhoneNumber(phNo):
            st.success("Valid Number")
            global flag
            flag = 1
            HistoryOrTrack()
            #st.success("An otp is generated to this Number")
            #otp(phNo)
        else:
            st.error("No user with this phone Number")
    st.write('<hr>', unsafe_allow_html=True)

def history():
    couriers = fetch_all_courier()
    #st.write(custId)
    courierId2 = [c for c in couriers if (c["customerId"]==str(custId))]
    #st.write(courierId2)
    num_sections = len(courierId2)

    # Create a for loop to create n number of sections
    for i in range(num_sections):
        # Create a container for the section
        with st.container():
            # Add content to the section
            st.write('<div class ="st-bd"> '+
                    "Date       &nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Date"]+"</span>"+"<br>"+
                    "Description      &nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Description"]+"</span>"+"<br>"+
                    "Destination     &nbsp&nbsp&nbsp :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Destination"]+"</span>"+"<br>"+
                    "Price          &nbsp&nbsp&nbsp  :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Price"]+"</span>"+"<br>"+
                    "Source         &nbsp&nbsp&nbsp  :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Source"]+"</span>"+"<br>"+
                    "Status         &nbsp&nbsp&nbsp  :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Status"]+"</span>"+"<br>"+
                    "Weight(kgs)     &nbsp&nbsp&nbsp :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["Weight(kgs)"]+"</span>"+"<br>"+
                    "customer ID    &nbsp&nbsp&nbsp  :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["customerId"]+"</span>"+"<br>"+
                    "Courier ID     &nbsp&nbsp&nbsp  :&nbsp&nbsp&nbsp"+"<span class = "r">"+courierId2[i]["key"]+"</span>"+"<br>"+
                     '</div>', unsafe_allow_html=True)
        st.markdown("""
            <style>
            .st-bd {
                background-color: #ff4b4b;
                border: 2px solid black;
                border-radius: 5px;
                padding: 20px;
                width:500px;
                margin-left:auto;
                margin-right:auto;
                font-size: 15px;
                font-weight: bold;
                text-align :center;
            }
            .r{
                text-align: right;
            }
            </style>
        """, unsafe_allow_html=True)

def HistoryOrTrack():
    if (flag==1):
        st.write("<hr", unsafe_allow_html=True)
        st.subheader("Choose")
        if st.checkbox("View your History"):
            history()
        if st.checkbox("Track Your Order"):
            trackId()

def otp(phNo):
    st.write('<hr>', unsafe_allow_html=True)
    # otp
    verified_number ="+91"+phNo

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)

    st.subheader("Please enter OTP to log in.")
    otp_ = st.text_input("")

    if  st.radio("Submit OTP"):

        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=verified_number, code=otp_)
        if (verification_check.status=='approved'):
            st.success("Logged In successfully!")
            global flag
            flag = 1
            st.write("Now You can access History and Track your Order")
            HistoryOrTrack()
        else:
            st.error("Invalid OTP")

        """
        if (otp_=="9876"):
            st.success("Logged In successfully!")
            st.write("Now You can access History and Track your Order")
            global flag
            flag = 1
            HistoryOrTrack()"""




# Define another Streamlit app for the About page
def about():
    st.write("<h1 style = 'text-align:center;color:#ff005c'>About Page<h1>", unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>Who we are?<h2>", unsafe_allow_html=True)
    st.write(
        "<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>Hello and welcome to our delivery service! We are committed to providing you with " +
        "prompt and dependable transportation services for all of your requirements." +
        "Our professional team is dedicated to ensuring that your packages and parcels arrive" +
        "securely and on time. With years of experience in the courier industry, we understand the" +
        "significance of timely and efficient deliveries.</div><hr style='color=#ffbf00;width:40%;margin-left:auto;margin-right:auto;'>", unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>What we do?<h2>", unsafe_allow_html=True)
    st.write(
        "<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>We offer a wide range of courier services to cater to your specific requirements. Our services are designed to cater to businesses of all sizes, from small startups to large corporations. At our courier service, we use the latest technology to track your packages and provide you with real-time updates on the status of your delivery. Our state-of-the-art fleet of vehicles is equipped with GPS tracking systems, ensuring that we can monitor and manage deliveries efficiently. </div><hr style='color=#ffbf00;width:40%;margin-left:auto;margin-right:auto;'>", unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>Our motto<h2>", unsafe_allow_html=True)
    st.markdown(
        """<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>We believe in building long-term relationships with our clients and are dedicated to providing personalized services
        that meet your specific requirements. Contact us today to learn more about our courier services and how we can assist
        you with all your delivery needs.</div><hr style='color=#ff005c;width:40%;margin-left:auto;margin-right:auto;'>""",
        unsafe_allow_html=True)

def services():
    st.write("<h1 style = 'text-align:center;color:#ff005c'>Services Us<h1>", unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>Express Parcel<h2>", unsafe_allow_html=True)
    st.write(
        "<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>We realize that you may "+
        "require your package to be delivered quickly . That is why we provide express parcel delivery services to ensure that your"+
        "package arrives at its location as soon as feasible. Our express delivery services are tailored to your particular needs, "+
        "ensuring that your package arrives safely and on time."+
        "Our express parcel delivery services are accessible 24/7 , so you can send your package whenever you want and have it delivered as soon as feasible. We provide a variety of delivery options to meet your requirements, including same-day and next-day delivery.</div><hr style='color=#ffbf00;width:40%;margin-left:auto;margin-right:auto;'>",
        unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>Truckload Freight<h2>", unsafe_allow_html=True)
    st.write(
        """<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>
        If you need a large shipment delivered, our truckload freight delivery services are the ideal answer. Our skilled team is prepared to handle all kinds of freight shipments, from large bulky items to hazardous materials.

Our truck fleet is specifically built to handle large freight shipments, guaranteeing that your package arrives safely and securely. We use cutting-edge technology to track your shipment and provide you with real-time updates on its progress, giving you peace of mind that your freight is in good hands.
</div><hr style='color=#ffbf00;width:40%;margin-left:auto;margin-right:auto;'>""",
        unsafe_allow_html=True)
    st.write("<br><h2 style = 'text-align:center;color:#ff005c'>Cross-State Services<h2>", unsafe_allow_html=True)
    st.markdown(
        """<div style = 'text-align:center;width:50%;margin-left:auto;margin-right:auto;margin-top:10px;'>Our cross-state delivery services are the perfect answer for delivering packages across state lines. Our team of professionals has extensive experience handling all kinds of deliveries, including cross-state deliveries, and will ensure that your package reaches safely and on time.
We have a large network across the nation, allowing us to provide fast and dependable cross-state delivery services.
Our team is committed to providing personalized services that suit your specific needs, ensuring that your package arrives on time, every time.
</div><hr style='color=#ff005c;width:40%;margin-left:auto;margin-right:auto;'>""",
        unsafe_allow_html=True)
def contacts():
    st.write("<h1 style = 'text-align:center;color:#ff005c'>Contact Us<h1>", unsafe_allow_html=True)

    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        insert_query(name, email, message)
        st.success("Thank you for contacting us. We will get back to you soon!")

    st.markdown("""<html>
        <head>
            <title>FAQs</title>
            <style>
                .faq {
                    margin: 50px;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    max-width: 800px;
                    background-color: #f73645;
                }
                .faq h2 {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .faq h3 {
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 30px;
                    margin-bottom: 10px;
                }
                .faq p {
                    margin-bottom: 20px;
                }
                .faq .question {
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .faq .answer {
                    margin-left: 20px;
                }
                .faq .answer p:last-child {
                    margin-bottom: 0;
                }
            </style>
        </head>
        <body>
            <div class="faq">
                <h2>Frequently Asked Questions</h2>
                <div class="question">
                    <p>How can I track my shipment?</p>
                    <div class="answer">
                        <p>To monitor your shipment, go to the website, enter your courier ID, and click the track button. You can track and act on all of your shipments at once by logging in with your mobile number. </p>
                    </div>
                </div>
                <div class="question">
                    <p>What do I do if my shipment is delayed?</p>
                    <div class="answer">
                        <p>Your delivery may be delayed due to unforeseen situations. When you track your shipment on our website, you will be given a revised delivery timeframe.</p>
                    </div>
                </div>
                <div class="question">
                    <p>What do I do if I haven't received the refund of my returned shipment?</p>
                    <div class="answer">
                        <p>We do not have any refund details as a delivery partner. Please call your merchant for further assistance.</p>
                    </div>
                </div>
                <div class="question">
                    <p>How can I get proof of delivery for my shipment?</p>
                    <div class="answer">
                        <p>On the tracking page, please select the print invoice button. You will be able to receive your invoice and proof of delivery</p>
                    </div>
                </div>
                <div class="question">
                    <p>What do I do on receiving a wrong/damaged/incorrect shipment?</p>
                    <div class="answer">
                        <p>CourierExpress, as your merchant's logistics partner, does not ensure product quality. We guarantee that all shipments in our network will arrive to you untampered and in the same state that they were handed over to us by your merchant. If you have a product-related issue, please notify your merchant or the marketplace.</p>
                    </div>
                </div>
                <div class="question">
                    <p>My shipment is out for delivery. When will I receive it?</p>
                    <div class="answer">
                        <p>If your status says shipment out for delivery then you will receive the package on that day between 10:00 am -8:00pm </p>
                    </div>
                </div>
            </div>
        </body>
        </html>""",
                unsafe_allow_html=True
                )

    st.markdown("""
        <style>
        .icon-container {
            bottom: 20px;
            right: 20px;
        }
        .icon-container a {
            margin-left: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="icon-container">
        <a href="https://instagram.com/courrier__express?igshid=ZDdkNTZiNTM=" ><img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" width="30" height="30"></a>
        <a href="#" ><img src="https://cdn3.iconfinder.com/data/icons/social-icons-5/607/Twitterbird.png" width="30" height="30"></a>
        <a href="#" ><img src="https://cdn2.iconfinder.com/data/icons/social-icons-circular-color/512/gmail-512.png" width="30" height="30"></a>
        </div>
        """,
        unsafe_allow_html=True
    )
# Run your Streamlit app
if __name__ == "__main__":
    pages = {"Home": main,"About": about,"Services":services,"Contacts":contacts}
    st.set_page_config(page_title="User", page_icon=":guardsman:", layout="wide")

    st.sidebar.title("Navigation")
    page_options = list(pages.keys())
    selected_page = st.sidebar.selectbox("", page_options)
    st.sidebar.markdown("""<br><br><br><br><br><br><br><br>
    <img style = "width:300px;height:200px;" src = "https://5.imimg.com/data5/XF/MS/GLADMIN-11712474/air-freight-courier-service-500x500.png">
    """,unsafe_allow_html=True)
    page = pages[selected_page]
    page()


#"home": main, "about": about,"services":services,"Contacts":contacts,"getPhNo":phoneNo,"getTrackId":trackId,"otp":otp
