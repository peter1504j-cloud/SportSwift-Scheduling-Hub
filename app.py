from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
app=Flask(__name__); app.secret_key='sportswift-bca-project'
DB=Path(__file__).with_name('sportswift.db')
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
 c=db(); c.executescript('''CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,sport TEXT,date TEXT,venue TEXT,status TEXT DEFAULT 'Upcoming'); CREATE TABLE IF NOT EXISTS teams(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,sport TEXT,captain TEXT,players INTEGER,status TEXT DEFAULT 'Registered'); CREATE TABLE IF NOT EXISTS matches(id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,time TEXT,sport TEXT,teams TEXT,venue TEXT,status TEXT DEFAULT 'Upcoming'); CREATE TABLE IF NOT EXISTS venues(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,type TEXT,capacity INTEGER,status TEXT DEFAULT 'Available'); CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT,teams TEXT,score TEXT,winner TEXT);''')
 if c.execute('SELECT COUNT(*) FROM events').fetchone()[0]==0:c.executemany('INSERT INTO events(name,sport,date,venue,status) VALUES(?,?,?,?,?)',[('Inter-College Basketball','Basketball','2026-10-10','Court A','Active'),('Annual Football Cup','Football','2026-10-15','Ground 1','Upcoming'),('Volleyball League','Volleyball','2026-10-20','Court B','Upcoming')])
 if c.execute('SELECT COUNT(*) FROM teams').fetchone()[0]==0:c.executemany('INSERT INTO teams(name,sport,captain,players) VALUES(?,?,?,?)',[('CSE Warriors','Basketball','Arun',8),('ECE Titans','Basketball','Rahul',8),('IT Strikers','Football','Kavin',11),('MECH United','Football','Vishnu',11)])
 if c.execute('SELECT COUNT(*) FROM matches').fetchone()[0]==0:c.executemany('INSERT INTO matches(date,time,sport,teams,venue) VALUES(?,?,?,?,?)',[('2026-10-07','09:00','Basketball','CSE Warriors vs ECE Titans','Court A'),('2026-10-08','11:00','Football','IT Strikers vs MECH United','Ground 1'),('2026-10-09','14:30','Volleyball','EEE Spikers vs CIVIL Stars','Court B')])
 if c.execute('SELECT COUNT(*) FROM venues').fetchone()[0]==0:c.executemany('INSERT INTO venues(name,type,capacity) VALUES(?,?,?)',[('Court A','Basketball Court',120),('Court B','Volleyball Court',100),('Ground 1','Football Ground',500),('Cricket Ground','Cricket Ground',800)])
 if c.execute('SELECT COUNT(*) FROM results').fetchone()[0]==0:c.executemany('INSERT INTO results(sport,teams,score,winner) VALUES(?,?,?,?)',[('Basketball','CSE Warriors vs ECE Titans','62 - 58','CSE Warriors'),('Football','IT Strikers vs MECH United','2 - 1','IT Strikers')])
 c.commit();c.close()
@app.route('/')
def home():
 c=db(); data={k:c.execute(f'SELECT * FROM {k} ORDER BY id DESC').fetchall() for k in ['events','teams','matches','venues','results']}; c.close(); return render_template('index.html',**data)
def add(table,fields):
 c=db(); vals=[request.form[x] for x in fields]; c.execute(f"INSERT INTO {table}({','.join(fields)}) VALUES({','.join(['?']*len(fields))})",vals); c.commit();c.close()
@app.post('/event/add')
def ae(): add('events',['name','sport','date','venue']); flash('Event created successfully!'); return redirect(url_for('home'))
@app.post('/team/add')
def at(): add('teams',['name','sport','captain','players']); flash('Team added successfully!'); return redirect(url_for('home'))
@app.post('/match/add')
def am(): add('matches',['date','time','sport','teams','venue']); flash('Match scheduled successfully!'); return redirect(url_for('home'))
@app.post('/delete/<table>/<int:item_id>')
def delete(table,item_id):
 if table not in {'events','teams','matches'}: return redirect(url_for('home'))
 c=db();c.execute(f'DELETE FROM {table} WHERE id=?',(item_id,));c.commit();c.close();flash('Deleted successfully!');return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)