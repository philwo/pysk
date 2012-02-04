<?php
/**
 * betterawstats - an alternative display for awstats data
 *
 * @author      Oliver Spiesshofer, support at betterawstats dot com
 * @copyright   2008 Oliver Spiesshofer
 * @version     1.0
 * @link        http://betterawstats.com
 *
 * Based on the GPL AWStats Totals script by:
 * Jeroen de Jong <jeroen@telartis.nl>
 * copyright   2004-2006 Telartis
 * version 1.13 (http://www.telartis.nl/xcms/awstats)
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

// this file can't be used on its own - do not change these 3 lines
if (strpos ($_SERVER['PHP_SELF'], 'config.php') !== false) {
    die ('This file can not be used on its own!');
}
// ATTENTION: BetterAWstats has an online config editor that you can use
// instead of editing this file here. The link is on the bottom of the menu!
// To use it, set $BAW_CONF['online_config']= true; and make sure that the
// file is writable by the server, AND protectthe BetterAWStats installation
// by a .htaccess file!

//*********************************************************/
//*          SITE SETTINGS
//*********************************************************/

// NAME:    Script URL
// INFO:    The url of BetterAWstats' directory, No trailing slash
// DEFAULT: 'http://awstats.local'
$BAW_CONF['site_url'] = 'https://' . gethostname() . '/betterawstats';

// NAME:    Script path
// INFO:    The path of BetterAWstats, No trailing slash
// DEFAULT: '/path/to/betterawstats/'
$BAW_CONF['site_path'] = '/opt/pysk/www/betterawstats';

// NAME:    Path to AWStats Data
// INFO:    Set this value to the directory where AWStats saves its database
//          files into. ATTENTION: If you read those files on windows but have
//          them created on linux or the other way round, make sure you transfer
//          them 'BINARY'. Otherwise they cannot be read properly. No trailing
//          slash
// DEFAULT: '/path/to/betterawstats/awstats/data'
$BAW_CONF['path_data'] = '/var/lib/awstats';

// NAME:    Path to AWStats Libraries
// INFO:    Set this value to the directory where AWStats saves its library
//          files into. No trailing slash
// DEFAULT: '/path/to/betterawstats/awstats/lib'
$BAW_CONF['path_lib'] = '/usr/local/awstats/wwwroot/cgi-bin/lib';

// NAME:    Path to AWStats Language files
// INFO:    Set this value to the directory where AWStats saves its language
//          files into. No trailing slash
// DEFAULT: '/path/to/betterawstats/awstats/lang'
$BAW_CONF['path_lang'] = '/usr/local/awstats/wwwroot/cgi-bin/lang';

// NAME:    URL to AWStats Icons
// INFO:    The url to the awstats icons, should include the whole http://...,
//          no trailing slash.
// DEFAULT: 'http://awstats.local/awstats/icon'
$BAW_CONF['icons_url'] = 'https://' . gethostname() . '/awstats/icon';

// NAME:    Web Configuration
// INFO:    Enable the online configuration editor? WARNING: Your config.php has
//          to be writable in order to enable this. This is a BAD idea to use
//          unless the folder is password-protected with a .htaccess file or
//          similar.
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['online_config'] = false;

// NAME:    Change configuration password?
// INFO:    This password is needed to access the online configuration. It has
//          to be longer than 5 letters.
// DEFAULT: ''
$BAW_CONF['online_config_password'] = '';

// NAME:    Limit to server?
// INFO:    Set this to a simgle server that you want to limit or "false" to
//          show all. The server name should be the one used for awstats.
// DEFAULT: 'show_all'
// POSSIBLE VALUES: 'sitename.org', 'show_all'
$BAW_CONF['limit_server'] = 'show_all';



//*********************************************************/
//*          LAYOUT SETTINGS
//*********************************************************/

// NAME:    Layout Type
// INFO:    Display page in vertical or horizontal layout?
// DEFAULT: 'vertical'
// POSSIBLE VALUES: 'vertical', 'horizontal'
$BAW_CONF['layout_type'] = 'vertical';

// NAME:    Language
// INFO:    Set your language. Set to "auto" to autodetect from browser
// DEFAULT: 'auto'
// POSSIBLE VALUES: 'auto', 'al', 'ba', 'bg', 'ca', 'tw', 'cn', 'cz', 'dk', 'nl',
//                  'en', 'et', 'eu', 'fi', 'fr', 'gl', 'de', 'gr', 'he', 'hu',
//                  'is', 'id', 'it', 'jp', 'kr', 'lv', 'nn', 'nb', 'pl', 'pt',
//                  'br', 'ro', 'ru', 'sr', 'sk', 'es', 'se', 'tr', 'ua', 'wlk'
$BAW_CONF['lang_setting'] = 'auto';

// NAME:    Decimal Point
// INFO:    Decimal Point Character (99.9)
// DEFAULT: '.'
$BAW_CONF['dec_point'] = '.';

// NAME:    Thousands separator
// INFO:    Thousand Digit separator (1'000)
// DEFAULT: "'"
$BAW_CONF['tho_point'] = "'";

// NAME:    Date format (2007-31-12)
// INFO:    How should a date look like? For formatting, please consult
//          http://php.net/manual/en/function.date.php
// DEFAULT: 'Y-M-d'
$BAW_CONF['date_format'] = 'Y-M-d';

// NAME:    Date & Time format (2007-31-12 23:59)
// INFO:    How should a date & time look like? For formatting,please consult
//          http://php.net/manual/en/function.date.php
// DEFAULT: 'Y-M-d H:i'
$BAW_CONF['date_time_format'] = 'Y-M-d - H:i';

// NAME:    Percentage decimals
// INFO:    How many decimals for percentage value? (99.9%)
// DEFAULT: '1'
$BAW_CONF['percent_decimals'] = '1';

// NAME:    Hide Empty data
// INFO:    Completely hide graphs with zero entries? (The menu will also be
//          hidden)
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['hideempty'] = true;

// NAME:    Submit dropdowns on change
// INFO:    If enabled, the site/date dropdowns do not have an "OK"-button. The
//          page is refreshed as soon as you choose a new value. Not recommended
//          for large sites.
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['auto_submit_form'] = true;



//*********************************************************/
//*          TABLE SETTINGS
//*********************************************************/

// NAME:    First day of the week
// INFO:    Should Sunday be the first day of the week or monday?
// DEFAULT: '1'
// POSSIBLE VALUES: '1', '2'
$BAW_CONF['firstdayofweek'] = '2';

// NAME:    Field Length
// INFO:    What is the max. text length of table fields? (Applies only to
//          links)
// DEFAULT: '65'
$BAW_CONF['field_length'] = '50';

// NAME:    Max. Table Lines
// INFO:    What is the max. no. of lines a table can have? Set to "false" to
//          disable. If a table reaches this number of lines, The rest is
//          summarized into one line. This also applies to the "full list" view
//          of a table
// DEFAULT: '10000'
$BAW_CONF['maxlines'] = '10000';



//*********************************************************/
//*          CHART SETTINGS
//*********************************************************/

// NAME:    Max scale for Visitors
// INFO:    The maximum value of the chosen option will define the maximum
//          height of the Visitors bars in the chart
// DEFAULT: 'layout_visits'
// POSSIBLE VALUES: 'layout_visitos', 'layout_visits', 'layout_pages',
//                  'layout_hits', 'layout_bytes'
$BAW_CONF['max_visitors'] = 'layout_visits';

// NAME:    Max scale for Visits
// INFO:    The maximum value of the chosen option will define the maximum
//          height of the Visits bars in the chart
// DEFAULT: 'layout_visits'
// POSSIBLE VALUES: 'layout_visits', 'layout_pages', 'layout_hits', 'layout_bytes'
$BAW_CONF['max_visits'] = 'layout_visits';

// NAME:    Max scale for Pages
// INFO:    The maximum value of the chosen option will define the maximum
//          height of the Pages bars in the chart
// DEFAULT: 'layout_pages'
// POSSIBLE VALUES: 'layout_pages', 'layout_hits', 'layout_bytes'
$BAW_CONF['max_pages'] = 'layout_pages';

// NAME:    Max scale for Hits
// INFO:    The maximum value of the chosen option will define the maximum
//          height of the Hits bars in the chart
// DEFAULT: 'layout_hits'
// POSSIBLE VALUES: 'layout_hits', 'layout_bytes'
$BAW_CONF['max_hits'] = 'layout_hits';

// NAME:    Max no of chart rows
// INFO:    When displaying the charts with the full lists, How many items can
//          there be displayed? The rest will sum up into "Others". This is done
//          to prevent too wide charts
// DEFAULT: '50'
$BAW_CONF['max_chart_items'] = '30';

// NAME:    Chart Titles?
// INFO:    If enabled, it will show a title on top of each chart.
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['chart_titles'] = false;



//*********************************************************/
//*          JPGRAPH SETTINGS
//*********************************************************/

// NAME:    Enable JPgraph?
// INFO:    To use JPGraph, you have to download it from
//          http://www.aditus.nu/jpgraph/jpdownload.php.
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['use_jpgraph'] = false;

// NAME:    Path to JPGraph
// INFO:    Where is your JPGraph installation? (The folder where jpgraph.php is
//          in. No trailing slash)
// DEFAULT: '/path/to/betterawstats/jpgraph/src'
$BAW_CONF['jpgraph_path'] = '/path/to/betterawstats/jpgraph/src';



//*********************************************************/
//*          ADVANCED SETTINGS
//*********************************************************/

// NAME:    XHTML/ HTML
// INFO:    Do you want output in HTML or XHTML?
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['xhtml'] = true;

// NAME:    Debug
// INFO:    Do you want to show debug-output (VERY detailed)?
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['debug'] = false;

// NAME:    Parser Stats
// INFO:    Do you want to show log file parsing data below the stats summary?
// DEFAULT: true
// POSSIBLE VALUES: true, false
$BAW_CONF['show_parser_stats'] = true;

// NAME:    Module settings
// INFO:    Are you using BetterAWstats as a module for another software?
//          (Currently only Drupal is supported)
// DEFAULT: 'none'
// POSSIBLE VALUES: 'none', 'drupal'
$BAW_CONF['module'] = 'none';



//*********************************************************/
//*          DISPLAY
//*********************************************************/

// NAME:    Summary
// INFO:    General Overview of key figures and dates
$BAW_CONF_DIS['overview'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '1',    // Item Sequence
);

// NAME:    Monthly history
// INFO:    Monthly data
$BAW_CONF_DIS['months'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '2',    // Item Sequence
    'top_x' => '24',    // Show how many entries?
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
);

// NAME:    Days of month
// INFO:    Daily data
$BAW_CONF_DIS['days'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '3',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
);

// NAME:    Days of week (Averages)
// INFO:    Weekdays
$BAW_CONF_DIS['weekdays'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '4',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => false,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
);

// NAME:    Hours (Averages)
// INFO:    Hours of the day
$BAW_CONF_DIS['hours'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '5',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => false,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '1'=Hours, '2'=Pages, '3'=Hits, '4'=Bandwidth
    'sort_dir' => SORT_ASC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Visitors domains/countries
// INFO:    Domains of visitors
$BAW_CONF_DIS['domains'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '6',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
    'map' => true,    // Show Map Image?
    'top_x' => '10',    // Show how many entries?
    'sort' => '0',    // Sort for which column?  Possible values are:
    // 'key'=Visitors domains/countries, '0'=Pages, '1'=Hits, '2'=Bandwidth
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Hosts
// INFO:    IP addresses of visitors
$BAW_CONF_DIS['visitors'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '7',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Hosts, '1'=Pages, '2'=Hits, '3'=Bandwidth, '4'=Ratio(Hits/Pages),
    // '5'=Last visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'assumebot' => '1',    // Hits/pages minimum ratio to assume normal user?
);

// NAME:    Authenticated users
// INFO:    Logins for username/password protected pages
$BAW_CONF_DIS['logins'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '8',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '5',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // 'key'=Authenticated users, '0'=Pages, '1'=Hits, '2'=Bandwidth, '3'=Last
    // visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Robots/Spiders visitors
// INFO:    Spiders, Robots of Search engines etc.
$BAW_CONF_DIS['robots'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '9',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Robots/Spiders visitors, '1'=Hits, '2'=Hits (robots.txt),
    // '3'=Bandwidth, '4'=Last visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Worms
// INFO:    Worms searching for security holes
$BAW_CONF_DIS['worms'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '10',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '2',    // Sort for which column?  Possible values are:
    // '0'=Worms, '1'=Sensitive targets, '2'=Hits, '3'=Bandwidth, '4'=Last visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Visits duration
// INFO:    How long have people been on the site?
$BAW_CONF_DIS['sessions'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '11',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
);

// NAME:    File type
// INFO:    What filetypes are on the site
$BAW_CONF_DIS['filetype'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '12',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'chart' => true,    // Show HTML chart?
    'sort' => '0',    // Sort for which column?  Possible values are:
    // 'key'=File type, '0'=Hits, '1'=Bandwidth, '2'=Compression on,
    // '3'=Compression result
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Pages-URL
// INFO:    Pages on the site
$BAW_CONF_DIS['urls'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '13',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Pages-URL, '1'=Viewed, '2'=Average size, '3'=Entry, '4'=Exit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Files/paths
// INFO:    Files/paths on the site
$BAW_CONF_DIS['paths'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '14',    // Item Sequence
    'avg' => true,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Files/paths, '1'=Viewed
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Operating Systems
// INFO:    Operating system of users
$BAW_CONF_DIS['os'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '15',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'chart' => true,    // Show HTML chart?
    'top_x' => '10',    // Show how many entries?
    'sort' => '2',    // Sort for which column?  Possible values are:
    // '1'=Operating Systems, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Unknown OS (useragent field)
// INFO:    Unknown Operating system
$BAW_CONF_DIS['unknownos'] = array(
    'show' => false,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '17',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '1'=User Agent, '2'=Last visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Operating Systems (+Versions)
// INFO:    Operating system of users including versions
$BAW_CONF_DIS['osversions'] = array(
    'show' => false,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '16',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'chart' => true,    // Show HTML chart?
    'top_x' => '10',    // Show how many entries?
    'sort' => '2',    // Sort for which column?  Possible values are:
    // '1'=Operating Systems, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Browsers
// INFO:    User Browser Type
$BAW_CONF_DIS['browsers'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '18',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'chart' => true,    // Show HTML chart?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '3',    // Sort for which column?  Possible values are:
    // '1'=Browsers, '2'=Grabber, '3'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Browsers (+Versions)
// INFO:    User Browser Type (+Versions)
$BAW_CONF_DIS['browserversions'] = array(
    'show' => false,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '19',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'chart' => false,    // Show HTML chart?
    'top_x' => '10',    // Show how many entries?
    'sort' => '4',    // Sort for which column?  Possible values are:
    // '2'=Browsers, '3'=Grabber, '4'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Unknown browsers (useragent field)
// INFO:    Unknown Browsers
$BAW_CONF_DIS['unknownbrowser'] = array(
    'show' => false,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '20',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '1'=User Agent, '2'=Last visit
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Screen sizes
// INFO:    Screensizes of users
$BAW_CONF_DIS['screensizes'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '21',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'chart' => true,    // Show HTML chart?
    'top_x' => '5',    // Show how many entries?
    'sort' => '2',    // Sort for which column?  Possible values are:
    // '1'=Screen sizes, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Referring search engines
// INFO:    Referrals from search engines
$BAW_CONF_DIS['se_referers'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '22',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Referring search engines, '1'=Pages, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'favicon' => true,    // Retrieve favicons for external URLs?
);

// NAME:    Referring sites
// INFO:    Referrals from other sites
$BAW_CONF_DIS['referers'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '23',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Referring sites, '1'=Pages, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'favicon' => false,    // Retrieve favicons for external URLs?
);

// NAME:    Referring sites by Domains
// INFO:    Referrals from other sites, grouped by 2-nd level domains
$BAW_CONF_DIS['referer_domains'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '24',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Referring sites, '1'=Pages, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'favicon' => false,    // Retrieve favicons for external URLs?
    'domain_lvls' => '3',    // Shorten URL to how many domain levels? (-1 to disable)
);

// NAME:    Hotlinks
// INFO:    Pages linking to images/data on your site
$BAW_CONF_DIS['hotlinks'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '25',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Referring sites, '1'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'favicon' => false,    // Retrieve favicons for external URLs?
);

// NAME:    Hotlinks by Domains
// INFO:    Domains linking to images/data on your site
$BAW_CONF_DIS['hotlink_domains'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '26',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Referring sites, '1'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
    'favicon' => false,    // Retrieve favicons for external URLs?
    'domain_lvls' => '3',    // Shorten URL to how many domain levels? (-1 to disable)
);

// NAME:    Search Keyphrases
// INFO:    Search phrases
$BAW_CONF_DIS['searchphrases'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '27',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=different keyphrases, '1'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Search Keywords
// INFO:    Search words
$BAW_CONF_DIS['searchwords'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '28',    // Item Sequence
    'avg' => false,    // Show averages?
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=different keywords, '1'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Miscellaneous
// INFO:    User system features
$BAW_CONF_DIS['misc'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '29',    // Item Sequence
    'table' => true,    // Show data table?
);

// NAME:    HTTP Status codes
// INFO:    Acesses to pages that returned errors
$BAW_CONF_DIS['errors'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '30',    // Item Sequence
    'total' => true,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '2',    // Sort for which column?  Possible values are:
    // '0'=HTTP Status codes, '2'=Hits, '3'=Average size
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Error Hits
// INFO:    Required but not found URLs (HTTP code 404)
$BAW_CONF_DIS['errors404'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '31',    // Item Sequence
    'table' => true,    // Show data table?
    'total' => true,    // Show total Sum?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Error Hits, '1'=Hits, '2'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);

// NAME:    Color depth
// INFO:    Screen colors of users
$BAW_CONF_DIS['extra_1'] = array(
    'show' => true,    // Show this Data?
    'collapse' => false,    // Collapsed?
    'order' => '32',    // Item Sequence
    'total' => false,    // Show total Sum?
    'table' => true,    // Show data table?
    'top_x' => '10',    // Show how many entries?
    'sort' => '1',    // Sort for which column?  Possible values are:
    // '0'=Color depth in bits, '1'=Hits
    'sort_dir' => SORT_DESC,    // Sort direction? Possible values are:
    // SORT_ASC=Ascending, SORT_DESC=Descending
);


?>
