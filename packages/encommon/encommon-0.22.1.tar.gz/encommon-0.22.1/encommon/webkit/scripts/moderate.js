/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function moderate(
  label=null,
  icon=null,
  small=null,
) {
  // Construct for containing a wide variety of value types.


  let element =
    $('<div/>').addClass(
      'encommon_moderate');


  if (!isnull(icon)) {

    if (isstr(icon))
      icon = svgicon(icon);

    let _icon =
      $('<div/>')
      .addClass('_icon')
      .replace(icon);

    element.append(_icon); }


  let value =
    $('<div/>')
    .addClass('_value');


  let _value = false;

  if (!isnull(label)) {

    let _label =
      $('<div/>')
      .addClass('_label')
      .html(label);

    value.append(_label);

    _value = true; }


  if (!isnull(small)) {

    let _small =
      $('<div/>')
      .addClass('_small')
      .html(small);

    value.append(_small);

    _value = true; }


  if (istrue(_value))
    element.append(value);


  return element; }
