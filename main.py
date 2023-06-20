#app.py
from flask import Flask, request, render_template, jsonify, json
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
  
app = Flask(__name__)
    
mysql = MySQL()
   
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'arslan12'
app.config['MYSQL_DATABASE_DB'] = 'hospitality'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
  
@app.route('/')
def home():
    return render_template('index.html')



@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
 
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from vitalsign")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from vitalsign WHERE patient_id LIKE %s OR VitalSignsSubclassName LIKE %s", (likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM vitalsign ORDER BY id asc limit %s, %s;", (row, rowperpage))
                employeelist = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM vitalsign WHERE patient_id LIKE %s OR VitalSignsSubclassName LIKE %s limit %s, %s;", (likeString, likeString, row, rowperpage))
                employeelist = cursor.fetchall()
 
            data = []
            
            for row in employeelist:
                data.append({
                    'id':row['id'],
                    'parentId': row['patient_id'],
                    'MedicalRecordNumber': row['MedicalRecordNumber'],
                    'CinicNumber': row['CinicNumber'],
                    'HospitalNumber': row['HospitalNumber'],
                    'MedicalIdentification': row['MedicalIdentification'],
                    'VitalSignsSubclassName': row['VitalSignsSubclassName'],
                    'VitatSignsPhysicalExamination': row['VitatSignsPhysicalExamination'],
                    'VitalSignsSubcategoryUnits': row['VitalSignsSubcategoryUnits'],
                    'ExaminationTime': row['ExaminationTime'],
                    
                    
                })
            
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()



if __name__ == "__main__":
    app.run(debug=True)