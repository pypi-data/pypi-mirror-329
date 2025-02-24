/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function duration(
  seconds,
) {
  // Convert the provided seconds in a human friendly format.

  assert(!isnull(seconds));


  let element =
    $('<div/>').addClass(
      'encommon_duration');


  if (isstr(seconds))
    seconds = _since(seconds);

  seconds =
    Math.floor(seconds);


  if (seconds < 0)
    seconds *= -1;

  if (seconds < 5) {

    element.append(
      $('<span/>')
      .addClass('_unit')
      .text('now'));

    return element; }


  let result = [];

  let remain = seconds;

  let groups = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60};

  let maps = {
    year: 'y',
    month: 'mon',
    week: 'w',
    day: 'd',
    hour: 'h',
    minute: 'm',
    second: 's'};


  for (
    let [unit, seconds]
    of Object.entries(groups)
  ) {

    if (remain < seconds)
      continue;

    let value =
      Math.floor(
        remain / seconds);

    remain %= seconds;

    let append =
      {unit, value};

    result.push(append); }


  if ((remain >= 1
        && seconds > 60)
      || seconds < 60)

    result.push(
      {'unit': 'second',
       'value': remain});


  let length = result.length;

  if (length >= 2) {

    let _result =
      result[length - 1];

    let unit = _result.unit;

    if (unit === 'second')
      result.pop(); }


  for (
    let {unit, value}
    of result
  ) {

    let _value =
      $('<span/>')
      .addClass('_value')
      .text(value);

    element.append(_value);

    let _unit =
      $('<span/>')
      .addClass(`_unit`)
      .text(maps[unit]);

    element.append(_unit); }


  return element; }



function _since(
  value,
) {
  // Determine the time in seconds occurring since instance.

  assert(!isnull(value));


  let date =
    new Date(value);

  let time =
    date.getTime();


  assert(time);

  delta = Date.now() - time;

  return delta / 1000; }
