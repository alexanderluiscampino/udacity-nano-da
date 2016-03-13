// Queries

users_one_post = db.chelyabinsk.aggregate([
    {$group: {"_id": "$created.user", "count": {$sum: 1}}},
    {$sort: {"count": 1}},
    {$group: {"_id": "$count", "users": {$sum: 1}}},
    {$match: {"_id": 1}}
])
;

road_speeds = db.chelyabinsk.aggregate([
    {$match: {type: "way", maxspeed: {$exists: true}}},
    {$group: {"_id": "$maxspeed", "count": {$sum: 1}}},
    {$sort: {"count": -1}},
])
;

road_attraction = db.chelyabinsk.find(
    {type: "way", attraction: {$exists: true}},
    {_id: 0, name: 1, attraction: 1}
).pretty()
;

amenities = db.chelyabinsk.aggregate([
    {$match: {"amenity": {$exists: true}}},
    {$group: {"_id": "$amenity", "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;

religions = db.chelyabinsk.aggregate([
    {$match: {"amenity": "place_of_worship"}},
    {$group: {"_id": "$religion", "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;

cuisine = db.chelyabinsk.aggregate([
    {$match: {"cuisine": {$exists: 1}}},
    {$group: {"_id": "$cuisine", "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;

aeroways = db.chelyabinsk.aggregate([
    {$match: {"aeroway": {$exists: 1}}},
    {$group: {"_id": "$aeroway", "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;

aeroport_nodes = db.chelyabinsk.find(
    {"type": "node", "aeroway": "aerodrome"},
    {_id: 0, name: 1, type: 1, type_tag: 1, landuse: 1, closest_town: 1, iata: 1, icao: 1, "created.user": 1}
).sort({name: 1})
;

aeroport_ways = db.chelyabinsk.find(
    {"type": "way", "aeroway": "aerodrome"},
    {_id: 0, name: 1, type: 1, type_tag: 1, landuse: 1, closest_town: 1, iata: 1, icao: 1, "created.user": 1}
).sort({name: 1})
;

aeroports_more = db.chelyabinsk.find(
    {"type": "node", "aeroway": "aerodrome"},
    {_id: 0, node_refs: 0}
).sort({name: 1})
;

incorrect_postcodes = db.chelyabinsk.aggregate([
    {$match: {"address.street": {$exists: 1}, "address.postcode": /[^0-9]/}},
    {$group: {"_id": {"postcode": "$address.postcode"}, "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;

missing_postcodes = db.chelyabinsk.aggregate([
    {$match: {"address.street": {$exists: 1}, "address.postcode": {$exists: 0}}},
    {$group: {"_id": {"postcode": "$address.postcode"}, "count": {$sum: 1}}}
])
;

contributors = db.chelyabinsk.aggregate([
    {$group: {"_id": "$created.user", "count": {$sum: 1}}},
    {$sort: {"count": -1}}
])
;