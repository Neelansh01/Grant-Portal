from flask import Flask, session, redirect, url_for, request, render_template, jsonify, send_file, flash
from datetime import timedelta
import mysql.connector
import base64
from io import BytesIO
from datetime import datetime
import mimetypes
from werkzeug.utils import secure_filename
import re
import os


 
app = Flask(__name__)
app.secret_key = 'Grant####secret***my_hard_to_crack_secret_key'
app.permanent_session_lifetime = timedelta(hours=3)
sqlconnection = ""
globalcities = ""
globalcountries = ""
globalorganizations = ""







@app.route('/grantize', methods =["GET", "POST"])
def grantize():
    global sqlconnection
    if "searchgrant" in request.form:
        try:
            title_query = request.form['tquery']
            mycursor = sqlconnection.cursor(dictionary=True)
            sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            return render_template('grantize/dashboard/browsegrants.html', grants=result)
        except:
            print("Database Connection Not Working!!")
            return render_template('grantize/grantize.html')
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        sql = "SELECT id,title,grant_source_url,expiration_date FROM ggrants LIMIT 12"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for r in result:
            if not r["expiration_date"] or r["expiration_date"]!=None:
                r["expiration_date"] = "Unknown"
            else:
                expiration_date = datetime.datetime.strptime(r["expiration_date"], '%Y-%m-%d').date()
                current_date = datetime.date.today()
                if expiration_date > current_date:
                    r["expiration_date"] = "Ongoing"
                else:
                    r["expiration_date"] = "Closed"
        documents = []
        documents.append(result[:4])
        documents.append(result[4:8])
        documents.append(result[8:])
        return render_template('grantize/grantize.html', documents=documents)
    except:
        print("Database Connection Not Working!!")
        return render_template('grantize/grantize.html')

@app.route('/logingrantizeoptions')
def logingrantizeoptions():
    return render_template('grantize/login/logingrantizeoptions.html')

@app.route('/logingrantizeres')
def logingrantizeres():
    return render_template('grantize/login/logingrantizeres.html')

@app.route('/logingrantizespo')
def logingrantizespo():
    return render_template('grantize/login/logingrantizespo.html')

@app.route('/createusergrantize')
def createusergrantize():
    global globalcountries
    return render_template('grantize/login/createusergrantize.html', globalcountries=globalcountries)

@app.route('/grantizewhyus')
def grantizewhyus():
    return render_template('grantize/navbar/whyus.html')

@app.route('/grantizeplans')
def grantizeplans():
    return render_template('grantize/navbar/plans.html')

@app.route('/grantizesponsors')
def grantizesponsors():
    return render_template('grantize/navbar/sponsors.html')

@app.route('/grantizeblogs')
def grantizeblogs():
    return render_template('grantize/navbar/blog.html')

@app.route('/grantizehelp')
def grantizehelp():
    return render_template('grantize/navbar/help.html')

@app.route('/termsnconditions')
def termsnconditions():
    return render_template('grantize/footer/termsnconditions.html')

@app.route('/grantizegrants')
def grantizegrants():
    return render_template('grantize/grants/grants.html')

@app.route('/registerresgrantize', methods =["GET", "POST"])
def registerresgrantize():
    global sqlconnection
    print("ENTER REGISTER FUNCTION")
    if "_tokenpersonal" in request.form:
        try:
            name_prefix = request.form['name_prefix']
            fname = request.form['fname']
            lname = request.form['lname']
            qualification = request.form['qualification']
            email = request.form['email_personal']
            mobile = request.form['mobile']
            username = request.form['uname']
            password = request.form['password']
            addl1 = request.form['address_line_one']
            addl2 = request.form['address_line_two']
            postcode = request.form['post_code']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
        except:
            print("REGISTER USER VARIABLES COULD NOT BE READ!!")
            return render_template('grantize/grantize.html')
        mycursor = sqlconnection.cursor()
        sql = "INSERT INTO gresearcherslist (prefix, firstname, lastname, qualification, email, mobile, username, password, addressline1, addressline2, postcode, country, state, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name_prefix, fname, lname, qualification, email, mobile, username, password, addl1, addl2, postcode, country, state, city)
        try:
            mycursor.execute(sql, val)
            sqlconnection.commit()
            sql = "SELECT id FROM gresearcherslist WHERE username = %s AND password = %s"
            values = (username, password)
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
            userid = result[0][0]
            sql = "INSERT INTO gprofilechecks (userid, sections, topics) VALUES (%s, %s, %s)"
            values = (userid, "1,-#-,2,-#-,3,-#-,4,-#-,5,-#-,6,-#-,7,-#-,8,-#-,9,-#-,10", "21,-#-,22,-#-,23,-#-,24,-#-,25,-#-,26,-#-,27,-#-,28,-#-,29,-#-,30,-#-,31,-#-,32,-#-,33,-#-,34,-#-,35,-#-,36,-#-,37,-#-,38,-#-,39,-#-,40,-#-,41,-#-,42,-#-,43,-#-,44,-#-,45,-#-,46,-#-,47,-#-,48,-#-,49,-#-,50,-#-,51,-#-,52,-#-,53,-#-,54,-#-,55,-#-,56,-#-,57,-#-,58,-#-,59")
            mycursor.execute(sql, values)
            sqlconnection.commit()
            mycursor.close()
            print("Database Insertion Successful....")
        except:
            print("Database Insertion Failed!!")
        return render_template('grantize/login/logingrantizeoptions.html')
    elif "_tokenmanager" in request.form:
        try:
            organization = request.form['organization']
            email_prefix = request.form['email_prefix']
            email_domain = request.form['email_domain']
            email_institutional = request.form['email_institutional']
            fname = request.form['fname']
            lname = request.form['lname']
            email_personal = request.form['email_personal']
            mobile = request.form['mobile']
            uname = request.form['uname']
            password = request.form['password']
            address_line_one = request.form['address_line_one']
            address_line_two = request.form['address_line_two']
            post_code = request.form['post_code']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
        except:
            print("REGISTER USER VARIABLES COULD NOT BE READ!!")
            return render_template('grantize/grantize.html')
        mycursor = sqlconnection.cursor()
        sql = "INSERT INTO gmanagerslist (organization, email_prefix, email_domain, email_institutional, fname, lname, email_personal, mobile, uname, password, address_line_one, address_line_two, postcode, country, state, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (organization, email_prefix, email_domain, email_institutional, fname, lname, email_personal, mobile, uname, password, address_line_one, address_line_two, post_code, country, state, city)
        try:
            mycursor.execute(sql, val)
            sqlconnection.commit()
            mycursor.close()
            print("Database Insertion Successful....")
        except:
            print("Database Insertion Failed!!")
        return render_template('grantize/login/logingrantizeoptions.html')
    else:
        #documents = {"qualification":qualification,"fullname":fname+" "+lname,"email":email}
        return render_template('grantize/login/logingrantizeoptions.html')


@app.route('/logingrantizeresdash', methods =["GET", "POST"])
def logingrantizeresdash():
    global sqlconnection
    print("ENTER DASHBOARD FUNCTION")
    if not session.get("loginnname"):
        if "_tokenresearcher" in request.form:
            try:
                username = request.form['user_name']
                password = request.form['pass_word']
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/grantize.html')
            mycursor = sqlconnection.cursor()
            sql = "SELECT * FROM gresearcherslist WHERE username = %s AND password = %s"
            values = (username, password)
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
            if result:
                print("Match Found..")
                session["loginnname"] = username
                session["loginid"] = result[0][0]
                print(session.get('loginid'))
                return render_template('grantize/dashboard/dashboard.html')
            else:
                print("Match Not Found..")
                return render_template('grantize/grantize.html')
        elif "_tokensponsor" in request.form:
            try:
                username = request.form['user_name']
                password = request.form['pass_word']
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/grantize.html')
            mycursor = sqlconnection.cursor()
            sql = "SELECT id FROM gmanagerslist WHERE username = %s AND password = %s"
            values = (username, password)
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
            if result:
                print("Match Found..")
                session["loginnname"] = username
                session["loginid"] = result[0][0]
                print(session.get('loginid'))
                return render_template('grantize/dashboard/dashboard.html')
            else:
                print("Match Not Found..")
                return render_template('grantize/grantize.html')
        else:
            return render_template('grantize/grantize.html')
    else:
        return render_template('grantize/dashboard/dashboard.html')
    
@app.route('/grantizelogout')
def grantizelogout():
    if session.get("loginnname"):
        session.pop("loginnname")
        session.pop("loginid")
        session.clear()
        return render_template('grantize/grantize.html')
    else:
        return render_template('grantize/grantize.html')

def read_user_checks(user, id_to_delete=100):
    global sqlconnection
    print("=-=-=-=-=-=-=-=-=")
    print("=-=-=-=-=-=-=-=-=")
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid'
        query = """
        SELECT id, userid, sections, topics
        FROM gprofilechecks
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        experiences = []
        for row in rows: 
            experiences.append(row)
            
        mycursor.close()
        
        sectionheads = {1:"Introduction",
                        2:"Academics and Experiences",
                        3:"Research Outcome",
                        4:"Publications",
                        5:"Protocols",
                        6:"Meetings and Memberships",
                        7:"Teaching and Mentoring Activities",
                        8:"Reviewing Roles",
                        9:"Other Activities",
                        10:"References"}
        topicheads = {21:"Summary",
                      22:"Objective",
                      23:"Research Statement",
                      24:"Teaching Philosophy",
                      25:"Educations",
                      26:"Credentials and Transcripts",
                      27:"Work Experiences",
                      28:"Volunteer Experiences",
                      29:"Awards and Honors",
                      30:"Grants or Contracts",
                      31:"Patents or Technology License",
                      32:"Journal Original Research",
                      33:"Journal Short Reports or Letters",
                      34:"Journal Review Articles",
                      35:"Journal Case Studies or Clinical Trials",
                      36:"Journal Methodologies",
                      37:"Journal Editorials",
                      38:"Journal Other Articles",
                      39:"Books",
                      40:"Book Chapters",
                      41:"Articles in New",
                      42:"Other Publications",
                      43:"Research Protocols",
                      44:"IACUC Protocols",
                      45:"Clinical Protocols",
                      46:"Conferences",
                      47:"Symposia",
                      48:"Workshops",
                      49:"Seminars",
                      50:"Professional Membership",
                      51:"Teaching Experiences",
                      52:"Supervision and Mentoring",
                      53:"Journals' Reviewer and Editorial Services",
                      54:"Grants' Review Services",
                      55:"Committee Activities",
                      56:"Hobbies",
                      57:"Language Proficiency",
                      58:"Other Activities",
                      59:"References"}
        urls =       {21:"grantizeprofilesummary",
                      22:"grantizeprofileobjective",
                      23:"grantizeprofileresstatement",
                      24:"grantizeprofileteachphil",
                      25:"grantizeprofileeducation",
                      26:"grantizeprofilerescredentials",
                      27:"grantizeprofileexperience",
                      28:"grantizeprofilevolunteer",
                      29:"grantizeprofileawards",
                      30:"grantizeprofilegrantscontracts",
                      31:"grantizeprofilepatents",
                      32:"grantizeprofilejourorgres",
                      33:"grantizeprofilejourshortsrep",
                      34:"grantizeprofilejourreviewarts",
                      35:"grantizeprofilejourcasestudy",
                      36:"grantizeprofilejourmethodologies",
                      37:"grantizeprofilejoureditorials",
                      38:"grantizeprofilejourotherarts",
                      39:"grantizeprofilebooks",
                      40:"grantizeprofilebookchapters",
                      41:"grantizeprofileartsinnews",
                      42:"grantizeprofileotherpubs",
                      43:"grantizeprofileresprotocols",
                      44:"grantizeprofileiacucprotocols",
                      45:"grantizeprofileclinicalprotocols",
                      46:"grantizeprofileconferences",
                      47:"grantizeprofilesymposia",
                      48:"grantizeprofileworkshops",
                      49:"grantizeprofileseminars",
                      50:"grantizeprofileprofmembers",
                      51:"grantizeprofileteachingex",
                      52:"grantizeprofilesupermentor",
                      53:"grantizeprofilejourreviewses",
                      54:"grantizeprofilegrantreviewservices",
                      55:"grantizeprofilecommactivities",
                      56:"grantizeprofilehobbies",
                      57:"grantizeprofilelangprof",
                      58:"grantizeprofileotheractivities",
                      59:"grantizeprofilereferences"}
        
        nestedtopics = {1:[21, 22, 23, 24],
                        2:[25, 26, 27, 28, 29],
                        3:[30, 31],
                        4:[32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
                        5:[43, 44, 45],
                        6:[46, 47, 48, 49, 50],
                        7:[51, 52],
                        8:[53, 54],
                        9:[55, 56, 57, 58],
                        10:[59]}

        for vals in experiences:
            print(vals)
            print(vals['sections'])
            vals['sections'] = vals['sections'].split(",-#-,")
            vals['sections'] = [int(v) for v in vals['sections']]
            vals['sectioncontent'] = {}
            vals['topics'] = vals['topics'].split(",-#-,")
            vals['topics'] = [int(v) for v in vals['topics']]
            if int(id_to_delete) in vals['topics']:
                vals['topics'].remove(int(id_to_delete))
            temp = vals['topics']
            for topic in temp:
                if int(topic) != int(id_to_delete):
                    if int(topic) in [21, 22, 23, 24]:
                        if 1 in vals['sectioncontent']:
                            vals['sectioncontent'][1].append(topic)
                        else:
                            vals['sectioncontent'][1] = [topic]
                    elif int(topic) in [25, 26, 27, 28, 29]:
                        if 2 in vals['sectioncontent']:
                            vals['sectioncontent'][2].append(topic)
                        else:
                            vals['sectioncontent'][2] = [topic]
                    elif int(topic) in [30, 31]:
                        if 3 in vals['sectioncontent']:
                            vals['sectioncontent'][3].append(topic)
                        else:
                            vals['sectioncontent'][3] = [topic]
                    elif int(topic) in [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]:
                        if 4 in vals['sectioncontent']:
                            vals['sectioncontent'][4].append(topic)
                        else:
                            vals['sectioncontent'][4] = [topic]
                    elif int(topic) in [43, 44, 45]:
                        if 5 in vals['sectioncontent']:
                            vals['sectioncontent'][5].append(topic)
                        else:
                            vals['sectioncontent'][5] = [topic]
                    elif int(topic) in [46, 47, 48, 49, 50]:
                        if 6 in vals['sectioncontent']:
                            vals['sectioncontent'][6].append(topic)
                        else:
                            vals['sectioncontent'][6] = [topic]
                    elif int(topic) in [51, 52]:
                        if 7 in vals['sectioncontent']:
                            vals['sectioncontent'][7].append(topic)
                        else:
                            vals['sectioncontent'][7] = [topic]
                    elif int(topic) in [53, 54]:
                        if 8 in vals['sectioncontent']:
                            vals['sectioncontent'][8].append(topic)
                        else:
                            vals['sectioncontent'][8] = [topic]
                    elif int(topic) in [55, 56, 57, 58]:
                        if 9 in vals['sectioncontent']:
                            vals['sectioncontent'][9].append(topic)
                        else:
                            vals['sectioncontent'][9] = [topic]
                    elif int(topic) in [59]:
                        if 10 in vals['sectioncontent']:
                            vals['sectioncontent'][10].append(topic)
                        else:
                            vals['sectioncontent'][10] = [topic]
        experiences[0]["sectionheads"]=sectionheads
        experiences[0]["topicheads"] = topicheads
        experiences[0]["urls"] = urls
        return experiences, nestedtopics
    except Exception as e:
        print("Error fetching work experience from database:", str(e))
        return []

def read_user_profile_info(user):
    global sqlconnection
    cursor = sqlconnection.cursor(dictionary=True)
    sql = ("SELECT firstname, middlename, lastname, mobile, email_institutional, "
            "email, organization, department, qualification, date_of_birth, citizenships,"
            "addressline1, addressline2, postcode, country, state, city, linkedln_url, "
            "pubmed_url, google_scholar, personal_blog, orcid FROM gresearcherslist WHERE id = %s")
    cursor.execute(sql, (user,))
    user_profile_info = cursor.fetchone()
    cursor.close()
    return user_profile_info

@app.route('/grantizeprofile', methods =["GET", "POST"])
def grantizeprofile():
    if session.get("loginnname"):
        user = session.get('loginid')
        cursor = sqlconnection.cursor()
        query = "SELECT id, qualification, email, firstname, lastname FROM gresearcherslist WHERE id = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            profileinfo = {
                "id": result[0],
                "qualification": result[1],
                "email": result[2],
                "fullname": result[3]+" "+result[4],
            }
        if "checks" in request.form:
            try:
                selected_sections = request.form.getlist('sections[]')
                sections, topics = [], []
                for ids in selected_sections:
                    if int(ids)<20:
                        sections.append(ids)
                    else:
                        topics.append(ids)
                sections = ",-#-,".join(sections)
                topics = ",-#-,".join(topics)
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                user_profile_info = read_user_profile_info(user)
                return render_template('grantize/dashboard/profile.html', profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
            try:
                mycursor = sqlconnection.cursor()
                # Use parameterized query for deletion to avoid SQL injection
                delete_query = "DELETE FROM gprofilechecks WHERE userid = %s"
                mycursor.execute(delete_query, (user,))
                sqlconnection.commit()
                sql = "INSERT INTO gprofilechecks (userid, sections, topics) VALUES (%s, %s, %s)"
                values = (user, sections, topics)
                mycursor.execute(sql, values)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("DATBASE FAILURE!!")
                return render_template('grantize/dashboard/profile.html', profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations)
            ## Code to Read
            user_profile_info = read_user_profile_info(user)
            documents, nestedtopics = read_user_checks(user)
            return render_template('grantize/dashboard/profile.html', documents=documents, nestedtopics=nestedtopics, profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
        if "updateprofile" in request.form:
            first_name = request.form.get('first_name')
            middle_name = request.form.get('middle_name')
            last_name = request.form.get('last_name')
            telephone_number = request.form.get('telephone_number')
            email_institutional = request.form.get('email_institutional')
            email_personal = request.form.get('email_personal')
            organization = request.form.get('organization')
            department = request.form.get('department')
            current_position = request.form.get('current_position')
            date_of_birth = request.form.get('date_of_birth')
            address_line_one = request.form.get('address_line_one')
            address_line_two = request.form.get('address_line_two')
            post_code = request.form.get('post_code')
            country = request.form.get('country')
            state = request.form.get('state')
            city = request.form.get('city')
            citizenships = request.form.get('citizenships')
            linkedin_url = request.form.get('linkedln_url')
            pubmed_url = request.form.get('pubmed_url')
            google_scholar = request.form.get('google_scholar')
            personal_blog = request.form.get('personal_blog')
            orcid = request.form.get('orcid')
            if date_of_birth:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            try:
                cursor = sqlconnection.cursor()
                sql = ("UPDATE gresearcherslist SET firstname=%s, middlename=%s, lastname=%s, "
                    "mobile=%s, email_institutional=%s, email=%s, organization=%s, "
                    "department=%s, qualification=%s, date_of_birth=%s, citizenships=%s, addressline1=%s, "
                    "addressline2=%s, postcode=%s, country=%s, state=%s, city=%s, linkedln_url=%s, "
                    "pubmed_url=%s, google_scholar=%s, personal_blog=%s, orcid=%s WHERE id=%s")
                values = (first_name, middle_name, last_name, telephone_number, email_institutional,
                        email_personal, organization, department, current_position, date_of_birth, citizenships,
                        address_line_one, address_line_two, post_code, country, state, city,
                        linkedin_url, pubmed_url, google_scholar, personal_blog, orcid, user)
                cursor.execute(sql, values)
                sqlconnection.commit()
                cursor.close()
            except Exception as e:
                print(e)
            documents, nestedtopics = read_user_checks(user)
            user_profile_info = read_user_profile_info(user)
            return render_template('grantize/dashboard/profile.html', documents=documents, nestedtopics=nestedtopics, profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
        if "changepassword" in request.form:
            password = request.form.get('password')
            try:
                cursor = sqlconnection.cursor()
                sql = ("UPDATE gresearcherslist SET password=%s WHERE id=%s")
                values = (password, user)
                cursor.execute(sql, values)
                sqlconnection.commit()
                cursor.close()
            except Exception as e:
                print(e)
            documents, nestedtopics = read_user_checks(user)
            user_profile_info = read_user_profile_info(user)
            return render_template('grantize/dashboard/profile.html', documents=documents, nestedtopics=nestedtopics, profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
        if "deletetopics" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/credentials.html')
            ## Code to Read
            documents, nestedtopics = read_user_checks(user, id_to_delete)
            user_profile_info = read_user_profile_info(user)
            return render_template('grantize/dashboard/profile.html', documents=documents, nestedtopics=nestedtopics, profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
        else:
            print("__________")
            print(user)
            print("__________")
            documents, nestedtopics = read_user_checks(user)
            user_profile_info = read_user_profile_info(user)
            print(documents)
            return render_template('grantize/dashboard/profile.html', documents=documents, nestedtopics=nestedtopics, profileinfo=profileinfo, globalcountries=globalcountries, globalorganizations=globalorganizations, user_profile_info=user_profile_info)
    else:
        return render_template('grantize/grantize.html')

def read_summary(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, description, keyword_description
        FROM gsummary
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []

@app.route('/grantizeprofilesummary', methods =["GET", "POST"])
def grantizeprofilesummary():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gsummary
                (userid, description, keyword_description)
                VALUES (%s, %s, %s)
                """
                values = [user, description, keyword_description]
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Summary chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_summary(user)
            return render_template('grantize/profile/summary.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gsummary SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_summary(user)
            return render_template('grantize/profile/summary.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gsummary WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/summary.html')
            ## Code to Read
            documents = read_summary(user)
            return render_template('grantize/profile/summary.html', documents = documents)
        else:
            documents = read_summary(user)
            print(documents)
            return render_template('grantize/profile/summary.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')

def read_objective(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, description, keyword_description
        FROM gobjective
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []

@app.route('/grantizeprofileobjective', methods =["GET", "POST"])
def grantizeprofileobjective():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gobjective
                (userid, description, keyword_description)
                VALUES (%s, %s, %s)
                """
                values = [user, description, keyword_description]
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Summary chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_objective(user)
            return render_template('grantize/profile/objective.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gobjective SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_objective(user)
            return render_template('grantize/profile/objective.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gobjective WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/objective.html')
            ## Code to Read
            documents = read_objective(user)
            return render_template('grantize/profile/objective.html', documents = documents)
        else:
            documents = read_objective(user)
            print(documents)
            return render_template('grantize/profile/objective.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_research_statement(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, description, keyword_description
        FROM gresstatement
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []

@app.route('/grantizeprofileresstatement', methods =["GET", "POST"])
def grantizeprofileresstatement():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gresstatement
                (userid, description, keyword_description)
                VALUES (%s, %s, %s)
                """
                values = [user, description, keyword_description]
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Summary chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_research_statement(user)
            return render_template('grantize/profile/resstatement.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gresstatement SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_research_statement(user)
            return render_template('grantize/profile/resstatement.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gresstatement WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/resstatement.html')
            ## Code to Read
            documents = read_research_statement(user)
            return render_template('grantize/profile/resstatement.html', documents = documents)
        else:
            documents = read_research_statement(user)
            print(documents)
            return render_template('grantize/profile/resstatement.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_teaching_philosophy(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, description, keyword_description
        FROM gteachphilosophy
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []

@app.route('/grantizeprofileteachphil', methods =["GET", "POST"])
def grantizeprofileteachphil():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gteachphilosophy
                (userid, description, keyword_description)
                VALUES (%s, %s, %s)
                """
                values = [user, description, keyword_description]
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Summary chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_teaching_philosophy(user)
            return render_template('grantize/profile/teachphilosophy.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gteachphilosophy SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_teaching_philosophy(user)
            return render_template('grantize/profile/teachphilosophy.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gteachphilosophy WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/teachphilosophy.html')
            ## Code to Read
            documents = read_teaching_philosophy(user)
            return render_template('grantize/profile/teachphilosophy.html', documents = documents)
        else:
            documents = read_teaching_philosophy(user)
            print(documents)
            return render_template('grantize/profile/teachphilosophy.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
# Helper functions
def get_form_data_or_none(field_name):
    return request.form.get(field_name, '').strip() or None

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m-%d-%Y').date() if date_str else None
    except:
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

def get_multiple_select(field_name):
    return request.form.getlist(field_name)  # Handles multiple select options

def read_education_details(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the profile table
        query = """
        SELECT id, userid, organization, department, degree, gpa_type, gpa_value, start_date, end_date, 
               disciplines, courses, subjects, majors, mentors, abstract, techniques, instruments, softwares,
               soft_skills, key_skills_experience
        FROM geducation
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            # If storing multiple selections as comma-separated, convert back to list
            for field in ['disciplines', 'courses', 'subjects', 'majors', 'mentors', 'techniques', 'instruments', 'softwares', 'soft_skills']:
                if row[field]:
                    row[field] = row[field].split(',')
                else:
                    row[field] = []
            profiles.append(row)
        
        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching profile details from database:", str(e))
        return []


@app.route('/grantizeprofileeducation', methods =["GET", "POST"])
def grantizeprofileeducation():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                degree = get_form_data_or_none('degree')
                gpa_type = get_form_data_or_none('type')
                gpa_value = get_form_data_or_none('name')
                start_date = parse_date(get_form_data_or_none('start_date'))
                end_date = parse_date(get_form_data_or_none('end_date'))
                disciplines = get_multiple_select('discipline')
                courses = get_multiple_select('courses')
                subjects = get_multiple_select('subjects')
                majors = get_multiple_select('major')
                mentors = get_multiple_select('mentors')
                abstract = get_form_data_or_none('abstract')
                keyword_abstract = get_multiple_select('keyword_abstract')
                techniques = get_multiple_select('techniques')
                instruments = get_multiple_select('instruments')
                softwares = get_multiple_select('softwares')
                soft_skills = get_multiple_select('soft_skills')
                key_skills_experience = get_form_data_or_none('description')

                sql = """INSERT INTO geducation (userid, organization, department, degree, gpa_type, gpa_value, start_date, end_date, disciplines, courses, subjects, majors, mentors, abstract, keyword_abstract, techniques, instruments, softwares, soft_skills, key_skills_experience)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = [user, organization, department, degree, gpa_type, gpa_value, start_date, end_date, ','.join(disciplines), ','.join(courses), ','.join(subjects), ','.join(majors), ','.join(mentors), abstract, ','.join(keyword_abstract), ','.join(techniques), ','.join(instruments), ','.join(softwares), ','.join(soft_skills), key_skills_experience]
                for i in range(len(values)):
                    if not values or values[i] is None or len(str(values[i]))==0:
                        values[i] = ""
                values = tuple(values)
                print("+_+_+_+_+_+")
                print(values)
                print("+_+_+_+_+_+")
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, values)
                sqlconnection.commit()
                mycursor.close()
                flash('Profile information added successfully!', 'success')
            except Exception as e:
                flash(f'Failed to add profile information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_education_details(user)
            return render_template('grantize/profile/education.html', documents = documents)
        elif "editsection" in request.form:
            profile_id = get_form_data_or_none('chapter_id')  # Assuming you have a hidden input for the profile ID
            try:
                updates = []
                values = []

                # Define a mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'organization',
                    'department': 'department',
                    'degree': 'degree',
                    'type': 'gpa_type',
                    'name': 'gpa_value',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'discipline': 'disciplines',
                    'courses': 'courses',
                    'subjects': 'subjects',
                    'major': 'majors',
                    'mentors': 'mentors',
                    'abstract': 'abstract',
                    'keyword_abstract': 'keyword_abstract',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills',
                    'description': 'key_skills_experience'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field) if '[]' not in form_field else ','.join(get_multiple_select(form_field))
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                # Append date conversion for start_date and end_date
                if 'start_date' in request.form:
                    start_date = parse_date(get_form_data_or_none('start_date'))
                    if start_date:
                        values[values.index(get_form_data_or_none('start_date'))] = start_date

                if 'end_date' in request.form:
                    end_date = parse_date(get_form_data_or_none('end_date'))
                    if end_date:
                        values[values.index(get_form_data_or_none('end_date'))] = end_date

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE geducation SET {update_sql} WHERE id = %s"
                    values.append(profile_id)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    flash('Profile details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update profile details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_education_details(user)
            return render_template('grantize/profile/education.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM geducation WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/education.html')
            ## Code to Read
            documents = read_education_details(user)
            return render_template('grantize/profile/education.html', documents = documents)
        else:
            documents = read_education_details(user)
            print(documents)
            return render_template('grantize/profile/education.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cred_read_table(user):
    global sqlconnection
    # SQL query to get all files and other data with condition "WHERE 1=1"
    mycursor = sqlconnection.cursor()
    query = "SELECT description, organization, filename, id FROM gcredentials WHERE userid = "+str(user)
    mycursor.execute(query)
    rows = mycursor.fetchall()
    documents = []
    # Prepare each row with base64 encoding for the file
    for row in rows:
        documents.append({
            'description': row[0],
            'organization': row[1],
            'filename' : row[2],
            'id' : row[3]
        })
    mycursor.close()
    return documents

@app.route('/download/<doc_id>')
def download_file(doc_id):
    global sqlconnection
    cursor = sqlconnection.cursor()
    try:
        # Prepare a query to fetch the file data by name
        query = "SELECT filename, filecontent FROM gcredentials WHERE id = %s"
        cursor.execute(query, (doc_id,))
        file_data = cursor.fetchone()
        if file_data is None:
            return jsonify({'error': 'File not found'}), 404

        # Secure the filename to prevent path traversal attacks
        filename = secure_filename(file_data[0])

        # Guess the MIME type of the file based on its extension
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Fallback to binary type if MIME type is undetectable

        # Send the file data as an attachment
        file_stream = BytesIO(file_data[1])
        return send_file(
            file_stream,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
    except mysql.connector.Error as err:
        print("Error: ", err)
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()

def prmission_show_me(main_table, except_persons, user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor()
        sql = "UPDATE "+main_table+" SET showme = '"+except_persons+"' WHERE userid = "+str(user)
        mycursor.execute(sql)
        sqlconnection.commit()
        mycursor.close()
    except:
        print("Database Operation Failed!!")

def prmission_hide_designation(main_table, multiselect, user):
    global sqlconnection
    try:
        except_persons = ",".join(multiselect)
        mycursor = sqlconnection.cursor()
        sql = "UPDATE "+main_table+" SET hidedesignation = '"+except_persons+"' WHERE userid = "+str(user)
        mycursor.execute(sql)
        sqlconnection.commit()
        mycursor.close()

    except:
        print("Database Operation Failed!!")

def prmission_hide_individuals(main_table, except_persons, user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor()
        sql = "UPDATE "+main_table+" SET hideindividuals = '"+except_persons+"' WHERE userid = "+str(user)
        mycursor.execute(sql)
        sqlconnection.commit()
        mycursor.close()
    except:
        print("Database Operation Failed!!")

@app.route('/grantizeprofilerescredentials', methods =["GET", "POST"])
def grantizeprofilerescredentials():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "addcredtrans" in request.form:
            try:
                credname, credorg, credfiles, credfilename = None, None, None, None
                if 'name' in request.form:
                    credname = request.form['name']
                if 'organization' in request.form:
                    credorg = request.form['organization']
                if 'filecred' in request.files and request.files['filecred'].filename != '' and allowed_file(request.files['filecred'].filename):
                    credfiles = request.files['filecred']
                    file_content = credfiles.read()
                    credfilename = secure_filename(credfiles.filename)
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/credentials.html')
            try:
                mycursor = sqlconnection.cursor()
                sql = "INSERT INTO gcredentials (userid, description, organization, filename, filecontent) VALUES (%s, %s, %s, %s, %s)"
                values = (user, credname, credorg, credfilename, file_content)
                mycursor.execute(sql, values)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("DATBASE FAILURE!!")
                return render_template('grantize/profile/credentials.html')
            ## Code to Read
            documents = cred_read_table(user)
            return render_template('grantize/profile/credentials.html', documents=documents)
        if "editform" in request.form:
            try:
                cred_id = request.form['credid']
                updates = []
                values = []

                # Check each field and add to the update statement if present
                if 'description' in request.form and request.form['description']:
                    updates.append("description = %s")
                    values.append(request.form['description'])

                if 'organization' in request.form and request.form['organization']:
                    updates.append("organization = %s")
                    values.append(request.form['organization'])

                # Handle file upload
                if 'changefile' in request.files and request.files['changefile'].filename != '' and allowed_file(request.files['changefile'].filename):
                    credfile = request.files['changefile']
                    file_content = credfile.read()
                    credfilename = secure_filename(credfile.filename)
                    updates.append("filename = %s")
                    values.append(credfilename)
                    updates.append("filecontent = %s")
                    values.append(file_content)
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/credentials.html')
            try:
                if updates:
                    sql = f"UPDATE gcredentials SET {', '.join(updates)} WHERE id = %s"
                    print(sql)
                    print(cred_id)
                    print(updates)
                    values.append(cred_id)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
            except:
                print("DATBASE FAILURE!!")
                return render_template('grantize/profile/credentials.html')
            ## Code to Read
            documents = cred_read_table(user)
            return render_template('grantize/profile/credentials.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['document_id']
                print("-=-=-")
                print(id_to_delete)
                print("-=-=-")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gcredentials WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/credentials.html')
            ## Code to Read
            documents = cred_read_table(user)
            return render_template('grantize/profile/credentials.html', documents=documents)
        else:
            documents = cred_read_table(user)
            return render_template('grantize/profile/credentials.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')


def work_experience_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid'
        query = """
        SELECT id, employer, department, type, appoint, title, 
                current, start, end, mentor, responsibilities, rkeywords,
                techniques, skilldesc, skeywords, instruments, softwares, softskills
        FROM gexperience
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        experiences = []
        for row in rows: 
            experiences.append(row)
            
        mycursor.close()
        return experiences
    except Exception as e:
        print("Error fetching work experience from database:", str(e))
        return []


@app.route('/grantizeprofileexperience', methods =["GET", "POST"])
def grantizeprofileexperience():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createexp" in request.form:
            print("_________________STEP 0__________________")
            try:
                # Helper function to get the form data or return None if blank
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Retrieve form data
                employer_name = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                job_type = get_form_data_or_none('type')
                appoint_type = get_form_data_or_none('name')
                job_title = get_form_data_or_none('title')
                current_job = request.form['is_this_current_job'] if 'is_this_current_job' in request.form else None
                start_date = get_form_data_or_none('start_date')
                end_date = get_form_data_or_none('end_date')
                mentor_name = get_form_data_or_none('mentors')
                main_responsibilities = get_form_data_or_none('description2')
                keyword_abstract = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')
                key_skills_experience = ','.join(filter(None, request.form.getlist('description')))
                keyword_description = get_form_data_or_none('keyword_description')
                start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
                end_date = datetime.strptime(end_date, '%m-%d-%Y').date()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/experience.html')
            print("_________________STEP 1__________________")
            try:
                mycursor = sqlconnection.cursor()
                sql = """
                INSERT INTO gexperience
                (userid, employer, department, type, appoint, title, 
                current, start, end, mentor, responsibilities, rkeywords,
                techniques, skilldesc, skeywords, instruments, softwares, softskills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, employer_name, department, job_type, appoint_type, job_title,
                        current_job, start_date, end_date, mentor_name, main_responsibilities, 
                        keyword_abstract, techniques, key_skills_experience, keyword_description,
                        instruments, softwares, soft_skills]
                for i in range(len(values)):
                    if values[i] == None:
                        values[i] = ""
                values = tuple(values)
                print(values)
                mycursor.execute(sql, values)
                sqlconnection.commit()
                mycursor.close()
                print("_________________STEP 3__________________")
                flash('Work experience added successfully!', 'success')
            except:
                print("DATBASE FAILURE!!")
                return render_template('grantize/profile/experience.html')
            ## Code to Read
            documents = work_experience_read_table(user)
            return render_template('grantize/profile/experience.html', documents = documents)
        if "editsection" in request.form:
            try:
                print("_________________EDIT STEP 0__________________")
                experience_id = request.form['document_id']
                updates = []
                values = []

                # Helper function to get form data or None
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'employer': 'employer',
                    'department': 'department',
                    'type': 'type',
                    'appoint': 'appoint',
                    'title': 'title',
                    'current': 'current',
                    # Assuming dates are in 'MM-DD-YYYY' format, we parse them to 'YYYY-MM-DD' format for SQL
                    'start': 'start',
                    'end': 'end',
                    'mentors': 'mentor',
                    'responsibilities': 'responsibilities',
                    'rkeywords': 'rkeywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'softskills',
                    'skilldesc': 'skilldesc',
                    'skeywords': 'skeywords'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_info in form_to_db_map.items():
                    # db_info can be either a string or a tuple (column_name, transform_function)
                    db_column, transform = db_info if isinstance(db_info, tuple) else (db_info, None)
                    form_data = get_form_data_or_none(form_field)
                    if form_field in ['start_date','end_date']:
                        form_data = parse_date(form_data)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        # Apply transformation function if provided
                        values.append(transform(form_data) if transform else form_data)
                print("_________________STEP 1__________________")
                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE gexperience SET {update_sql} WHERE id = %s"
                    values.append(experience_id)
                    print(update_sql)
                    print(experience_id)
                    print(values)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________STEP 2 EDIT__________________")
                    flash('Experience updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash('Failed to update experience due to an error.', 'error')
                print(f"Error updating experience: {e}")
                return render_template('error_template.html'), 500
            ## Code to Read
            documents = work_experience_read_table(user)
            return render_template('grantize/profile/experience.html', documents = documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gexperience WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/credentials.html')
            ## Code to Read
            documents = work_experience_read_table(user)
            return render_template('grantize/profile/experience.html', documents = documents)
        else:
            documents = work_experience_read_table(user)
            print(documents)
            return render_template('grantize/profile/experience.html', documents = documents)
    else:
        return render_template('grantize/grantize.html')
    
def volunteer_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid'
        query = """
        SELECT id, employer, department, type, appoint, title, 
                current, start, end, mentor, responsibilities, rkeywords,
                techniques, skilldesc, skeywords, instruments, softwares, softskills
        FROM gvolunteer
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        experiences = []
        for row in rows: 
            experiences.append(row)
            
        mycursor.close()
        return experiences
    except Exception as e:
        print("Error fetching work experience from database:", str(e))
        return []

@app.route('/grantizeprofilevolunteer', methods =["GET", "POST"])
def grantizeprofilevolunteer():
    global sqlconnection
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createexp" in request.form:
            print("_________________STEP 0__________________")
            try:
                # Helper function to get the form data or return None if blank
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Retrieve form data
                employer_name = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                job_type = get_form_data_or_none('type')
                appoint_type = get_form_data_or_none('name')
                job_title = get_form_data_or_none('title')
                current_job = request.form['is_this_current_job'] if 'is_this_current_job' in request.form else None
                start_date = get_form_data_or_none('start_date')
                end_date = get_form_data_or_none('end_date')
                mentor_name = get_form_data_or_none('mentors')
                main_responsibilities = get_form_data_or_none('description2')
                keyword_abstract = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')
                key_skills_experience = ','.join(filter(None, request.form.getlist('description')))
                keyword_description = get_form_data_or_none('keyword_description')
                start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
                end_date = datetime.strptime(end_date, '%m-%d-%Y').date()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/volunteer.html')
            print("_________________STEP 1__________________")
            try:
                mycursor = sqlconnection.cursor()
                sql = """
                INSERT INTO gvolunteer
                (userid, employer, department, type, appoint, title, 
                current, start, end, mentor, responsibilities, rkeywords,
                techniques, skilldesc, skeywords, instruments, softwares, softskills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, employer_name, department, job_type, appoint_type, job_title,
                        current_job, start_date, end_date, mentor_name, main_responsibilities, 
                        keyword_abstract, techniques, key_skills_experience, keyword_description,
                        instruments, softwares, soft_skills]
                for i in range(len(values)):
                    if values[i] == None:
                        values[i] = ""
                values = tuple(values)
                print(values)
                mycursor.execute(sql, values)
                sqlconnection.commit()
                mycursor.close()
                print("_________________STEP 3__________________")
                flash('Work experience added successfully!', 'success')
            except:
                print("DATBASE FAILURE!!")
                return render_template('grantize/profile/volunteer.html')
            ## Code to Read
            documents = volunteer_read_table(user)
            return render_template('grantize/profile/volunteer.html', documents = documents)
        if "editsection" in request.form:
            try:
                print("_________________EDIT STEP 0__________________")
                experience_id = request.form['document_id']
                updates = []
                values = []

                # Helper function to get form data or None
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'employer',
                    'department': 'department',
                    'type': 'type',
                    'name': 'appoint',
                    'title': 'title',
                    'is_this_current_job': 'current',
                    # Assuming dates are in 'MM-DD-YYYY' format, we parse them to 'YYYY-MM-DD' format for SQL
                    'start_date': 'start',
                    'end_date': 'end',
                    'mentors': 'mentor',
                    'description2': 'responsibilities',
                    'keyword_abstract': 'rkeywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'softskills',
                    'description': 'skilldesc',
                    'keyword_description': 'skeywords'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_info in form_to_db_map.items():
                    # db_info can be either a string or a tuple (column_name, transform_function)
                    db_column, transform = db_info if isinstance(db_info, tuple) else (db_info, None)
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if form_field in ['start_date','end_date']:
                            form_data = parse_date(form_data)
                        updates.append(f"{db_column} = %s")
                        # Apply transformation function if provided
                        values.append(transform(form_data) if transform else form_data)
                print("_________________STEP 1__________________")
                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE gvolunteer SET {update_sql} WHERE id = %s"
                    values.append(experience_id)
                    print(update_sql)
                    print(experience_id)
                    print(sql)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________STEP 2 EDIT__________________")
                    flash('Experience updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash('Failed to update experience due to an error.', 'error')
                print(f"Error updating experience: {e}")
                return render_template('error_template.html'), 500
            ## Code to Read
            documents = volunteer_read_table(user)
            return render_template('grantize/profile/volunteer.html', documents = documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gvolunteer WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/volunteer.html')
            ## Code to Read
            documents = volunteer_read_table(user)
            return render_template('grantize/profile/volunteer.html', documents = documents)
        else:
            documents = volunteer_read_table(user)
            print(documents)
            return render_template('grantize/profile/volunteer.html', documents = documents)
    else:
        return render_template('grantize/grantize.html')
    
def awards_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid' from gawards
        query = """
        SELECT id, awards, type, vdate, organization, department, description
        FROM gawards
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        awards = []
        for row in rows:
            awards.append(row)
            
        mycursor.close()
        return awards
    except Exception as e:
        print("Error fetching awards from database:", str(e))
        return []
    
@app.route('/grantizeprofileawards', methods =["GET", "POST"])
def grantizeprofileawards():
    global sqlconnection
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createawards" in request.form:
            try:
                # Helper function to get the form data or return None if blank
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None
                # Retrieve form data
                awards = get_form_data_or_none('awards')  # Assuming you populate this select in your form
                award_type = get_form_data_or_none('type')
                award_date = get_form_data_or_none('vdate')
                award_organization = get_form_data_or_none('organization')
                award_department = get_form_data_or_none('department')
                award_description = get_form_data_or_none('description')
                keywords = ','.join(request.form.getlist('keyword_description'))  # Convert list of keywords into a string
                # Convert date from string to date object
                award_date = datetime.strptime(award_date, '%m-%d-%Y').date() if award_date else None
            except Exception as e:
                print(f"Error reading form data: {str(e)}")
                return render_template('grantize/profile/awards.html')
            try:
                cursor = sqlconnection.cursor()
                sql = """
                INSERT INTO gawards (userid, awards, type, vdate, organization, department, description, keywords)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, awards, award_type, award_date, award_organization, award_department, award_description, keywords)  # Example with user ID as 1
                cursor.execute(sql, values)
                sqlconnection.commit()
                flash('Award added successfully!', 'success')
            except Exception as e:
                print(f"Database Error: {str(e)}")
                sqlconnection.rollback()
                flash('Failed to add award.', 'error')
                return render_template('grantize/profile/awards.html', error="Failed to add award.")
            finally:
                if sqlconnection.is_connected():
                    cursor.close()
            ## Code to Read
            documents = awards_read_table(user)
            return render_template('grantize/profile/awards.html', documents = documents)
        if "editsection" in request.form:
            try:
                print("_________________EDIT STEP 0__________________")
                award_id = request.form['award_id']  # Ensure you have an input in your form with name='award_id'
                updates = []
                values = []

                # Helper function to get form data or None
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'awards': 'awards',
                    'type': 'type',
                    'vdate': ('vdate', lambda x: datetime.strptime(x, '%m-%d-%Y').strftime('%Y-%m-%d') if x else None),
                    'organization': 'organization',
                    'department': 'department',
                    'description': 'description',
                    'keyword_description': 'keywords'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_info in form_to_db_map.items():
                    db_column, transform = db_info if isinstance(db_info, tuple) else (db_info, None)
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        # Apply transformation function if provided
                        values.append(transform(form_data) if transform else form_data)

                print("_________________EDIT STEP 1__________________")

                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE gawards SET {update_sql} WHERE id = %s"
                    print(sql)
                    print(values)
                    values.append(award_id)
                    print(award_id)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    flash('Award updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

                print("_________________EDIT STEP 2__________________")

            except Exception as e:
                flash(f'Failed to update award due to an error: {e}', 'error')
                return render_template('error_template.html'), 500
            ## Code to Read updated data
            documents = awards_read_table(user)
            return render_template('grantize/profile/awards.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gawards WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/awards.html')
            ## Code to Read
            documents = awards_read_table(user)
            return render_template('grantize/profile/awards.html', documents = documents)
        else:
            documents = awards_read_table(user)
            print(documents)
            return render_template('grantize/profile/awards.html', documents = documents)
    else:
        return render_template('grantize/grantize.html')
    
def grants_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid' from ggrants
        query = """
        SELECT id, title, project_number, total_funding, url, start_date, end_date, principal_investigators,
               investigators, funding_org, funding_dept, awardee_org, awardee_dept, project_terms, 
               abstract, abstract_keywords
        FROM ggrantscontracts
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        grants = []
        for row in rows:
            grants.append(row)
            
        mycursor.close()
        return grants
    except Exception as e:
        print("Error fetching grants from database:", str(e))
        return []

@app.route('/grantizeprofilegrantscontracts', methods =["GET", "POST"])
def grantizeprofilegrantscontracts():
    global sqlconnection
    if session.get("loginnname"):
        user = session.get('loginid')
        if "creategrant" in request.form:
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                title = get_form_data_or_none('title')
                project_number = get_form_data_or_none('name')
                total_funding = get_form_data_or_none('type')
                url = get_form_data_or_none('url')
                start_date = get_form_data_or_none('start_date')
                end_date = get_form_data_or_none('end_date')
                principal_investigators = get_form_data_or_none('authors')
                investigators = get_form_data_or_none('co_authors')
                funding_org = get_form_data_or_none('sponsor')
                funding_dept = get_form_data_or_none('sponsor_department')
                awardee_org = get_form_data_or_none('organization')
                awardee_dept = get_form_data_or_none('department')
                project_terms = request.form.getlist('keywords')  # Handle multiple select inputs
                abstract = get_form_data_or_none('description')
                abstract_keywords = get_form_data_or_none('keyword_abstract')

                # Format dates
                if start_date:
                    start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%m-%d-%Y').date()

                # Prepare SQL query and data
                sql = """
                INSERT INTO ggrantscontracts
                (userid, title, project_number, total_funding, url, start_date, end_date, 
                principal_investigators, investigators, funding_org, funding_dept, 
                awardee_org, awardee_dept, project_terms, abstract, abstract_keywords)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, project_number, total_funding, url, start_date, end_date, 
                        principal_investigators, investigators, funding_org, funding_dept, 
                        awardee_org, awardee_dept, ','.join(project_terms), abstract, abstract_keywords]
                for i in range(len(values)):
                    if values[i] == None:
                        values[i] = ""
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Grant contract added successfully!', 'success')
            except Exception as e:
                flash(f'Failed to add grant contract due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = grants_read_table(user)
            return render_template('grantize/profile/grantscontracts.html', documents = documents)
        if "editsection" in request.form:
            try:
                print("_________________EDIT STEP 0__________________")
                grant_id = request.form['grant_id']  # Ensure you have a hidden input in your form with the name 'document_id'
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'name': 'project_number',
                    'type': 'total_funding',
                    'url': 'url',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'authors': 'principal_investigators',
                    'co_authors': 'investigators',
                    'sponsor': 'funding_org',
                    'sponsor_department': '	funding_dept',
                    'organization': 'awardee_org',
                    'department': 'awardee_dept',
                    'keywords': 'project_terms',
                    'abstract': 'abstract',
                    'keyword_abstract': 'abstract_keywords'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_info in form_to_db_map.items():
                    db_column, transform = db_info if isinstance(db_info, tuple) else (db_info, None)
                    form_data = get_form_data_or_none(form_field)
                    if form_field in ['start_date','end_date']:
                        form_data = parse_date(form_data)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        # Apply transformation function if provided
                        values.append(transform(form_data) if transform else form_data)

                print("_________________EDIT STEP 1__________________")

                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE ggrantscontracts SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(grant_id)
                    print(values)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    flash('Grant details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

                print("_________________EDIT STEP 2__________________")

            except Exception as e:
                flash(f'Failed to update grant details due to an error: {e}', 'error')
                return render_template('error_template.html'), 500
            documents = grants_read_table(user)
            return render_template('grantize/profile/grantscontracts.html', documents = documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM ggrantscontracts WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/grantscontracts.html')
            ## Code to Read
            documents = grants_read_table(user)
            return render_template('grantize/profile/grantscontracts.html', documents = documents)
        else:
            documents = grants_read_table(user)
            return render_template('grantize/profile/grantscontracts.html', documents = documents)
    else:
        return render_template('grantize/grantize.html')
    
def patents_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get all columns except 'id' and 'userid' from ggrants
        query = """
        SELECT id, title, project_number, total_funding, url, start_date, end_date, principal_investigators,
               investigators, funding_org, funding_dept, awardee_org, awardee_dept, project_terms, 
               abstract, abstract_keywords
        FROM gpatents
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries for easy handling in the template
        grants = []
        for row in rows:
            grants.append(row)
            
        mycursor.close()
        return grants
    except Exception as e:
        print("Error fetching grants from database:", str(e))
        return []

@app.route('/grantizeprofilepatents', methods =["GET", "POST"])
def grantizeprofilepatents():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "creategrant" in request.form:
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                title = get_form_data_or_none('title')
                project_number = get_form_data_or_none('name')
                total_funding = get_form_data_or_none('type')
                url = get_form_data_or_none('url')
                start_date = get_form_data_or_none('start_date')
                end_date = get_form_data_or_none('end_date')
                principal_investigators = get_form_data_or_none('authors')
                investigators = get_form_data_or_none('co_authors')
                funding_org = get_form_data_or_none('sponsor')
                funding_dept = get_form_data_or_none('sponsor_department')
                awardee_org = get_form_data_or_none('organization')
                awardee_dept = get_form_data_or_none('department')
                project_terms = request.form.getlist('keywords')  # Handle multiple select inputs
                abstract = get_form_data_or_none('description')
                abstract_keywords = get_form_data_or_none('keyword_abstract')

                # Format dates
                if start_date:
                    start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%m-%d-%Y').date()

                # Prepare SQL query and data
                sql = """
                INSERT INTO gpatents
                (userid, title, project_number, total_funding, url, start_date, end_date, 
                principal_investigators, investigators, funding_org, funding_dept, 
                awardee_org, awardee_dept, project_terms, abstract, abstract_keywords)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, project_number, total_funding, url, start_date, end_date, 
                        principal_investigators, investigators, funding_org, funding_dept, 
                        awardee_org, awardee_dept, ','.join(project_terms), abstract, abstract_keywords]
                for i in range(len(values)):
                    if values[i] == None:
                        values[i] = ""
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Grant contract added successfully!', 'success')
            except Exception as e:
                flash(f'Failed to add grant contract due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = patents_read_table(user)
            return render_template('grantize/profile/patents.html', documents = documents)
        if "editsection" in request.form:
            try:
                print("_________________EDIT STEP 0__________________")
                grant_id = request.form['grant_id']  # Ensure you have a hidden input in your form with the name 'document_id'
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'name': 'project_number',
                    'type': 'total_funding',
                    'url': 'url',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'authors': 'principal_investigators',
                    'co_authors': 'investigators',
                    'sponsor': 'funding_org',
                    'sponsor_department': '	funding_dept',
                    'organization': 'awardee_org',
                    'department': 'awardee_dept',
                    'keywords': 'project_terms',
                    'abstract': 'abstract',
                    'keyword_abstract': 'abstract_keywords'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_info in form_to_db_map.items():
                    db_column, transform = db_info if isinstance(db_info, tuple) else (db_info, None)
                    form_data = get_form_data_or_none(form_field)
                    if form_field in ['start_date','end_date']:
                        try:
                            form_data = parse_date(form_data)
                        except:
                            form_data = None
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        # Apply transformation function if provided
                        values.append(transform(form_data) if transform else form_data)

                print("_________________EDIT STEP 1__________________")

                if updates:
                    update_sql = ", ".join(updates)
                    sql = f"UPDATE gpatents SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(grant_id)
                    print(values)
                    mycursor = sqlconnection.cursor()
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    flash('Grant details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

                print("_________________EDIT STEP 2__________________")

            except Exception as e:
                flash(f'Failed to update grant details due to an error: {e}', 'error')
                return render_template('error_template.html'), 500
            documents = patents_read_table(user)
            return render_template('grantize/profile/patents.html', documents = documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gpatents WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/patents.html')
            ## Code to Read
            documents = patents_read_table(user)
            return render_template('grantize/profile/patents.html', documents = documents)
        else:
            documents = patents_read_table(user)
            return render_template('grantize/profile/patents.html', documents = documents)
    else:
        return render_template('grantize/grantize.html')
    
def journalres_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM gjournals
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return []



@app.route('/grantizeprofilejourorgres', methods =["GET", "POST"])
def grantizeprofilejourorgres():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createjourres" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gjournals
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = journalres_read_table(user)
            return render_template('grantize/profile/journalresearch.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gjournals SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = journalres_read_table(user)
            return render_template('grantize/profile/journalresearch.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gjournals WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalresearch.html')
            ## Code to Read
            documents = journalres_read_table(user)
            return render_template('grantize/profile/journalresearch.html', documents = documents)
        else:
            documents = journalres_read_table(user)
            print(documents)
            return render_template('grantize/profile/journalresearch.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')

def shorts_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM gshorts
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return []

@app.route('/grantizeprofilejourshortsrep', methods =["GET", "POST"])
def grantizeprofilejourshortsrep():
    print("YOOOOOOOOOOOOOO")
    if session.get("loginnname"):
        print("=-=-=-=-=-=-=-")
        user = session.get('loginid')
        if "createjourshorts" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gshorts
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = shorts_read_table(user)
            return render_template('grantize/profile/journalshortreport.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gshorts SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = shorts_read_table(user)
            return render_template('grantize/profile/journalshortreport.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gshorts WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalshortreport.html')
            ## Code to Read
            documents = shorts_read_table(user)
            return render_template('grantize/profile/journalshortreport.html', documents = documents)
        else:
            documents = shorts_read_table(user)
            print(documents)
            return render_template('grantize/profile/journalshortreport.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')

def articles_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM garticles
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return []  

@app.route('/grantizeprofilejourreviewarts', methods =["GET", "POST"])
def grantizeprofilejourreviewarts():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createjourshorts" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO garticles
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = articles_read_table(user)
            return render_template('grantize/profile/journalreviewarticles.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE garticles SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = articles_read_table(user)
            return render_template('grantize/profile/journalreviewarticles.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM garticles WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalreviewarticles.html')
            ## Code to Read
            documents = articles_read_table(user)
            return render_template('grantize/profile/journalreviewarticles.html', documents = documents)
        else:
            documents = articles_read_table(user)
            print(documents)
            return render_template('grantize/profile/journalreviewarticles.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
@app.route('/grantizeprofilejourcasestudy', methods =["GET", "POST"])
def grantizeprofilejourcasestudy():
    if session.get("loginnname"):
        return render_template('grantize/profile/resstatement.html')
    else:
        return render_template('grantize/grantize.html')
    
def method_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM gmethods
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return [] 

@app.route('/grantizeprofilejourmethodologies', methods =["GET", "POST"])
def grantizeprofilejourmethodologies():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createmethods" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gmethods
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = method_read_table(user)
            return render_template('grantize/profile/journalmethodologies.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gmethods SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = method_read_table(user)
            return render_template('grantize/profile/journalmethodologies.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gmethods WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalmethodologies.html')
            ## Code to Read
            documents = method_read_table(user)
            return render_template('grantize/profile/journalmethodologies.html', documents = documents)
        else:
            documents = method_read_table(user)
            print(documents)
            return render_template('grantize/profile/journalmethodologies.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def editorials_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM geditorials
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return [] 

@app.route('/grantizeprofilejoureditorials', methods =["GET", "POST"])
def grantizeprofilejoureditorials():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createeditorial" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO geditorials
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = editorials_read_table(user)
            return render_template('grantize/profile/journaleditorials.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE geditorials SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = editorials_read_table(user)
            return render_template('grantize/profile/journaleditorials.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM geditorials WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journaleditorials.html')
            ## Code to Read
            documents = editorials_read_table(user)
            return render_template('grantize/profile/journaleditorials.html', documents = documents)
        else:
            documents = editorials_read_table(user)
            print(documents)
            return render_template('grantize/profile/journaleditorials.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def other_read_table(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the journals table that are used in the INSERT query
        query = """
        SELECT id, publication_status, publisher, journal, year, volume, issue, page, title, url, doi,
               organization, department, authors, co_authors, corresponding_authors, keywords,
               abstract, abstract_keywords, techniques, instruments, softwares, soft_skills
        FROM gothers
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        documents = []
        for row in rows:
            documents.append(row)
        
        mycursor.close()
        return documents
    except Exception as e:
        print("Error fetching documents from database:", str(e))
        return [] 

@app.route('/grantizeprofilejourotherarts', methods =["GET", "POST"])
def grantizeprofilejourotherarts():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publication_status = get_form_data_or_none('publication_status')
                publisher = get_form_data_or_none('publisher')
                journal = get_form_data_or_none('journal')
                year = get_form_data_or_none('year')
                volume = get_form_data_or_none('volume')
                issue = get_form_data_or_none('issue')
                page = get_form_data_or_none('page')
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                doi = get_form_data_or_none('doi')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                keywords = get_form_data_or_none('keywords')
                abstract = get_form_data_or_none('abstract')
                abstract_keywords = get_form_data_or_none('keyword_abstract')
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                soft_skills = get_form_data_or_none('soft_skills')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gothers
                (userid, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                techniques, instruments, softwares, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publication_status, publisher, journal, year, volume, issue, page, title, url, doi, organization, 
                        department, authors, co_authors, corresponding_authors, keywords, abstract, abstract_keywords, 
                        techniques, instruments, softwares, soft_skills]
                
                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Journal information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add journal information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = other_read_table(user)
            return render_template('grantize/profile/journalotherarticles.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                journal_id = request.form['journal_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publication_status': 'publication_status',
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'year': 'year',
                    'volume': 'volume',
                    'issue': 'issue',
                    'page': 'page',
                    'title': 'title',
                    'url': 'url',
                    'doi': 'doi',
                    'organization': 'organization',
                    'department': 'department',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'abstract_keywords': 'abstract_keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gothers SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(journal_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Journal details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update journal details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = other_read_table(user)
            return render_template('grantize/profile/journalotherarticles.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gothers WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalotherarticles.html')
            ## Code to Read
            documents = other_read_table(user)
            return render_template('grantize/profile/journalotherarticles.html', documents = documents)
        else:
            documents = other_read_table(user)
            print(documents)
            return render_template('grantize/profile/journalotherarticles.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_books(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, publisher, book_id, edition, title, chapter_number, page, url,
               authors, co_authors, corresponding_authors
        FROM gbooks
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []


@app.route('/grantizeprofilebooks', methods =["GET", "POST"])
def grantizeprofilebooks():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publisher = get_form_data_or_none('publisher')
                book_id = get_form_data_or_none('book_id')
                edition = get_form_data_or_none('edition')
                title = get_form_data_or_none('title')
                chapter_number = get_form_data_or_none('chapter_number')
                page = get_form_data_or_none('page')
                url = get_form_data_or_none('url')
                authors = request.form.getlist('authors')  # Multi-select fields
                co_authors = request.form.getlist('co_authors')  # Multi-select fields
                corresponding_authors = request.form.getlist('corresponding_authors')  # Multi-select fields

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gbooks
                (userid, publisher, book_id, edition, title, chapter_number, page, url, authors, co_authors, corresponding_authors)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publisher, book_id, edition, title, chapter_number, page, url, 
                        ','.join(authors), ','.join(co_authors), ','.join(corresponding_authors)]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Book chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_books(user)
            return render_template('grantize/profile/books.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publisher': 'publisher',
                    'book_id': 'book_id',
                    'edition': 'edition',
                    'title': 'title',
                    'chapter_number': 'chapter_number',
                    'page': 'page',
                    'url': 'url',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gbooks SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_books(user)
            return render_template('grantize/profile/books.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gbooks WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/books.html')
            ## Code to Read
            documents = read_books(user)
            return render_template('grantize/profile/books.html', documents = documents)
        else:
            documents = read_books(user)
            print(documents)
            return render_template('grantize/profile/books.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    

def read_book_chapters(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the gbookchapters table
        query = """
        SELECT id, userid, publisher, book_id, edition, title, chapter_number, page, url,
               authors, co_authors, corresponding_authors
        FROM gbooks
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        chapters = []
        for row in rows:
            chapters.append(row)
        
        mycursor.close()
        return chapters
    except Exception as e:
        print("Error fetching book chapters from database:", str(e))
        return []




@app.route('/grantizeprofilebookchapters', methods =["GET", "POST"])
def grantizeprofilebookchapters():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                publisher = get_form_data_or_none('publisher')
                book_id = get_form_data_or_none('book_id')
                edition = get_form_data_or_none('edition')
                title = get_form_data_or_none('title')
                chapter_number = get_form_data_or_none('chapter_number')
                page = get_form_data_or_none('page')
                url = get_form_data_or_none('url')
                authors = request.form.getlist('authors')  # Multi-select fields
                co_authors = request.form.getlist('co_authors')  # Multi-select fields
                corresponding_authors = request.form.getlist('corresponding_authors')  # Multi-select fields

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gbooks
                (userid, publisher, book_id, edition, title, chapter_number, page, url, authors, co_authors, corresponding_authors)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, publisher, book_id, edition, title, chapter_number, page, url, 
                        ','.join(authors), ','.join(co_authors), ','.join(corresponding_authors)]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Book chapter information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add book chapter information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_book_chapters(user)
            return render_template('grantize/profile/bookchapters.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form['chapter_id']
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publisher': 'publisher',
                    'book_id': 'book_id',
                    'edition': 'edition',
                    'title': 'title',
                    'chapter_number': 'chapter_number',
                    'page': 'page',
                    'url': 'url',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gbooks SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Book chapter details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
                    return redirect(url_for('some_function_to_redirect_to'))
            except Exception as e:
                flash(f'Failed to update book chapter details due to an error: {str(e)}', 'error')
            documents = read_book_chapters(user)
            return render_template('grantize/profile/bookchapters.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gbooks WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/bookchapters.html')
            ## Code to Read
            documents = read_book_chapters(user)
            return render_template('grantize/profile/bookchapters.html', documents = documents)
        else:
            documents = read_book_chapters(user)
            print(documents)
            return render_template('grantize/profile/bookchapters.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_articles(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the articlesinnews table
        query = """
        SELECT id, userid, title, publisher, date, url, abstract, keyword_abstract
        FROM articlesinnews
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        articles = []
        for row in rows:
            articles.append(row)
        
        mycursor.close()
        return articles
    except Exception as e:
        print("Error fetching articles from database:", str(e))
        return []


@app.route('/grantizeprofileartsinnews', methods =["GET", "POST"])
def grantizeprofileartsinnews():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                title = get_form_data_or_none('title')
                publisher = get_form_data_or_none('publisher')
                date = get_form_data_or_none('date')
                url = get_form_data_or_none('url')
                abstract = get_form_data_or_none('abstract')
                keyword_abstract = get_form_data_or_none('keyword_abstract')

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO articlesinnews
                (userid, title, publisher, date, url, abstract, keyword_abstract)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, publisher, date, url, abstract, keyword_abstract]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Article information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add article information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_articles(user)
            return render_template('grantize/profile/articlesinnews.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                article_id = request.form['article_id']  # This should be a hidden input in your form for the article's ID
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'publisher': 'publisher',
                    'date': 'date',
                    'url': 'url',
                    'abstract': 'abstract',
                    'keyword_abstract': 'keyword_abstract'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE articlesinnews SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(article_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Article details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update article details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_articles(user)
            return render_template('grantize/profile/articlesinnews.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM articlesinnews WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/articlesinnews.html')
            ## Code to Read
            documents = read_articles(user)
            return render_template('grantize/profile/articlesinnews.html', documents = documents)
        else:
            documents = read_articles(user)
            print(documents)
            return render_template('grantize/profile/articlesinnews.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')

def read_publications(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the articlesinnews table
        query = """
        SELECT id, userid, title, url, authors, keywords, abstract, keyword_abstract
        FROM gotherpubs
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()
        
        # Convert rows to a list of dictionaries to facilitate handling in the template
        articles = []
        for row in rows:
            articles.append(row)
        
        mycursor.close()
        return articles
    except Exception as e:
        print("Error fetching articles from database:", str(e))
        return []

@app.route('/grantizeprofileotherpubs', methods =["GET", "POST"])
def grantizeprofileotherpubs():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name] if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                title = get_form_data_or_none('title')
                url = get_form_data_or_none('url')
                authors = get_form_data_or_none('authors')  # assuming a single author text field, adjust if necessary
                keywords = get_form_data_or_none('keywords')  # assuming a single keyword text field, adjust if necessary
                abstract = get_form_data_or_none('abstract')
                keyword_abstract = get_form_data_or_none('keyword_abstract')  # additional keywords related to the abstract

                print("_________________CREATE STEP 1__________________")
                # Prepare SQL query and data
                sql = """
                INSERT INTO gotherpubs
                (userid, title, url, authors, keywords, abstract, keyword_abstract)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                ## user = request.form['userid']   this should be set somewhere in your session or passed as a hidden input
                values = [user, title, url, authors, keywords, abstract, keyword_abstract]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print(values)
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Publication information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add publication information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_publications(user)
            return render_template('grantize/profile/otherpublications.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                publication_id = request.form.get('publication_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'url': 'url',
                    'authors': 'authors',
                    'keywords': 'keywords',
                    'abstract': 'abstract',
                    'keyword_abstract': 'keyword_abstract'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gotherpubs SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(publication_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Publication details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update publication details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_publications(user)
            return render_template('grantize/profile/otherpublications.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gotherpubs WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/otherpublications.html')
            ## Code to Read
            documents = read_publications(user)
            return render_template('grantize/profile/otherpublications.html', documents = documents)
        else:
            documents = read_publications(user)
            print(documents)
            return render_template('grantize/profile/otherpublications.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_research_protocols(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description
        FROM grespro
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileresprotocols', methods =["GET", "POST"])
def grantizeprofileresprotocols():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name].strip() if field_name in request.form and request.form[field_name].strip() else None
                
                # Extract form data
                title = get_form_data_or_none('title')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                start_date = parse_date(get_form_data_or_none('start_date'))
                end_date = parse_date(get_form_data_or_none('end_date'))
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                # Prepare SQL query and data
                sql = """
                INSERT INTO grespro (userid, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print("_________________CREATE STEP 1__________________")
                print(values)
                
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Experience profile information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add experience profile information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_research_protocols(user)
            return render_template('grantize/profile/researchprotocols.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form.get('chapter_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'organization': 'organization',
                    'department': 'department',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'description': 'description',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE grespro SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Profile details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update profile details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_research_protocols(user)
            return render_template('grantize/profile/researchprotocols.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM grespro WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/researchprotocols.html')
            ## Code to Read
            documents = read_research_protocols(user)
            return render_template('grantize/profile/researchprotocols.html', documents = documents)
        else:
            documents = read_research_protocols(user)
            print(documents)
            return render_template('grantize/profile/researchprotocols.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_iupac_protocols(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description
        FROM giupacpro
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileiacucprotocols', methods =["GET", "POST"])
def grantizeprofileiacucprotocols():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name].strip() if field_name in request.form and request.form[field_name].strip() else None
                
                # Extract form data
                title = get_form_data_or_none('title')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                start_date = parse_date(get_form_data_or_none('start_date'))
                end_date = parse_date(get_form_data_or_none('end_date'))
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                # Prepare SQL query and data
                sql = """
                INSERT INTO giupacpro (userid, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print("_________________CREATE STEP 1__________________")
                print(values)
                
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Experience profile information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add experience profile information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_iupac_protocols(user)
            return render_template('grantize/profile/iacucprotoocols.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form.get('chapter_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'organization': 'organization',
                    'department': 'department',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'description': 'description',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_field in ['start_date','end_date']:
                        try:
                            form_data = parse_date(form_data)
                        except:
                            form_data = None
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE giupacpro SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Profile details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update profile details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_iupac_protocols(user)
            return render_template('grantize/profile/iacucprotoocols.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM giupacpro WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/iacucprotoocols.html')
            ## Code to Read
            documents = read_iupac_protocols(user)
            return render_template('grantize/profile/iacucprotoocols.html', documents = documents)
        else:
            documents = read_iupac_protocols(user)
            print(documents)
            return render_template('grantize/profile/iacucprotoocols.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_clinical_protocols(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, title, phase, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description
        FROM gclinipro
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileclinicalprotocols', methods =["GET", "POST"])
def grantizeprofileclinicalprotocols():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            print("_________________CREATE STEP 0__________________")
            try:
                # Helper function to retrieve form data or None if the field is empty
                def get_form_data_or_none(field_name):
                    return request.form[field_name].strip() if field_name in request.form and request.form[field_name].strip() else None

                # Extract form data
                title = get_form_data_or_none('title')
                phase = get_form_data_or_none('phase')
                authors = get_form_data_or_none('authors')
                co_authors = get_form_data_or_none('co_authors')
                corresponding_authors = get_form_data_or_none('corresponding_authors')
                organization = get_form_data_or_none('organization')
                department = get_form_data_or_none('department')
                start_date = parse_date(get_form_data_or_none('start_date'))
                end_date = parse_date(get_form_data_or_none('end_date'))
                techniques = get_form_data_or_none('techniques')
                instruments = get_form_data_or_none('instruments')
                softwares = get_form_data_or_none('softwares')
                description = get_form_data_or_none('description')
                keyword_description = get_form_data_or_none('keyword_description')

                # Prepare SQL query and data
                sql = """
                INSERT INTO gclinipro (userid, title, phase, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [user, title, phase, authors, co_authors, corresponding_authors, organization, department, start_date, end_date, techniques, instruments, softwares, description, keyword_description]

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print("_________________CREATE STEP 1__________________")
                print(values)
                
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Experience profile information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add experience profile information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_clinical_protocols(user)
            return render_template('grantize/profile/clinicalprotocols.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                chapter_id = request.form.get('chapter_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'title': 'title',
                    'phase': 'phase',
                    'authors': 'authors',
                    'co_authors': 'co_authors',
                    'corresponding_authors': 'corresponding_authors',
                    'organization': 'organization',
                    'department': 'department',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'description': 'description',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gclinipro SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(chapter_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Profile details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')
            except Exception as e:
                flash(f'Failed to update profile details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_clinical_protocols(user)
            return render_template('grantize/profile/clinicalprotocols.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gclinipro WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/clinicalprotocols.html')
            ## Code to Read
            documents = read_clinical_protocols(user)
            return render_template('grantize/profile/clinicalprotocols.html', documents = documents)
        else:
            documents = read_clinical_protocols(user)
            print(documents)
            return render_template('grantize/profile/clinicalprotocols.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_conferences(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, conference, role, title, keywords, filecontent, filename, techniques, instruments, softwares, abstract, keyword_description
        FROM gconferences
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/download_file_conf/<doc_id>')
def download_file_conf(doc_id):
    global sqlconnection
    print("____________")
    print("ENTER DOWNLOAD")
    print(doc_id)
    print("____________")
    cursor = sqlconnection.cursor()
    try:
        # Prepare a query to fetch the file data by name
        query = "SELECT filename, filecontent FROM gconferences WHERE id = %s"
        cursor.execute(query, (doc_id,))
        file_data = cursor.fetchone()
        if file_data is None:
            return jsonify({'error': 'File not found'}), 404

        # Secure the filename to prevent path traversal attacks
        filename = secure_filename(file_data[0])

        # Guess the MIME type of the file based on its extension
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Fallback to binary type if MIME type is undetectable

        # Send the file data as an attachment
        file_stream = BytesIO(file_data[1])
        return send_file(
            file_stream,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
    except mysql.connector.Error as err:
        print("Error: ", err)
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()

@app.route('/grantizeprofileconferences', methods =["GET", "POST"])
def grantizeprofileconferences():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                print("_________________CREATE STEP 0__________________")
                # Retrieving form data
                conference = request.form.get('conference', '').strip()
                role = request.form.get('role', '').strip()
                title = request.form.get('title', '').strip()
                keywords = request.form.get('keywords', '').strip()
                file = request.files.get('filecontent')  # Handling file input
                techniques = request.form.get('techniques', '').strip()
                instruments = request.form.get('instruments', '').strip()
                softwares = request.form.get('softwares', '').strip()
                abstract = request.form.get('abstract', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # SQL Insert Query
                sql = """
                INSERT INTO gconferences (userid, conference, role, title, keywords, filecontent, filename, techniques, instruments, softwares, abstract, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Preparing data for insertion
                values = (user, conference, role, title, keywords, file.read() if file else None, secure_filename(file.filename) if file else None, techniques, instruments, softwares, abstract, keyword_description)

                # Convert None values to empty strings before executing
                values = ["" if v is None else v for v in values]
                print("_________________CREATE STEP 1__________________")
                print(values)
                
                # Execute the query
                mycursor = sqlconnection.cursor()
                mycursor.execute(sql, tuple(values))
                sqlconnection.commit()
                mycursor.close()
                flash('Experience profile information added successfully!', 'success')
                print("_________________CREATE STEP 2__________________")
            except Exception as e:
                flash(f'Failed to add conference information due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_conferences(user)
            return render_template('grantize/profile/conferences.html', documents=documents)
        if "editsection" in request.form:
            conference_id = request.form.get('conference_id', '').strip()  # Assuming chapter_id is the record's unique identifier
            try:
                updates = []
                values = []
                
                # Mapping form fields to database columns
                form_to_db = {
                    'conference': 'conference',
                    'role': 'role',
                    'title': 'title',
                    'keywords': 'keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills',
                    'abstract': 'abstract',
                    'keyword_description': 'keyword_description'
                }

                # Collect updates for non-empty fields
                for form_field, db_field in form_to_db.items():
                    data = request.form.get(form_field, '').strip()
                    if data:
                        updates.append(f"{db_field} = %s")
                        values.append(data)
                
                # Handle file upload if any
                if 'filecontent' in request.files and request.files['filecontent']:
                    file = request.files['filecontent']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        #filepath = os.path.join('/path/to/upload/directory', filename)
                        #file.save(filepath)
                        updates.append("filename = %s, filecontent = %s")
                        values.extend([filename, file.read()])
                
                # Execute update if there are changes
                if updates:
                    sql = f"UPDATE gconferences SET {', '.join(updates)} WHERE id = %s"
                    values.append(conference_id)
                    with sqlconnection.cursor() as cursor:
                        cursor.execute(sql, tuple(values))
                        sqlconnection.commit()
                    flash('Conference information updated successfully!', 'success')
                else:
                    flash('No changes detected.', 'info')
                    
            except Exception as e:
                flash(f'Error updating conference information: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_conferences(user)
            return render_template('grantize/profile/conferences.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gconferences WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/conferences.html')
            ## Code to Read
            documents = read_conferences(user)
            return render_template('grantize/profile/conferences.html', documents = documents)
        else:
            documents = read_conferences(user)
            print(documents)
            return render_template('grantize/profile/conferences.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_symposia(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description
        FROM gsymposia
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilesymposia', methods =["GET", "POST"])
def grantizeprofilesymposia():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                conference = request.form.get('conference', '').strip()
                role = request.form.get('role', '').strip()
                title = request.form.get('title', '').strip()
                keywords = request.form.get('keywords', '').strip()
                techniques = request.form.get('techniques', '').strip()
                instruments = request.form.get('instruments', '').strip()
                softwares = request.form.get('softwares', '').strip()
                soft_skills = request.form.get('soft_skills', '').strip()
                abstract = request.form.get('abstract', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # SQL Query to insert the data
                sql = """
                INSERT INTO gsymposia (userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                    flash("Profile information added successfully!", "success")

            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_symposia(user)
            return render_template('grantize/profile/symposia.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'conference': 'conference',
                    'role': 'role',
                    'title': 'title',
                    'keywords': 'keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills',
                    'abstract': 'abstract',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gsymposia SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_symposia(user)
            return render_template('grantize/profile/symposia.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gsymposia WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/symposia.html')
            ## Code to Read
            documents = read_symposia(user)
            return render_template('grantize/profile/symposia.html', documents = documents)
        else:
            documents = read_symposia(user)
            print(documents)
            return render_template('grantize/profile/symposia.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_workshops(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description
        FROM gworkshops
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileworkshops', methods =["GET", "POST"])
def grantizeprofileworkshops():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                conference = request.form.get('conference', '').strip()
                role = request.form.get('role', '').strip()
                title = request.form.get('title', '').strip()
                keywords = request.form.get('keywords', '').strip()
                techniques = request.form.get('techniques', '').strip()
                instruments = request.form.get('instruments', '').strip()
                softwares = request.form.get('softwares', '').strip()
                soft_skills = request.form.get('soft_skills', '').strip()
                abstract = request.form.get('abstract', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # SQL Query to insert the data
                sql = """
                INSERT INTO gworkshops (userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                    flash("Profile information added successfully!", "success")

            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_workshops(user)
            return render_template('grantize/profile/workshops.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'conference': 'conference',
                    'role': 'role',
                    'title': 'title',
                    'keywords': 'keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills',
                    'abstract': 'abstract',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gworkshops SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_workshops(user)
            return render_template('grantize/profile/workshops.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gworkshops WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/workshops.html')
            ## Code to Read
            documents = read_workshops(user)
            return render_template('grantize/profile/workshops.html', documents = documents)
        else:
            documents = read_workshops(user)
            print(documents)
            return render_template('grantize/profile/workshops.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_seminars(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description
        FROM gseminars
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileseminars', methods =["GET", "POST"])
def grantizeprofileseminars():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                conference = request.form.get('conference', '').strip()
                role = request.form.get('role', '').strip()
                title = request.form.get('title', '').strip()
                keywords = request.form.get('keywords', '').strip()
                techniques = request.form.get('techniques', '').strip()
                instruments = request.form.get('instruments', '').strip()
                softwares = request.form.get('softwares', '').strip()
                soft_skills = request.form.get('soft_skills', '').strip()
                abstract = request.form.get('abstract', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # SQL Query to insert the data
                sql = """
                INSERT INTO gseminars (userid, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, conference, role, title, keywords, techniques, instruments, softwares, soft_skills, abstract, keyword_description)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                    flash("Profile information added successfully!", "success")

            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_seminars(user)
            return render_template('grantize/profile/seminars.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'conference': 'conference',
                    'role': 'role',
                    'title': 'title',
                    'keywords': 'keywords',
                    'techniques': 'techniques',
                    'instruments': 'instruments',
                    'softwares': 'softwares',
                    'soft_skills': 'soft_skills',
                    'abstract': 'abstract',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gseminars SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_seminars(user)
            return render_template('grantize/profile/seminars.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gseminars WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/seminars.html')
            ## Code to Read
            documents = read_seminars(user)
            return render_template('grantize/profile/seminars.html', documents = documents)
        else:
            documents = read_seminars(user)
            print(documents)
            return render_template('grantize/profile/seminars.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_prof_members(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, organization, role, activity, start_date, end_date
        FROM gpromem
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileprofmembers', methods =["GET", "POST"])
def grantizeprofileprofmembers():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                organization = request.form.get('organization', '').strip()
                role = request.form.get('role', '').strip()
                activity = request.form.get('activity', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()

                 # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else None

                # SQL Query to insert the data
                sql = """
                INSERT INTO gpromem (userid, organization, role, activity, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (user, organization, role, activity, start_date, end_date)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                    flash("Profile information added successfully!", "success")

            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_prof_members(user)
            return render_template('grantize/profile/professionalmemberships.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'organization',
                    'role': 'role',
                    'activity': 'activity',
                    'start_date': 'start_date',
                    'end_date': 'end_date'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gpromem SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_prof_members(user)
            return render_template('grantize/profile/professionalmemberships.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gpromem WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/professionalmemberships.html')
            ## Code to Read
            documents = read_prof_members(user)
            return render_template('grantize/profile/professionalmemberships.html', documents = documents)
        else:
            documents = read_prof_members(user)
            print(documents)
            return render_template('grantize/profile/professionalmemberships.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_teaching_experience(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, organization, department, type, start_date, end_date, discipline, courses, subjects, major
        FROM gteachingex
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileteachingex', methods =["GET", "POST"])
def grantizeprofileteachingex():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                organization = request.form.get('organization', '').strip()
                department = request.form.get('department', '').strip()
                type_ = request.form.get('type', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()
                discipline = request.form.get('discipline', '').strip()
                courses = request.form.get('courses', '').strip()
                subjects = request.form.get('subjects', '').strip()
                major = request.form.get('major', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else None

                # SQL Query to insert the data
                sql = """
                INSERT INTO gteachingex (userid, organization, department, type, start_date, end_date, discipline, courses, subjects, major)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, organization, department, type_, start_date, end_date, discipline, courses, subjects, major)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                    flash("Teaching experience information added successfully!", "success")

            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_teaching_experience(user)
            return render_template('grantize/profile/teachingexperiences.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'organization',
                    'department': 'department',
                    'type': 'type',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'discipline': 'discipline',
                    'courses': 'courses',
                    'subjects': 'subjects',
                    'major': 'major'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if form_field in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gteachingex SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_teaching_experience(user)
            return render_template('grantize/profile/teachingexperiences.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gteachingex WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/teachingexperiences.html')
            ## Code to Read
            documents = read_teaching_experience(user)
            return render_template('grantize/profile/teachingexperiences.html', documents = documents)
        else:
            documents = read_teaching_experience(user)
            print(documents)
            return render_template('grantize/profile/teachingexperiences.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_supervisor_mentor(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, mentors, degree, designation, organization, department, discipline, courses, subjects, major, role, keyword_description, start_date, end_date
        FROM gsuperment
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilesupermentor', methods =["GET", "POST"])
def grantizeprofilesupermentor():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                mentors = request.form.get('mentors', '').strip()
                degree = request.form.get('degree', '').strip()
                designation = request.form.get('designation', '').strip()
                organization = request.form.get('organization', '').strip()
                department = request.form.get('department', '').strip()
                discipline = request.form.get('discipline', '').strip()
                courses = request.form.get('courses', '').strip()
                subjects = request.form.get('subjects', '').strip()
                major = request.form.get('major', '').strip()
                role = request.form.get('role', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else ''
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else ''

                # SQL Query to insert the data
                sql = """
                INSERT INTO gsuperment (userid, mentors, degree, designation, organization, department, discipline, courses, subjects, major, role, keyword_description, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, mentors, degree, designation, organization, department, discipline, courses, subjects, major, role, keyword_description, start_date, end_date)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Profile information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_supervisor_mentor(user)
            return render_template('grantize/profile/supervisionmentoring.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'mentors': 'mentors',
                    'degree': 'degree',
                    'designation': 'designation',
                    'organization': 'organization',
                    'department': 'department',
                    'discipline': 'discipline',
                    'courses': 'courses',
                    'subjects': 'subjects',
                    'major': 'major',
                    'role': 'role',
                    'keyword_description': 'keyword_description',
                    'start_date': 'start_date',
                    'end_date': 'end_date'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gsuperment SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_supervisor_mentor(user)
            return render_template('grantize/profile/supervisionmentoring.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gsuperment WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/supervisionmentoring.html')
            ## Code to Read
            documents = read_supervisor_mentor(user)
            return render_template('grantize/profile/supervisionmentoring.html', documents = documents)
        else:
            documents = read_supervisor_mentor(user)
            print(documents)
            return render_template('grantize/profile/supervisionmentoring.html', documents=documents)
        return render_template('grantize/profile/supervisionmentoring.html')
    else:
        return render_template('grantize/grantize.html')
    
def read_journal_review(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, publisher, journal, position, start_date, end_date, degree, keyword_description
        FROM gjourreview
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilejourreviewses', methods =["GET", "POST"])
def grantizeprofilejourreviewses():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                publisher = request.form.get('publisher', '').strip()
                journal = request.form.get('journal', '').strip()
                position = request.form.get('position', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()
                degree = request.form.get('degree', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else ''
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else ''

                # SQL Query to insert the data
                sql = """
                INSERT INTO gjourreview (userid, publisher, journal, position, start_date, end_date, degree, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, publisher, journal, position, start_date, end_date, degree, keyword_description)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Profile information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_journal_review(user)
            return render_template('grantize/profile/journalreviewAES.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'publisher': 'publisher',
                    'journal': 'journal',
                    'position': 'position',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'degree': 'degree',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gjourreview SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_journal_review(user)
            return render_template('grantize/profile/journalreviewAES.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gjourreview WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/journalreviewAES.html')
            ## Code to Read
            documents = read_journal_review(user)
            return render_template('grantize/profile/journalreviewAES.html', documents = documents)
        else:
            documents = read_journal_review(user)
            print(documents)
            return render_template('grantize/profile/journalreviewAES.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_grant_review(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, organization, department, section, start_date, end_date, role, keyword_description
        FROM ggrantreview
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilegrantreviewservices', methods =["GET", "POST"])
def grantizeprofilegrantreviewservices():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                organization = request.form.get('organization', '').strip()
                department = request.form.get('department', '').strip()
                section = request.form.get('section', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()
                role = request.form.get('role', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else ''
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else ''

                # SQL Query to insert the data
                sql = """
                INSERT INTO ggrantreview (userid, organization, department, section, start_date, end_date, role, keyword_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, organization, department, section, start_date, end_date, role, keyword_description)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Profile information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_grant_review(user)
            return render_template('grantize/profile/grantsreviewS.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'organization',
                    'department': 'department',
                    'section': 'section',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'role': 'role',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print(updates)
                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE ggrantreview SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_grant_review(user)
            return render_template('grantize/profile/grantsreviewS.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM ggrantreview WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/grantsreviewS.html')
            ## Code to Read
            documents = read_grant_review(user)
            return render_template('grantize/profile/grantsreviewS.html', documents = documents)
        else:
            documents = read_grant_review(user)
            print(documents)
            return render_template('grantize/profile/grantsreviewS.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_committee(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, organization, department, committee_type, committee_name, role, description, keyword_description, start_date, end_date
        FROM gcommittee
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilecommactivities', methods =["GET", "POST"])
def grantizeprofilecommactivities():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                organization = request.form.get('organization', '').strip()
                department = request.form.get('department', '').strip()
                type_ = request.form.get('type', '').strip()
                committee = request.form.get('committee', '').strip()
                role = request.form.get('role', '').strip()
                description = request.form.get('description', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else ''
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else ''

                # SQL Query to insert the data
                sql = """
                INSERT INTO gcommittee (userid, organization, department, committee_type, committee_name, role, description, keyword_description, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (user, organization, department, type_, committee, role, description, keyword_description, start_date, end_date)

                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Committee information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_committee(user)
            return render_template('grantize/profile/committeeactivity.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('activity_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else ''

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'organization': 'organization',
                    'department': 'department',
                    'type': 'committee_type',
                    'committee': 'committee_name',
                    'role': 'role',
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                    'start_date': 'start_date',
                    'end_date': 'end_date'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except: 
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print(updates)
                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gcommittee SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_committee(user)
            return render_template('grantize/profile/committeeactivity.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gcommittee WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/committeeactivity.html')
            ## Code to Read
            documents = read_committee(user)
            return render_template('grantize/profile/committeeactivity.html', documents = documents)
        else:
            documents = read_committee(user)
            print(documents)
            return render_template('grantize/profile/committeeactivity.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_hobbies(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, hobbies, description, keyword_description
        FROM ghobbies
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilehobbies', methods =["GET", "POST"])
def grantizeprofilehobbies():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                hobbies = request.form.get('hobbies', '').strip()
                description = request.form.get('description', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()

                # SQL Query to insert the data
                sql = """
                INSERT INTO ghobbies (userid, hobbies, description, keyword_description)
                VALUES (%s, %s, %s, %s)
                """
                values = (user, hobbies, description, keyword_description)

                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Committee information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_hobbies(user)
            return render_template('grantize/profile/hobbies.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'hobbies': 'hobbies',
                    'description': 'description',
                    'keyword_description': 'keyword_description'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print(updates)
                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE ghobbies SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_hobbies(user)
            return render_template('grantize/profile/hobbies.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM ghobbies WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/hobbies.html')
            ## Code to Read
            documents = read_hobbies(user)
            return render_template('grantize/profile/hobbies.html', documents = documents)
        else:
            documents = read_hobbies(user)
            print(documents)
            return render_template('grantize/profile/hobbies.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_language_proficiency(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, language, reading, writing, speaking
        FROM glangprof
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofilelangprof', methods =["GET", "POST"])
def grantizeprofilelangprof():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                language = request.form.get('language', '').strip()
                reading = request.form.get('reading', '').strip()
                writing = request.form.get('writing', '').strip()
                speaking = request.form.get('speaking', '').strip()

                # SQL Query to insert the data
                sql = """
                INSERT INTO glangprof (userid, language, reading, writing, speaking)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (user, language, reading, writing, speaking)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Language proficiency information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_language_proficiency(user)
            return render_template('grantize/profile/langprof.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'language': 'language',
                    'reading': 'reading',
                    'writing': 'writing',
                    'speaking': 'speaking'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print(updates)
                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE glangprof SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_language_proficiency(user)
            return render_template('grantize/profile/langprof.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM glangprof WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/langprof.html')
            ## Code to Read
            documents = read_language_proficiency(user)
            return render_template('grantize/profile/langprof.html', documents = documents)
        else:
            documents = read_language_proficiency(user)
            print(documents)
            return render_template('grantize/profile/langprof.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
def read_other_activities(user):
    global sqlconnection
    try:
        mycursor = sqlconnection.cursor(dictionary=True)
        # SQL query to get specific columns from the grespro table
        query = """
        SELECT id, userid, activity, description, keyword_description, start_date, end_date
        FROM gotheractivities
        WHERE userid = %s
        """
        mycursor.execute(query, (user,))
        rows = mycursor.fetchall()

        # Convert rows to a list of dictionaries to facilitate handling in the template
        profiles = []
        for row in rows:
            profiles.append(row)

        mycursor.close()
        return profiles
    except Exception as e:
        print("Error fetching experience profiles from database:", str(e))
        return []

@app.route('/grantizeprofileotheractivities', methods =["GET", "POST"])
def grantizeprofileotheractivities():
    if session.get("loginnname"):
        user = session.get('loginid')
        if "createform" in request.form:
            try:
                # Retrieve data from form fields
                activity = request.form.get('activity', '').strip()
                description = request.form.get('description', '').strip()
                keyword_description = request.form.get('keyword_description', '').strip()
                start_date_str = request.form.get('start_date', '').strip()
                end_date_str = request.form.get('end_date', '').strip()

                # Convert date strings to date objects
                start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%m-%d-%Y').date() if end_date_str else None

                # SQL Query to insert the data
                sql = """
                INSERT INTO gotheractivities (userid, activity, description, keyword_description, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (user, activity, description, keyword_description, start_date, end_date)

                # Execute the SQL command
                with sqlconnection.cursor() as cursor:
                    cursor.execute(sql, values)
                    sqlconnection.commit()
                flash("Activity information added successfully!", "success")
            except Exception as e:
                sqlconnection.rollback()
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            documents = read_other_activities(user)
            return render_template('grantize/profile/otheractivities.html', documents=documents)
        if "editsection" in request.form:
            print("_________________EDIT STEP 0__________________")
            try:
                symposia_id = request.form.get('symposia_id', '')  # ID from the hidden input in the form
                updates = []
                values = []

                # Helper function to get form data or return None if blank
                def get_form_data_or_none(field):
                    return request.form[field].strip() if field in request.form and request.form[field].strip() else None

                # Define the mapping from form fields to database columns
                form_to_db_map = {
                    'activity': 'activity',
                    'description': 'description',
                    'keyword_description': 'keyword_description',
                    'start_date': 'start_date',
                    'end_date': 'end_date'
                }

                # Loop over the fields and prepare SQL update statement
                for form_field, db_column in form_to_db_map.items():
                    form_data = get_form_data_or_none(form_field)
                    if form_data is not None:
                        if db_column in ["start_date","end_date"]:
                            try:
                                form_data = datetime.strptime(form_data, '%m-%d-%Y').date() if form_data else None
                            except:
                                form_data = datetime.strptime(form_data, '%Y-%m-%d').date() if form_data else None
                        updates.append(f"{db_column} = %s")
                        values.append(form_data)

                print(updates)
                print("_________________EDIT STEP 1__________________")

                # Check if there are any updates to be made
                if updates:
                    update_sql = ", ".join(updates)
                    print("_________________EDIT STEP 2__________________")
                    sql = f"UPDATE gotheractivities SET {update_sql} WHERE id = %s"
                    print(sql)
                    values.append(symposia_id)
                    mycursor = sqlconnection.cursor()
                    print(values)
                    mycursor.execute(sql, tuple(values))
                    sqlconnection.commit()
                    mycursor.close()
                    print("_________________EDIT STEP 3__________________")
                    flash('Symposia details updated successfully!', 'success')
                else:
                    flash('No changes to update.', 'info')

            except Exception as e:
                flash(f'Failed to update symposia details due to an error: {str(e)}', 'error')
                return render_template('error_template.html'), 500
            documents = read_other_activities(user)
            return render_template('grantize/profile/otheractivities.html', documents=documents)
        if "delete" in request.form:
            try:
                id_to_delete = request.form['id']
                print("-------------")
                print(id_to_delete)
                print("--------------")
                mycursor = sqlconnection.cursor()
                sql = "DELETE FROM gotheractivities WHERE id = "+str(id_to_delete)
                mycursor.execute(sql)
                sqlconnection.commit()
                mycursor.close()
            except:
                print("REGISTER USER VARIABLES COULD NOT BE READ!!")
                return render_template('grantize/profile/otheractivities.html')
            ## Code to Read
            documents = read_other_activities(user)
            return render_template('grantize/profile/otheractivities.html', documents = documents)
        else:
            documents = read_other_activities(user)
            print(documents)
            return render_template('grantize/profile/otheractivities.html', documents=documents)
    else:
        return render_template('grantize/grantize.html')
    
@app.route('/grantizeprofilereferences')
def grantizeprofilereferences():
    if session.get("loginnname"):
        return render_template('grantize/profile/references.html')
    else:
        return render_template('grantize/grantize.html')
    

    
    















@app.route('/grantizerefreq')
def grantizerefreq():
    return redirect(url_for('grantizeprofilereferences'))


def parse_and_format_sql_conditions(sql, operators, mapper, field_types):
    # Replace all field names with their database equivalents before any splitting
    for key, db_field in mapper.items():
        # Regex pattern to match full field names outside of quotes
        key_pattern = r'\b' + re.escape(key) + r'\b'
        sql = re.sub(key_pattern, db_field, sql)

    # Regex pattern to split by operators while preserving quoted text and keeping the operators
    pattern = r'(\b(?:' + '|'.join(re.escape(op) for op in operators) + r')\b)'

    # Split the string while keeping the delimiter
    parts = re.split(pattern, sql)

    # Initialize a list to collect conditions and include operators
    conditions = []
    for part in parts:
        stripped_part = part.strip()
        if stripped_part:
            # Check if the part is an operator
            if stripped_part in operators:
                conditions.append(stripped_part)  # Append operator directly
            else:
                # Further handle the replacement and ensure values are correctly quoted
                modified_part = stripped_part
                for db_field, type_info in field_types.items():
                    if type_info in ['varchar(255)', 'text']:
                        # Add quotes around varchar and text fields if they are not already quoted
                        modified_part = re.sub(r"(\b" + re.escape(db_field) + r"\s*=\s*)(?!')(.*?)(?=\s|$|AND|OR)",
                                               r"\1'\2'", modified_part)
                    elif 'date' in type_info:
                        # Ensure dates are properly quoted
                        modified_part = re.sub(r"(\b" + re.escape(db_field) + r"\s*=\s*)(?!')(.*?)(?=\s|$|AND|OR)",
                                               r"\1'\2'", modified_part)
                        # Handle BETWEEN specially
                        modified_part = re.sub(r"(\b" + re.escape(db_field) + r"\s+BETWEEN\s+)(?!')(.*?)(\s+AND\s+)(?!')(.*?)(?=\s|$|AND|OR)",
                                               r"\1'\2'\3'\4'", modified_part)
                conditions.append(modified_part)
    conditions = replace_conditions_with_db_fields(conditions, mapper)
    return conditions

def replace_conditions_with_db_fields(conditions, mapper):
    # Iterate over each condition in the list
    for i in range(len(conditions)):
        # For each key in the mapper, replace it in the current condition
        for key, db_field in mapper.items():
            conditions[i] = conditions[i].replace(key, db_field)
    return conditions

@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    item_id = request.form.get('id')
    # Perform operation to toggle favorite status
    # Here, we're just simulating the response
    print(item_id)
    response = {'status': 'success', 'action': 'toggle'}
    return jsonify(response)

@app.route('/toggle_save', methods=['POST'])
def toggle_save():
    item_id = request.form.get('id')
    # Similar operation for saving an item
    response = {'status': 'success', 'action': 'toggle'}
    return jsonify(response)

@app.route('/toggle_share', methods=['POST'])
def toggle_share():
    item_id = request.form.get('id')
    # Similar operation for sharing an item
    response = {'status': 'success', 'action': 'toggle'}
    return jsonify(response)

@app.route('/update_favorite', methods=['POST'])
def update_favorite():
    id = request.form['id']
    print("-----------")
    print("-----------")
    print(type(id))
    print("-----------")
    print("-----------")
    # Database logic to update favorite status
    mycursor = sqlconnection.cursor()
    # SQL query to get specific columns from the grespro table
    query = """
    SELECT grantid
    FROM gfavs
    WHERE userid = %s
    """
    mycursor.execute(query, (session.get('loginid'),))
    checklist = mycursor.fetchall()
    checklist = [f[0] for f in checklist]
    print("-----------")
    print("-----------")
    print(type(checklist[0]))
    print("-----------")
    print("-----------")
    mycursor.close()
    if int(id) not in checklist:
        sql = "INSERT INTO gfavs (userid, grantid) VALUES (%s, %s)"
        val = (session.get('loginid'), id)
        try:
            mycursor = sqlconnection.cursor()
            mycursor.execute(sql, val)
            sqlconnection.commit()
            mycursor.close()
            print("Database Insertion Successful....")
        except:
            print("Database Insertion Failed!!")
    else:
        try:
            with sqlconnection.cursor() as mycursor:
                sql = "DELETE FROM gfavs WHERE grantid = %s"
                mycursor.execute(sql, (id,))  # Use tuple for parameters
                sqlconnection.commit()
            print("Database Deletion Successful....")
        except:
            print("Database Deletion Failed!!")
    return jsonify(status="success")

@app.route('/update_save', methods=['POST'])
def update_save():
    id = request.form['id']
    # Database logic to update favorite status
    mycursor = sqlconnection.cursor()
    # SQL query to get specific columns from the grespro table
    query = """
    SELECT grantid
    FROM gsaved
    WHERE userid = %s
    """
    mycursor.execute(query, (session.get('loginid'),))
    checklist = mycursor.fetchall()
    checklist = [f[0] for f in checklist]
    mycursor.close()
    if int(id) not in checklist:
        sql = "INSERT INTO gsaved (userid, grantid) VALUES (%s, %s)"
        val = (session.get('loginid'), id)
        try:
            mycursor = sqlconnection.cursor()
            mycursor.execute(sql, val)
            sqlconnection.commit()
            mycursor.close()
            print("Database Insertion Successful....")
        except:
            print("Database Insertion Failed!!")
    else:
        try:
            with sqlconnection.cursor() as mycursor:
                sql = "DELETE FROM gsaved WHERE grantid = %s"
                mycursor.execute(sql, (id,))  # Use tuple for parameters
                sqlconnection.commit()
            print("Database Deletion Successful....")
        except:
            print("Database Deletion Failed!!")
    return jsonify(status="success")

@app.route('/grantizebrowsegrants', methods =["GET", "POST"])
def grantizebrowsegrants():
    global sqlconnection
    dummy = "all"
    if session.get("loginnname"):
        user = session.get('loginid')
        try:
            mycursor = sqlconnection.cursor()
            # SQL query to get specific columns from the grespro table
            query = """
            SELECT grantid
            FROM gfavs
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            favlist = mycursor.fetchall()
            query = """
            SELECT grantid
            FROM gsaved
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            savlist = mycursor.fetchall()
            mycursor.close()
            favlist = [f[0] for f in favlist]
            savlist = [f[0] for f in savlist]
        except Exception as e:
            print("Error fetching experience profiles from database:", str(e))
            return []
        if "searchbytitle" in request.form:
            clicked_button = request.form['grants_status']
            title_query = request.form['tquery']
            if title_query and title_query!=None and str(title_query)!="":
                if clicked_button=="all":
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
                elif clicked_button=="open":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND application_due_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="continuous":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date < CURRENT_TIMESTAMP
                        AND application_due_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="comingsoon":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND open_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="recentlyclosed":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="archived":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date < DATE_SUB(NOW(), INTERVAL 1 YEAR)
                        """
                else:
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
            else:
                if clicked_button=="all":
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants"
                elif clicked_button=="open":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE application_due_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="continuous":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date < CURRENT_TIMESTAMP
                        AND application_due_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="comingsoon":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE open_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="recentlyclosed":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="archived":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date < DATE_SUB(NOW(), INTERVAL 1 YEAR)
                        """
                else:
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants"
        elif "addquery" in request.form:
            sql_string = request.form['query_front']
            mapper_db = {"Title":"title",
                         "Grant Status": "grant_status",
                         "Open date": "open_date",
                         "Sponsor": "sponsor",
                         "Sponsor type": "sponsor_types",
                         "Grants type": "grants_type",
                         "Applicant type": "applicant_types",
                         "Award min (n)": "award_min",
                         "Award max (n)": "award_max",
                         "CFDA": "cfda",
                         "Earliest start date": "earliest_start_date",
                         "Expiration date": "expiration_date",
                         "Keywords": "keywords",
                         "Subjects": "subjects",
                         "Submit date": "submit_date",
                         "Activity Code": "activity_code",
                         "Citizenships": "citizenships",
                         "Application due date": "application_due_date",
                         "Intent due date": "intent_due_date",
                         "Applicant locations": "countries",
                         "Activity locations": "countries",
                         "Amount per Grant (max)": "amount_per_grant_max",
                         "Amount per Grant (min)": "amount_per_grant_min"}
            field_types = {
                        "title": "varchar(255)",
                        "grant_status": "varchar(255)",
                        "open_date": "date",
                        "earliest_start_date": "date",
                        "expiration_date": "date",
                        "sponsor": "int(11)",
                        "sponsor_types": "text",
                        "grants_type": "text",
                        "applicant_types": "text",
                        "award_min": "int(11)",
                        "award_max": "int(11)",
                        "cfda": "text",
                        "keywords": "text",
                        "subjects": "text",
                        "submit_date": "date",
                        "activity_code": "text",
                        "citizenships": "text",
                        "application_due_date": "date",
                        "intent_due_date": "date",
                        "countries": "text",
                        "amount_per_grant_max": "int(11)",
                        "amount_per_grant_min": "int(11)"
                    }
            operators = ["AND", "OR", "NOT"]
            conditions = parse_and_format_sql_conditions(sql_string, operators, mapper_db, field_types)
            sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE " + " ".join(conditions)
            print(sql)
            with sqlconnection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()  # Fetch all records matching the query
                print(result)
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            if "submit_search_add" in request.form:
                print("--------------------------")
                title_query = request.form['savetitle']
                print(title_query)
                print("--------------------------")
                mycursor = sqlconnection.cursor()
                sql = "INSERT INTO gsearchquery (userid, title, query) VALUES (%s, %s, %s)"
                val = (user, title_query, " ".join(conditions))
                try:
                    mycursor.execute(sql, val)
                    sqlconnection.commit()
                    mycursor.close()
                    print("Database Insertion Successful....")
                except:
                    print("Database Insertion Failed!!")
            return render_template('grantize/dashboard/browsegrants.html', grants=result, dummy="all", favlist=favlist, savlist=savlist)
        elif "sharewithothers" in request.form:
            try:
                # Retrieve data from form fields
                mycursor = sqlconnection.cursor()
                useremail = request.form.get('users', '').strip()
                grant_id = request.form.get('grant_id', '').strip()
                print("--------")
                print(grant_id)
                print(useremail)
                print("---------")
                flash("Activity information added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            try:
                # Fetch the user ID where email matches 'dummy'
                sql_select_query = """
                    SELECT id FROM gresearcherslist WHERE email = %s
                """
                mycursor.execute(sql_select_query, (useremail,))
                user_record = mycursor.fetchone()
                print("--------")
                print(user_record)
                print("---------")
                if user_record:
                    # Insert record into gshared
                    sql_insert_query = """
                        INSERT INTO gshared (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user, grant_id))
                    sqlconnection.commit()
                    # Insert record into gsharedwith
                    sql_insert_query = """
                        INSERT INTO gsharedwith (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user_record[0], grant_id))
                    sqlconnection.commit()
            except mysql.connector.Error as err:
                print("Error:", err)
                return jsonify({"status": "error", "message": str(err)}), 500
            sql = "SELECT id,title,grants_type,subjects FROM ggrants"
        else:
            sql = "SELECT id,title,grants_type,subjects FROM ggrants"
        try:
            print(sql)
            if not clicked_button:
                clicked_button = "all"
            mycursor = sqlconnection.cursor(dictionary=True)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            print(result)
            mycursor.close()
            return render_template('grantize/dashboard/browsegrants.html', grants=result, dummy=clicked_button, favlist=favlist, savlist=savlist)
        except:
            print("Database Connection Not Working!!")
            return render_template('grantize/dashboard/browsegrants.html')
    else:
        favlist = []
        savlist = []
        if "searchbytitle" in request.form:
            clicked_button = request.form['grants_status']
            title_query = request.form['tquery']
            if title_query and title_query!=None and str(title_query)!="":
                if clicked_button=="all":
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
                elif clicked_button=="open":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND application_due_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="continuous":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date < CURRENT_TIMESTAMP
                        AND application_due_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="comingsoon":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND open_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="recentlyclosed":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="archived":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE title LIKE '%""" + title_query + """%' 
                        AND expiration_date < DATE_SUB(NOW(), INTERVAL 1 YEAR)
                        """
                else:
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
            else:
                if clicked_button=="all":
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants"
                elif clicked_button=="open":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE application_due_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="continuous":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date < CURRENT_TIMESTAMP
                        AND application_due_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="comingsoon":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE open_date < CURRENT_TIMESTAMP
                        """
                elif clicked_button=="recentlyclosed":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date > CURRENT_TIMESTAMP
                        """
                elif clicked_button=="archived":
                    sql = """
                        SELECT id, title, grants_type, subjects 
                        FROM ggrants 
                        WHERE expiration_date < DATE_SUB(NOW(), INTERVAL 1 YEAR)
                        """
                else:
                    sql = "SELECT id,title,grants_type,subjects FROM ggrants"
        elif "addquery" in request.form:
            sql_string = request.form['query_front']
            mapper_db = {"Title":"title",
                         "Grant Status": "grant_status",
                         "Open date": "open_date",
                         "Sponsor": "sponsor",
                         "Sponsor type": "sponsor_types",
                         "Grants type": "grants_type",
                         "Applicant type": "applicant_types",
                         "Award min (n)": "award_min",
                         "Award max (n)": "award_max",
                         "CFDA": "cfda",
                         "Earliest start date": "earliest_start_date",
                         "Expiration date": "expiration_date",
                         "Keywords": "keywords",
                         "Subjects": "subjects",
                         "Submit date": "submit_date",
                         "Activity Code": "activity_code",
                         "Citizenships": "citizenships",
                         "Application due date": "application_due_date",
                         "Intent due date": "intent_due_date",
                         "Applicant locations": "countries",
                         "Activity locations": "countries",
                         "Amount per Grant (max)": "amount_per_grant_max",
                         "Amount per Grant (min)": "amount_per_grant_min"}
            field_types = {
                        "title": "varchar(255)",
                        "grant_status": "varchar(255)",
                        "open_date": "date",
                        "earliest_start_date": "date",
                        "expiration_date": "date",
                        "sponsor": "int(11)",
                        "sponsor_types": "text",
                        "grants_type": "text",
                        "applicant_types": "text",
                        "award_min": "int(11)",
                        "award_max": "int(11)",
                        "cfda": "text",
                        "keywords": "text",
                        "subjects": "text",
                        "submit_date": "date",
                        "activity_code": "text",
                        "citizenships": "text",
                        "application_due_date": "date",
                        "intent_due_date": "date",
                        "countries": "text",
                        "amount_per_grant_max": "int(11)",
                        "amount_per_grant_min": "int(11)"
                    }
            operators = ["AND", "OR", "NOT"]
            conditions = parse_and_format_sql_conditions(sql_string, operators, mapper_db, field_types)
            sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE " + " ".join(conditions)
            with sqlconnection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()  # Fetch all records matching the query
                print(result)
            return render_template('grantize/dashboard/browsegrants.html', grants=result, dummy="all")
        else:
            sql = "SELECT id,title,grants_type,subjects FROM ggrants"
        try:
            print(sql)
            if not clicked_button:
                clicked_button = "all"
            mycursor = sqlconnection.cursor(dictionary=True)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            print(result)
            mycursor.close()
            return render_template('grantize/dashboard/browsegrants.html', grants=result, dummy=clicked_button,  favlist=favlist, savlist=savlist)
        except:
            print("Database Connection Not Working!!")
            return render_template('grantize/dashboard/browsegrants.html')
    
@app.route('/grantizeviewgrants', methods =["GET", "POST"])
def grantizeviewgrants():
    global sqlconnection
    if session.get("loginnname"):
        grantid = request.form['grantid']
        print("--------")
        print(grantid)
        mycursor = sqlconnection.cursor()
        sql = "SELECT id,title,subjects,description,submission_info,amount_info,cost_sharing,data_management,contacts,countries,citizenships,grants_type,applicant_types,activity_code,grant_status,open_date,intent_due_date,application_due_date,earliest_start_date,expiration_date,currency,amount_per_grant_min,amount_per_grant_max,award_min,award_max,cfda,grant_source_url FROM ggrants WHERE id = %s"
        values = (grantid,)
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
        print(result[0])
        id,title,subjects,description,submission_info,amount_info,cost_sharing,data_management,contacts,countries,citizenships,grants_type,applicant_types,activity_code,grant_status,open_date,intent_due_date,application_due_date,earliest_start_date,expiration_date,currency,amount_per_grant_min,amount_per_grant_max,award_min,award_max,cfda,grant_source_url = result[0]
        return render_template('grantize/dashboard/viewgrants.html', id=id, title=title, subjects=subjects, description=description, submission_info=submission_info, amount_info=amount_info, cost_sharing=cost_sharing, data_management=data_management, contacts=contacts, countries=countries, citizenships=citizenships, grants_type=grants_type, applicant_types=applicant_types, activity_code=activity_code, grant_status=grant_status, open_date=open_date, intent_due_date=intent_due_date, application_due_date=application_due_date, earliest_start_date=earliest_start_date, expiration_date=expiration_date, currency=currency, amount_per_grant_min=amount_per_grant_min, amount_per_grant_max=amount_per_grant_max, award_min=award_min, award_max=award_max, cfda=cfda, grant_source_url=grant_source_url)
    else:
        return render_template('grantize/grantize.html')

@app.route('/grantizesearchquery', methods =["GET", "POST"])
def grantizesearchquery():
    global sqlconnection
    if session.get("loginnname"):
        user = session.get('loginid')
        if "_tokensearchquery" in request.form:
            try:
                title_query = request.form['tquery']
                mycursor = sqlconnection.cursor()
                sql = "SELECT id,title,grants_type,subjects FROM ggrants WHERE title LIKE '%"+title_query+"%'"
                mycursor.execute(sql)
                result = mycursor.fetchall()
                print(result[:1])
                return render_template('grantize/dashboard/searchquery.html', grants=result)
            except:
                print("Database Connection Not Working!!")
                return render_template('grantize/dashboard/searchquery.html')
        else:
            return render_template('grantize/dashboard/searchquery.html')
    else:
        return render_template('grantize/grantize.html')

@app.route('/grantizefavquery', methods =["GET", "POST"])
def grantizefavquery():
    global sqlconnection
    if session.get("loginnname"):
        print("=-=-=-=-=-=-=-=-=")
        user = session.get('loginid')
        try:
            mycursor = sqlconnection.cursor()
            # SQL query to get specific columns from the grespro table
            query = """
            SELECT grantid
            FROM gfavs
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            favlist = mycursor.fetchall()
            query = """
            SELECT grantid
            FROM gsaved
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            savlist = mycursor.fetchall()
            mycursor.close()
            favlist = [f[0] for f in favlist]
            savlist = [f[0] for f in savlist]
        except Exception as e:
            print("Error fetching experience profiles from database:", str(e))
            return []
        if "_tokensearchquery" in request.form:
            try:
                title_query = request.form['tquery']
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gfavs s ON g.id = s.grantid WHERE s.userid = "+str(user)+" AND g.title LIKE '%"+title_query+"%'"
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/favquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 1!!")
                return render_template('grantize/dashboard/favquery.html')
        if "sharewithothers" in request.form:
            try:
                # Retrieve data from form fields
                mycursor = sqlconnection.cursor()
                useremail = request.form.get('users', '').strip()
                grant_id = request.form.get('grant_id', '').strip()
                print("--------")
                print(grant_id)
                print(useremail)
                print("---------")
                flash("Activity information added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            try:
                # Fetch the user ID where email matches 'dummy'
                sql_select_query = """
                    SELECT id FROM gresearcherslist WHERE email = %s
                """
                mycursor.execute(sql_select_query, (useremail,))
                user_record = mycursor.fetchone()
                print("--------")
                print(user_record)
                print("---------")
                if user_record:
                    # Insert record into gshared
                    sql_insert_query = """
                        INSERT INTO gshared (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user, grant_id))
                    sqlconnection.commit()
                    # Insert record into gsharedwith
                    sql_insert_query = """
                        INSERT INTO gsharedwith (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user_record[0], grant_id))
                    sqlconnection.commit()
            except mysql.connector.Error as err:
                print("Error:", err)
                return jsonify({"status": "error", "message": str(err)}), 500
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gfavs s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/favquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/favquery.html')
        else:
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gfavs s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/favquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/favquery.html')
    else:
        return render_template('grantize/grantize.html')

@app.route('/grantizesavedquery', methods =["GET", "POST"])
def grantizesavedquery():
    global sqlconnection
    if session.get("loginnname"):
        print("=-=-=-=-=-=-=-=-=")
        user = session.get('loginid')
        try:
            mycursor = sqlconnection.cursor()
            # SQL query to get specific columns from the grespro table
            query = """
            SELECT grantid
            FROM gfavs
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            favlist = mycursor.fetchall()
            query = """
            SELECT grantid
            FROM gsaved
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            savlist = mycursor.fetchall()
            mycursor.close()
            favlist = [f[0] for f in favlist]
            savlist = [f[0] for f in savlist]
        except Exception as e:
            print("Error fetching experience profiles from database:", str(e))
            return []
        if "_tokensearchquery" in request.form:
            try:
                title_query = request.form['tquery']
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsaved s ON g.id = s.grantid WHERE s.userid = "+str(user)+" AND g.title LIKE '%"+title_query+"%'"
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/savedquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 1!!")
                return render_template('grantize/dashboard/savedquery.html')
        if "sharewithothers" in request.form:
            try:
                # Retrieve data from form fields
                mycursor = sqlconnection.cursor()
                useremail = request.form.get('users', '').strip()
                grant_id = request.form.get('grant_id', '').strip()
                print("--------")
                print(grant_id)
                print(useremail)
                print("---------")
                flash("Activity information added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            try:
                # Fetch the user ID where email matches 'dummy'
                sql_select_query = """
                    SELECT id FROM gresearcherslist WHERE email = %s
                """
                mycursor.execute(sql_select_query, (useremail,))
                user_record = mycursor.fetchone()
                print("--------")
                print(user_record)
                print("---------")
                if user_record:
                    # Insert record into gshared
                    sql_insert_query = """
                        INSERT INTO gshared (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user, grant_id))
                    sqlconnection.commit()
                    # Insert record into gsharedwith
                    sql_insert_query = """
                        INSERT INTO gsharedwith (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user_record[0], grant_id))
                    sqlconnection.commit()
            except mysql.connector.Error as err:
                print("Error:", err)
                return jsonify({"status": "error", "message": str(err)}), 500
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsaved s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/savedquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/savedquery.html')
        else:
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsaved s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/savedquery.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/savedquery.html')
    else:
        return render_template('grantize/grantize.html')
    

@app.route('/grantizesharedbyme', methods =["GET", "POST"])
def grantizesharedbyme():
    global sqlconnection
    if session.get("loginnname"):
        print("=-=-=-=-=-=-=-=-=")
        user = session.get('loginid')
        try:
            mycursor = sqlconnection.cursor()
            # SQL query to get specific columns from the grespro table
            query = """
            SELECT grantid
            FROM gfavs
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            favlist = mycursor.fetchall()
            query = """
            SELECT grantid
            FROM gsaved
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            savlist = mycursor.fetchall()
            mycursor.close()
            favlist = [f[0] for f in favlist]
            savlist = [f[0] for f in savlist]
        except Exception as e:
            print("Error fetching experience profiles from database:", str(e))
            return []
        if "_tokensearchquery" in request.form:
            try:
                title_query = request.form['tquery']
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gshared s ON g.id = s.grantid WHERE s.userid = "+str(user)+" AND g.title LIKE '%"+title_query+"%'"
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedbyme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 1!!")
                return render_template('grantize/dashboard/sharedbyme.html')
        if "sharewithothers" in request.form:
            try:
                # Retrieve data from form fields
                mycursor = sqlconnection.cursor()
                useremail = request.form.get('users', '').strip()
                grant_id = request.form.get('grant_id', '').strip()
                print("--------")
                print(grant_id)
                print(useremail)
                print("---------")
                flash("Activity information added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            try:
                # Fetch the user ID where email matches 'dummy'
                sql_select_query = """
                    SELECT id FROM gresearcherslist WHERE email = %s
                """
                mycursor.execute(sql_select_query, (useremail,))
                user_record = mycursor.fetchone()
                print("--------")
                print(user_record)
                print("---------")
                if user_record:
                    # Insert record into gshared
                    sql_insert_query = """
                        INSERT INTO gshared (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user, grant_id))
                    sqlconnection.commit()
                    # Insert record into gsharedwith
                    sql_insert_query = """
                        INSERT INTO gsharedwith (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user_record[0], grant_id))
                    sqlconnection.commit()
            except mysql.connector.Error as err:
                print("Error:", err)
                return jsonify({"status": "error", "message": str(err)}), 500
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gshared s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedbyme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/sharedbyme.html')
        else:
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gshared s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedbyme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/sharedbyme.html')
    else:
        return render_template('grantize/grantize.html')

@app.route('/grantizesharedwithme', methods =["GET", "POST"])
def grantizesharedwithme():
    global sqlconnection
    if session.get("loginnname"):
        print("=-=-=-=-=-=-=-=-=")
        user = session.get('loginid')
        try:
            mycursor = sqlconnection.cursor()
            # SQL query to get specific columns from the grespro table
            query = """
            SELECT grantid
            FROM gfavs
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            favlist = mycursor.fetchall()
            query = """
            SELECT grantid
            FROM gsaved
            WHERE userid = %s
            """
            mycursor.execute(query, (user,))
            savlist = mycursor.fetchall()
            mycursor.close()
            favlist = [f[0] for f in favlist]
            savlist = [f[0] for f in savlist]
        except Exception as e:
            print("Error fetching experience profiles from database:", str(e))
            return []
        if "_tokensearchquery" in request.form:
            try:
                title_query = request.form['tquery']
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsharedwith s ON g.id = s.grantid WHERE s.userid = "+str(user)+" AND g.title LIKE '%"+title_query+"%'"
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedwithme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 1!!")
                return render_template('grantize/dashboard/sharedwithme.html')
        if "sharewithothers" in request.form:
            try:
                # Retrieve data from form fields
                mycursor = sqlconnection.cursor()
                useremail = request.form.get('users', '').strip()
                grant_id = request.form.get('grant_id', '').strip()
                print("--------")
                print(grant_id)
                print(useremail)
                print("---------")
                flash("Activity information added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('error_template.html'), 500
            try:
                # Fetch the user ID where email matches 'dummy'
                sql_select_query = """
                    SELECT id FROM gresearcherslist WHERE email = %s
                """
                mycursor.execute(sql_select_query, (useremail,))
                user_record = mycursor.fetchone()
                print("--------")
                print(user_record)
                print("---------")
                if user_record:
                    # Insert record into gshared
                    sql_insert_query = """
                        INSERT INTO gshared (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user, grant_id))
                    sqlconnection.commit()
                    # Insert record into gsharedwith
                    sql_insert_query = """
                        INSERT INTO gsharedwith (userid, grantid) VALUES (%s, %s)
                    """
                    mycursor.execute(sql_insert_query, (user_record[0], grant_id))
                    sqlconnection.commit()
            except mysql.connector.Error as err:
                print("Error:", err)
                return jsonify({"status": "error", "message": str(err)}), 500
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsharedwith s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedwithme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/sharedwithme.html')
        else:
            try:
                mycursor = sqlconnection.cursor(dictionary=True)
                sql = "SELECT g.id,g.title,g.grants_type,g.subjects FROM ggrants g JOIN gsharedwith s ON g.id = s.grantid WHERE s.userid = "+str(user)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                mycursor.close()
                print(result[:1])
                return render_template('grantize/dashboard/sharedwithme.html', grants=result, favlist=favlist, savlist=savlist)
            except:
                print("Database Connection Not Working -- 2!!")
                return render_template('grantize/dashboard/sharedwithme.html')
    else:
        return render_template('grantize/grantize.html')



































@app.route('/recruitphd')
def recruitphd():
    return render_template('recruitphd/recruitphd.html')

@app.route('/recphdwhyus')
def recphdwhyus():
    return render_template('recruitphd/navbar/whyus.html')

@app.route('/recphdplans')
def recphdplans():
    return render_template('recruitphd/navbar/plans.html')

@app.route('/recphdblogs')
def recphdblogs():
    return render_template('recruitphd/navbar/blogs.html')

@app.route('/recphdhelp')
def recphdhelp():
    return render_template('recruitphd/navbar/help.html')

@app.route('/loginrecphdoptions')
def loginrecphdoptions():
    return render_template('recruitphd/login/loginoptions.html')

@app.route('/loginrecphdseeker')
def loginrecphdseeker():
    return render_template('recruitphd/login/loginresearcher.html')

@app.route('/loginrecphdrecruiter')
def loginrecphdrecruiter():
    return render_template('recruitphd/login/loginsponsors.html')

@app.route('/createuserrecphd')
def createuserrecphd():
    return render_template('recruitphd/login/createrecruiter.html')

@app.route('/recphdjobs')
def recphdjobs():
    return render_template('recruitphd/jobs/jobs.html')






























@app.route('/sisterlab')
def sisterlab():
    return render_template('sisterlab/sisterlab.html')

@app.route('/loginsislab')
def loginsislab():
    return render_template('sisterlab/login/loginsislabs.html')

@app.route('/authloginsislab', methods =["GET", "POST"])
def authloginsislab():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "admin@gmail.com" and password == "User@123":
            return render_template('sisterlab/dashboard/dashboard.html')
    return render_template('sisterlab/sisterlab.html')

@app.route('/sislabstaff')
def sislabstaff():
    return render_template('sisterlab/dashboard/staff.html')

@app.route('/sislabstaffpermission')
def sislabstaffpermission():
    return render_template('sisterlab/dashboard/staffpermission.html')

@app.route('/sislabactivity')
def sislabactivity():
    return render_template('sisterlab/dashboard/activity.html')

@app.route('/sislabactivitycode')
def sislabactivitycode():
    return render_template('sisterlab/dashboard/activitycode.html')

@app.route('/sislabapplicanttype')
def sislabapplicanttype():
    return render_template('sisterlab/dashboard/applicanttype.html')

@app.route('/sislabawards')
def sislabawards():
    return render_template('sisterlab/dashboard/awards.html')

@app.route('/sislabcfda')
def sislabcfda():
    return render_template('sisterlab/dashboard/cfda.html')

@app.route('/sislabcommittee')
def sislabcommittee():
    return render_template('sisterlab/dashboard/committee.html')

@app.route('/sislabconferences')
def sislabconferences():
    return render_template('sisterlab/dashboard/conferences.html')

@app.route('/sislabdegree')
def sislabdegree():
    return render_template('sisterlab/dashboard/degree.html')

@app.route('/sislabdepartments')
def sislabdepartments():
    return render_template('sisterlab/dashboard/departments.html')

@app.route('/sislabgranttypes')
def sislabgranttypes():
    return render_template('sisterlab/dashboard/granttype.html')

@app.route('/sislabhobbies')
def sislabhobbies():
    return render_template('sisterlab/dashboard/hobbies.html')

@app.route('/sislabjobbenefit')
def sislabjobbenefit():
    return render_template('sisterlab/dashboard/jobbenefits.html')

@app.route('/sislabjournals')
def sislabjournals():
    return render_template('sisterlab/dashboard/journals.html')

@app.route('/sislabkeywords')
def sislabkeywords():
    return render_template('sisterlab/dashboard/keywords.html')

@app.route('/sislablanguages')
def sislablanguages():
    return render_template('sisterlab/dashboard/languages.html')

@app.route('/sislabskillsgained')
def sislabskillsgained():
    return render_template('sisterlab/dashboard/skillsgained.html')

@app.route('/sislabsubjects')
def sislabsubjects():
    return render_template('sisterlab/dashboard/subjects.html')

@app.route('/sislabwtformula')
def sislabwtformula():
    return render_template('sisterlab/dashboard/wtformula.html')

@app.route('/sislabwtforjobs')
def sislabwtforjobs():
    return render_template('sisterlab/dashboard/wtforjobs.html')

@app.route('/sislabskillsets')
def sislabskillsets():
    return render_template('sisterlab/dashboard/skillsets.html')

@app.route('/sislablocations')
def sislablocations():
    return render_template('sisterlab/dashboard/skillsets.html')

@app.route('/sislabgrants')
def sislabgrants():
    return render_template('sisterlab/grantize/grants.html')

@app.route('/sislabsponsors')
def sislabsponsors():
    return render_template('sisterlab/grantize/sponsors.html')

@app.route('/sislabresearchers')
def sislabresearchers():
    return render_template('sisterlab/grantize/researchers.html')

@app.route('/sislabsponsorplan')
def sislabsponsorplan():
    return render_template('sisterlab/grantize/sponsorplan.html')

@app.route('/sislabresearcherplan')
def sislabresearcherplan():
    return render_template('sisterlab/grantize/researcherplan.html')

@app.route('/sislabnotifications')
def sislabnotifications():
    return render_template('sisterlab/grantize/notifications.html')

@app.route('/sislabbanners')
def sislabbanners():
    return render_template('sisterlab/grantize/banners.html')

@app.route('/sislabtestimonials')
def sislabtestimonials():
    return render_template('sisterlab/grantize/testimonials.html')

@app.route('/sislabvidtestimonials')
def sislabvidtestimonials():
    return render_template('sisterlab/grantize/vidtestimonials.html')

@app.route('/sislabwhygrant')
def sislabwhygrant():
    return render_template('sisterlab/grantize/whyus.html')

@app.route('/sislabgrantblogs')
def sislabgrantblogs():
    return render_template('sisterlab/grantize/blogs.html')

@app.route('/sislabgrantfaqs')
def sislabgrantfaqs():
    return render_template('sisterlab/grantize/faq.html')

@app.route('/sislabgrantpages')
def sislabgrantpages():
    return render_template('sisterlab/grantize/pages.html')

@app.route('/sislabrecjobs')
def sislabrecjobs():
    return render_template('sisterlab/recruitphd/jobs.html')

@app.route('/sislabrecjobapplications')
def sislabrecjobapplications():
    return render_template('sisterlab/recruitphd/jobapplications.html')

@app.route('/sislabrecrecruiters')
def sislabrecrecruiters():
    return render_template('sisterlab/recruitphd/recruiters.html')

@app.route('/sislabrecseekers')
def sislabrecseekers():
    return render_template('sisterlab/recruitphd/jobseekers.html')

@app.route('/sislabrecplans')
def sislabrecplans():
    return render_template('sisterlab/recruitphd/plans.html')

@app.route('/sislabrecplanseeker')
def sislabrecplanseeker():
    return render_template('sisterlab/recruitphd/jobseekers.html')

@app.route('/sislabrecnotifications')
def sislabrecnotifications():
    return render_template('sisterlab/recruitphd/notifications.html')

@app.route('/sislabrecbanners')
def sislabrecbanners():
    return render_template('sisterlab/recruitphd/banners.html')

@app.route('/sislabrectestimonials')
def sislabrectestimonials():
    return render_template('sisterlab/recruitphd/testimonials.html')

@app.route('/sislabrectestimonialsvideo')
def sislabrectestimonialsvideo():
    return render_template('sisterlab/recruitphd/videotestimonials.html')

@app.route('/sislabrecwhyus')
def sislabrecwhyus():
    return render_template('sisterlab/recruitphd/whyus.html')

@app.route('/sislabrecblogs')
def sislabrecblogs():
    return render_template('sisterlab/recruitphd/blogs.html')

@app.route('/sislabrecfaqs')
def sislabrecfaqs():
    return render_template('sisterlab/recruitphd/faq.html')

@app.route('/sislabrecpages')
def sislabrecpages():
    return render_template('sisterlab/recruitphd/pages.html')











def connect_with_database():
    global sqlconnection
    global globalcities
    global globalcountries
    global globalorganizations
    sqlconnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="grant"
        )
    if sqlconnection.is_connected():
        print("Database Connection Succeeded!!")
        mycursor = sqlconnection.cursor()
        sql = "SELECT name FROM cities"
        mycursor.execute(sql)
        globalcities = mycursor.fetchall()
        sql = "SELECT name FROM countries"
        mycursor.execute(sql)
        globalcountries = mycursor.fetchall()
        sql = "SELECT name FROM organizations"
        mycursor.execute(sql)
        globalorganizations = mycursor.fetchall()
        mycursor.close()
        globalcities = [g[0] for g in globalcities]
        globalcountries = [g[0] for g in globalcountries]
        globalorganizations = [g[0] for g in globalorganizations]
        print(globalcities[:10])
    else:
        print("Database Connection Failed!!")
        exit

 
# main driver function
if __name__ == '__main__':
    connect_with_database()
    app.run(port = 6991, debug = True)