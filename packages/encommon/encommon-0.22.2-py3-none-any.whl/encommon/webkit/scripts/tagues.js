/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function tagues(
  values,
  brafter=true,
) {
  // Construct for containing the values that are tag like.

  assert(!isnull(values));


  let element =
    $('<div/>').addClass(
      'encommon_tagues');


  if (!islist(values))
    values = [values];

  for (const x of values)
    element.append(
      $('<div/>')
      .addClass('_value')
      .text(x));


  return element; }
