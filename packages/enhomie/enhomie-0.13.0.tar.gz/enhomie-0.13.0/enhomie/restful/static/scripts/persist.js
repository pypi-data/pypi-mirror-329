/*
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
*/



async function
 persist_datagrid(
  refresh,
) {
  // Construct the table with the header using the contents.

  let payload = null;


  function _refresh() {
    persist_datagrid(refresh); }


  try {

    payload =
      await restful_get(
        '/api/persists'); }

  catch (e) {

    $('#persists>table')
      .css('opacity', .5)

    $('#persists>table'
      + '>tbody>tr>td')
      .css(
        'border-color',
        'rgb(var(--color-red-lite))');

    $('#persists>table'
      + '>thead>tr>th')
      .css(
        'border-color',
        'rgb(var(--color-red-lite))');

    if (!isnull(refresh))
      setTimeout(
        _refresh, refresh);

    return; }


  let fields = {
    'unique': 'Unique',
    'value': 'Value',
    'about': 'About',
    'level': 'Severity',
    'tags': 'Tags',
    'expire': 'Expires',
    'update': 'Updated'};


  let entries =
    persist_entries(
      payload.entries);

  let element =
    datagrid(fields, entries);


  $('#persists')
    .replace(element);

  if (!isnull(refresh))
    setTimeout(
      _refresh, refresh); }



function persist_entries(
  entries,
) {
  // Return the entries but enhanced using various elements.

  assert(!isnull(entries));


  let returned = [];


  function _unique(entry) {

    let unique = entry.unique;
    let label = entry.about_label;
    let icon = entry.about_icon;

    /* handle label present */
    if (!isnull(label))
      entry.unique =
        moderate(
          label, icon, unique);

    /* handle label absence */
    else
      entry.unique =
        moderate(unique, icon); }


  function _value(entry) {

    let value = entry.value;
    let label = entry.value_label;
    let icon = entry.value_icon;
    let unit = entry.value_unit;

    /* handle known units */
    if (unit == 'fahrenheit')
      entry.value =
        numeric_ftemp(value);
    else if (unit == 'celsius')
      entry.value =
        numeric_cftemp(value);
    else if (unit == 'bytes')
      entry.value =
        numeric_bytes(value);
    else if (unit == 'since')
      entry.value =
        duration(value);
    else if (unit == 'color') {
      entry.value =
        colordiv(value, label);
      entry.value_label = null; }
    else if (unit == 'contact') {
      entry.value =
        statate(value, label);
      entry.value_label = null; }

    /* handle stamp unit */
    else if (unit == 'datestamp')
      entry.value =
        datestamp(value);
    else if (unit == 'datesince')
      entry.value =
        $('<div/>')
        .append(datestamp(value))
        .append($('<br/>'))
        .append(duration(value));

    /* handle other units */
    else if (!isnull(unit))
      entry.value =
        numeric(value, unit);

    /* handle without unit */
    else if (isnum(value))
      entry.value =
        numeric_count(value);

    /* updates in upstream */
    value = entry.value;
    label = entry.value_label;
    icon = entry.value_icon;

    /* handle label present */
    if (entry.value_label)
      entry.value =
        moderate(
          label, icon, value);

    /* handle label absence */
    else
      entry.value =
        moderate(value, icon); }


  entries.map(entry => {

    _unique(entry);
    _value(entry);

    if (isstr(entry.level))
      entry.level =
        statate(entry.level);

    if (!isnull(entry.tags))
      entry.tags =
        tagues(entry.tags);

    if (istime(entry.expire))
      entry.expire =
        duration(entry.expire);

    entry.update =
      duration(entry.update);

    returned.push({
      'unique': entry.unique,
      'value': entry.value,
      'about': entry.about,
      'level': entry.level,
      'tags': entry.tags,
      'expire': entry.expire,
      'update': entry.update}); });


  return returned; }
