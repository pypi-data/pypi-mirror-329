/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function statate(
  status,
  label=null,
  small=null,
) {
  // Construct for containing the value status information.

  assert(!isnull(status));


  let element =
    moderate(
      label,
      svgicon(status),
      small);


  element.addClass(
    'encommon_statate');

  element.attr(
    'data-status',
    status);


  return element; }
