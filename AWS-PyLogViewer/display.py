#! /usr/bin/python

from pymongo import Connection
from flask import Flask, url_for, Markup, request

DB_URL='localhost';
DB_PORT = 27017;
MAX_ROWS = 10;

con = Connection(DB_URL,DB_PORT);
db = con['reader'];
collection = db.log;

Desc = 'Desc'

def html(content, sort, start, requesturl):
	requrl = requesturl;
	html = "<html><head><title>PyLogViewer</title><link href='"+url_for('static', filename='style.css')+"' rel='stylesheet' type='text/css'/> </head><body><div id='controls'><a href='/'>ALL</a> <a href='/info'>INFO</a> <a href='/warn'>WARN</a> <a href='/error'>ERROR</a>  <a href='' >REFRESH</a> ";
	html+= "<a href='"+"/".join(requrl.split("/")[:3])+"/"+sort+"/"+str(int(start)+MAX_ROWS)+"'>NEXT</a> <a href='"+"/".join(requrl.split("/")[:3])+"/"+sort+"/"+str(int(start)-MAX_ROWS if int(start) > MAX_ROWS else 0)+"'>PREV</a> <a href='"+"/".join(requrl.split("/")[:3])+"/Asc/"+start+"'>ASC</a> <a href='"+"/".join(requrl.split("/")[:3])+"/"+Desc+"/"+start+"'>DESC</a> <a href='/clear'>CLEAR LOGS</a></div>"+content;
	html += "</body></html>";
	return html;

def clear_data(requrl):
	collection.remove();
	return html("<h2>Cleared logs!!</h2>",Desc,'0',requrl);

def display_content(filter,sort,start,requrl):
	content = "<table border='1px'><tr><th>Date</th><th>Type</th><th>Log</th><th>StackTrace</th></tr>";
	for log in list(collection.find(filter).skip(int(start)).limit(MAX_ROWS).sort('Date', -1 if sort == Desc else 1)):
		content += "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ( log['Type'],log['Date'], log['Type'],Markup.escape(log['log']), "-" if not log.has_key('stacktrace') else "<input type='button' value='stacktrace' onclick=\"alert('"+Markup.encode(' '.join(log['stacktrace'].strip().split('\n')))+"');\" />");
	content += "</table>";
	return html(content,sort,start,requrl);

app = Flask(__name__)


@app.route("/info/<sort>/<start>/")
@app.route("/info/<sort>/", defaults={'start':'0'})
@app.route("/info/", defaults={'sort':Desc,'start':'0'})
def info(sort,start):
	print "i am here %s " % (request.url);
	return display_content({'Type':'INFO'},sort,start,request.url);

@app.route("/warn/<sort>/<start>/")
@app.route("/warn/<sort>/", defaults={'start':'0'})
@app.route("/warn/", defaults={'sort':Desc,'start':'0'})
def warn(sort,start):
	return display_content({'Type':'WARN'},sort,start,request.url);

@app.route("/error/<sort>/<start>/")
@app.route("/error/<sort>/", defaults={'start':'0'})
@app.route("/error/", defaults={'sort':Desc,'start':'0'})
def error(sort,start):
	return display_content({'Type':'ERROR'},sort,start,request.url);

@app.route("/clear/")
def clear():
	return clear_data(request.url);

@app.route("/<sort>/<start>/")
@app.route("/<sort>/", defaults={'start':'0'})
@app.route("/", defaults={'sort':Desc,'start':'0'})
def home(sort,start):
	return display_content({},sort,start,request.url);

if __name__ == "__main__":
    app.debug = True;
    app.run();

