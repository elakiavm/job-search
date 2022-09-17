from unittest import result
import streamlit as st
from pymongo import MongoClient 
import pymongo
import requests
import os
from dotenv import load_dotenv

# base_url= "https://jobs.github.com/positions.json?description={}&location={}"

load_dotenv()

MONGO_URI="mongodb+srv://elakia:Kvtohindu@cluster0.dyhgo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# connecting to the mongoDb client 
cluster = MongoClient(MONGO_URI)

# giving the cluster name 
db      = cluster['Job-search']

# giving the collection name 
col     = db['data']


def get_data():
    # resp=requests.get()
    result = {
        "job_company":"Google",
        "job_post_data":"13th July,2022",
        "job_howtoapply": "https://careers.google.com/jobs/results/"
    }
    return result

JOB_HTML_TEMPLATE = """"
<div>
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
</div>
"""


def main():
    menu = ["Home","About"]
    choice =st.sidebar.selectbox("Menu",menu)

    st.title("DevDeeds -Search Jobs")

    if choice == "Home":
        st.subheader("Home")

        with st.form(key='searchform'):
            nav1,nav2,nav3 = st.columns([3,2,1])

            with nav1:
                search_term =st.text_input("Search Job")
            with nav2:
                location=st.text_input("Location")
            with nav3:
                st.text("Search")
                submit_search=st.form_submit_button(label='Search')

        st.success("You searched for {} in {}".format(search_term,location))

        col1 , col2 = st.beta_columns([2,1])

        with col1:
            if submit_search:
                # search_url = base_url.format(search_term,location)
                # st.write(search_url)
                data = get_data()
                # st.write(data)
                # nos_of_results = len(data)
                # st.subheader("Showing {} jobs".format(nos_of_results))
                
            
                job_company=data['job_company']
                st.write(job_company)
                job_post_data=data['job_post_data']
                st.write(job_post_data)
                job_howtoapply=data['job_howtoapply']
                st.write(job_howtoapply)
                #     job_location=i['location']
                #     job_company=i['company']
                #     job_company_url=i['company_url']
                #     job_post_data=i['created_at']
                #     job_des=i['description']
                #     job_howtoapply=i['how_to_apply']
                # st.markdown(JOB_HTML_TEMPLATE.format(job_company,job_post_data,job_howtoapply),
                #     unsafe_allow_html=True)
        with col2:
            with st.form(key='email_form'):
                email =st.text_input('Email')
                submit_email =st.form_submit_button(label='Subscribe')
                if submit_email:
                    st.success("A msg sent {}".format(email))

                    data_dict = {
                        "email":email,
                        "job_company":job_company,
                        "search_term":search_term,
                        "job_post_data":job_post_data
                    }

                    (data_dict)




    else:
        st.subheader("About")
        data = col.find()
        st.write(data_dict)

if __name__ == '__main__':
    main()
