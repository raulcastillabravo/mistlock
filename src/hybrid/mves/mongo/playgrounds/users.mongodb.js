const dbName = 'my_db';
const collectionName = 'users';
const userEmail = 'john.doe.playground@example.com';

use(dbName);

db.getCollection(collectionName).deleteOne({ email: userEmail });

db.getCollection(collectionName).insertOne({
  name: "John Doe Playground",
  email: userEmail,
  created_at: new ISODate()
});
