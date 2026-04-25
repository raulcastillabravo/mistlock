// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('my_db');

// Create a new document in the collection.
db.getCollection('users').insertOne({
  name: "John Doe Playground",
  email: "john.doe.playground@example.com",
  created_at: new ISODate()
});
