function createXMLHttpRequest() {  
  var xmlHttp = null;  
  if (window.XMLHttpRequest) {  
    xmlHttp = new XMLHttpRequest();  
    if (xmlHttp.overrideMimeType)  
      xmlHttp.overrideMimeType('text/xml');}
  else if (window.ActiveXObject) {  
    try {  
      xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");}
    catch (e) {  
      try {  
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");}
      catch (e) {
      }
    }
  }
  return xmlHttp;
}

function httpGet(url, isCallBack, callback) {
   if(typeof(isCallBack) === 'undefined') 
     isCallBack = false;
   if(typeof(callback) === 'undefined') 
     callback = null;
  var xmlHttp = createXMLHttpRequest();  
  if (xmlHttp != null) {
    xmlHttp.open("GET", url, isCallBack);
    xmlHttp.onreadystatechange = callback;   
    xmlHttp.setRequestHeader("Content-Type",  
                             "application/x-www-form-urlencoded;");  
    xmlHttp.send();
  }
  else
    alert("Your browser does not support XMLHTTP");
}
