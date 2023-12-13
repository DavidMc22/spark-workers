from flask import Flask
from flask import request
import requests
import os
import json
from google.cloud import secretmanager_v1
app = Flask(__name__)

def get_api_key() -> str:
    
    #secret = os.environ.get("COMPUTE_API_KEY")
    project_id = "fluent-protocol-400911"
    secret_id = "compute-api-key" 
    
    client = secretmanager_v1.SecretManagerServiceClient()
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    
    return response.payload.data.decode("UTF-8")
    #if secret:
    #    return secret
    #else:
        #local testing
       # with open('.key') as f:
          #  return f.read()
      
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Use post to add" # replace with form template
  else:
    token="ya29.a0AfB_byDPRsFkwyRiBOi-WIRxIEuZ_0853HMH6W2SLLB3b3XBGb-JxZMiTfKCnqVG8IC97h_a_OBErr5o9MZoT0RLK97esd1DtuiJ0Xal687rHo-VI6xPAWs-oSezkZl_5EbvmTrTp-JaGBvFeo0bfd5WnQ3oxOFVeL2LAkXL9EZ4Kc1cS6hEMP14kIqlo_dSYtfMiXgvhlvt0We98ecoe9otT7M4u8cKDgLxgxrB6uV-XqiIFgryAJMftDi7hj1hVq_Ro6Uz5QkCVv0Myzq-Kug4kQBMfiywt2NWyePYSkAJsidM7DaFlcve9t9eO4cPss5zbgTl6m5G_pveCl_Cfnf_5dNnEfGch2JM9B5A57Ne3LNm4eC7LJBeS0iAPJjcxbi5YZ05x_uGcs4PfVWcI8gdK5UdXB4aCgYKAYgSARMSFQHGX2MiPBMjhHRfYEhEwaDyu14EUg0422"
    ret = addWorker(token,request.form['num'])
    return ret


def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/fluent-protocol-400911/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')

#test
