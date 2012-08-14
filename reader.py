#! /usr/bin/python

from pymongo import Connection

DB_URL = 'localhost';
DB_PORT = 27017;
connection = Connection(DB_URL,DB_PORT);
db = connection['reader'];
collection =  db.log;

stacktrace = '';
last_log_id = 0;

def log_it(line):
	data = line.split(' ');
	date = ' '.join(data[:2]);
	type = data[2];
	log = ' '.join(data[3:]);
	log_entry = {'Date': date, 'Type': type, 'log' : log} ;
	return collection.insert(log_entry);

while True:
	line = raw_input();
	if(len(line) > 0):
		if(line[0].isdigit()):
			if(len(stacktrace) > 0 and last_log_id != 0):
				collection.update({'_id':last_log_id},{'$set':{'stacktrace':stacktrace}});
			stacktrace = '';
			last_log_id = log_it(line);
		else:
			stacktrace = '\n'.join((stacktrace,line));
