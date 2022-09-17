'''
Created on 
    March 26, 202

Course work: 
    MongoDB CURD
    
@author: Elakia

Source:
    
'''

from crypt import methods
from flask import Flask, request, jsonify,render_template
import pymongo
from pymongo import MongoClient 
from flask import Markup
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Getting the url from the  env file
MONGO_URI = os.environ.get('MONGO_URI')

# connecting to the mongoDb client 
cluster = MongoClient(MONGO_URI)

# giving the cluster name 
db      = cluster['Job-Search']

# giving the collection name 
col     = db['data']

{"(1) Job Title": "Java Software Developer", "(4) Job Link": "https://www.indeed.ca/viewjob?cmp=Western-Financial-Group-Insurance-Solutions&t=Junior+Developer&jk=d414f2d81aebf42a&sjdu=vQIlM60yK_PwYat7ToXhk_BtMgCfoRREjwFTpnTZpxBItyyCDDYJailt3JH9enIYBR5pWX60rpkBc2AB4IZ1_A&tk=1e06gj8lrpahp800&adid=256288292&pub=4a1b367933fd867b19b072952f68dceb&vjs=3", "(2) Company Name": "Momentum Healthware", "(3) Job Description": "[\nAt Western Financial Group Insurance Solutions we help businesses evaluate their risks and develop solutions for their commercial insurance and employee benefits requirements tailored to \ntheir\n needs. We specialize in sales, underwriting and placement and servicing of commercial insurance and employee benefits products across Canada.\nWe are looking for a Junior Developer to join our team Information Technology team.\nThe Information Technology Department is responsible for the computer systems/network and business applications/software for Group Insurance Solutions. Information and Technology is committed to providing Reliable, Accessible and Relevant system solutions.\nOur Developers analyze, design, code, test, implement and document moderately complex software applications. Individuals with the ability to recommend and participate in continuous improvement efforts will thrive in this position.\nWhat we are looking for: \nBeing successful in this role requires the ability to deliver excellence in identifying, studying, learning and applying knowledge of new/emerging technologies, methodologies and products to evaluate value of new technologies to support business objectives and strategy and drive continuous improvement efforts. The ability to deliver in difficult situations and to contribute to a positive work environment\nWhat We Offer You: \nVibrant, collaborative team environment\nCompetitve compensation package\nExtended health and dental benefits, 50% premium paid\nThree weeks\\u2019 vacation plus paid personal days\nCompany-matched investment and saving programs\nWhat You Offer Us: \n2+ years\\u2019 experience as a developer ideally in a multi-tiered and web based applications\nExperience with the following technologies: ASP.NET, C#, IIS, SQL Server, MVC Architecture, and Agile Development\nExperience with HTML, CSS, Javascript, JQuery, AJAX, JSON, XML\nKnowledge of SQL and relational databases\nStrong understanding of object-oriented programming, design principles and software patterns\nSuperior communications skills\nComputer Programmer diploma or Degree in Computer Science\nDemonstrated effective analytical skills with a strong work ethic\nTeam player who brings solutions to problems and encompasses strong time management skills\nWe thank all interested candidates in advance; however, only individuals selected for interviews will be contacted\nJob Type: Full-time\n]"},


# for incrementing the entries
@app.route("/", methods='GET')
def home():
    return render_template("job_search.html")
def get_last_job_search_id():

    last_job_search_id  = col.find().sort([('search_id', -1)]).limit(1)

    try:
        last_job_search_id = last_job_search_id[0]['search_id']

    except:
        last_job_search_id = 0

    return last_job_search_id

# inserting ech entire
@app.route("/", methods=['POST'])
def startpy():

    name  = request.json['name']
    job_domain = request.json['job_domain']
    
    last_job_search_id = get_last_job_search_id()

    current_job_search = last_job_search_id + 1

    movie_dict = {

        "search_id": current_job_search,
        "name"    : name,
        "job_domain"   : job_domain

    }

    col.insert_one(movie_dict)

    return "success"

# seeing all the entries    
@app.route("/get", methods=['GET'])
def get_all_movie():

    movie = col.find()
    print(movie)

    movie_list = []

    for item in movie:

        movie_dict = {
            "search_id": item['search_id'],
            "name"    : item['name'],
            "job_domain"   : item['job_domain']

        }

        movie_list.append(movie_dict)

        print(item)
    
    return jsonify(movie_list)

#for seeing the particular entire
@app.route("/get/<search_id>", methods=['GET'])
def get_one_movie(search_id):

    movie = col.find_one({'search_id': int(search_id)})
    print(movie)

   
    movie_dict = {
        "name" : movie['name'],
        "job_domain": movie['job_domain']

    }

    return movie_dict

# update the existing entire
@app.route("/edit/<search_id>", methods=['POST'])
def edit_movie(search_id):
    # movie = col.find_one({'search_id': int(search_id)})

    name  = request.json['name']
    job_domain = request.json['job_domain']

    movie_dict = {
    
        "name" : name,
        "job_domain": job_domain

    }

    col.update_many({'search_id': int(search_id)}, {'$set': movie_dict})
    
    return 'success'
    
@app.route("/delete/<search_id>", methods=['DELETE'])
def delete_one_movie(search_id):

    col.delete_many({'search_id': int(search_id)})

    return 'success'
if __name__ == "__main__":
    app.run()