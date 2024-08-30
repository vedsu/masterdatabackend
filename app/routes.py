# Routing

from flask import request, jsonify
from app import app
from app import mongo
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from app.model_order import Order
from app.model_category import Category
from app.model_website import Website

import string
import random
from bson import Binary
import re
import io
import base64
from PIL import Image
import os
from datetime import datetime
from app import s3_client, s3_resource


@app.route('/', methods =['POST'])
def master_login():
    if request.method in 'POST':
        login_email = request.json.get("Email")
        login_password = request.json.get("Password")

        response_login = Login.authenticate(login_email, login_password)
        return response_login
    
@app.route('/webinar_panel', methods = ['GET'])
def webinar_panel():
    
    webinar_list = Webinar.view_webinar()
    speaker_list = Speaker.view_speaker()
    website_list = Website.view_website()
    # industry_list = Category.industry()
        
    if request.method in 'GET':
       
        return jsonify(webinar_list, speaker_list, website_list),200
    
def process_url(topic):

    # Convert the sentence to lowercase
    sentence = topic.lower()
    
    # Remove special characters using regex
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    
    # Replace spaces between words with dashes
    sentence = sentence.replace(' ', '-')
    
    return sentence

@app.route('/webinar_panel/create_webinar', methods= ['POST'])
def create_webinar():
    webinar_list = Webinar.view_webinar()
    id = str(len(list(webinar_list)))
    N = 3
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    w_id = res+"_"+id
    if request.method in ['POST']:
        webinar_topic = request.json.get("topic")
        speaker = request.json.get("speaker")
        date_time = request.json.get("date")
        website = request.json.get("website")
        
        # Parse the datetime string
        dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Extract the date and time as separate strings
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S.%f")[:-10]  # Trim the last three digits of microseconds to match milliseconds
        
        webinar_data ={
        
        "id": w_id,
        
        "topic":webinar_topic,
        "speaker":speaker,
        "industry":request.json.get("industry"),
        "date_time":dt,
        "time":time_str,
        "date":date_str,
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":"Active",
        "webinar_url": process_url(webinar_topic),
        "website": website,
        "description":request.json.get("description"),
        
        }
        
        response_create_webinar = Webinar.create_webinar(webinar_data)
        respone_history_speaker = Speaker.update_history(speaker,webinar_topic)
        response = Website.insert_webinar(website, webinar_topic)
        if response.get("success") == True:
            return jsonify(response_create_webinar,respone_history_speaker,response),201
        else:
            response, 403
            
@app.route('/webinar_panel/<w_id>', methods= ['GET','PUT','POST','DELETE'])
def update_webinar_panel(w_id):    
    
    
    webinar_data = Webinar.data_webinar(w_id)
    
    if request.method  == 'GET':
        
        return webinar_data,200
       
    elif request.method  =='POST':
        
        webinar_status = request.json.get("status")
        
        response = Webinar.edit_webinar(w_id, webinar_status)
        
        if response.get("success") == True:
            return response, 201
        
        else:
            return response,304
                
        
        
    elif request.method =='PUT':
        
        topic = request.json.get("topic")
        speaker = request.json.get("speaker")
        website = request.json.get("website")
        
        date_time = request.json.get("date")
        # Parse the datetime string
        dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Extract the date and time as separate strings
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S.%f")[:-10]  # Trim the last three digits of microseconds to match milliseconds
        
        webinar_data = {
        "id":w_id,
        
        "topic":topic,
        "industry":request.json.get("industry"),
        "speaker":speaker,
        "date_time":dt,
        "date":date_str,
        "time":time_str,
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":request.json.get("status"),
        "webinar_url": process_url(topic),
        "website": website,
        "description":request.json.get("description"),
        }
        
        Speaker.update_history(speaker, topic)
        Website.insert_webinar(website, topic)
        
        response = Webinar.update_webinar(w_id, webinar_data)
        if response.get("success") == True:
            return response,200
    
        else:
            return response,304
        
    elif request.method =='DELETE':
         
        response = Webinar.delete_webinar(w_id)
        
        if response.get("success") == True:
            
            return response, 202
        else:
            return response, 204

@app.route('/speaker_panel', methods = ['GET'])
def speaker_panel():
    
    speaker_list = Speaker.list_speaker()
    if request.method in 'GET':
        return jsonify(speaker_list),200
    

@app.route('/speaker_panel/create_speaker', methods = ['POST'])
def create_speaker():
    
    speaker_list = Speaker.view_speaker()
    
    id = str(len(speaker_list))
    
    if request.method == 'POST':
         
        speaker_name = request.form.get("name")
        # initializing size of string
        N = 3
        
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=N))
        s_id = res+"_"+id
        
        bucket_name = "webinarprofs"
        object_key = ''.join(speaker_name.split(" "))+"_"+res
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/speaker/{object_key}.jpeg"
        image = request.files.get("photo")
        s3_client.put_object(
        Body=image, 
        Bucket=bucket_name, 
        Key=f'speaker/{object_key}.jpeg'
        )
        speaker_data ={
            "id": s_id,
            "name" :speaker_name,
            "email": request.form.get("email"),
            "industry": request.form.get("industry"),
            "contact" : request.form.get("contact"),
            "status":"Active",
            "bio": request.form.get("bio"),
            "history": [],
            "photo": s3_url,

        }
        
        response = Speaker.create_speaker(speaker_data)
        if response.get("success") == True:
            return response,201
        else:
            return response,403

@app.route('/speaker_panel/<s_id>', methods =['GET','PUT', 'POST', 'DELETE'])
def update_speaker_panel(s_id):
    
    
    
    if request.method == 'GET':
        speaker_data = Speaker.data_speaker(s_id)
       
        return jsonify(speaker_data),200        
            
    
    elif request.method == 'POST':

        speaker_status = request.json.get("status")
        
        response = Speaker.edit_speaker(s_id, speaker_status)
        
        if response.get("success") == True:
            return response, 201
        
        else:
            return response,304
        
    
    elif request.method == 'PUT':
        try:
            s3_url = request.form.get("photo")
            speaker_name = request.form.get("name")
            # initializing size of string
            """N = 3
            
            # using random.choices()
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=N))
            bucket_name = "webinarprofs"
            object_key = ''.join(speaker_name.split(" "))+"_"+res
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/speaker/{object_key}.jpeg"
            s3_client.put_object(
            Body=image, 
            Bucket=bucket_name, 
            Key=f'speaker/{object_key}.jpeg')"""
            
            speaker_dict = {
                "id": s_id,
                "name": speaker_name,
                "email": request.form.get("email"),
                "contact" : request.form.get("contact"),
                "industry": request.form.get("industry"),
                "status": "Active",
                "bio": request.form.get("bio"),
                "photo": s3_url,
                
            }
            
            response= Speaker.update_speaker(s_id, speaker_dict)
            if response.get("success") == True:
                return response,200
        
            else:
                return response,500

        except Exception as e:
            return {"success": False, "message": str(e)}, 500
      
        
    elif request.method == 'DELETE':

        response= Speaker.delete_speaker(s_id)
    
        if response.get("success") == True:
            
            return response, 202
        else:
            return response, 400


@app.route('/order_panel', methods =['GET'])
def order_panel():
    
    order_list = Order.view_order()
    if request.method in 'GET':
        
        return jsonify(order_list), 200
    
@app.route('/order_panel/<int:o_id>', methods = ['GET'])
def order_detail(o_id):
    
    order_data = Order.order_data(o_id)
    
    if request.method in 'GET':
           return order_data,200
    

@app.route('/category', methods = ['GET', 'POST'])
def category():
    
    if request.method in 'GET':
        
        industry_data =  Category.industry()
        return jsonify(industry_data),200
        
    elif request.method in 'POST':
        industry_selected = request.json.get("industry")
        category_added = request.json.get("category")
        
        response = Category.categories(industry_selected,category_added)
        if response.get("success") == True:
            return response,201
        else:
            return response,403
        
@app.route('/website_panel', methods= ['GET', 'POST'])
def website_utility():
    
    if request.method in 'GET':
        website_list = Website.view_website()
        return jsonify(website_list),200
    
    elif request.method in 'POST':
        
        website=request.json.get("website")
        response = Website.insert_website(website)
        if response.get("success") == True:
            return response,201
        else:
            return response,403
