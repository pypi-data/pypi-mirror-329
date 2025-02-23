/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function colordiv(
  input,
  label=null,
) {
  // Construct element for displaying the specified color.

  assert(!isnull(input));


  let element =
    $('<div/>').addClass(
      'encommon_colordiv');


  let known = [
    'gray',
    'red',
    'blue',
    'green',
    'yellow',
    'pink',
    'teal'];

  if (known.includes(input))
    input =
      'rgb(var(--color-'
      + `${input}-dark))`;


  let value =
    $('<div/>')
    .addClass('_value');

  value.css(
    'background-color',
    input);

  element.append(value);


  if (!isnull(label)) {

    let _label =
      $('<div/>')
      .addClass('_label')
      .html(label);

    element.append(_label); }


  return element; }
