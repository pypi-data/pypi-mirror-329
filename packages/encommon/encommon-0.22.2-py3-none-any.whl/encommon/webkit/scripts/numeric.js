/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function numeric(
  value,
  unit=null,
) {
  // Construct for containing a wide variety of value types.

  assert(!isnull(value));


  let element =
    $('<div/>').addClass(
      'encommon_numeric');


  if (!isnum(value))
    value =
      parseFloat(value);

  value = Number(
    value.toFixed(1));


  let parts =
    value.toString()
    .split('.');


  element.append(
    $('<span/>')
    .addClass('_value')
    .text(parts[0]));


  if (parts.length == 2) {

    element.append(
      $('<span/>')
      .addClass('_delim')
      .text('.'));

    element.append(
      $('<span/>')
      .addClass('_decimal')
      .text(parts[1])); }


  if (!isnull(unit))

    element.append(
      $('<span/>')
      .addClass('_unit')
      .html(unit));


  return element; }



function numeric_count(
  value,
) {
  // Construct for containing a wide variety of value types.

  assert(!isnull(value));


  if (!isnum(value))
    value =
      parseFloat(value);

  let unit = '';

  if (value >= 1e12) {
    value /= 1e12;
    unit = 'trillion'; }

  else if (value >= 1e9) {
    value /= 1e9;
    unit = 'billion'; }

  else if (value >= 1e6) {
    value /= 1e6;
    unit = 'million'; }

  else if (value >= 1e3) {
    value /= 1e3;
    unit = 'thousand'; }


  let element =
    numeric(value, unit);


  return element; }



function numeric_bytes(
  value,
) {
  // Construct for containing a wide variety of value types.

  assert(!isnull(value));


  if (!isnum(value))
    value =
      parseFloat(value);

  let unit = 'B';

  if (value >= 1e12) {
    value /= 1e12;
    unit = 'TB'; }

  else if (value >= 1e9) {
    value /= 1e9;
    unit = 'GB'; }

  else if (value >= 1e6) {
    value /= 1e6;
    unit = 'MB'; }

  else if (value >= 1e3) {
    value /= 1e3;
    unit = 'KB'; }


  let element =
    numeric(value, unit);


  return element; }



function numeric_ftemp(
  value,
) {
  // Construct for containing a wide variety of value types.

  assert(!isnull(value));


  if (!isnum(value))
    value =
      parseFloat(value);

  let unit = '°F';


  let element =
    numeric(value, unit);


  return element; }



function numeric_cftemp(
  value,
) {
  // Construct for containing a wide variety of value types.

  assert(!isnull(value));


  if (!isnum(value))
    value =
      parseFloat(value);

  value = value * (9 / 5);
  value += 32;


  let element =
    numeric_ftemp(value);


  return element; }
