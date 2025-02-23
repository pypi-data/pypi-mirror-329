/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function message(
  level,
  about=null,
) {
  // Generate the severity based toast like message element.

  assert(!isnull(level));


  let element =
    $('<div/>').addClass(
      'encommon_message');


  element.attr(
    'data-level',
    level);

  element.html(about);


  return element; }
