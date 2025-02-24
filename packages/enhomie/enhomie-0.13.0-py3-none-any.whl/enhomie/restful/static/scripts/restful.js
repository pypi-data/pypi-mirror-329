/*
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



async function
 restful_get(
  path,
) {
  // Return the contents from the API using specified path.

  assert(!isnull(path));

  let response =
    await fetch(path);

  let payload =
    await response.json();

  return payload; }
