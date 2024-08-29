# Webinar component

from app import mongo
from datetime import datetime
import pytz

class Webinar():
    
    @staticmethod
    def update_live_status():
        # Get current time in EST
        est = pytz.timezone('US/Eastern')
        current_time_est = datetime.now(est)
        try:
    
            # Update documents where the current time in EST is greater than the date_time and live is still true
            result = mongo.db.webinar_data.update_many(
                {
                    "date_time": {"$lt": current_time_est},
                    "sessionLive": True
                },
                {"$set": {"sessionLive": False}}
            )
            return {"success":True, "message":"live session updated"}
        except Exception as e:
            return {"success":False, "message":str(e)}
        
    @staticmethod
    def view_webinar():
        
        # Webinar list for display
    
        webinar_list =[]
        try: 
        
            
            webinar_data = list(mongo.db.webinar_data.find({}).sort({"date_time":-1}))
            for webinar in webinar_data:
                webinar_dict ={
        
                "id":webinar.get("id"),

                "topic":webinar.get("topic"),
                "industry":webinar.get("industry"),
                "speaker":webinar.get("speaker"),
                "date":webinar.get("date_time"),
                "time":webinar.get("time"),
                "timeZone":webinar.get("timeZone"),
                "duration":webinar.get("duration"),
                "category":webinar.get("category"),
                
                "sessionLive":webinar.get("sessionLive"),
                "priceLive":webinar.get("priceLive"),
                "urlLive":webinar.get("urlLive"),
                
                "sessionRecording":webinar.get("sessionRecording"),
                "priceRecording":webinar.get("priceRecording"),
                "urlRecording":webinar.get("urlRecording"),

                "sessionDigitalDownload":webinar.get("sessionDigitalDownload"),
                "priceDigitalDownload":webinar.get("priceDigitalDownload"),
                "urlDigitalDownload":webinar.get("urlDigitalDownload"),
                
                "sessionTranscript":webinar.get("sessionTranscript"),
                "priceTranscript":webinar.get("priceTranscript"),
                "urlTranscript":webinar.get("urlTranscript"),

                "status":webinar.get("status"),
                "webinar_url": webinar.get("webinar_url"),
                "description":webinar.get("description"),
                    
                    }
                    
                webinar_list.append(webinar_dict)
            
        
        except Exception as e:
                webinar_list = []
        
        
        return webinar_list
          
    
    @staticmethod
    def create_webinar(webinar_data):
        
        try:
            mongo.db.webinar_data.insert_one(webinar_data)
            return {"success":True, "message": "webinar created successfully"} 
        
        except Exception as e:
            return {"success":False, "message":str(e)}
    
    @staticmethod
    def data_webinar(w_id):
        
        webinar_info = None
        try: 
            
            webinar_data = list(mongo.db.webinar_data.find({"id":w_id}))
            webinar = webinar_data[0]
               
            webinar_data_dict ={
            
                    "id":webinar.get("id"),

                    "topic":webinar.get("topic"),
                    "industry":webinar.get("industry"),
                    "speaker":webinar.get("speaker"),
                    "date":webinar.get("date_time"),
                    "time":webinar.get("time"),
                    "timeZone":webinar.get("timeZone"),
                    "duration":webinar.get("duration"),
                    "category":webinar.get("category"),
                    
                    "sessionLive":webinar.get("sessionLive"),
                    "priceLive":webinar.get("priceLive"),
                    "urlLive":webinar.get("urlLive"),
                    
                    "sessionRecording":webinar.get("sessionRecording"),
                    "priceRecording":webinar.get("priceRecording"),
                    "urlRecording":webinar.get("urlRecording"),

                    "sessionDigitalDownload":webinar.get("sessionDigitalDownload"),
                    "priceDigitalDownload":webinar.get("priceDigitalDownload"),
                    "urlDigitalDownload":webinar.get("urlDigitalDownload"),
                    
                    "sessionTranscript":webinar.get("sessionTranscript"),
                    "priceTranscript":webinar.get("priceTranscript"),
                    "urlTranscript":webinar.get("urlTranscript"),

                    "status":webinar.get("status"),
                    "webinar_url": webinar.get("webinar_url"),
                    "description":webinar.get("description"),

                    }
            webinar_info = webinar_data_dict
        except Exception as e:
            webinar_info = None
        
        return webinar_info

    @staticmethod
    def update_webinar(w_id, webinar_data):
        
        try:
            
            mongo.db.webinar_data.update_one({"id":w_id},{"$set": webinar_data})
            return {"success":True, "message":"webinar update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        

    @staticmethod
    def edit_webinar(w_id, webinar_status):
        
        try:
            
            mongo.db.webinar_data.update_one({"id":w_id},{"$set": {"status": webinar_status}})
            return {"success":True, "message":"status update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def delete_webinar(w_id):
        
        try: 
            mongo.db.webinar_data.delete_one({"id":w_id})
            return {"success":True,"message": " deleted sucessfully"}
        
        except Exception as e:
            return {"success":False, "message": str(e)}
    
