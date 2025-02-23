/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function assert(
  condition,
) {
  // Assert the provided condition similar how using Python.

  if (condition)
    return true;

  throw new Error('Assertion'); }



function whenready(
  callback,
) {
  // Attach the callback to the window session ready state.

  assert(!isnull(callback));

  let state =
    document.readyState;

  if (state == 'loading')
    document
    .addEventListener(
      'DOMContentLoaded',
      callback);

  else callback(); }



function isnull(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  let haystack = [null, undefined];

  if (haystack.includes(value))
    return true;

  return false; }



function isempty(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (isstr(value))
    return value.length == 0;

  if (isdict(value)) {

    let keys =
      Object.keys(value)
      .length;

    if (length == 0)
        return true; }

  if (islist(value))
    return value.length == 0;

  return isnull(value); }



function isbool(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  let haystack = [true, false];

  if (haystack.includes(value))
    return true;

  return false; }



function isstr(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (typeof value === 'string')
    return true;

  return false; }



function isnum(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (typeof value === 'number')
    return true;

  return false; }



function isquery(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  try {

    if (value.enquery)
      return true; }

  catch (e) { }

  return false; }



function isnode(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (value instanceof Node)
    return true;

  return false; }



function isnodes(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (value instanceof NodeList)
    return true;

  return false; }



function istime(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  let date =
    new Date(value);

  if (!isNaN(date.getTime()))
      return true;

  return false; }



function islist(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (Array.isArray(value))
    return true;

  return false; }



function isdict(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (typeof(value) == 'object'
      && !isnull(value)
      && !Array.isArray(value))
    return true;

  return false; }



function istrue(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (value === true)
    return true;

  return false; }



function isfalse(
  value,
) {
  // Return the boolean indicating the conditional outcome.

  if (value === false)
    return true;

  return false; }



function loads(
  value,
) {
  // Return the object value from the provided JSON string.

  assert(isstr(value));

  return JSON.parse(value); }



function dumps(
  value,
  indent=null,
) {
  // Return the JSON string from the provided object value.

  assert(!isnull(value));
  assert(!isstr(value));

  let returned =
    JSON.stringify(
      value, null, indent);

  return returned; }
