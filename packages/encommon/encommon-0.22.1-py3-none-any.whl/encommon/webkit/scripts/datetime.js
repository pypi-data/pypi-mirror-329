/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function datestamp(
  value,
) {
  // Return the timestamp using provided format for instance.

  assert(!isnull(value));


  let element =
    $('<div/>').addClass(
      'encommon_datestamp');


  let date =
    new Date(value);

  let time =
    date.getTime();

  assert(time);


  let pad = num =>
    String(num)
    .padStart(2, '0');

  let source_month =
    pad(date.getMonth() + 1);

  let source_day =
    pad(date.getDate());

  let source_year =
    date.getFullYear();

  let source_hours =
    pad(date.getHours());

  let source_minutes =
    pad(date.getMinutes());

  let source_seconds =
    pad(date.getSeconds());

  let source_tzname =
    _tzname(date);

  if (source_tzname == 'GMT')
    source_tzname = 'UTC';


  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_year')
    .text(source_year));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_slash')
    .text('-'));

  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_month')
    .text(source_month));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_slash')
    .text('-'));

  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_day')
    .text(source_day));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_space')
    .html('&nbsp;'));

  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_hours')
    .text(source_hours));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_colon')
    .text(':'));

  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_minutes')
    .text(source_minutes));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_colon')
    .text(':'));

  element.append(
    $('<span/>')
    .addClass('_value')
    .addClass('_seconds')
    .text(source_seconds));

  element.append(
    $('<span/>')
    .addClass('_delim')
    .addClass('_space')
    .html('&nbsp;'));

  element.append(
    $('<span/>')
    .addClass('_tzname')
    .text(source_tzname));


  return element; }



function _tzname(
  date,
) {
  // Return the located timezone object for the provided date.

  assert(!isnull(date));

  let tzname =
    new Intl.DateTimeFormat(
      'en-US',
      {'timeZoneName': 'short'})
    .formatToParts(date)
    .find(
      x =>
      x.type === 'timeZoneName')
    .value;

  return tzname; }
