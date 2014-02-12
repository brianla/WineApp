SELECT *
FROM (
         SELECT * 
         FROM LocationInventory li
         WHERE li.li_locationID IN (
            SELECT lm.locationID
            FROM LocationMap lm
            WHERE lm.lm_userID = USERID
         )
      ) as userWines INNER JOIN Wines w
    ON userWines.li_wineID = w.wineID;


SELECT w.wineID as wine_wineID, w.winery as wine_winery, w.tags as wine_tags, li.tags as user_tags
FROM Wines w, LocationInventory li
WHERE w.wineID = li.li_wineID
   AND li.li_locationID IN (
      SELECT lm.locationID
      FROM LocationMap lm
      WHERE lm.lm_userID = 25
   )