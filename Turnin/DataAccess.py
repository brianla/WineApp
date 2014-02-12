"""Data access module
"""

import RecommenderModelAccess
import UserModelAccess
import InventoryModelAccess

''' Add entry '''
#con.execute(userInfo.insert(), emailAddress = 'a5hwang@ucsd.edu', password = 'pass', name = 'Andrew Hwang', location = 'ermegerd')
''' Query entry '''
#user1 = userInfo.select(userInfo.c.emailAddress=='a5hwang@ucsd.edu').execute().first()
##print user1
''' Edit entries '''
#con.execute(userInfo.update(userInfo.c.userID==0), location = 'New location')
'''Query (again) '''
#user2 = userInfo.select(userInfo.c.emailAddress=='a5hwang@ucsd.edu').execute().first()
##print user2
##print user2[3]
##print user2['emailAddress']
''' Delete entry '''
#con.execute(userInfo.delete(userInfo.c.emailAddress=='a5hwang@ucsd.edu'))

#SQL Wine Rating Update Query
#SET w.averageStarRating = (
#    SELECT avg( li.personalStarRating )
#    FROM LocationInventory li
#    WHERE li.li_wineID = 1
#)
#WHERE w.wineID = 1;



#def row2dict(row):
#  d = {}
#  for column in row.__table__.columns:
#    d[column.name] = getattr(row, column.name)

#  return d





# RECOMMENDATION SYSTEM



# INVENTORY SYSTEM

