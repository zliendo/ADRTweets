from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2 




class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

        cur = self.conn.cursor()

        # check if tweetwordcount table exists
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('tweetwordcount',))

        self.conn.commit()


        if cur.fetchone()[0] :
            #table exists, delete records
            cur.execute("DELETE FROM tweetwordcount")
            self.conn.commit()
        else:
            #table does not exist, create it and authorizations
            cur.execute('''CREATE TABLE tweetwordcount
                 (word TEXT PRIMARY KEY     NOT NULL,
                  count INT     NOT NULL);''')
            cur.execute("DROP ROLE IF EXISTS w205user;")
            cur.execute("CREATE USER w205user WITH PASSWORD 'aleluya';")
            cur.execute("GRANT SELECT ON tweetwordcount TO w205user;")
            self.conn.commit()

       

    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        cur = self.conn.cursor()
        if (self.counts[word] == 0):
            #insert database
            cur.execute("INSERT INTO Tweetwordcount (word,count) VALUES (%s, %s)", (word,1))            
        else:
            #update
            count = self.counts[word] + 1 
            cur.execute("UPDATE Tweetwordcount SET count=%s WHERE word=%s", (count,word))
        self.conn.commit()
        

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
