/*
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



function datagrid(
  fields,
  values,
) {
  // Construct the table with the header using the contents.

  assert(!isnull(fields));
  assert(!isnull(values));


  let element =
    $('<table/>').addClass(
      'encommon_datagrid');


  element.append(
    _table_header(fields));

  element.append(
    _table_records(
      fields, values));


  return element; }



function _table_header(
  fields,
) {
  // Construct the header for use with the table contents.

  let element = $('<thead/>');
  let trow = $('<tr/>');


  let _fields =
    Object.keys(fields);

  _fields.forEach(key => {

    let tcell = $('<th/>');

    let value = fields[key];

    tcell.text(value);

    trow.append(tcell); });


  element.append(trow);

  return element; }



function _table_records(
  fields,
  values,
) {
  // Construct the records for use with the table contents.

  let element = $('<tbody/>');


  values.forEach(record => {

    let trow = $('<tr/>');


    let _fields =
      Object.keys(fields);

    _fields.forEach(key => {

      let tcell = $('<td/>');
      let value = record[key];

      if (isquery(value))
        tcell.html(
          value[0].outerHTML);

      else if (isnode(value))
        tcell.html(
          value.outerHTML);

      else if (!isnull(value))
        tcell.text(value);

      trow.append(tcell); });


    element.append(trow); });


  return element; }
